# Video Sender
# It will wait receiver's connection
# On the receiver:
# vlc tcp/h264://{sender's IP}:8000/



import socket
import time
import picamera

camera = picamera.PiCamera()
camera.resolution = (480, 270)
camera.framerate = 5

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('wb')
try:
    camera.start_recording(connection, format='h264')
    camera.wait_recording(6000)
    camera.stop_recording()
finally:
    connection.close()
    server_socket.close()