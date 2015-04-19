# -*- coding: utf-8 -*-

import os
import time
import threading

import cherrypy

import config
import camera
import server

def removeOldImages(interval, folder, old):
	for filename in os.listdir(folder):
		image = os.path.join(folder, filename)

		if os.path.isfile(image) and os.stat(image).st_mtime < time.time() - old:
			os.unlink(image)

	threading.Timer(interval, removeOldImages, [interval, folder, old]).start()

def storeImageByTimer(webCamera, interval, folder):
	webCamera.saveImageToFile(time.strftime("%d-%m-%Y_%H-%M-%S"), folder)

	threading.Timer(interval, storeImageByTimer, [webCamera, interval, folder]).start()

if __name__ == "__main__":
	if not os.path.exists(config.camera['folder']):
		os.makedirs(config.camera['folder'])

	cameraInstance = camera.Camera(config.camera['width'], config.camera['height'])

	if config.camera['interval'] > 0:
		removeOldImages(config.cleaner['interval'], config.camera['folder'], config.cleaner['old'])

		storeImageByTimer(cameraInstance, config.camera['interval'], config.camera['folder'])

	cherrypy.config.update({
	"engine.autoreload.on": False,
	"server.socket_host": config.server['host'],
	"server.socket_port": config.server['port']
	})

	cherrypy.quickstart(server.Server(cameraInstance, config.server['html'], config.camera['folder'], config.camera['count']), "/", config={"/": {}})