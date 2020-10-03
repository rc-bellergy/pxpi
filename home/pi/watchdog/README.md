# Watchdog
The `watchdog` is a background program on a offboard computer. I will monitoring the connection to ground station. If the connection lost, it sill send a RTL request to the PX4 flight stack.

## Why not use PX4 flight stack native failsfe actions?
I need to do following:
    If there is RC connection, use RC;
    If RC lost, use datalink (joystick) control;
    If datalink lost and flight mode is `POSITION`, change the flight mode to `RETURN`;

## Install

    pip3 install mavsdk
    pip3 install aioconsole