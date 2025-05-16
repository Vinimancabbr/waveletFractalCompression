import cv2 as cv
import numpy as np
import os
import tempfile
import matplotlib.pyplot as plt
import pywt

image = cv.imread("imageTest\\real-nature-hd-1920x1200-wallpaper-preview.jpg")
#Debug functions  ------------------------------
def getYCbCrSizeData(path, Y, Cb, Cr):
    np.savez(path, Y=Y, Cb=Cb, Cr=Cr)
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

def subSampleChrominance(channel, factor):
    h, w = channel.shape
    result = np.zeros((h // factor, w // factor), dtype=np.uint8)
    
    for i in range(0, h - h % factor, factor):
        for j in range(0, w - w % factor, factor):
            block = channel[i:i+factor, j:j+factor]
            mainColor = block[0][0]
            result[i // factor, j // factor] = np.uint8(mainColor)

    return result

#Discrete Wavelet Transform Compression (code adapted from: https://www.youtube.com/watch?v=eJLF9HeZA8I&ab_channel=SteveBrunton)
def DWTCompression(channel, factor=2, wavelet='haar', threshHold=0.05):
    '''
        Haar wavelet is one of the main choices for image compression
    '''
    coeffs = pywt.wavedec2(channel, wavelet=wavelet, level=factor)
    coeffArr, coeffSlices, = pywt.coeffs_to_array(coeffs)
    #TreshHolding ---------------------
    CoeffSort = np.sort(np.abs(coeffArr.reshape(-1)))
    thresh = CoeffSort[int(np.floor((threshHold) * len(CoeffSort)))]
    ind = np.abs(coeffArr) > thresh
    
    Cfiltered = coeffArr * ind #treshold small indices
    
    return Cfiltered, coeffSlices, wavelet
    
def DWTDecompression(Cfiltered, coeffSlices, wavelet='haar'): 
    coeffsThresholded = pywt.array_to_coeffs(Cfiltered, coeffSlices, output_format='wavedec2')
    reconstructedImage = pywt.waverec2(coeffsThresholded, wavelet=wavelet)
    
    return reconstructedImage.astype('uint8')
    
    
"""
    Usually, the chrominance downsampling factor is fixed at 2, which essentially halves the file size. Since we have three channels (Y, Cb, Cr) 
    that we can consider to be of size "X", when we divide the rows and columns of the chrominance channels by 2, we get: X + X/4 + X/4 = 1.5X, 
    which is half the original size.
    Note: This is not exactly reflected in the size information provided by the getYCbCrSizeData method, since the file format itself has its own intrinsic overhead.
    
"""
Y, Cb, Cr = YCbCrImage(image)
#getYCbCrSizeData("original_444", Y, Cb, Cr)

cv.imshow("Original image", image)

#Discrete Wavelet Transfornm test ------------------------------

#cv.imshow("DWT not compressed", Y)

dwtImage, coeffSlices, wavelet = DWTCompression(Y, 4, 'db1', 0.1)
reconstructedImage = DWTDecompression(dwtImage, coeffSlices, wavelet)

Y2, Cb2, Cr2 = YCbCrImage(reconstructedImage)

YResized = cv.resize(Y2, (image.shape[1], image.shape[0]), interpolation=cv.INTER_CUBIC)

reconstructedImage = cv.merge([YResized, Cb, Cr])
reconstructedImage = cv.cvtColor(reconstructedImage, cv.COLOR_YCrCb2BGR)
cv.imshow("Y DWT compressed", reconstructedImage)
#cv.imshow("DWT compressed image", reconstructedImage)


#Downsampling test ------------------------------
'''
CbDownSample = downSampleChrominance(Cb, 2)
CrDownSample = downSampleChrominance(Cr, 2)
'''




#Subsampling test------------------------------
'''
CbSubSampled = subSampleChrominance(Cb, 100)
CrSubSampled = subSampleChrominance(Cr, 100)
'''

#getYCbCrSizeData("subsampled_420", Y, CbDownSample, CrDownSample)


#Rebuilding image for visualization ------------------------------
'''
CbResized = cv.resize(CbDownSample, (image.shape[1], image.shape[0]), interpolation=cv.INTER_CUBIC)
CrResized = cv.resize(CrDownSample, (image.shape[1], image.shape[0]), interpolation=cv.INTER_CUBIC)
'''


#Subsampling visualization ------------------------------
'''
cv.imshow("Chroma blue original: ", Cb)
cv.imshow("Chroma blue subsample", CbResized)
cv.imshow("Chroma red original: ", Cr)
cv.imshow("Chroma red subsample", CrResized)
cv.imshow("Y: ", Y)
'''



#Image visualization:

'''
reconstructedImage = cv.merge([Y, CbResized, CrResized])
reconstructedImage = cv.cvtColor(reconstructedImage, cv.COLOR_YCrCb2BGR)

cv.imshow("Original image", image)
cv.imshow("Reconstructed image", reconstructedImage)
'''

cv.waitKey(0)