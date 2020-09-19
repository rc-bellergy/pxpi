import datetime, time
import threading
import socket
import numpy
from picamera import PiCamera
from picamera.array import PiRGBArray
from cv2 import IMWRITE_JPEG_QUALITY, imencode

class Sender:

    def __init__(self, ip="192.168.192.101", port=5800, stream_quality=20, stream_size=(352, 256)):

        self.ip = ip 
        self.port = port
        self.stream_quality = stream_quality # JPEG quality 0-100
        self.stream_size = stream_size
        self.streaming = False
        self.recording = False
        self.stoppingStreamThread = False

        self.sock = socket.socket()
        print("Connecting to socket %s:%d" % (self.ip, self.port))
        self.sock.connect((self.ip, self.port))

        # Enable instant reconnection and disable timeout system
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("Connected!")

        # initialize the camera and grab a reference to the raw camera capture
        self.camera = PiCamera()
        self.camera.resolution = "1024x768"
        self.camera.rotation = 180
        self.camera.annotate_text_size = 50
        self.camera.annotate_frame_num = True
        self.rawCapture = PiRGBArray(self.camera, size=self.stream_size)

    def recordingStart(self):
        # Start highres. video recording
        if self.recording == False:
            print("Recording Start")
            self.recording = True
            video_file = '/data/highres-{}.h264'.format(datetime.datetime.now())
            self.camera.start_recording(video_file)
            print("Recording video to "+video_file)

    def recordingStop(self):
        if self.recording == True:
            print("Recording Stop")
            self.recording = False
            self.camera.stop_recording()

    def streamStart(self):
        if self.streaming == False:
            self.streaming = True
            if self.stoppingStreamThread == False:
                print("Video stream started")
                t = threading.Thread(target=self.streamThread)
                t.start()
            else:
                print("Video stream start again.")
                self.stoppingStreamThread = False

    def streamThread(self):
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True, resize=self.stream_size):
            image = frame.array
            encode_param = [IMWRITE_JPEG_QUALITY, self.stream_quality]
            result, imgencode = imencode('.jpg', image, encode_param)
            data = numpy.array(imgencode)
            stringData = data.tostring()
            self.sock.send(str(len(stringData)).ljust(16).encode())
            self.sock.send(stringData)
            self.rawCapture.truncate(0)
            time.sleep(0.1)
            if self.streaming == False:
                self.stoppingStreamThread = False
                print("Video stream stop")
                break

    def streamStop(self):
        if self.streaming == True and self.stoppingStreamThread == False:
            self.streaming = False
            self.stoppingStreamThread = True
