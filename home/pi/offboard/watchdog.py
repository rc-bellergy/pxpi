#!/usr/bin/env python3

import os
import asyncio
from mavsdk import System, telemetry


async def run():
    # Init the drone
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state.uuid}")
            break

    # If ping ground station fail, return to launch
    async for flight_mode in drone.telemetry.flight_mode():
        # http://mavsdk-python-docs.s3-website.eu-central-1.amazonaws.com/plugins/telemetry.html#mavsdk.telemetry.FlightMode
        if flight_mode == telemetry.FlightMode.POSCTL or flight_mode == telemetry.FlightMode.HOLD:
            if pingGroundstation() == False:
                print("Lost connection to the ground station")
                await drone.action.return_to_launch()
                print("Return to Launch")

        await asyncio.sleep(1)

def pingGroundstation():

    hostname = "groundstation.zt"
    response = os.system("ping -c 1 " + hostname)
    return response==0


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
