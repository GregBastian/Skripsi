# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 20:08:06 2018

@author: Admin
"""

import cv2
import glob
import numpy as np

folder_training="alltrains/"
list_label=[]
        
#loop over the training images        
for files in glob.glob(folder_training + "*"):
    list_label.append(files+"/")    

#OTSU SEGMENTATION
for i in range (0,len(list_label)):
    for files in glob.glob(list_label[i] + "*"):
        r = 0
        r+=1
        img = cv2.imread(files)
        image = cv2.resize(img, (500, 500))
        #cv2.imshow('resize',image)
        mask = cv2.GaussianBlur(image, (11, 11), 0)
        #cv2.imshow('blur',mask)
        lab = cv2.cvtColor(mask, cv2.COLOR_BGR2LAB)
        b = lab[:,:,2]
        #cv2.imshow('Gray', b)
        #cv2.waitKey(0)
        ret3,th3 = cv2.threshold(b,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        #cv2.imshow('treshold', th3)
        #cv2.waitKey(0)
        inv = cv2.bitwise_not(th3)
        # cv2.imshow('inverse', inv)
        # cv2.waitKey(0)
        kernel = np.ones((7, 7), np.uint8)
        dilation = cv2.dilate(inv,kernel,iterations = 1)
        #cv2.imshow('Dilation', dilation)
        #cv2.waitKey(0)
        erotion = cv2.erode(dilation,np.ones((7, 7), np.uint8),iterations = 1)
        #cv2.imshow('Erotion', erotion)
        #cv2.waitKey(0)
        '''
        contour_info = []
        im2, contours, hierarchy = cv2.findContours(erotion, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            contour_info.append((
                c,
                cv2.isContourConvex(c),
                cv2.contourArea(c),
            ))
        contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
        max_contour = contour_info[0]
        cnt = max_contour[0]
        leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
        rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
        topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
        bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
        cropBW = erotion[topmost[1]:bottommost[1], leftmost[0]:rightmost[0]]
        cropImage = image[topmost[1]:bottommost[1], leftmost[0]:rightmost[0]]
        #cv2.imshow("img",cropImage)
        #cv2.waitKey()
        '''
        h, w = image.shape[:2]
        for x in range(h):
            for y in range(w):
                if (erotion[x][y] == 0):
                    image[x][y] = 0
        cv2.imwrite(files+"_baru.jpg", image)
    cv2.destroyAllWindows()
        #cv2.imshow('pre', cropImage)
        #cv2.waitKey(0)