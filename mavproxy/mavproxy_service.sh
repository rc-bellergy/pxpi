## NOT IN USE. ##
## Now using /etc/rc.local

#!/bin/bash
echo "MAVProxy service starting..."
echo $USER
cd /home/bellergy/mavproxy
mavproxy.py --master=/dev/ttyS0,57600 --out=udp:192.168.192.100:14550 --out=udp:192.168.192.101:14550 --out=udp:127.0.0.1:14550 --aircraft pxpi
echo "MAVProxy service started"
exit 0
