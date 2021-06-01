#%%
from lib import LCD_2inch4
from PIL import Image
import cv2
import time
from picamera import PiCamera
import numpy as np


#%%

# takes a camera, captures the image into a numpy array
# instead of writing it to a file for reading

#%% setup
print("Preparing... ", end="")
# screen
disp = LCD_2inch4.LCD_2inch4()
disp.Init()
disp.clear()

# camera
w,h=(320,240)
resolution = (w,h)
camera = PiCamera()
camera.resolution = resolution
camera.framerate = 40
camera.sensor_mode = 4
#camera.rotation = 180


# size of the frame to be captured (even 32x16 blocks)
fwidth = (resolution[0] + 31) // 32 * 32
fheight = (resolution[1] + 15) // 16 * 16

# array for writing image to
img_raw = np.empty((fheight, fwidth, 3), dtype=np.uint8)
img = np.empty((h, w, 3), dtype=np.uint8)

print("Done\nWarming Up...")

for i in [4,3,2,1]:
    print(i)
    time.sleep(1/4)

print("Done\nRunning")
#%% run
# take picture
frames = 120
s0 = time.time()
for i in range(frames):
    # read image
    camera.capture(img_raw, 'rgb')
    img = img_raw[:resolution[1], :resolution[0], :]
    
    # 


    #display
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    d_im = Image.fromarray(img)
    disp.ShowImage(d_im)

s1 = time.time()
print("Done")
#%%
disp.module_exit()
spf = (s1-s0)/frames
print(spf, "s/frame")

print((1/spf), "fps")

