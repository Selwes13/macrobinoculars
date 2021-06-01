#%%https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
#%% setup camera and screen
s0 = time.time()
w,h=(320,240)
camera = PiCamera(resolution=(w,h))
rawCapture = PiRGBArray(camera)


s1 = time.time()

# grab an image from the camera
camera.capture(rawCapture, format="bgr")
image = rawCapture.array

s2 = time.time()

cv2.imwrite("cv_test.png", image)
#%%
print("setup: ", str(s1-s0))
print("picture: ", str(s2-s1))