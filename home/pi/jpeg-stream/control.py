


import time
import threading
from sender2 import Sender
import pymavlink.mavutil as mavutil

def testingVideo(length=10):
    print("--- Testing streaming video start ---")
    sender = Sender()
    time.sleep(0.1) # Wait camera init

    # Strat the video stream in a thread
    stream = threading.Thread(target=sender.streamStart)
    stream.start()

    # Strat the highres. video recording
    sender.recordingStart()

    # Let the camera runs n sec.
    time.sleep(length)

    # Stop the streaming
    sender.streamStop()

    # Stop the recording
    sender.recordingStop()
    
    print("--- Testing streaming video end ---")

def connectMavlink():
    # Connect to mavlink
    print("Connecting Mavlink")
    mav = mavutil.mavlink_connection("udpin:127.0.0.1:14551")
    mav.wait_heartbeat()
    print("Mavlink heartbeat received!")
    return mav

# mav = connectMavlink()
# print("Watch RC channel 6")
# while True:
#     #  Watch channel 6
#     channels = mav.recv_match(type='RC_CHANNELS', blocking=True)
#     v = channels.chan6_raw

#     # switch on bottom
#     if v<1200: 
#         sender.recordingStart()
#         sender.streaming = True

#     # switch on middle
#     if v>=1200v && v<1800: 
#         sender.recordingStop()
#         sender.streaming = True

#     # switch on middle
#     if v>=1800:
#         sender.recordingStop()
#         sender.streaming = False

testingVideo()