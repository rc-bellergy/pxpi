#!/usr/bin/env python

###
# Get the download and upload values (KB/s) of wlan0
# Send the result to mavlink

import os
import time
import pymavlink.mavutil as mavutil


NETWORK = "zt2lrwgvd2" # The Zerotier network interface
UDP = "192.168.192.101:14550" # The IP and port of QGroundcontrol. (Can't it be a broadcast IP? I tried 192.168.192.255 but not work)
SOURCE_SYSTEM_ID = 99 # Me, the sender
TARGET_SYSTEM_ID = 255 # QGroundcontrol

seq = 0
interval = 2 # send the result every 2 sec.
download = None
upload = None

mav = mavutil.mavlink_connection('udpout:' + UDP, source_system=SOURCE_SYSTEM_ID, dialect="common")
print("Mavlink2.0:", mav.mavlink20())
sh_command = "awk '/%s/ {print $2, $10}' /proc/net/dev" % NETWORK
print("Monitoring Network: %s" % NETWORK)

while True:
    stream = os.popen(sh_command)
    output = stream.read()
    data = output.split()
    now_download = int(data[0])
    now_upload = int(data[1])

    if download is not None:
        output_d = float(now_download - download)/1024/interval
        output_u = float(now_upload - upload)/1024/interval
        print("Rx: %f | Tx: %f" % (output_d, output_u))

        # Send the result to mavlink (Under testing)
        # Changed to mavlink v2 and dialect to "common", but still command not found. Why?
        # Using message https://mavlink.io/en/messages/common.html#ONBOARD_COMPUTER_STATUS

        seq = seq +1
        msg = mav.mav.ping_send(int(time.time() * 1000), seq, TARGET_SYSTEM_ID, 1) # PING and other Mavlink v1 commands work.
        # msg = mav.mav.param_ext_value_send("Testing","Hello",3,4,5)
        # msg = mav.mav.onboard_computer_status_send(int(time.time() * 1000), int(time.time() * 1000), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        

    download = now_download
    upload = now_upload
    
    time.sleep(interval)