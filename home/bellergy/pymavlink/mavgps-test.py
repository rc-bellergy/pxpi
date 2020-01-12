#!/usr/bin/python

# Sample: ./mavgps-test.py 127.0.0.1:14550

from __future__ import print_function

import pymavlink.mavutil as mavutil
import sys
import time

mav = mavutil.mavlink_connection('udpin:127.0.0.1:14550')
print("Waitting Heartbeat...")
mav.wait_heartbeat()
print("Received Heartbeat!")

print("Mavlink version 2.0:", mav.mavlink20())

while True:
    gps_status = mav.recv_match(type='GPS_RAW', blocking=False)
    if gps_status is not None:
        print("GPS Status:", gps_status)

    # Get UTM_GLOBAL_POSITION from BAD_DATA
    # https://mavlink.io/en/messages/common.html#UTM_GLOBAL_POSITION
    # pymavlink didn't implement it?
    bad_data = mav.recv_match(type='BAD_DATA', blocking=False) # DFMessage

    # if the bad_data message id is 340, it is UTM_GLOBAL_POSITION
    if bad_data is not None:
        if bad_data.reason == "unknown MAVLink message ID 340":
            print(bad_data.data)

    ## Print all mavlink messages
    # msg = mav.recv_msg()
    # if msg is not None:
    #     print("msg:", msg)