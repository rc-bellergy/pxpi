#!/usr/bin/env python3

'''
Adjust RTL altitude based on the max elevation on the RTL path.
Note: It on work on Position flight mode

Install:
pip3 install mavsdk
pip3 install "python-socketio[asyncio_client]"
'''

import os
import asyncio
import requests
import socketio
import json
import googlemaps

from mavsdk import System, telemetry
from googlemaps_apikey import apikey

home_elevation = 0
default_return_alt = 0 # The ground station RTL altitude setting.
max_alt = 500 # If something goes wrong, limit the mistake.
droneserver = 'http://192.168.192.103:3000'

# Google Maps APi client
# You need to get your api key from Gooogle
# https://developers.google.com/maps/documentation/javascript/get-api-key
gmaps = googlemaps.Client(key=apikey)

# A proxy server to get and convert Google Map API data
# https://github.com/rc-bellergy/droneserver/blob/master/routes/api.php
# api = "http://droneserver.dq.hk/api/rtl-altitude/"

async def run():
    # Init the drone
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state.uuid}")            
            break

    # Connect to droneserver
    sio = socketio.Client()
    sio.connect(droneserver)
    print("droneserver connected")

    # Get RTL altitude from ground station setting
    default_return_alt = await drone.action.get_return_to_launch_altitude()
    print("Default RTL altitude", default_return_alt)

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

        # When 'Position' flight mode, monitoring the drone position and update the Return to Home altitude
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
                    sio.emit('json', location)
                    
                    # try:
                    #     r = requests.get(get_rtl_altitude).json()
                    # except Exception as ex:
                    #     print(ex)

                    # if r is not None: 
                    #     max_elevation = r["max_alt"]
                    #     print("Max elevation:", max_elevation)

                    #     # Update the RTL alt
                    #     return_alt = max_elevation - home_elevation + default_return_alt
                    #     if return_alt < default_return_alt:
                    #         return_alt = default_return_alt
                    #     if return_alt > max_alt:
                    #         return_alt = max_alt
                    #     await drone.action.set_return_to_launch_altitude(return_alt)
                    #     print("Update RTL alt:", return_alt)

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