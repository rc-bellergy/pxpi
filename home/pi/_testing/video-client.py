import asyncio
import time
import cv2
import numpy
from picamera.array import PiRGBArray
from picamera import PiCamera

IP = "192.168.192.101"
PORT = 5800
VIDEO_SIZE = "1024x768" # video size for save
STREAM_SIZE = (352, 256) # video size for streaming

camera = PiCamera()
rawCapture = PiRGBArray(camera, size=STREAM_SIZE)
time.sleep(0.1)


async def connect():
    reader, writer = await asyncio.open_connection(IP, PORT)
    return reader, writer

async def sender(message, writer):
    print(f'Send: {message!r}')
    writer.write(message.encode())
    await writer.drain()

async def close():
    print('Close the connection')
    writer.close()
    await writer.wait_closed()
    

reader, writer = connect()
asyncio.run(sender('Hello World!', writer))
asyncio.run(sender('It is message2', writer))
close()
        