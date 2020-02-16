import cv2

from CameraServer import CameraServer

# Method that starts the ServerFolde system
def startStreamer():

    # Create and start the camera threads
    # These threads cannot die.  They now only need to be started once.

    c1 = CameraServer(5800)
    c1.run()
    # c2 = CameraServer(5801)
    # c2.start()
    # c3 = CameraServer(5802)
    # c3.start()
    # c4 = CameraServer(5804)
    # c4.start()


# Start this flaming pile of garbage
startStreamer()
