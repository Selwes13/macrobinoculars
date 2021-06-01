#%%
import os
import numpy as np
import cv2
from utility import prep_map
#%% average pixel value (turn grey) then multiply to blue-ish colour

def process_frame_grey (frame, include_map=False, im_map=None, shifts=(1,1,1)):
    h,w = frame.shape[:2]
    im2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if (include_map):
        im2 = im2[0:h, 0:w] * im_map[0:h, 0:w]

    # pixel = gray_pixel * map * shift_colour
    frame[0:h, 0:w, 0] = im2[0:h, 0:w] * shifts[0]
    frame[0:h, 0:w, 1] = im2[0:h, 0:w] * shifts[1]
    frame[0:h, 0:w, 2] = im2[0:h, 0:w] * shifts[2]

    frame = frame.astype('uint8')
    return frame

#%%
if __name__ == "__main__":
    img = cv2.imread('data\\Images\\\mando_test_image.png')
    h,w = img.shape[:2]

    ratio = 800 / w  
    # Creating a tuple containing width and height
    dim = (800, int(h * ratio))
    # Resizing the image
    img = cv2.resize(img, dim)

    # lower saturation and shift colour in one move
    desat = 0.6 # values to multiply all RGB values by (desaturating them)
    shifts = (1.3, 1.3, 0.8) # scale up of B,G,R values to give the blue tint
    shifts = [s*desat if s*desat < 1 else 1 for s in shifts]
    print(shifts)

    h,w = img.shape[:2]
    print(img.shape)

    # load contour map
    im_map = prep_map(h,w)

    im_out = process_frame_grey(img, include_map=True, im_map=im_map, shifts=shifts)

    cv2.imshow('test', im_out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# %%
