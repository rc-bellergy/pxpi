#!/usr/bin/env python3

# When drone armed, start the video streaming
# when disarmed, kill the video streaming

import os, subprocess, psutil
import asyncio
from mavsdk import System, telemetry

def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

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
            if video_streaming == False:
                print("Armed")
                # Start video stream process
                video_streaming = True
                proc = subprocess.Popen("./stream.sh", stdout=subprocess.PIPE, shell=True)
                print("Video Streaming Start")
        else:
            if video_streaming:
                print("Disarmed")
                # Kill video stream process
                video_streaming = False
                try:
                    kill(proc.pid)
                    print("Video Streaming Stop")
                except:
                    print("Loop")

        await asyncio.sleep(1)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
