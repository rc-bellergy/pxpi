#!/usr/bin/env python

# Config file sample
# Update the data below and save file as config.py

drone = { 
    "name": "pxpi" ,
    "endpoint": "udpin:127.0.0.1:14550" }

# Register glympse API:
# https://developer.glympse.com/account/apps
# Platform: Web API
# OS: Web
glympse = { 
    "gateway": "https://api.glympse.com/v2/",
    "key": "REPLACE-GLYMPSE-API-KEY-HERE",
    "user_id": "REPLACE-GLYMPSE-USER_ID",
    "user_pw": "REPLACE-GLYMPSE-USER_PASSWORD" }


pushbullet = { 
    "gateway": "https://api.pushbullet.com/v2/pushes",
    "key": "REPLACE-PUSHBULLET-API-KEY-HERE" }
    
