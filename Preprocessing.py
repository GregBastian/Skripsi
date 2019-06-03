# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 20:34:24 2018

@author: User
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt



# =============================================================================
# def remove_shadow(img):
#     '''
#     img : unaltered image in GBR Channel
#     returns an image with its shadows removed
#     '''
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     dilated_img = cv2.dilate(img, np.ones((5,5), np.uint8))
#     bg_img = cv2.medianBlur(dilated_img, 21)
#     diff_img = 255 - cv2.absdiff(img, bg_img)
#     norm_img = diff_img.copy() # Needed for 3.x compatibility
#     cv2.normalize(diff_img, norm_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
#     _, thr_img = cv2.threshold(norm_img, 230, 0, cv2.THRESH_TRUNC)
#     cv2.normalize(thr_img, thr_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
#     return thr_img
# =============================================================================

def gaussian_thresh(img):
    '''
    img : a grayscale image
    return an image with erosion and dilation with 5 iterations respectively using a
        5x5 (0) matrix
    '''
    img = np.asarray(np.dot(img[:,:,:3], [0.299, 0.587, 0.114]),dtype=np.uint8)
    img = cv2.GaussianBlur(img,(5,5),0)
    th = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2) 
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel, iterations = 15)
    erosion = cv2.dilate(opening,kernel, iterations = 3)
    return cv2.bitwise_not(erosion)

def cropping(img):
    '''
    img: any 3 channel image
    returns a cropped image containing object of interest in the image
    '''
    edged = cv2.Canny(result, 10, 250)
    (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    idx = 0
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        if w>50 and h>50:
            idx+=1
            new_img=img[y:y+h,x:x+w]
    return new_img

def resizing (img, x, y):
    '''
    x,y : dimensions of resizing
    img : src image that wants to be resized
    returns a resized image with dimensions x and y
    '''
    dimension = (x, y)
    resized = cv2.resize(img, dimension)
    return resized
    
    
    

# Load a color image
img = cv2.imread("001_0004_Iphone7+.jpeg")

threshold = cv2.cvtColor(gaussian_thresh(img), cv2.COLOR_GRAY2BGR)

result = cv2.bitwise_and(img, threshold)

result_cropped = cropping(result)

# Mengubah ukuran citra digital

stacks = np.hstack((resizing(img, 500, 500),resizing(result, 500, 500)))
    

#cv2.imshow('Original Image', resize(300,300,result))
#cv2.imshow('Otsu Segmentation', resize(300,300,result))
#cv2.imshow('Otsu Segmentation+Cropping', resize(300,300, result_cropped))
#cv2.imshow('Original & Segmentated', stacks)
#cv2.imshow('Cropped', resize(300,300, result_cropped))


def algoritma_LBP(img):
    '''
    img : a segmentated image with RGB color channel
    returns an LBP for the img with P = 8 ,R = 1
    '''
    def count_LBP(img,x,y):
        '''
        x,y : current pixel coordinate
        img : current processed image
        returns LBP for current pixel
        '''
        array_twos = np.array([1,2,4,8,16,32,64,128])
        lbp_array_all = [img[x-1,y-1]] + [img[x-1,y]] + [img[x-1,y+1]] + \
                        [img[x,y+1]] + \
                        [img[x+1,y-1]] + [img[x+1,y]] + [img[x+1,y+1]] +\
                        [img[x,y-1]]
        
        lbp_array_convert = [1 if x >= img[x,y] else 0 for x in lbp_array_all]
        return np.sum(np.multiply(lbp_array_convert , array_twos))
        
    reflect_padding = cv2.copyMakeBorder(img,1,1,1,1,cv2.BORDER_REFLECT)
    process = cv2.cvtColor(reflect_padding, cv2.COLOR_BGR2GRAY)
    LBP_hist = {}
    
    for (x,y), value in np.ndenumerate(process):
        if x in [0,process.shape[0]-1] or y in [0,process.shape[1]-1]:
            pass
        else:
            result = count_LBP(process,x,y)
            LBP_hist[result] = LBP_hist.get(result,0) + 1
    return LBP_hist

def algoritma_color_moments(img):
    '''
    img : a segmented image with RGB color channel
    returns a 3x3 matrix where the rows are the mean , standard deviation 
            and skewness and the columns represent color channel B,G,R from 
            top to bottom
    '''
    def get_mean(channel):
        N = channel.size
        mean = 1/N * np.sum(channel)
        return mean
    
    def get_sd(channel, mean):
        N = channel.size
        sd = ( 1/N * np.sum(abs(channel-mean)**2))**(1/2)
        return sd
    
    def get_skewness(channel, mean):
        N = channel.size
        skewness = ( 1/N * np.sum(abs(channel-mean)**3)) ** (1/3)
        return skewness
    

    result = []
    for index in range(3):
        channel = img[:,:,index]
        mean = get_mean(channel)
        sd = get_sd(channel, mean)
        skewness = get_skewness(channel, mean)
        result.append([mean, sd, skewness])
    
    return np.array(result)

def algoritma_color_indexing(cm1, cm2):
    '''
    cm1 : color moments of an image that's part of the training dataset
    cm2 : color moments of an image image that's used for testing
    returns the similarity score between img1 and img2 using color indexing
    '''
    w1,w2,w3 = 1, 2, 1 
    #values of weight is decided by user
    dmom = 0
    for channel in range(3):
        dmom +=  w1*abs(cm1[channel,0] - cm2[channel,0]) +\
                w2*abs(cm1[channel,1] - cm2[channel,1]) +\
                w3*abs(cm1[channel,2] - cm2[channel,2])
                
    return dmom
                
        
    
    
    

test_LBP = algoritma_LBP(resizing(500,500,img))
test_CM = algoritma_color_moments(resizing(500,500,img))
    
        
        
            
            
            
LBP_histogram = algoritma_LBP(resizing(300,300,result_cropped))   
        

cv2.waitKey(0)
cv2.destroyAllWindows()









