#!/usr/bin/env python

# Listen the RC channel change
# then take related action
# https://mavlink.io/en/messages/common.html#RC_CHANNELS

import time
import os
import logging
import pymavlink.mavutil as mavutil
import config

# Init logging
dir_path = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(filename=dir_path + "/rc.log",
                    format='%(asctime)s - %(message)s', level=logging.INFO, filemode='w')
console = logging.StreamHandler()
logger = logging.getLogger()
logger.addHandler(console)

logging.info("**RC script start**")

drone_endpoint = config.drone["endpoint"]
video_streaming = False

# Connect to mavlink
logging.info("Waitting heartbeat from " + drone_endpoint)
mav = mavutil.mavlink_connection(drone_endpoint)
mav.wait_heartbeat()
logging.info("Heartbeat received!")

# Listen channels

while True:

    # Watch the channel 6, if the switch position on middle, start the video streaming, else stop it.
    channels = mav.recv_match(type='RC_CHANNELS', blocking=True)
    ch = channels.chan6_raw
    # logging.info(ch)
    if video_streaming is not True:
        if ch > 1400 and ch < 1800:
            os.system('sudo systemctl start raspicam')
            logging.info("Video streaming started")
            video_streaming = True
            # TODO: Send status to mavlink
    else:
        if ch > 1800:
            os.system('sudo systemctl stop raspicam')
            logging.info("Video streaming stopped")
            video_streaming = False
            # TODO: Send status to mavlink

quit()
