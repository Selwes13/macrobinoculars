#%%
from lib import LCD_2inch4
from PIL import Image
import cv2
import time
from picamera import PiCamera
import numpy as np

#%% recording function times
times = []
lbls = []
times.append(time.time())

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
camera.framerate = 80
camera.sensor_mode = 4
#camera.rotation = 180


# size of the frame to be captured (even 32x16 blocks)
fwidth = (resolution[0] + 31) // 32 * 32
fheight = (resolution[1] + 15) // 16 * 16

# array for writing image to
img_raw = np.empty((fheight, fwidth, 3), dtype=np.uint8)
img = np.empty((h, w, 3), dtype=np.uint8)

print("Done\nWarming Up...", end="")
times.append(time.time())
lbls.append("Setup")

time.sleep(2)
times.append(time.time())
lbls.append("Warmup")

print("Done\nRunning")
#%% run

# read image
camera.capture(img_raw, 'rgb')

times.append(time.time())
lbls.append("Read")

# trim full frame to size
img = img_raw[:resolution[1], :resolution[0], :]

times.append(time.time())
lbls.append("Trim")


#img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
#img = cv2.resize(img, (h,w))

#change format
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
times.append(time.time())
lbls.append("Format")

#display
d_im = Image.fromarray(img)
times.append(time.time())
lbls.append("To Pillow")


disp.ShowImage(d_im)
times.append(time.time())
lbls.append("Display")

print("Done")

#%% close
disp.module_exit()

#%% display timeline

for i in range(len(lbls)):
    print(lbls[i], "->", times[i+1] - times[i])


