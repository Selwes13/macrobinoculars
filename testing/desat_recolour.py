#%%
import os
import cv2
from grayscale_recolour import prep_map
from utility import prep_map
home = os.getcwd()
#%%
def process_frame_desat (frame, saturation=0.6, shifts=(1,1,1), include_map=False, im_map=None):
    h,w = frame.shape[:2]
    shifts = [s*saturation if s*saturation < 1 else 1 for s in shifts]

    if (include_map):
        frame[0:h, 0:w, 0] = frame[0:h, 0:w, 0] * im_map[0:h, 0:w]
        frame[0:h, 0:w, 1] = frame[0:h, 0:w, 1] * im_map[0:h, 0:w]
        frame[0:h, 0:w, 2] = frame[0:h, 0:w, 2] * im_map[0:h, 0:w]

    frame[0:h, 0:w, 0] = frame[0:h, 0:w, 0] * shifts[0]
    frame[0:h, 0:w, 1] = frame[0:h, 0:w, 1] * shifts[1]
    frame[0:h, 0:w, 2] = frame[0:h, 0:w, 2] * shifts[2]

    return frame

# %% show

if __name__ == "__main__":
    img = cv2.imread('data\\Images\\\mando_test_image.png')
    h,w = img.shape[:2]

    ratio = 800 / w  
    # Creating a tuple containing width and height
    dim = (800, int(h * ratio))
    # Resizing the image
    img = cv2.resize(img, dim)
    h,w = img.shape[:2]
    
    # lower saturation and shift colour in one move
    saturation = 0.5 # values to multiply all RGB values by (desaturating them)
    shifts = (1.3, 1.3, 0.8) # scale up of B,G,R values to give the blue tint

    im_map = prep_map(h,w)

    im_out = process_frame_desat(img, saturation, shifts, im_map=im_map, include_map=True)

    cv2.imshow('test', im_out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# %%
