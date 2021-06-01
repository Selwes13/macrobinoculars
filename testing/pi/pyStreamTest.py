print("Start")
from PiVideoStream import PiVideoStream
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import time
import cv2
from PIL import Image
from lib import LCD_2inch4
import sys
#%% setup
# initialize the camera and stream
print("Setup")
print(sys.argv)

disp_screen = True
if (len(sys.argv) > 1):
    disp_screen = 'true' == sys.argv[1].lower()

print("Display on Screen", disp_screen)
#camera = PiCamera()
#camera.resolution = (320, 240)
#camera.framerate = 32
#rawCapture = PiRGBArray(camera, size=(320, 240))
#stream = camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)

# screen
#def __init__(self,spi=spidev.SpiDev(0,0),spi_freq=40000000,rst = 27,dc = 25,bl = 18,bl_freq=1000,i2c=None,i2c_freq=100000):
disp = LCD_2inch4.LCD_2inch4(spi_freq=95000000)
disp.Init()
disp.clear()

#%% run
# created a *threaded *video stream, allow the camera sensor to warmup,

print("[INFO] sampling THREADED frames from `picamera` module...")
vs = PiVideoStream(framerate=24)
vs.start()
time.sleep(2.0)
print("Running")

numFrames = 0
frames = 120
s0 = time.time()
# loop over some frames...this time using the threaded stream
while numFrames < frames:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
    frame = vs.read()

    # displays image on screen
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    d_im = Image.fromarray(frame)
    
    if (disp_screen):
        disp.ShowImage(d_im)

	# update the FPS counter
    numFrames += 1

s1 = time.time()
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()

spf = (s1-s0)/frames
print(spf, "s/frame")

print((1/spf), "fps")
