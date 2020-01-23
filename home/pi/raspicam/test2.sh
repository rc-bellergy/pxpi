#!/bin/bash

NOW=$(date +"%Y%m%d-%H%M")
TMP_VIDEO=${PWD}/videos/$NOW.h264
OUT_VIDEO=${PWD}/videos/$NOW.mp4
UDP_IP=192.168.192.104 # The iPhone
UDP_PORT=5600

raspivid -o - -t 0 -w 1280 -h 720 -fps 25 -b 4000000 -g 50 | \
ffmpeg -re -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -f h264 \
-i - -vcodec copy -acodec aac -ab 128k -g 50 -strict experimental -f flv rtmp://a.rtmp.youtube.com/live2/<key goes here>
