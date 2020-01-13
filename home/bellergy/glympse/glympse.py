#!/usr/bin/env python

# Funcations:
# Connect Glympse by REST API
# Send Glympse shared link through Pushbullet
# Connect mavlink through mavlink-router
# Every 5 sec., get GPS data using Mavlink
# Send current location, groundspeed, heading, altitude to Glympse

# Created by: rc@bellergy.com

import sys
import os
import time
import datetime
import logging
import requests
import json
import pymavlink.mavutil as mavutil
import config

# Init logging
dir_path = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(filename=dir_path + "/glympse.log",
                    format='%(asctime)s - %(message)s', level=logging.INFO, filemode='w')
console = logging.StreamHandler()
logger = logging.getLogger()
logger.addHandler(console)

logging.info("**Glympse script start**")

# Load config
drone_name = config.drone["name"]
drone_endpoint = config.drone["endpoint"]
gateway = config.glympse["gateway"]
glympse_api_key = config.glympse["key"]
pb_gateway = config.pushbullet["gateway"]
pb_access_token = config.pushbullet["key"]


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
# logging.info("[Glympse] User:" + glympse_user_id)
# logging.info("[Glympse] Password:" + glympse_password)


glympse_user_id = config.glympse["user_id"]
glympse_password = config.glympse["user_pw"]

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
msg = "You can track the location of your %s here: https://glympse.com/%s" % (
    drone_name, invite_id)
title = "%s's GPS share link" % (drone_name)
send_message(title, msg)
logging.info("[Pushbullet] Sent invite message to Pushbullet")

# Glympse API: setting identifier to the drone_name
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
logging.info("[Glympse] Set identifier to " + drone_name)

# Glympse API: setting Disco thumbnail image
# https://developer.glympse.com/docs/core/api/reference/tickets/append_data/post
response = requests.post(
    gateway+"tickets/" + ticket + "/append_data",
    headers=auth_header,
    json=[{
        't': get_time(),
        'pid': 0,
        'n': 'avatar',
        'v': 'http://bellergy.com/wp-content/uploads/Parrot_Disco_FPV.jpg',
    }]
)
check_return(response)
logging.info("[Glympse] Set Disco thumbnail image")

# Reading drone GPS coordinates every 5 seconds to update Glympse via API

# More information of glympse API:
# https://developer.glympse.com/docs/core/api/reference/tickets/append_location/post
# https://developer.glympse.com/docs/core/api/reference/objects/location-points

# Mavlink GPS message
# https://mavlink.io/en/messages/common.html#GPS_RAW_INT

# Connect to mavlink
logging.info("Waitting heartbeat from " + drone_endpoint)
mav = mavutil.mavlink_connection(drone_endpoint)
mav.wait_heartbeat()
logging.info("Heartbeat received!")

while True:

    # If GPS fix, send data to Glympse
    vfr = mav.recv_match(type='VFR_HUD', blocking=True)
    gps = mav.recv_match(type='GPS_RAW_INT', blocking=True)
    if gps is not None:
        logging.info(gps)
        # Send message only when GPS Fix ready
        if (gps.fix_type > 1):
            data = [[get_time(),
                     gps.lat * 0.1,
                     gps.lon * 0.1,
                     vfr.groundspeed * 100,
                     vfr.heading,
                     vfr.alt]]
            logging.info("Send GPS data: %s" % data)
            response = requests.post(
                gateway+"tickets/" + ticket + "/append_location",
                json=data,
                headers=auth_header
            )
    else:
        logging.info("No GPS Fix")

    time.sleep(5)

quit()
