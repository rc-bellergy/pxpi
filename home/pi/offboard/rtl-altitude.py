#!/usr/bin/env python3

'''
Adjust RTL altitude based on the max elevation on the RTL path.
Note: It on work on Position flight mode

Install:
pip3 install mavsdk
pip3 install "python-socketio[asyncio_client]"

Install the droneserver:
https://github.com/rc-bellergy/droneserver

Start the mavsdk server: /home/travmix/pi/MAVSDK-Python/mavsdk/bin/
MAVSDK-Python/mavsdk/bin/mavsdk_server udp://127.0.0.1:14550 -p 5000
'''

import os
import asyncio
import requests
import socketio
import json
import googlemaps
from mavsdk import System, telemetry, action
from googlemaps_apikey import apikey

home_elevation = 0
default_return_alt = 0 # The ground station RTL altitude setting.
max_alt = 500 # If something goes wrong, limit the mistake.
droneserver = 'http://droneserver.zt:3000'

# Google Maps APi client
# You need to get your api key from Gooogle
# https://developers.google.com/maps/documentation/javascript/get-api-key
gmaps = googlemaps.Client(key=apikey)

async def run():
    # Init the drone
    # Read here for setup mavsdk_server
    
    # drone = System(mavsdk_server_address='localhost', port="5000")
    # await drone.connect(system_address="udp://127.0.0.1:14550")

    drone = System()
    await drone.connect(system_address="udp://:14540")
    print("Waiting for drone...")
    
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state.uuid}")            
            break

    # Create socket to droneserver
    sio = socketio.AsyncClient()
    await sio.connect(droneserver)
    await sio.emit('message', "Hello from rtl-altitude3.py")
    print("droneserver connected")

    # Receive RTL altutude update request from droneserver
    @sio.on('set_rtl_altitude')
    async def set_rtl_altitude(data):
        max_elevation = data['max_alt']['elevation']
        print("Received max elevation:", data['max_alt'])

        # Update the RTL alt
        return_alt = max_elevation - home_elevation + default_return_alt
        if return_alt < default_return_alt:
            return_alt = default_return_alt
        if return_alt > max_alt:
            return_alt = max_alt
        await drone.action.set_return_to_launch_altitude(return_alt)
        print("Set RTL alt:", return_alt)

    # Get RTL altitude from ground station setting
    default_return_alt = await drone.action.get_return_to_launch_altitude()
    print("Default RTL altitude", default_return_alt)

    # Send updated location to drone server
    while True:

        # Wait armed
        print("Wait Armed")
        async for is_armed in drone.telemetry.armed():
            if is_armed == True:
                break

        # Get home position
        async for h in drone.telemetry.home():
            home_position = (h.latitude_deg, h.longitude_deg)
            print("Home position:", home_position)
            break

        # Get home elevation
        home_elevation =  gmaps.elevation(home_position)[0]["elevation"]
        print("Home elevation:", home_elevation)

        # When 'Position' flight mode, send the drone location to drone server
        while True:

            # Wait Position mode
            # http://mavsdk-python-docs.s3-website.eu-central-1.amazonaws.com/plugins/telemetry.html#mavsdk.telemetry.FlightMode
            async for flight_mode in drone.telemetry.flight_mode():
                break
                
            if flight_mode == telemetry.FlightMode.POSCTL: 
                async for p in drone.telemetry.position():

                    location = {
                        "home":"{},{}".format(home_position[0], home_position[1]),
                        "drone":"{},{}".format(p.latitude_deg,p.longitude_deg)
                    }
                    await sio.emit('get_rtl_altitude', location)
                    print("Drone location", location)                    

                    break

            async for status in drone.telemetry.landed_state():
                break

            if status == telemetry.LandedState.ON_GROUND:
                # Reset the default return alt when quit
                await drone.action.set_return_to_launch_altitude(default_return_alt)
                print("On Ground")
                print("Reset Return to Home alt:", default_return_alt)
                print("---------")
                break
            else:
                await asyncio.sleep(2)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())