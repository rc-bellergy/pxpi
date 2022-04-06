#!/usr/bin/python

# Testing send mavlink message

from __future__ import print_function
from threading import Thread
from time import sleep

import pymavlink.mavutil as mavutil
import sys
import time

UDP = "192.168.192.101:14550" # The IP and port of QGroundcontrol. It can't be a broadcast IP.
SOURCE_SYSTEM_ID = 99 # Me, the sender
TARGET_SYSTEM_ID = 255 # QGroundcontrol

mav = mavutil.mavlink_connection('udpout:' + UDP, source_system=SOURCE_SYSTEM_ID)

def pingloop():
    i = 0
    while (True):
        msg = mav.mav.ping_send(int(time.time() * 1000), i, TARGET_SYSTEM_ID, 1)
        i = i + 1
        sleep(1)


pingthread = Thread(target=pingloop)
pingthread.daemon = True
pingthread.start()

while (True):
    msg = mav.recv_match(blocking=True)
    print("Message from %d: %s" % (msg.get_srcSystem(), msg))