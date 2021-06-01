#%%
import cv2
import numpy as np
#%% loads shape cutout and scales it to the input image

def prep_map (w,h, im_path='data\\Images\\\cutout_map.png'):
    im_map = cv2.imread(im_path, cv2.IMREAD_GRAYSCALE)

    # scale to size of input image
    dim = (w,h)
    im_map = cv2.resize(im_map, dim)

    # makes it a scale from 0-1

    def scale_pixels(v):
        return v//255

    scale_pixel_vect  = np.vectorize(scale_pixels)
    im_map = scale_pixel_vect(im_map)

    return im_map
#im_map[0:h, 0:w] = im_map[0:h, 0:w] + 1
#h,w = img.shape[:2]
#print(np.unique(im_map))
#print(im_map.shape)
#print(np.unique(im_map))

#%% adds scan lines by darkening alternating sets of 10 horizontal lines
def scan_lines (frame, size=10, saturation=0.8):
    w = len(frame[0])

    dim = False # if line should be dimmed or not
    # adds pointer for each row
    for i in range(len(frame)):
        if (dim):
            frame[i, 0:w] = frame[i, 0:w] * saturation
        
        # alternates dimming every 'size' lines
        if (i%size == 0):
            dim = not dim

    return frame


if __name__ == "__main__":
    img = cv2.imread('data\\Images\\\mando_test_image.png')
    h,w = img.shape[:2]

    ratio = 800 / w  
    # Creating a tuple containing width and height
    dim = (800, int(h * ratio))
    # Resizing the image
    img = cv2.resize(img, dim)

    # adds scanline
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = scan_lines(img, size=4)
    

    cv2.imshow('test', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# %%
