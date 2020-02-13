#!/bin/bash

# Features:
# 1. read raspicam and stream the video to GCS
# 2. save the video to .h264 
# 3. convert the .h264 to .mp4 when the program exit

# Note:
# Since the 4G/3G network offers limited and unstable bandwidth, so the video streaming is limited to the lowest level for monitoring.
# Max bandwidth: 100kB/sec (800000 bits / 8000)
# Play on iPhone 11 full screen 1792 x 828px, 
# Resize video to 320 x 180 aspect ratio 1.777777 (16:9)

# Todo:
# Capture and save the HD video, then resize it for video streaming

NOW=$(date +"%Y%m%d-%H%M")
PATH=/home/pi/raspicam/videos
TMP_VIDEO=$PATH/$NOW.h264
OUT_VIDEO=$PATH/$NOW.mp4
UDP_IP=192.168.192.101 # The MacbookPro
UDP_PORT=5600

/usr/bin/raspivid -v -w 320 -h 180 --rotation 180 --bitrate 800000 -fps 15 \
    --vstab --nopreview --timeout 0 --output - | \
/usr/bin/gst-launch-1.0 -v fdsrc ! \
    h264parse ! rtph264pay ! \
    udpsink host=$UDP_IP port=$UDP_PORT
#/usr/bin/tee $TMP_VIDEO | \


# set -e
# function convert {
#     /usr/bin/MP4Box -add $TMP_VIDEO $OUT_VIDEO
#     /bin/rm $TMP_VIDEO
# }
# trap convert EXIT

