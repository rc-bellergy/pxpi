import time
import socket
import cv2
import numpy
import os
import curses
import datetime

from picamera.array import PiRGBArray
from picamera import PiCamera

TCP_IP = "192.168.192.101"
TCP_PORT = 5800
VIDEO_SIZE = "1024x768" # video size for save
STREAM_SIZE = (352, 256) # video size for streaming

print("Connecting to socket %s:%d" % (TCP_IP, TCP_PORT))
sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))

# Enable instant reconnection and disable timeout system
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print("Connected!")

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = VIDEO_SIZE
camera.rotation = 180
camera.annotate_text_size = 50
camera.annotate_frame_num = True

# Start highres. video recording
camera.start_recording('/data/highres-{}.h264'.format(datetime.datetime.now()))

# Camera capture
rawCapture = PiRGBArray(camera, size=STREAM_SIZE)

# allow the camera to warmup
time.sleep(0.1)

def streamLoop():

	# Start from very low quality to make the JPEG as small as possible 
	# The range is 0-100. If you want better quality, you can adjust it.
	jpegQuality = 20

	# capture frames from the camera
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True, resize=STREAM_SIZE):
		# grab the raw NumPy array representing the image, then initialize the timestamp
		# and occupied/unoccupied text
		image = frame.array

		# compress JPG image
		encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), jpegQuality]
		result, imgencode = cv2.imencode('.jpg', image, encode_param)

		# Encode that JPEG string into a NumPy array for compatibility on the other side
		data = numpy.array(imgencode)

		# Turn NumPy array into a string so we can ship er' on over the information superhighway
		stringData = data.tostring()

		# Send the size of the data for efficient unpacking
		sock.send(str(len(stringData)).ljust(16).encode())

		# Might as well send the actual data while we're sending things
		sock.send(stringData)
		# print(sys.getsizeof(stringData))
		
		# clear the stream in preparation for the next frame
		rawCapture.truncate(0)
		key = cv2.waitKey(1) & 0xFF

		time.sleep(0.1) 

# Start the stream
# curses.wrapper(streamLoop)
streamLoop()

# Before quit
camera.stop_recording()
