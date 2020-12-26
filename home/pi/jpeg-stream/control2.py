#!/usr/bin/env python

import time, os
from sender2 import Sender
import pigpio


streaming = False
recording = False

video_sender = Sender()
time.sleep(0.1)  # Wait camera init

# Camera servo
PIN=24              # Camera serbo at GPIO24 PIN
CAM_LEVEL = 1000
CAM_MAX_UP = 800
CAM_MAX_DOWN = 2000
pwm = pigpio.pi()   # Accesses the local Pi's GPIO
pwm.set_mode(PIN, pigpio.OUTPUT) # Set GPIO24 as output
pwm.set_PWM_frequency(PIN, 50)

# Testing move
pwm.set_servo_pulsewidth(PIN, 0)
time.sleep(0.1)
pwm.set_servo_pulsewidth(PIN, CAM_MAX_UP)  # 18 deg up (max)
time.sleep(1)
pwm.set_servo_pulsewidth(PIN, CAM_MAX_DOWN) # 90 deg down (max)
time.sleep(1)
pwm.set_servo_pulsewidth(PIN, CAM_LEVEL) # Level

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

    # Camera angle
    if c=="vl": # view level
        pwm.set_servo_pulsewidth(PIN, CAM_LEVEL) 
    if c=="vu": # view level
        pwm.set_servo_pulsewidth(PIN, CAM_MAX_UP) 
    if c=="vd": # view level
        pwm.set_servo_pulsewidth(PIN, CAM_MAX_DOWN)    
                 
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


