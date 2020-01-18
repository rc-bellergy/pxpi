# Live Camera Videos

The live camera videos saved here.
The video format .h264 can be converted to mp4 using the script below:

```
ffmpeg -framerate 15 -i 2020-01-18-livecam.h264 -c copy output.mp4
```