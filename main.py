print("Start")
from PiVideoStream import PiVideoStream
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import time
import cv2
import numpy as np
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

resolution=(480, 320)
w,h=resolution
print("Display on Screen", disp_screen)

# lower saturation and shift colour in one move
saturation = 0.5 # values to multiply all RGB values by (desaturating them)
shifts = (1.3, 1.3, 0.8) # scale up of B,G,R values to give the blue tint
shifts = [s*saturation if s*saturation < 1 else 1 for s in shifts]
include_map = False# include cutout overlay
print("Shifts: ", shifts)
# memory for frame editing
img = np.empty((h, w, 3), dtype=np.uint8)

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
frameMax = 120
s0 = time.time()
# loop over some frames...this time using the threaded stream
while numFrames < frameMax:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
    img = vs.read().copy()

    # transform frame
    if (include_map):
        img[0:h, 0:w, 0] = img[0:h, 0:w, 0] * img[0:h, 0:w]
        img[0:h, 0:w, 1] = img[0:h, 0:w, 1] * img[0:h, 0:w]
        img[0:h, 0:w, 2] = img[0:h, 0:w, 2] * img[0:h, 0:w]

    img[0:h, 0:w, 0] = img[0:h, 0:w, 0] * shifts[0]
    img[0:h, 0:w, 1] = img[0:h, 0:w, 1] * shifts[1]
    img[0:h, 0:w, 2] = img[0:h, 0:w, 2] * shifts[2]


    # displays image on screen
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    d_im = Image.fromarray(img)
    
    if (disp_screen):
        disp.ShowImage(d_im)

	# update the FPS counter
    numFrames += 1

s1 = time.time()
# do a bit of cleanup
vs.stop()

spf = (s1-s0)/frameMax
print(spf, "s/frame")

print((1/spf), "fps")
