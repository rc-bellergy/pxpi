# pxpi drone project
Pixhawk + Raspberry Pi + 4G network drone development\
It is the source code of the Raspberry Pi files.

## Features
- Connect Pixhawk and Raspberry Pi using `mavlink-router` and `pymavlink`
- Raspberry Pi send mavlink data to ground station through UDP;
- Raspberry Pi read mavlink GPS data and submit the drone position to `glympse` through glympse API in real-time;
- Raspberry Pi camera send video streaming to ground station;
- The pilot can use radio control to switch on/off the video streaming;

## Source Files
| files                                    | descriptions                                  |
| ---------------------------------------- | --------------------------------------------- |
| glympse/glympse.py                       | Send GPS position to Glympse API              |
| mavlink-router-service/mavlink-router.sh | strat mavlink-router service when system boot |
| raspicam/raspicam.sh                     | start raspicam service when system boot       |
| rc/rc.py                                 | Switch video streaming on/off                 |


