import math
import time
import traceback
import numpy
import socket
import cv2
import os

TCP_IP = "0.0.0.0"
TCP_PORT = 5800

conn = None

# Method to grab the size of the image array and verify that it is being decoded correctly
def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def attemptConnection():

    global conn

    # Create a new socket with standard SOCK STREAM settings
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set socket to be able to reconnect immediately and ignore timeouts
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind socket to IP and port supplied from constructor
    s.bind((TCP_IP, TCP_PORT))

    # Listen for exactly 1 host
    s.listen(1)

    # Accept first connection and set connection to be class-wide
    print("Listening for video streaming on port", TCP_PORT)
    conn, addr = s.accept()
    print("Accepted connection")

def loop():
    print("Receiving stream ...")

    global conn
    winName = "Streaming video at %s port" % str(TCP_PORT)
    winSize = (550, 400)

    while True:
        try:
            # Grab length data sent by client to correctly format image
            length = recvall(conn, 16)

            # Grab image data based on the length data previously recieved
            if length is not None:
                stringData = recvall(conn, int(length))
                # print(stringData)
            else:
                print("No streaming data!!")
                print("--- Strat over ---")
                cv2.destroyAllWindows() # Not work!
                break

            # Decode JPG base64 string into a NumPy matrix of RGB data
            data = numpy.frombuffer(stringData, dtype='uint8')

            # Convert NumPy color matrix into OpenCV Matrix
            decimg = cv2.imdecode(data, 1)

            # update the image on window
            decimg = cv2.resize(decimg, winSize)
            cv2.imshow(winName, decimg)

            # Use the OpenCV famous break statement to allow imshow to function properly.
            k = cv2.waitKey(5) & 0xFF
            if k == '+':
                break

        # If something breaks, say what happened
        except Exception as e:
            print("Broke in show loop")
            print(traceback.format_exc())
            break
    # Close and destroy OpenCV stuff on crash.

while True:
    try:
        # Attempt to connect to socket
        attemptConnection()
        # Strat the playback loop
        loop()
    except ConnectionRefusedError:
        pass
        # Start the connection again if lost data

