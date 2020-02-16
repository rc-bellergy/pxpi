#!/usr/bin/python
import socket
import sys
import time
import traceback

import cv2
import numpy

capture = None

def runClient(sock):
    global capture

    # Set those constants for easy access
    TCP_IP = 'MAXPC.local'

    # Grab the port number from the command line
    TCP_PORT = int(sys.argv[1])

    # Connect to the socket with the previous information
    print("Connecting to Socket")
    sock.connect((TCP_IP, TCP_PORT))

    # Enable instant reconnection and disable timeout system
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Spread the good news
    print("Connected!")

    # If the constructor is an integer, make it one.  Otherwise leave it as a string.
    try:
        vid = int(sys.argv[2])
    except:
        vid = sys.argv[2]

    # Create the VideoCapture object with the adjusted parameter
    capture = cv2.VideoCapture(vid)

    # C R O N C H  that image for minimal latency
    capture.set(3, 480)
    capture.set(4, 360)

    while True:

        # Grab a frame from the webcam
        ret, frame = capture.read()

        # C R O N C H   that image down to half size
        newX, newY = frame.shape[1] * .5, frame.shape[0] * .5
        frame = cv2.resize(frame, (int(newX), int(newY)))

        # C R O N C H   that image down to extremely compressed JPEG
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 7]
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)

        # Encode that JPEG string into a NumPy array for compatibility on the other side
        data = numpy.array(imgencode)

        # Turn NumPy array into a string so we can ship er' on over the information superhighway
        stringData = data.tostring()

        print(sys.getsizeof(stringData))

        # Send the size of the data for efficient unpacking
        sock.send(str(len(stringData)).ljust(16).encode())

        # Might as well send the actual data while we're sending things
        sock.send(stringData)

        # Arbitrary OpenCV wait statement that I still don't understand the purpose of but when I take it out it
        # doesn't work so here it will stay.
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.waitKey(10)
    cv2.destroyAllWindows()


# This horrific piece of garbage just verifies that even if it crashes it gets up and tries again.  Please don't throw
# things at me.

def start():
    global capture

    while True:
        # Create the socket object
        sock = socket.socket()

        try:
            # Start the client
            runClient(sock)
        except Exception as e:
            # If it dies, give it a second to rest and force it to try again.
            sock.close()
            capture.release()
            print(traceback.format_exc())
            time.sleep(1)
            start()


# Start the Client
start()
