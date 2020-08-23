import socket
import cv2
import numpy
import time

from picamera.array import PiRGBArray
from picamera import PiCamera

class JPEGSender:

	VIDEO_SIZE = (1024, 768)  # video size for save
	STREAM_SIZE = (352, 256)  # video size for streaming

	def __init__(self, targetIP, tragetPort=5800, jpegQuality=10):

		# The video will send to this IP:PORT
		self.targetIP = targetIP
		self.targetPort = tragetPort

		# Start from very low quality to make the JPEG as small as possible
		# The range is 0-100. If you want better quality, you can adjust it.
		self.jpegQuality = jpegQuality

	def connect(self):
		print("Connecting to socket %s:%i" % (self.targetIP, self.targetPort))
		self.sock = socket.socket()
		self.sock.connect((self.targetIP, self.targetPort))

		# Enable instant reconnection and disable timeout system
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		print("Connected!")

		# initialize the camera and grab a reference to the raw camera capture
		self.camera = PiCamera()
		self.camera.resolution = JPEGSender.VIDEO_SIZE

	def streamStart(self):
		self.camera.start_recording('highres.h264')
		rawCapture = PiRGBArray(self.camera, size=JPEGSender.STREAM_SIZE)

		# allow the camera to warmup
		time.sleep(0.1)

		# capture frames from the camera
		for frame in self.camera.capture_continuous(rawCapture, format="bgr", use_video_port=True, resize=JPEGSender.STREAM_SIZE):

			try:
				# grab the raw NumPy array representing the image, then initialize the timestamp
				# and occupied/unoccupied text
				image = frame.array

				# compress JPG image
				encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), self.jpegQuality]
				result, imgencode = cv2.imencode('.jpg', image, encode_param)

				# Encode that JPEG string into a NumPy array for compatibility on the other side
				data = numpy.array(imgencode)

				# Turn NumPy array into a string so we can ship er' on over the information superhighway
				stringData = data.tostring()

				# Send the size of the data for efficient unpacking
				self.sock.send(str(len(stringData)).ljust(16).encode())

				# Might as well send the actual data while we're sending things
				self.sock.send(stringData)
				# print(sys.getsizeof(stringData))

				# clear the stream in preparation for the next frame
				rawCapture.truncate(0)

				# use it to reduces the framerate
				time.sleep(0.1) 

			# If something breaks, say what happened
			except Exception as e:
				print("Broke in show loop")
				print(traceback.format_exc())
				break

# Testing
# sender = JPEGSender('192.168.192.101')
# sender.connect()
# sender.streamStart()
