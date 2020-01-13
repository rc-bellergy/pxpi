#!/bin/bash

# Since the 4G network offers limited bandwidth, so the video streaming is limited to the lowest level.
# Video: 320w x 180h on 15 FPS 
# Max bandwidth: 500kB/sec

NOW=$(date +"%Y-%m-%d")
VIDEO_FILE=${PWD}/$NOW/cam.mp4
UDP_IP=192.168.192.103
UDP_PORT=5600

/usr/bin/raspivid -n -w 320 -h 180 -rot 180 -b 500000 -fps 15 -ISO 800 -vs -drc high -t 0 -o - | \
/usr/bin/gst-launch-1.0 -v fdsrc ! \
h264parse ! rtph264pay config-interval=10 pt=96 ! \
udpsink host=$UDP_IP port=$UDP_PORT
# multiudpsink clients=192.168.192.103:5600,192.168.192.104:5600
