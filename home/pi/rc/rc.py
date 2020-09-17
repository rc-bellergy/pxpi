#!/usr/bin/env python

# Listen the RC channel change
# then take related action
# https://mavlink.io/en/messages/common.html#RC_CHANNELS

import time
import os
import logging
import pymavlink.mavutil as mavutil
import config
import sys
sys.path.insert(0, "/home/pi/jpeg-stream")
import jpegsender
reload(jpegsender)


# Init logging
dir_path = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(filename=dir_path + "/rc.log",
                    format='%(asctime)s - %(message)s', level=logging.INFO, filemode='w')
console = logging.StreamHandler()
logger = logging.getLogger()
logger.addHandler(console)
logging.info("**RC script start**")

# Connect to mavlink
drone_endpoint = config.drone["endpoint"]
logging.info("Waitting heartbeat from " + drone_endpoint)
mav = mavutil.mavlink_connection(drone_endpoint)
mav.wait_heartbeat()
logging.info("Heartbeat received!")

# Create JPEGSender and connection
sender = jpegsender.JPEGSender("192.168.192.101")
sender.connect()

# Listen channels
logging.info("Listening the RC_CHANNEL 6")
while True:

    
    # Watch the channel 6, if the switch position on middle, start the video streaming, else stop it.
    # channels = mav.recv_match(type='RC_CHANNELS', blocking=True)
    # ch = channels.chan6_raw
    # logging.info(ch)
    # if sender.isStreaming() is not True:
    #     if ch > 1400 and ch < 1800:
    #         sender.streamStart()
    #         logging.info("Video streaming started")
    #         # TODO: Send status to mavlink
    # else:
    #     if ch > 1800:
    #         sender.streamStop()
    #         logging.info("Video streaming stopped")
    #         # TODO: Send status to mavlink

quit()
