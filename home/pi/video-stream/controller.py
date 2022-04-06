#!/usr/bin/env python3

import os, subprocess
import asyncio
from mavsdk import System, telemetry

async def run():

    # Init the drone
    drone = System()
    print("Waiting for drone to connect...")
    await drone.connect(system_address="udp://:14550")

    video_streaming = False

    async for state in drone.core.connection_state():
        if state.is_connected:
            print(state)
            break

    async for is_armed in drone.telemetry.armed():
        if is_armed:
            print("Armed")
            if video_streaming == False:
                video_streaming = True
                subprocess.Popen()
                os.system("./stream.sh")
                print("Video Streaming Start")
        else:
            print("Disarmed")
            if video_streaming:
                video_streaming = False
                # Kill video stream process

                print("Video Streaming Stop")
        await asyncio.sleep(1)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
