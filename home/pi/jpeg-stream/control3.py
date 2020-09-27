#!/usr/bin/env python3

import time, os, asyncio
from sender2 import Sender
from mavsdk import System

def testingVideo(sender):
    print("--- Testing streaming video start ---")
    sender.streamStart()
    time.sleep(5)
    sender.streamStop()
    print("--- Testing streaming video end ---")

video_sender = Sender()
time.sleep(0.1)  # Wait camera init
# testingVideo(video_sender)

streaming = False
recording = False
flight_mode = "No data"

async def run():

    drone = System(mavsdk_server_address='localhost', port=50051)
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state.uuid}")
            break

    async for fm in drone.telemetry.flight_mode():
        # if flight_mode != fm:
        #     flight_mode = fm
        print("FlightMode:", fm)

    while True:
        print("")
        c = raw_input("Input (s)tream (r)ecord (q)uit: ")
        if c=="s":
            if streaming:
                video_sender.streamStop()
                streaming = False
            else:
                video_sender.streamStart()
                streaming = True
        if c=="r":
            if recording:
                video_sender.recordingStop()
                recording = False
            else:
                video_sender.recordingStart()
                recording = True
                
        if c=="q":
            break

        time.sleep(0.1)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())

# stop all before quit
video_sender.recordingStop()
video_sender.streamStop()


