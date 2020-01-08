#!/usr/bin/env python

# Connect Glympse by REST API
# Send current location
# Created by: rc@bellergy.com
# Updated: 20191226

import sys,os,time,datetime
import logging
import requests,json
from dronekit import connect

logging.basicConfig(pathname="/tmp/glympse.log", format='%(asctime)s - %(message)s', level=logging.INFO, filemode='w')
logging.StreamHandler()
logging.info("**Glympse script start**")

drone_name = "PxPi"
gateway = "https://api.glympse.com/v2/"
glympse_api_key = "0i4vFATHsIo4OZm9bheI"
pb_gateway = "https://api.pushbullet.com/v2/pushes"
pb_access_token = "o.8wRiGgA35DDAYfLRX6OOyVmggwqU80VW"

def check_return(response):
    if response.status_code != 200 or response.json()["result"] != "ok":
        logging.info("[Glympse] API Error ")
        logging.info(response.json())
        quit()


def get_time():
    return int(time.time()) * 1000

def send_message(title, msg):
    response = requests.post(
    pb_gateway,
    headers={"Access-Token": pb_access_token},
    json={
        'type': 'note',
        'title': title,
        'body': msg
    }
)

# Connect to mavproxy
logging.info("[Dronekit] Connecting the drone through udp:127.0.0.1:14550")
vehicle = connect('127.0.0.1:14550', wait_ready=True)
logging.info("[Dronekit] Connected")

# Craete account
# logging.info("[Glympse] Creating account")
# response = requests.post(
#     gateway+"account/create",
#     params={'api_key': glympse_api_key}
# )
# check_return(response)
# account = response.json()["response"]
# glympse_user_id = account["id"]
# glympse_password = account["password"]
glympse_user_id="0Y73-FQ8A-7DKZA"
glympse_password="ev_SF519dbd7JORLq_n"

# Login
logging.info("[Glympse] Login")
response = requests.post(
    gateway+"account/login",
    params={
        'api_key': glympse_api_key,
        'id': glympse_user_id,
        'password': glympse_password
    }
)
check_return(response)
access_token = response.json()["response"]["access_token"]
logging.info("[Glympse] Access Token: " + access_token)

# Create ticket
auth_header = {"Authorization": "Bearer " + access_token}
response = requests.post(
    gateway+"users/self/create_ticket",
    headers=auth_header,
    params={
        'duration': '14400000'
    }
)
check_return(response)
ticket = response.json()["response"]["id"]
logging.info("[Glympse] Ticket: " + ticket)

# Craete Invite
response = requests.post(
    gateway+"tickets/" + ticket + "/create_invite",
    headers=auth_header,
    params={
        'type': 'sms',
        'address': '1234567890',
        'send': 'client'
    }
)
check_return(response)
invite_id = response.json()["response"]["id"]
logging.info("[Glympse] Invite Id: " + invite_id)

# Send Invite Message to Pushbullet
msg = "You can track the location of your %s here: https://glympse.com/%s" % (drone_name, invite_id)
title = "%s's GPS share link" % (drone_name)
send_message(title, msg)
logging.info("[Pushbullet] Sent invite message to Pushbullet")

# Glympse API: setting identifier to Disco ID
# https://developer.glympse.com/docs/core/api/reference/tickets/append_data/post
response = requests.post(
    gateway+"tickets/" + ticket + "/append_data",
    headers=auth_header,
    json=[{
        't': get_time(),
        'pid': 0,
        'n': 'name',
        'v': drone_name,
    }]
)

check_return(response)
logging.info("[Glympse] Set identifier to Disco ID")

# Glympse API: setting Disco thumbnail image
# https://developer.glympse.com/docs/core/api/reference/tickets/append_data/post
response = requests.post(
    gateway+"tickets/" + ticket + "/append_data",
    headers=auth_header,
    json=[{
        't': get_time(),
        'pid': 0,
        'n': 'avatar',
        'v': 'https://uavpal.com/img/disco.png',
    }]
)
check_return(response)
logging.info("[Glympse] Set Disco thumbnail image")

# Reading out drone GPS coordinates every 5 seconds to update Glympse via API
# Where is the drone GPS data? I use the DroneKit.

# More information of glympse API:
# https://developer.glympse.com/docs/core/api/reference/tickets/append_location/post
# https://developer.glympse.com/docs/core/api/reference/objects/location-points

# send_message("%s Status Update" % drone_name, "Connected to mavproxy, ready to send GPS.")

while True:

    # If GPS fix, send data to Glympse
    fix_type = vehicle.gps_0.fix_type
    logging.info("vehicle.gps_0.fix_type: %s" % fix_type)

    if fix_type > 1:
        data = [[get_time(),
            vehicle.location.global_frame.lat * 1000000,
            vehicle.location.global_frame.lon * 1000000,
            vehicle.groundspeed,
            0,
            vehicle.location.global_frame.alt]]
        logging.info("Send GPS data: %s" % data)
        response = requests.post(
            gateway+"tickets/" + ticket + "/append_location",
            json=data,
            headers=auth_header
        )
    else:
        logging.info("[Dronekit] GPS No Fix.")
        time.sleep(5)

quit()