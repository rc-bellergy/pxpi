#!/usr/bin/env python3

import os
import asyncio
from mavsdk import System, telemetry


async def run():

    # In the RPi, need to start the mavsdk_server first
    # The udp://127.0.0.1:14550 is connection port from mavlink-router
    # ~/MAVSDK-Python/mavsdk/bin/mavsdk_server udp://127.0.0.1:14550
    
    # Init the drone
    drone = System()
    print("Waiting for drone to connect...")
    await drone.connect(system_address="udp://:14550")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print(state)
            break

    # If ping ground station fail, return to launch
    async for flight_mode in drone.telemetry.flight_mode():
        print(flight_mode)
        await asyncio.sleep(1)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
