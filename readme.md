# WebCamServer

Easy web camera server on Python, based on CherryPy and OpenCV. Tested on Raspberry Pi Model B with Logitech C110 webcam.

# Configurations

## Cleaner

* **cleaner.interval** - Interval of deleting old image (seconds, 0 to disable)
* **cleaner.old** - How old images must be (seconds)

## Camera

* **camera.index** - Index of camera (use -1 for first available camera)
* **camera.count** - Count of images in downloadable archive
* **camera.width** - Width of image (camera resolution)
* **camera.height** - Height of image (camera resolution)
* **camera.interval** - Interval of storing images (seconds, 0 to disable)
* **camera.folder** - Folder to store images

## Server

* **server.host** - Server host (0.0.0.0 to all connections, 127.0.0.1 to local connections)
* **server.port** - Server port
* **server.html** - HTML code of main page (in default code - asynchronous updates once per second)