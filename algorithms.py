import cv2 as cv
import numpy as np
import os
import tempfile

image = cv.imread("imageTest\\real-nature-hd-1920x1200-wallpaper-preview.jpg")


#Debug functions  ------------------------------
def getYCbCrSizeData(path, Y, Cb, Cr):
    np.savez_compressed(path, Y=Y, Cb=Cb, Cr=Cr)
    size_bytes = os.path.getsize(path + ".npz")
    size_kb = size_bytes / 1024
    size_mb = size_kb / 1024
    print(f"{path}.npz -> {size_bytes} bytes ({size_kb:.2f} KB / {size_mb:.2f} MB)")
    os.remove(path + ".npz")
    
#JPEG Processing  ------------------------------
def YCbCrImage(originalImage):
    imageRGB = cv.cvtColor(originalImage, cv.COLOR_BGR2RGB)
    imageYCbCr = cv.cvtColor(imageRGB, cv.COLOR_RGB2YCrCb)
    Y, Cb, Cr = cv.split(imageYCbCr)
    return Y, Cb, Cr

def downSampleChrominance(channel, factor):
    h, w = channel.shape
    result = np.zeros((h // factor, w // factor), dtype=np.uint8)
    
    for i in range(0, h - h % factor, factor):
        for j in range(0, w - w % factor, factor):
            block = channel[i:i+factor, j:j+factor]
            mean_val = np.mean(block, dtype=np.float32)
            result[i // factor, j // factor] = np.uint8(mean_val)

    return result

"""
    Usually, the chrominance downsampling factor is fixed at 2, which essentially halves the file size. Since we have three channels (Y, Cb, Cr) 
    that we can consider to be of size "X", when we divide the rows and columns of the chrominance channels by 2, we get: X + X/4 + X/4 = 1.5X, 
    which is half the original size.
    Note: This is not exactly reflected in the size information provided by the getYCbCrSizeData method, since the file format itself has its own intrinsic overhead.
    
"""
Y, Cb, Cr = YCbCrImage(image)
getYCbCrSizeData("original_444", Y, Cb, Cr)

Cb = downSampleChrominance(Cb, 2)
Cr = downSampleChrominance(Cr, 2)
getYCbCrSizeData("subsampled_420", Y, Cb, Cr)


#Rebuilding image for visualization ------------------------------
CbResized = cv.resize(Cb, (image.shape[1], image.shape[0]), interpolation=cv.INTER_CUBIC)
CrResized = cv.resize(Cr, (image.shape[1], image.shape[0]), interpolation=cv.INTER_CUBIC)


reconstructedImage = cv.merge([Y, CbResized, CrResized])
reconstructedImage = cv.cvtColor(reconstructedImage, cv.COLOR_YCrCb2BGR)


cv.imshow("Original image", image)
cv.imshow("Reconstructed image", reconstructedImage)

cv.waitKey(0)