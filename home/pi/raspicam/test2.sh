#!/bin/bash

# Testing: gstreamer resize

NOW=$(date +"%Y%m%d-%H%M")
PATH=/home/pi/raspicam/videos
TMP_VIDEO=$PATH/$NOW.h264
OUT_VIDEO=$PATH/$NOW.mp4
UDP_IP=192.168.192.101 # The MacbookPro
UDP_PORT=5600

/usr/bin/raspivid -w 320 -h 180 --rotation 180 --bitrate 800000 -fps 15 \
    --vstab --nopreview --timeout 0 --output - | \
/usr/bin/gst-launch-1.0 -v fdsrc ! \
    videoscale ! video/x-raw,width=160,height=90 ! \
    x264enc ! h264parse ! rtph264pay ! \
    udpsink host=$UDP_IP port=$UDP_PORT
