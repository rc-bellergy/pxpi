#!/bin/bash

# Since the 4G/3G network offers limited bandwidth, so the video streaming is limited to the lowest level for FPV.
# Video: 360w x 202h on 15 FPS 
# Max bandwidth: 187.5kB/sec (1500000 bits / 8000)

NOW=$(date +"%Y-%m-%d")
VIDEO_FILE=${PWD}/$NOW/cam.mp4
UDP_IP=192.168.192.103
UDP_PORT=5600

/usr/bin/raspivid -n -w 360 -h 202 -rot 180 -b 1500000 -fps 15 -ISO 800 -vs -drc high -t 0 -o - | \
tee test.h264 | \
/usr/bin/gst-launch-1.0 -v fdsrc ! \
h264parse ! rtph264pay config-interval=10 pt=96 ! \
udpsink host=$UDP_IP port=$UDP_PORT

### Don't use multiudpsink, it increases the bandwidth
# multiudpsink clients=192.168.192.103:5600,192.168.192.104:5600


### Save the stream to .h264 file
# /usr/bin/raspivid -n -w 360 -h 202 -rot 180 -b 1500000 -fps 15 -ISO 800 -vs -drc high -t 0 -o - | \
# tee test.h264 | \
# /usr/bin/gst-launch-1.0 -v fdsrc ! \
# h264parse ! rtph264pay config-interval=10 pt=96 ! \
# udpsink host=$UDP_IP port=$UDP_PORT

# gst-launch-0.10 filesrc location=input.yuv ! video/x-raw-yuv,width=1280,height=720,framerate=30/1 ! ffmpegcolorspace ! autovideosink

# raspivid -t 999999 -h 720 -w 1080 -fps 25 -hf -b 2000000 -o - | \
# tee YOURFILENAME.h264 | \
# gst-launch-1.0 -v fdsrc ! h264parse !  rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host=YOUR-PI-IP-ADDRESS port=5000 

# Capture 30 seconds of raw video at 640x480 and 150kB/s bit rate into a pivideo.h264 file:
    # raspivid -t 30000 -w 640 -h 480 -fps 25 -b 1200000 -p 0,0,640,480 -o pivideo.h264 
# Wrap the raw video with an MP4 container: 
    # MP4Box -add pivideo.h264 pivideo.mp4
# Remove the source raw file, leaving the remaining pivideo.mp4 file to play
# rm pivideo.h264

# gst-launch-1.0 filesrc location=test.h264 ! video/x-h264 ! h264parse ! mp4mux ! filesink location=output.mp4

# gst-launch-1.0 -v filesrc location=test.h264 ! \
# h264parse ! rtph264pay config-interval=10 pt=96 ! \
# filesink location=output.mp4