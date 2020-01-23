#!/bin/bash

# Testing
# Direct use 
#

UDP_IP=192.168.192.104 # The iPhone
UDP_PORT=5600

gst-launch-1.0 v4l2src device=/dev/video0 ! \
video/x-h264,width=360,height=202,framerate=25/1 ! \
rtph264pay ! \
udpsink host=$UDP_IP port=$UDP_PORT
