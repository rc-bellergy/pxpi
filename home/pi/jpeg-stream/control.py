


import time
from sender2 import Sender
import pymavlink.mavutil as mavutil


def testingVideo(sender):
    print("--- Testing streaming video start ---")
    sender.streamStart()
    time.sleep(5)
    sender.streamStop()
    print("--- Testing streaming video end ---")

def connectMavlink():
    # Connect to mavlink
    print("Connecting Mavlink")
    mav = mavutil.mavlink_connection("udpin:127.0.0.1:14551")
    mav.wait_heartbeat()
    print("Mavlink heartbeat received!")
    return mav

def watchChannel(mav, sender):
    print("Watch RC channel 6")
    while True:
        #  Watch channel 6
        channels = mav.recv_match(type='RC_CHANNELS', blocking=True)
        v = channels.chan6_raw

        # switch on bottom
        if v<1200: 
            sender.recordingStart()
            sender.streamStart()

        # switch on middle
        if v>=1200 and v<1800: 
            sender.recordingStop()
            sender.streamStart()

        # switch on top
        if v>=1800:
            sender.recordingStop()
            sender.streamStop()

video_sender = Sender()
time.sleep(0.1)  # Wait camera init
testingVideo(video_sender)
mav = connectMavlink()
watchChannel(mav, video_sender)
