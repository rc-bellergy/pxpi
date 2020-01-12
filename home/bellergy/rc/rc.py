#!/usr/bin/env python

# Listen the RC channel change
# then take related action
# https://mavlink.io/en/messages/common.html#RC_CHANNELS
 
import time
import os
import logging
import pymavlink.mavutil as mavutil
import config

logging.basicConfig(pathname="/tmp/rc.log", format='%(asctime)s - %(message)s', level=logging.INFO, filemode='w')
logging.StreamHandler()
logging.info("**RC script start**")

drone_endpoint = config.drone["endpoint"]
video_streaming = False

# Connect to mavlink
logging.info("Waitting heartbeat from " + drone_endpoint)
mav = mavutil.mavlink_connection(drone_endpoint)
mav.wait_heartbeat()
logging.info("Heartbeat received!")

# Listen channels
logging.info("Waitting mavlink 'RC_CHANNELS'")

while True:

    # Watch the channel 8.
    # If the switch position on middle, start the video streaming, else stop it.

    # Note: It assumes that 
    # 1. The systemd raspicam service has been set up;
    # 2. The channel 8 mapped a 3 position switch  
    
    channels = mav.recv_match(type='RC_CHANNELS', blocking=True)
    ch8 = channels.chan8_raw
    if video_streaming is not True:
        if ch8 > 1200 and ch8 < 1800:
            os.system('sudo systemctl start raspicam')
            logging.info("Video streaming started")
            video_streaming = True
            # TODO: Send status to mavlink
    else:
        if ch8 <=1200 or ch8 >=1800:
            os.system('sudo systemctl stop raspicam')
            logging.info("Video streaming stopped")
            video_streaming = False
            # TODO: Send status to mavlink

quit()