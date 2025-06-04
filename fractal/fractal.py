import cv2 as cv
import numpy as np

# --- Functions ---

def encode(image):
    pass

def decode(image):
    pass

# --- Functions ---

img = cv.imread('fractal/assets/Old classic/zelda.bmp')

# Ensures the image is grayscale
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY, img)

encode(img)

cv.imshow('Image', img)
cv.waitKey(0)
