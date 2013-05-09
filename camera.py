# Подключение библиотек
import os, cv2, uuid, cherrypy

# HTML код страницы
html = """<html>
	<head>
		<meta http-equiv="refresh" content="3" url="/">
	</head>
	<body>
		<image src="/image">
	</body>
</html>"""

# Класс, реализующий сервер
class Camera(object):
	# Конструктор класса
	def __init__(self):
		# Камера
		self.camera = cv2.VideoCapture(-1)

		# Настройки камеры (разрешение)
		self.camera.set(3, 640)
		self.camera.set(4, 480)

	# Ответ на получение любого запроса, кроме /image
	@cherrypy.expose
	def default(self):
		return html

	# Ответ на запрос /image
	@cherrypy.expose
	def image(self):
		# Получаем фрейм (изображение) с камеры
		_, frame = self.camera.read()

		# Имя файла с использование UID, для предотвращения ошибок
		filename = "%s.jpg" % str(uuid.uuid1())

		# Записываем фрейм в файл
		cv2.imwrite(filename, frame)
		# Открываем файл и читаем данные
		with open(filename, "rb") as data: image = data.read()
		# Удаляем файл
		os.unlink(filename)

		# Устанавливаем заголовки
		cherrypy.response.headers['Content-Type'] = "image/jpeg"
		cherrypy.response.headers['Pragma'] = "no-cache"

		# Отдаем изображение
		return image

# Настраиваем сервер
cherrypy.config.update({ "server.socket_host": "0.0.0.0", "server.socket_port": 8081 })
# Запускаем сервер
cherrypy.quickstart(Camera())