#!/usr/bin/env python

# A JPEG stream sender (Echo client)

import datetime
import time
import threading
import socket, IN
import numpy
from picamera import PiCamera, Color
from picamera.array import PiRGBArray
from cv2 import IMWRITE_JPEG_QUALITY, imencode

'''
Capture Raspberry Pi camera,
- send low-res video streaming to ground station
- save high-res .h264 video to disk
'''


class Sender:

    '''
    :param str ip: the IP of the groundstation
    :param int port: the receiving port of the groundstation
    :param int stream_quality: the JPEG compression rate (0-100)
    :param tuple stream_quality: the size of streaming video (width, height)
    '''

    def __init__(self, ip="192.168.192.101", port=5800, stream_quality=15, stream_size=(352, 256), fps=4.0):

        self.ip = ip  # IP of ground station
        self.port = port  # port of socket
        self.stream_quality = stream_quality  # JPEG quality 0-100
        self.stream_size = stream_size
        self.streaming = False  # flag of streaming video
        self.recording = False  # flag of recording video
        # If TRUE, user requested streamStop(), but waitting __streamThread() stop the thread
        self.stoppingStreamThread = False
        self.fps = fps

        self.sock = socket.socket()
        # self.sock.setsockopt(socket.SOL_SOCKET, IN.SO_BINDTODEVICE, "zt2lrwgvd2"+'\0')

        print("Connecting to socket %s:%d" % (self.ip, self.port))
        self.sock.connect((self.ip, self.port))

        # Enable instant reconnection and disable timeout system
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("Connected!")

        # initialize the camera and grab a reference to the raw camera capture
        self.camera = PiCamera()
        self.camera.resolution = "1024x768"
        # self.camera.rotation = 180
        self.camera.exposure_compensation = 5  # -25 to 25
        self.rawCapture = PiRGBArray(self.camera, size=self.stream_size)

        print("Stream quality:", self.stream_quality)
        print("Stream size:", self.stream_size)
        print("FPS:", self.fps)


    def changeQuality(self, qty):
        if qty > 100:
            qty = 100
        if qty < 0:
            qty = 0
        self.stream_quality = qty
        print("Video quality: %i" % qty)

    def changeResolution(self, res):
        if res == "HD":
            self.stream_size = (704, 512)
            self.rawCapture = PiRGBArray(self.camera, size=self.stream_size)
            self.streamRestart()
            print("Change to High Res.")

        if res == "SD":
            self.stream_size = (352, 256)
            self.rawCapture = PiRGBArray(self.camera, size=self.stream_size)
            self.streamRestart()
            print("Change to Low Res.")

    def _videoFileName(self):
        now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
        return '/data/v-{}.h264'.format(now)

    def recordingStart(self):
        # Start highres. video recording
        if self.recording == False:
            print("Recording Start")
            self.recording = True
            video_file = self._videoFileName()
            self.camera.start_recording(video_file)
            print("Recording video to "+video_file)

    def recordingStop(self):
        if self.recording == True:
            print("Recording Stop")
            self.recording = False
            self.camera.stop_recording()

    # Continue the recording in the specified output; close existing output
    def splitRecording(self):
        if self.recording == True:
            video_file = self._videoFileName()
            self.camera.split_recording(video_file)
            print("Split video to "+video_file)
        else:
            print("No video is recording")

    def streamStart(self):
        if self.streaming == False:
            self.streaming = True
            if self.stoppingStreamThread == False:
                print("Video stream started")
                t = threading.Thread(target=self.__streamThread)
                t.start()
            else:
                print("Video stream start again.")
                self.stoppingStreamThread = False

    def streamStop(self):
        if self.streaming == True and self.stoppingStreamThread == False:
            self.streaming = False
            self.stoppingStreamThread = True

    def streamRestart(self):
        self.streamStop()
        while self.stoppingStreamThread == True:
            pass
        self.streamStart()

    def increaseExposure(self):
        if self.camera.exposure_compensation < 25:
            self.camera.exposure_compensation = self.camera.exposure_compensation + 5
            print("Exposure compensation:", self.camera.exposure_compensation)

    def reduceExposure(self):
        if self.camera.exposure_compensation > -25:
            self.camera.exposure_compensation = self.camera.exposure_compensation - 5
            print("Exposure compensation:", self.camera.exposure_compensation)

    def changeFPS(self, data):
        if data > 0 and data < 60:
            self.fps = data
        print("FPS:", self.fps)

    # encode the capture image + timestamp
    # send it by socket
    def __streamThread(self):
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True, resize=self.stream_size):
            image = frame.array
            encode_param = [IMWRITE_JPEG_QUALITY, self.stream_quality]
            result, imgencode = imencode('.jpg', image, encode_param)
            data = numpy.array(imgencode)

            # Add timestamp
            stringData = data.tostring() + str(time.time()).ljust(13)

            # Send the size of the data for efficient unpacking
            self.sock.sendall(str(len(stringData)).ljust(16).encode())

            # Send the data
            self.sock.sendall(stringData)

            # Limit FPS to save bandwidth
            s = 1/self.fps-0.03
            if s < 0:
                s = 0
            time.sleep(s)

            # Clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)

            # Check if request to stop the stream thread
            if self.streaming == False:
                self.stoppingStreamThread = False
                print("Video stream stop")
                break


# Testing
# s=Sender()
# s.streamStart()
