import time
import sys
import socket
import traceback

import cv2
import numpy

from picamera.array import PiRGBArray
from picamera import PiCamera

TCP_IP = "192.168.192.101"
TCP_PORT = 5800
VIDEO_SIZE = (1024, 768)
STREAM_SCALE = 0.4

print("Connecting to socket %s:%d" % (TCP_IP, TCP_PORT))
sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))

# Enable instant reconnection and disable timeout system
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print("Connected!")

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = VIDEO_SIZE
camera.framerate = 30
camera.start_recording('highres.h264')

rawCapture = PiRGBArray(camera, size=VIDEO_SIZE)

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array

	# Reduce image down to half size
	newX, newY = image.shape[1] * STREAM_SCALE, image.shape[0] * STREAM_SCALE
	image = cv2.resize(image, (int(newX), int(newY)))

	# compress JPG image
	encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 10]
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

	key = cv2.waitKey(1) & 0xFF
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
	
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

	time.sleep(0.1) # reduce the framerate lower then 10

# cv2.waitKey(10)
# cv2.destroyAllWindows()

camera.stop_recording()
