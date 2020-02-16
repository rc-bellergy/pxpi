
# Recording to a network stream
# https://picamera.readthedocs.io/en/release-1.13/recipes1.html#recording-to-a-network-stream
# Client (sender) will wait server (receiver) connection

import socket
import time
import picamera

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(('192.168.192.101', 8000))

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
print("Server connected")
try:
    camera = picamera.PiCamera()
    camera.resolution = (720, 540)
    camera.framerate = 5
    # Start a preview and let the camera warm up for 2 seconds
    camera.start_preview()
    time.sleep(2)
    # Start recording, sending the output to the connection for 60
    # seconds, then stop
    camera.start_recording(connection, format='h264')
    print("video streaming")
    camera.wait_recording(60)
    camera.stop_recording()
finally:
    connection.close()
    client_socket.close()
    print("Connection closed")