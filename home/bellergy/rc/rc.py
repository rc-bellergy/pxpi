#!/usr/bin/env python2

# Listen the channel change
# then take related action

# There is how to get channels data from dronekit, but don't know how to listen it.
# https://dronekit-python.readthedocs.io/en/latest/automodule.html#dronekit.Vehicle.channels
 
import time
import os
import logging
from dronekit import connect

logging.basicConfig(pathname="/home/bellergy/rc/",filename='rc.log', format='%(asctime)s - %(message)s', level=logging.INFO, filemode='w')
logging.StreamHandler()
print("**RC script start**")

PORT = '127.0.0.1:14551'
video_streaming = False

def channels_callback(self,attr_name, value):
    switchVideoStreaming(value[6])
    # Channel 8: on/off video recording

def switchVideoStreaming(value):
    global video_streaming
    if value > 1500:
        if video_streaming != True:
            video_streaming = True
            # Start video streaming service
            # os.system('sudo systemd start raspicam')
            print("Video streaming started")
            # TODO: Send status to mavlink
    else:
        if video_streaming == True:
            video_streaming = False
            # Stop video streaming service
            # os.system('sudo systemd stop raspicam')
            print("Video streaming stopped")
            # TODO: Send status to mavlink


print("Connecting %s" % PORT)
vehicle = connect(PORT, wait_ready=True, baud=57600)
# init the video streaming service
switchVideoStreaming(vehicle.channels[6])

# Add listener to readio channels
vehicle.add_attribute_listener("channels", channels_callback)

# keep the program runs ;)
while True:
    time.sleep(10)