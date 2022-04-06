#!/bin/bash

NOW=$(date +"%Y%m%d-%H%M")
VIDEO_FILE=/home/pi/video-stream/videos/$NOW-livecam.h264
UDP_IP=192.168.192.102 # The receiver IP
UDP_PORT=5600

/usr/bin/raspivid -n -w 640 -h 360 -b 1000000 -fps 15 --flush --timeout 0 -o - | \
tee $VIDEO_FILE | \
/usr/bin/gst-launch-1.0 -v fdsrc ! \
h264parse ! rtph264pay config-interval=10 pt=96 ! \
udpsink host=$UDP_IP port=$UDP_PORT