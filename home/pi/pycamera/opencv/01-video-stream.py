# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy
import sys


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(0.1)
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array

	# Reduce image down to half size
	# newX, newY = image.shape[1] * .5, image.shape[0] * .5
	# image = cv2.resize(image, (int(newX), int(newY)))

	# compress JPG image
	encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 7]
	result, imgencode = cv2.imencode('.jpg', image, encode_param)

	# Encode that JPEG string into a NumPy array for compatibility on the other side
	data = numpy.array(imgencode)

	# Turn NumPy array into a string so we can ship er' on over the information superhighway
	stringData = data.tostring()

	# print(sys.getsizeof(stringData))

	# Server code testing
	# Decode JPG base64 string into a NumPy matrix of RGB data
	data = numpy.fromstring(stringData, dtype='uint8')

	# Convert NumPy color matrix into OpenCV Matrix
	decimg = cv2.imdecode(data, 1)

	# Blow image back up to size
	# newX, newY = decimg.shape[1] * 2, decimg.shape[0] * 2
	# decimg = cv2.resize(decimg, (int(newX), int(newY)))

	# show the frame
	cv2.imshow("Frame", decimg)
	key = cv2.waitKey(1) & 0xFF
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break