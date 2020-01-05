#!/bin/bash

# It echo the upload and download speed every 5 sec.
while true; do
    awk '{if(l1){print "Down:"($2-l1)/1024"kB/s","Up:"($10-l2)/1024"kB/s"} else{l1=$2; l2=$10;}}' \
        <(grep wlan0 /proc/net/dev) <(sleep 5; grep wlan0 /proc/net/dev)
done