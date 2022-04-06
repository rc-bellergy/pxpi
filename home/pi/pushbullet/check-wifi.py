# A cronjob call this script every minute,
# If the Wi-Fi hotspot changed, send a message to pushbullet
# The ESSID will be saved to wifi-status.txt
# Everytime the system boot, the wifi-status.txt will be cleaned by the /etc/rc.local

#!/usr/bin/env python3
from multiprocessing.connection import wait
from urllib import response
import requests, subprocess, re
import sys, os, time
os.chdir('/home/pi/pushbullet')
sys.path.insert(0,'..')
import config

# Load config
pb_gateway = config.pushbullet["gateway"]
pb_access_token = config.pushbullet["key"]

def send_message(title, msg):
    response = requests.post(
        pb_gateway + 'pushes',
        headers={"Access-Token": pb_access_token},
        json={
            'type': 'note',
            'title': title,
            'body': msg
        }
    )

def get_wifi_info():
    result = "No wifi connected"
    r = subprocess.Popen("iwconfig wlan0", stdout=subprocess.PIPE, shell=True)
    r = r.communicate()[0].decode("utf-8")
    r = re.search("ESSID:\".*\"", r)
    if r:
        result = r.group(0)
    return result

if __name__=="__main__":
    wifi = get_wifi_info()
    send_message('Wi-Fi updated: ', wifi)
    