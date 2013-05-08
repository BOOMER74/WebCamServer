import os
import cv2
import uuid
import cherrypy

html = """<html>
	<head>
		<meta http-equiv="refresh" content="3" url="/">
	</head>
	<body>
		<image src="/image">
	</body>
</html>"""

class Camera(object):
	def __init__(self):
		self.camera = cv2.VideoCapture(-1)

		self.camera.set(3, 640) #352)
		self.camera.set(4, 480) #288)

	@cherrypy.expose
	def default(self):
		return html

	@cherrypy.expose
	def image(self):
		_, frame = self.camera.read()

		filename = "%s.jpg" % str(uuid.uuid1())

		cv2.imwrite(filename, frame)
		with open(filename, "rb") as data: image = data.read()
		os.unlink(filename)

		cherrypy.response.headers['Content-Type'] = "image/jpeg"
		cherrypy.response.headers['Pragma'] = "no-cache"

		return image

cherrypy.config.update({ "server.socket_host": "0.0.0.0", "server.socket_port": 8081 })
cherrypy.quickstart(Camera())