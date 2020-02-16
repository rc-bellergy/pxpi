import math
import time
import traceback

import numpy
import socket
from threading import Thread

import cv2

# Method to grab the size of the image array and verify that it is being decoded correctly
def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf


class CameraServer():

    # Define the IP for easy changing
    TCP_IP = ''

    debug = False

    # For FPS counting
    fps = -1
    start_time = time.time()
    fps_update_time = time.time()

    byte_size = -1

    def attemptConnection(self):

        # Create a new socket with standard SOCK STREAM settings
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set socket to be able to reconnect immediately and ignore timeouts
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind socket to IP and port supplied from constructor
        self.s.bind(('', self.port))

        # Listen for exactly 1 host
        self.s.listen(1)

        # Accept first connection and set connection to be class-wide
        print("searching for camera on port", self.port)
        self.conn, self.addr = self.s.accept()
        print("accepted connection")

    def __init__(self, port):
        # Thread.__init__(self)
        self.port = port

    # Close the socket
    def disconnect(self):
        print("Port", self.port, "Disconnecting")
        self.s.close()

    def startLoop(self):

        print("startLoop")
        while True:

            try:

                # Grab length data sent by client to correctly format image
                length = recvall(self.conn, 16)

                # Grab image data based on the length data previously recieved
                if length is not None:
                    stringData = recvall(self.conn, int(length))
                else:
                    break
                # Decode JPG base64 string into a NumPy matrix of RGB data
                data = numpy.fromstring(stringData, dtype='uint8')

                # Convert NumPy color matrix into OpenCV Matrix
                decimg = cv2.imdecode(data, 1)

                # Blow image back up to size
                newX, newY = decimg.shape[1] * 2, decimg.shape[0] * 2
                decimg = cv2.resize(decimg, (int(newX), int(newY)))

                if self.debug:

                    # Draw the size of the image
                    if time.time() - self.fps_update_time > 0.5:
                        self.byte_size = length
                    cv2.putText(decimg, str(int(self.byte_size)) + " bytes", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                    # Draw an FPS counter
                    if time.time() - self.fps_update_time > 0.5:
                        self.fps = 1 / (time.time() - self.start_time)
                        self.fps_update_time = time.time()
                    self.start_time = time.time()
                    cv2.putText(decimg, str(math.floor(self.fps)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                # Show image on a window named after its port.
                cv2.imshow(str(self.port), decimg)

                # Use the OpenCV famous break statement to allow imshow to function properly.
                # Don't ask me i'm not smart enough to understand OpenCV under the hood
                k = cv2.waitKey(5) & 0xFF
                if k == '+':
                    break

            # If something breaks, say what happened
            except Exception as e:
                print("Broke in show loop")
                print(traceback.format_exc())
                break
        # Close and destroy OpenCV stuff on crash.


    def run(self):

        # Keep trying forever
        while True:
            try:
                # Attempt to connect to socket
                self.attemptConnection()
                # You made it this far, start the processing loop
                self.startLoop()
            except ConnectionRefusedError:
                pass
            except:
                # Something went wrong.  Try to reconnect
                print("Socket", self.port, "Died!  Trying again")

