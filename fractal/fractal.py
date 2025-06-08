import cv2 as cv
import numpy as np

# --- Functions ---

def subsample(image, ratio=4):
    # Creates a new, empty image (ratio²) times smaller than the original
    new_image = np.zeros((len(image) // ratio, len(image[0]) // ratio, 1), dtype=np.uint8)
    
    # Runs once for each set of (ratio) pixels
    for y in range(0, len(image), ratio):
        for x in range(0, len(image[y]), ratio):
            
            # Calculates the average...
            avg = 0
            for i in range(y, y + ratio):
                for j in range(x, x + ratio):
                    avg = avg + (image[i][j] / (ratio * ratio))

            # ...then sets it as the value for a pixel on the new image
            for i in range(y, y + ratio):
                for j in range(x, x + ratio):
                    new_image[i // ratio][j // ratio] = int(avg)
    
    return new_image

def encode(image):
    pass

def decode(image):
    pass

# --- Functions ---

img = cv.imread('fractal/assets/Old classic/zelda.bmp')

# Ensures the image is grayscale
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY, img)

img = encode(img)

cv.imshow('Image', img)
cv.waitKey(0)
