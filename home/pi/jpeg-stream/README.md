# JPEG Stream
It provides a low bandwidth, low latency video stream service.

## The Purpose
For long-range FPV flight, it doesn't care about the image quality. It provides just enough information to let the pilot knows how to control the plane. The most important thing is that it can provide low latency video and use low bandwidth.

## Low bandwidth
The streaming video uses around 100 Kb - 150 Kb per sec. It can stream real-time video in a low bandwidth network. (e.g. a weak signal 4G network)

## Low latency
In actual tests on a weak signal a 4G network, the streaming video latency can be as low as 48ms.
![](references/video-latency.png)

[Demo video](https://www.youtube.com/embed/BpVMlIxjAsc)

## Low CPU load
In actual tests on a Raspberry PI 3, the sender.py script used under 20% CPU load.

---
## Hardware Requirements
### Sender
- Raspberry PI
- Raspberry Pi Camera Module\
(Tested: Raspberry PI 3 and Raspberry Pi Camera v1.3)

### Receiver
- Any machine that can run Python 2 or 3\
(Tested: MacbookPro with Python 3)
