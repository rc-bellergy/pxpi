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

default_return_alt = 0 # The ground station RTL altitude setting.
home_location = None
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
    print("Connecting to droneserver")
    sio = socketio.AsyncClient()
    await sio.connect(droneserver)
    await sio.emit('message', "Hello from rtl-altitude.py")
    print("droneserver connected")

    # Events handle
    @sio.on('rtl_altitude_updated')
    async def set_rtl_altitude(max_elevation):
        print("Received max elevation:", max_elevation)

        # Update the RTL alt
        return_alt = max_elevation - home_location['alt'] + default_return_alt
        if return_alt < default_return_alt:
            return_alt = default_return_alt
        if return_alt > max_alt:
            return_alt = max_alt
        await drone.action.set_return_to_launch_altitude(return_alt)
        print("Set RTL alt:", return_alt)

    # Get RTL altitude from ground station setting
    default_return_alt = await drone.action.get_return_to_launch_altitude()
    print("Default RTL altitude", default_return_alt)

    while True:

        # Wait armed
        print("Wait Armed")
        async for is_armed in drone.telemetry.armed():
            if is_armed == True:
                break

        # Get home position from the drone
        async for h in drone.telemetry.home():
            a = gmaps.elevation((h.latitude_deg, h.longitude_deg))[0]["elevation"]
            home_location = { "lat": h.latitude_deg, "lon": h.longitude_deg, "alt": a }
            print("Home position", home_location)
            await sio.emit('home_location_updated', home_location)
            break

        # Wait the drone launch
        print("Wait the drone launch")
        async for state in drone.telemetry.landed_state():
            if state == telemetry.LandedState.IN_AIR:
                break

        # Main Loop
        while True:
            
            # Wait GPS 3D Fixed
            async for gps_info in drone.telemetry.gps_info():
                if gps_info.fix_type.value > 2: #FixType.FIX_2D = 2 
                    break
                else:
                    print("Wait GPS 3D Fix")

            # Wait support flight mode
            async for flight_mode in drone.telemetry.flight_mode():
                if flight_mode == telemetry.FlightMode.MISSION or flight_mode == telemetry.FlightMode.OFFBOARD  or flight_mode == telemetry.FlightMode.MANUAL or flight_mode == telemetry.FlightMode.POSCTL or flight_mode == telemetry.FlightMode.RATTITUDE or flight_mode == telemetry.FlightMode.STABILIZED:
                    break

            # Update the drone location and emit to droneserver
            async for p in drone.telemetry.position():
                data = {
                    "lat": p.latitude_deg,
                    "lon": p.longitude_deg
                }
                await sio.emit('drone_location_updated', data)
                print("Drone location", data)                    

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