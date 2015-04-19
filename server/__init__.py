# -*- coding: utf-8 -*-

import os
import uuid
import zipfile
import StringIO

import cherrypy

class Server(object):
	def __init__(self, camera, html, folder, count):
		self.working = True
		self.camera = camera
		self.html = html.strip()

		self.folder = folder
		self.count = count

		cherrypy.engine.subscribe("stop", self.stop)

	def stop(self):
		self.working = False

	# noinspection PyUnusedLocal
	@cherrypy.expose
	def default(self, *args, **kwargs):
		return self.html

	# noinspection PyUnusedLocal
	@cherrypy.expose
	def image(self, *args, **kwargs):
		cherrypy.response.headers['Content-Type'] = "text/html"
		cherrypy.response.headers['Pragma'] = "no-cache"

		return "<img src=\"data:image/jpeg;base64,%s\">" % self.camera.getBase64Image()

	# noinspection PyUnusedLocal
	@cherrypy.expose
	def images(self, *args, **kwargs):
		cherrypy.response.headers['Content-Type'] = "application/zip"
		cherrypy.response.headers['Pragma'] = "no-cache"

		cherrypy.response.headers['Content-Disposition'] = "attachment; filename=\"%s.zip\"" % str(uuid.uuid1())[:8]

		zipOutput = StringIO.StringIO()
		zipContainer = zipfile.ZipFile(zipOutput, "w")

		for root, _, images in os.walk(self.folder):
			for i, image in enumerate(sorted(images, key=lambda img: os.stat(os.path.join(root, img)).st_mtime, reverse=True)):
				if i < self.count:
					zipContainer.write(os.path.join(root, image), image)

		zipContainer.close()

		return zipOutput.getvalue()