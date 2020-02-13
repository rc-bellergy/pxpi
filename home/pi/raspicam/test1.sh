#!/bin/bash

# Use gstreamer only

/usr/bin/gst-launch-1.0 -v v4l2src ! tee name=t ! queue ! \
'video/x-h264,width=800,height=448,framerate=30/1' ! \
h264parse ! rtph264pay config-interval=10 pt=96 ! \
udpsink host=192.168.192.101 port=5600 \
# t. ! queue ! filesink location="test.h264"

set -e
function convert {
    /usr/bin/MP4Box -add test.h264 test.mp4
    /bin/rm test.h264
}
trap convert EXIT