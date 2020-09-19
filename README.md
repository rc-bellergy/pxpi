# Toritaka drone project
Pixhawk + Raspberry Pi + 4G network drone development\
It is the source code of the Raspberry Pi files.

## Tested on Hardwares/Components
- Body: **Parrot Disco**
- FC: **Pixhawk (FMU V2)**
- Onboard computer: **Raspberry Pi 3**
- Network: **HUAWEI E3372** (3G/4G)

## Support Firmware
- Firmware: **ArduPlane 3.0**

## Features
- Connect Pixhawk and Raspberry Pi using `mavlink-router` and `pymavlink`
- Raspberry Pi send mavlink data to ground station through UDP;
- Raspberry Pi read mavlink GPS data and submit the drone position to `glympse` through glympse API in real-time;
- Raspberry Pi camera send video streaming to ground station;
- The pilot can use radio control to switch on/off the video streaming;

## Source Files in /home/pi/
| files in                                 | descriptions                                               |
| ---------------------------------------- | ---------------------------------------------------------- |
| glympse/glympse.py                       | Send drone's GPS position to Glympse                       |
| mavlink-router-service/mavlink-router.sh | Routing mavlink from FC to GCS                             |
| jpeg-stream/sender2.py                   | Sending low bandwidth, low latency video stream            |
| jpeg-stream/receiver.py                  | Receiving and playback the stream video (on groundstation) |
| jpeg-stream/control.py                   | Use remote control to start, stop, recording video         |

## systemd enabled services
- mavlink-router.service
- wvdial.service

## Restart mavlink-router
sudo systemctl restart mavlink-router.service

## Check mavlink-router service log
sudo journalctl -u mavlink-router

## Notes
For more information of the project, please read [here](https://github.com/rc-bellergy/drone-notes/tree/master/ardupilot/toritaka)
