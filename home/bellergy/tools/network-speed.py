#!/usr/bin/env python

###
# Get the download and upload values (KB/s) of wlan0
# Send the result to mavlink

import os
import time
import pymavlink.mavutil as mavutil


UDP = "192.168.192.103:14550" # The IP and port of QGroundcontrol. It can't be a broadcast IP.
SOURCE_SYSTEM_ID = 99 # Me, the sender
TARGET_SYSTEM_ID = 255 # QGroundcontrol

seq = 0
interval = 1 # send the result every 5 sec.
download = None
upload = None

mav = mavutil.mavlink_connection('udpout:' + UDP, source_system=SOURCE_SYSTEM_ID, dialect="common")
print("Mavlink2.0:", mav.mavlink20())

while True:
    stream = os.popen("awk '/wlan0/ {print $2, $10}' /proc/net/dev")
    output = stream.read()
    data = output.split()
    now_download = int(data[0])
    now_upload = int(data[1])

    if download is not None:
        output_d = float(now_download - download)/1024/interval
        output_u = float(now_upload - upload)/1024/interval
        print("Rx: %f | Tx: %f" % (output_d, output_u))

        # Send the result to mavlink
        # Using message https://mavlink.io/en/messages/common.html#ONBOARD_COMPUTER_STATUS
        seq = seq +1
        # msg = mav.mav.ping_send(int(time.time() * 1000), seq, TARGET_SYSTEM_ID, 1)
        # msg = mav.mav.param_ext_value_send("Testing","Hello",3,4,5)
        msg = mav.mav.onboard_computer_status_send(int(time.time() * 1000), int(time.time() * 1000), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        

    download = now_download
    upload = now_upload
    
    time.sleep(interval)