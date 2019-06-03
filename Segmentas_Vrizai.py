# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 03:25:11 2018

@author: Vriza Wahyu Saputra
"""
import numpy as np
import cv2
import os
from os import walk
class Segmentasi:  
    def preprocessing(image):
        #Ubah ukuran gambar
        img1 = cv2.resize(image, (200,200))
        img2 = cv2.resize(image, (200,200))
        
        #Blur gambar dan ubah warna dari RGB ke HSV
        gaussianBlur = cv2.GaussianBlur(img2, (5, 5), 30)
        image = cv2.cvtColor(gaussianBlur, cv2.COLOR_BGR2HSV)
        
        #Ubah warna HSV menjadi biner
        ret, mask = cv2.threshold(image, 80, 255, cv2.THRESH_BINARY)
        img2gray = cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY)
        ret, mask1 = cv2.threshold(img2gray, 110, 255, cv2.THRESH_BINARY)
        
        # Menghapus noise menggunakan opening
        kernel = np.ones((3,3),np.uint8)
        opening = cv2.morphologyEx(mask1,cv2.MORPH_OPEN,kernel, iterations =3)
        
        #hasil = cv2.bitwise_not(opening)
        img1_bg = cv2.bitwise_and(img1,img1,mask = opening)
        cv2.imshow('Vriza', img1_bg)
        return None
#        cv2.imwrite(os.path.join(path , filenames),img1_bg)

        """cv2.imshow('Gambar Asli', img1)
        cv2.imshow('Gaussian Blur', gaussianBlur)
        cv2.imshow('HSV', image)
        cv2.imshow('GRAY', img2gray)
        cv2.imshow('EROSI DILASI', opening)
        cv2.imshow('Hasil Segmentasi', img1_bg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()"""

Segmentasi.preprocessing(cv2.imread('009_0159_Iphone7+.jpeg'))



# =============================================================================
# 
#     def saveImages(self):
#         for dirpath, dirnames, filenames in walk('../Dataset/Asli/029'):
#             for x in filenames:
#                 image = cv2.imread(dirpath+'/'+x)
#                 self.preprocessing(image, '../Dataset/Preprocessing2',x)
# =============================================================================
