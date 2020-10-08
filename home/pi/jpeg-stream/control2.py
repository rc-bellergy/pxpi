#!/usr/bin/env python2

import time, os
from sender2 import Sender

def testingVideo(sender):
    print("--- Testing streaming video start ---")
    sender.streamStart()
    time.sleep(5)
    sender.streamStop()
    print("--- Testing streaming video end ---")

video_sender = Sender()
time.sleep(0.1)  # Wait camera init
# testingVideo(video_sender)

streaming = False
recording = False

while True:
    print("")
    c = raw_input("Input (s)tream (r)ecord (q)uit: ")

    # Change video quality (0-9)
    try:
        c = int(c)
        if c>=0 and c<=9:
            qty = c * 10
            video_sender.changeQuality(qty)
    except ValueError:
        pass

    # Start / Stop video streaming
    if c=="s":
        if streaming:
            video_sender.streamStop()
            streaming = False
        else:
            video_sender.streamStart()
            streaming = True

    # Start / Stop video recording
    if c=="r":
        if recording:
            video_sender.recordingStop()
            recording = False
        else:
            video_sender.recordingStart()
            recording = True

    # Change to high-resolution video
    if c=="h":
        video_sender.changeResolution("HD")
    
    # Change to low-resolution video 
    if c=="l":
        video_sender.changeResolution("SD")
            
    # Quit
    if c=="q":
        break

    time.sleep(0.1)

# stop all before quit
# video_sender.recordingStop()
# video_sender.streamStop()


