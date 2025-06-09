from random import randint
from math import sqrt
import cv2 as cv
import numpy as np

# --- Functions ---

def subsample(image, ratio=2):
    # Creates a new, empty image (ratio²) times smaller than the original
    new_image = np.zeros((len(image) // ratio, len(image[0]) // ratio, 1), dtype=np.uint8)

    # Runs once for each set of (ratio) pixels
    for y in range(0, len(image), ratio):
        for x in range(0, len(image[y]), ratio):
            # Calculates the average...
            avg = np.average(image[y:y+ratio, x:x+ratio])

            # ...then sets it as the value for a pixel on the new image
            for i in range(y, y + ratio):
                for j in range(x, x + ratio):
                    new_image[i // ratio, j // ratio] = int(avg)
    
    return new_image

def transform(image, axis, rotation_times, contrast=1, brightness=0):
    return contrast*np.rot90(np.flip(image, axis), rotation_times)+brightness

def all_transforms(image) -> list:
    transforms = []

    for i in range(1, 3):
        transforms.append({'axis': 1, 'rotation': i, 't': transform(image, 1, i)})
        transforms.append({'axis': 2, 'rotation': i, 't': transform(image, 2, i)})

    return transforms

# Function taken from https://github.com/pvigier/fractal-image-compression/blob/master/compression.py
def find_contrast_and_brightness2(D, S):
    # Fit the contrast and the brightness
    A = np.concatenate((np.ones((S.size, 1)), np.reshape(S, (S.size, 1))), axis=1)
    b = np.reshape(D, (D.size,))
    x, _, _, _ = np.linalg.lstsq(A, b)
    return x[1], x[0]

def encode(image, segsize=4):
    transforms = []

    domain = subsample(image)

    for i in range(0, len(domain), segsize):
        for j in range(0, len(domain), segsize):
            segment = domain[i:i+segsize, j:j+segsize]
            t = all_transforms(segment)

            d = 0
            for k in range(0, len(t)):
                contrast, brightness = find_contrast_and_brightness2(t[k]['t'], segment)

                val = abs(np.sum(contrast*t[k]['t']+brightness) - np.sum(segment))

                if val <= abs(np.sum(contrast*t[d]['t']+brightness) - np.sum(segment)):
                    d = k
            
            domain[i:i+segsize, j:j+segsize] = contrast*t[k]['t']+brightness

            # cv.imshow('D', domain)
            # cv.waitKey(0)

            transforms.append({'axis': t[d]['axis'], 'rotation': t[d]['rotation'], 'contrast': contrast, 'brightness': brightness})

    return transforms

def decode(transforms, steps=8, res=512):
    new_image = np.zeros((res, res, 1), dtype=np.uint8)

    for i in range(0, res):
        for j in range(0, res):
            new_image[i, j] = randint(0, 255)

    segsize = res // int(sqrt(len(transforms)))

    for i in range(0, steps):
        k = 0
        for i in range(0, res, segsize):
            for j in range(0, res, segsize):
                new_image[i:i+segsize, j:j+segsize] = transform(image=new_image[i:i+segsize, j:j+segsize], axis=transforms[k]['axis'], rotation_times=transforms[k]['rotation'], contrast=transforms[k]['contrast'], brightness=transforms[k]['brightness'])
                k += 1

                # cv.imshow('ni', new_image)
                # cv.waitKey(0)

    return new_image
# --- Functions ---

img = cv.imread('fractal/assets/Old classic/zelda.bmp')

# Ensures the image is grayscale
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY, img)
img = decode(encode(img))

cv.imshow('Image', img)
cv.waitKey(0)
