#!/usr/bin/env python3

import asyncio
import pymavlink.mavutil as mavutil
import time, os
from mavsdk import System



def connectMavlink():
    # Connect to mavlink
    link = "udpin:127.0.0.1:14551"
    print("Connecting Mavlink:", link)
    mav = mavutil.mavlink_connection(link)
    mav.wait_heartbeat()
    print("Mavlink heartbeat received!")
    return mav

async def run():

    gcsIP = "192.168.192.101"

    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state.uuid}")
            break

    async for flight_mode in drone.telemetry.flight_mode():
        print("FlightMode:", flight_mode)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())

# while (True):
#     response = os.system("ping -c 1 192.168.192.101 >/dev/null 2>&1")
#     if response == 0:
#         print('Datalink is up!')
#     else:
#         print('Datalink is down!')
#     time.sleep(5)

