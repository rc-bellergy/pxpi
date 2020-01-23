#!/bin/bash

# Since the 4G/3G network offers limited bandwidth, so the video streaming is limited to the lowest level for FPV.
# Video: 360w x 202h on 15 FPS 
# Max bandwidth: 180kB/sec (1440000 bits / 8000)

NOW=$(date +"%Y%m%d-%H%M")
TMP_VIDEO=${PWD}/videos/$NOW.h264
OUT_VIDEO=${PWD}/videos/$NOW.mp4
UDP_IP=192.168.192.104 # The iPhone
UDP_PORT=5600

/usr/bin/raspivid -w 360 -h 202 --rotation 180 --bitrate 1440000 -fps 15 \
    --flush --vstab --nopreview --timeout 0 --output - | \
/usr/bin/tee $TMP_VIDEO | \
/usr/bin/gst-launch-1.0 fdsrc ! \
h264parse ! rtph264pay config-interval=10 pt=96 ! \
udpsink host=$UDP_IP port=$UDP_PORT

set -e
function convert {
    MP4Box -add $TMP_VIDEO $OUT_VIDEO
    rm $TMP_VIDEO
}
trap convert EXIT