#!/usr/bin/env python

# Listen the RC channel change
# then take related action
# https://mavlink.io/en/messages/common.html#RC_CHANNELS

import time, os, sys, datetime, logging
import pymavlink.mavutil as mavutil

sys.path.append('/home/pi/')
import config

if __name__=="__main__":
    # Init logging
    dir_path = os.path.dirname(os.path.realpath(__file__))
    now = datetime.datetime.now()
    logging.basicConfig(filename=dir_path + now.strftime("/logs/%Y%m%d-%H%M.log"),
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

    # Listen channels
    logging.info("Listening the RC_CHANNEL")
    while True:

        print("loop")
        channels = mav.recv_match(type='RC_CHANNELS', blocking=True)
        ch = channels.chan6_raw
        logging.info(ch)

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