#!/bin/bash

/usr/bin/raspivid -n -w 320 -h 180 -rot 0 -b 500000 -fps 15 -ISO 800 -vs -drc high -t 0 -o - | \
/usr/bin/gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=10 pt=96 ! udpsink host=192.168.192.101 port=5600