#!/usr/bin/python

# Testing receive mavlink message
# The mavlink-router setting is
# mavlink-routerd -e 127.0.0.1:14550 0.0.0.0:5760

from __future__ import print_function

import pymavlink.mavutil as mavutil
import sys
import time

# if len(sys.argv) != 3:
#     print("Usage: %s <ip:udp_port> <system-id>" % (sys.argv[0]))
#     print("Receive mavlink heartbeats on specified interface. "
#           "Respond with a ping message")
#     quit()

UDP = "127.0.0.1:14550"
SYSTEM_ID = 50

srcSystem = SYSTEM_ID
mav = mavutil.mavlink_connection(
    'udpin:' + UDP, source_system=srcSystem)

while (True):
    msg = mav.recv_match(type='PING', blocking=True)
    print("Message from %d: %s" % (msg.get_srcSystem(), msg))
    if msg.target_system == 0:
        print("\tMessage sent to all")
    elif msg.target_system == srcSystem:
        print("\tMessage sent to me")
    else:
        print("\tMessage sent to other")
    mav.mav.ping_send(
        int(time.time() * 1000), msg.seq,
        msg.get_srcSystem(), msg.get_srcComponent())