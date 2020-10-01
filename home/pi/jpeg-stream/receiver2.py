# A JPEG stream receiver (Echo server)
# It waits socket connection on port 5800
# It will decode the data and show it on CV image viewer
# If connection closed, it will restart 

import math
import time
import traceback
import numpy
import socket
import cv2
import os

TCP_IP = "0.0.0.0" # Any IP can connect me
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
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    print("Listening for video streaming on port", TCP_PORT)
    conn, addr = s.accept()
    print("Connected by", addr)

def main():
    print("Waitting video stream ...")

    global conn
    winName = "Streaming video at %s port" % str(TCP_PORT)
    winSize = (550, 400)

    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10,380)
    fontScale              = 0.6
    fontColor              = (255,255,255)
    lineType               = 1

    lastFrame = time.time()

    adjustTime = 0

    while True:
        try:
            
            # receive data from socket
            # the last 13 digit is timestamp
            # use the timestamp to calculate the latency of the video
            # encode remaining data to image

            length = recvall(conn, 16)
            if length is not None:
                stringData = recvall(conn, int(length))
                timestamp = float(stringData[-13:])
                latency = time.time() - timestamp - adjustTime
                # two system time clock not sync, use adjustTime to make it reasonable
                if latency < 0:
                    adjustTime = adjustTime + latency
                info = "Latency: %s   " % "{:.2f}".format(time.time() - timestamp - adjustTime)
                imgData = stringData[0:-13]
                # print(stringData)
            else:
                print("No streaming data!!")
                print("--- Strat over ---")
                cv2.waitKey(10)
                cv2.destroyAllWindows() # Not work on Mac!
                break
            
            data = numpy.frombuffer(imgData, dtype='uint8')
            img = cv2.imdecode(data, 1)
            img = cv2.resize(img, winSize)

            # Framerate
            thisFrame = time.time()
            f = 1 / (thisFrame - lastFrame)
            lastFrame = thisFrame
            framerate = "FPS "+ ("%s" % "{:.0f}".format(f)).zfill(2)
            info = info + framerate

            # On Screen Display
            cv2.putText(img, info, 
            bottomLeftCornerOfText, 
            font, 
            fontScale,
            fontColor,
            lineType)

            cv2.imshow(winName, img)

            # Use the OpenCV famous break statement to allow imshow to function properly.
            k = cv2.waitKey(5) & 0xFF
            if k == '+':
                break

        except Exception as e:
            print("Something wrong! Broke in show loop")
            print(traceback.format_exc())
            break

while True:
    try:
        attemptConnection()
        main()
    except ConnectionRefusedError:
        pass
        # Keep the receive alive even on error
