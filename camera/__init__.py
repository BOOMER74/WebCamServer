# -*- coding: utf-8 -*-

import base64

import cv2

class Camera(object):
	def __init__(self, width, height):
		# noinspection PyArgumentList
		self.camera = cv2.VideoCapture(-1)

		self.camera.set(3, width)
		self.camera.set(4, height)

	def getBase64Image(self):
		_, frame = self.camera.read()

		_, image = cv2.imencode(".jpg", frame)

		return base64.b64encode(image.tostring())

	def saveImageToFile(self, name, folder="."):
		_, frame = self.camera.read()

		cv2.imwrite("%s/%s.jpg" % (folder, name), frame)