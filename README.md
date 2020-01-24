# pxpi drone project
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

## Source Files
| files                                    | descriptions                                  |
| ---------------------------------------- | --------------------------------------------- |
| glympse/glympse.py                       | Send drone's GPS position to Glympse          |
| mavlink-router-service/mavlink-router.sh | Routing mavlink from FC to GCS                |
| raspicam/raspicam.sh                     | Start raspicam and streaming the video to GCS |
| rc/rc.py                                 | Use RC to switch video streaming on/off       |

## Notes
For more information of the project, please read [here](https://github.com/rc-bellergy/drone-notes/tree/master/ardupilot/pxpi-plane)
