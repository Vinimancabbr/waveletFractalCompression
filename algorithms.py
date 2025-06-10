import cv2 as cv
import numpy as np
import os
import tempfile
import matplotlib.pyplot as plt
import pywt
import pickle

#image = cv.imread("waveletFractalCompression\\imageTest\\real-nature-hd-1920x1200-wallpaper-preview.jpg")

#Debug functions  ------------------------------
def getSerializedSize(data, name="Data"):
    serialized = pickle.dumps(data)
    total_bytes = len(serialized)
    size_kb = total_bytes / 1024
    size_mb = size_kb / 1024

    print(f"{name} -> {total_bytes} bytes ({size_kb:.2f} KB / {size_mb:.2f} MB)")
    return total_bytes
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

def channelsResize(Y, Cb, Cr, imageShape):
    YResized = cv.resize(Y, (imageShape[1], imageShape[0]), interpolation=cv.INTER_CUBIC)
    CbResized = cv.resize(Cb, (imageShape[1], imageShape[0]), interpolation=cv.INTER_CUBIC)
    CrResized = cv.resize(Cr, (imageShape[1], imageShape[0]), interpolation=cv.INTER_CUBIC)
    
    reconstructedImage = cv.merge([YResized, CbResized, CrResized])
    reconstructedImage = cv.cvtColor(reconstructedImage, cv.COLOR_YCrCb2BGR)
    return reconstructedImage
    
#Discrete Wavelet Transform Compression (code adapted from: https://www.youtube.com/watch?v=eJLF9HeZA8I&ab_channel=SteveBrunton)
def DWTCompression(channel, factor=2, wavelet='haar', threshHold=0.05):
    '''
        Haar wavelet is one of the main choices for image compression
    '''
    coeffs = pywt.wavedec2(channel, wavelet=wavelet, level=factor)
    
    coeffArr, coeffSlices, = pywt.coeffs_to_array(coeffs)
    
    
    #TreshHolding ---------------------
    CoeffSort = np.sort(np.abs(coeffArr.reshape(-1)))

    thresh = CoeffSort[int(np.floor((1 - threshHold) * len(CoeffSort)))]
    ind = np.abs(coeffArr) > thresh
    
    Cfiltered = coeffArr * ind #treshold small indices
    data = Cfiltered, coeffSlices, wavelet
    #cv.imshow("Decomposição DWT", Cfiltered)
    return data
    
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
#cv.imshow("Original image", image)

#cv.imshow("Original image", image)


#Y, Cb, Cr = YCbCrImage(image)
#originalData = (Y, Cb, Cr)
#getSerializedSize(originalData, "OriginalImageInfo")


#Discrete Wavelet Transfornm test ------------------------------

#cv.imshow("DWT not compressed", Y)

#DWTData = DWTCompression(Y, 15, 'haar', 1)

#reconstructedImage = DWTDecompression(DWTData[0], DWTData[1], DWTData[2])
#getSerializedSize(DWTData, "DWTDecompressedImageInfo")
#Y2, Cb2, Cr2 = YCbCrImage(reconstructedImage)


#reconstructedImage = channelsResize(Y2, Cb, Cr, image.shape)
#cv.imshow("DWT compressed image", reconstructedImage)

#Downsampling test ------------------------------
'''
CbSampled = downSampleChrominance(Cb, 10)
CrSampled = downSampleChrominance(Cr, 10)
'''

#Downsampling test ------------------------------
#CbSampled = downSampleChrominance(Cb, 20)
#CrSampled = downSampleChrominance(Cr, 20)


#Subsampling test------------------------------
'''
CbSampled = subSampleChrominance(Cb, 100)
CrSampled = subSampleChrominance(Cr, 100)
'''

#getYCbCrSizeData("subsampled_420", Y, CbDownSample, CrDownSample)


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
downSampledImageData = (Y, CbSampled, CrSampled)
getSerializedSize(downSampledImageData, "downSampledImageData")
reconstructedImage = channelsResize(Y ,CbSampled, CrSampled, image.shape)
cv.imshow("Original image", image)
cv.imshow("Reconstructed image", reconstructedImage)
'''

#cv.waitKey(0)