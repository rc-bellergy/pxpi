#!/usr/bin/python

# Testing send mavlink message
# The mavlink-router setting is
# mavlink-routerd -e 127.0.0.1:14550 0.0.0.0:5760

from __future__ import print_function
from threading import Thread
from time import sleep

import pymavlink.mavutil as mavutil
import sys
import time

UDP = "127.0.0.1:14550"
SOURCE_SYSTEM_ID = 99
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