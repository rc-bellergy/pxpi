#!/usr/bin/env python3

import asyncio
from mavsdk import System


async def print_flight_mode():
    drone = System()
    print("Waiting for drone to connect...")
    await drone.connect(system_address="udp://127.0.0.1:14550")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state.uuid}")
            break

    async for flight_mode in drone.telemetry.flight_mode():
        print("FlightMode:", flight_mode)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_flight_mode())
