#!/usr/bin/env python

import time, os
from sender2 import Sender

streaming = False
recording = False

video_sender = Sender()
time.sleep(0.1)  # Wait camera init



while True:
    print("")
    c = raw_input("(s)tream (r)ecord (0-9)Qty (f1-30)FPS (q)uit:")

    # Change video quality (0-9)
    try:
        c = int(c)
        if c>=0 and c<=9:
            qty = c * 10
            video_sender.changeQuality(qty)
        if c>=10 and c<=100:
            video_sender.changeQuality(c)
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

    # split and save the video
    if c=="/":
        video_sender.splitRecording()

    if c=="+":
        video_sender.increaseExposure()

    if c=="-":
        video_sender.reduceExposure()

    # Change to high-resolution video
    if c=="h":
        video_sender.changeResolution("HD")
    
    # Change to low-resolution video 
    if c=="l":
        video_sender.changeResolution("SD")
            
    # Quit
    if c=="q":
        break

    # Change FPS
    try:
        if c[:1]=="f":
            try:
                fps = float(c[1:])
                video_sender.changeFPS(fps)
            except:
                print("Wrong FPS number")
    except:
        pass


    time.sleep(0.2)

# stop all before quit
video_sender.recordingStop()
video_sender.streamStop()


