#%%
import os
import cv2
import numpy as np

from utility import prep_map, scan_lines
from grayscale_recolour import  process_frame_grey
from desat_recolour import process_frame_desat
#%%
reshape = True

cap = cv2.VideoCapture(0)

ret, frame = cap.read()

if (reshape):
    w,h = (480, 320)
    #h,w = frame.shape[:2]


# sets up the RGB transformations
desat = 0.6 # values to multiply all RGB values by (desaturating them)
shifts = (1.4, 1.4, 0.9) # scale up of B,G,R values to give the blue tint
shifts = [s*desat for s in shifts]
print(shifts)

im_map = prep_map(w=w,h=h, im_path='images\\\cutout_map_320x240.png')

for i in range(24*20):
    #read frame
    ret, frame = cap.read()

    if (reshape):
        frame = cv2.resize(frame, (w,h))

    frame_grey = process_frame_grey(frame.copy(), 
                                    shifts=shifts,
                                    include_map=True, 
                                    im_map=im_map
                                    )
    frame_grey = scan_lines(frame_grey, size=3)

    frame_desat = process_frame_desat(frame.copy(), 
                                        saturation=desat, 
                                        shifts=shifts,
                                        include_map=True, 
                                        im_map=im_map
                                        )
    frame_desat = scan_lines(frame_desat, size=3)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    cv2.imshow('grey',frame_grey)
    cv2.imshow('desat',frame_desat)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
# %%

# %%
