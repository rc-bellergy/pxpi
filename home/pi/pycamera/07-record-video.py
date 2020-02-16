# Recording video to a file
# https://picamera.readthedocs.io/en/release-1.13/recipes1.html#recording-video-to-a-file

import picamera

camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.start_recording('output/07_video.h264')
camera.wait_recording(5)
camera.stop_recording()