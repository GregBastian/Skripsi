# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 00:14:33 2019

@author: Wulan
"""

import csv
import numpy as np
import math
import text_preprocessing as pp
import os
from tfidf import tfidf
from Document import Document

'''
with open('hasilpreprop.csv', mode='w', newline='') as test_file:
    for nomor, hasil_preprocessing in enumerate(hasil):
        file_writer = csv.writer(test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # yang diatas nggk perlu kamu ganti

        file_writer.writerow([nomor, hasil_preprocessing])
        # yang diatas ini masukin data ke tiap row dalam urutan nomor lalu ke
        # hasil preprocessing
'''

directory = os.fsencode(os.getcwd())
totalDocuments = 0

BOW = set([]) #biar gak duplikat
df = {}
docObjects = []
 
#proses pembuatan BOW & freOfWords untuk menghitung idf
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename == '2017 ganjil TI lama.csv':
        with open(filename) as csv_file:
            fileReader = csv.reader(csv_file, delimiter=',')
            hasilReadCSV = ''
            for column in fileReader:
                totalDocuments += 1
                namaDosen = column[0]
                matkul = column[1]
                hasilReadCSV += column[4] + ' '
                review = pp.preprocessing(hasilReadCSV)
                docObjects.append(Document(namaDosen, matkul, review))
                
                BOW.update(pp.preprocessing(hasilReadCSV, tokenize = True))
            for word in BOW:
                df[word] = df.get(word,0) + 1
    else:
        pass
    
    
with open('HASIL PREPROCESSING.csv', mode='w', newline = '') as test_file:
    for document in docObjects:
        image_writer = csv.writer(test_file, delimiter=',', quotechar='"', 
                                  quoting=csv.QUOTE_MINIMAL)
        namaDosen = document.get_namaDosen()
        matkul = document.get_matkul()
        review = document.get_review()
        image_writer.writerow([namaDosen, matkul, review])
    
    


#proses menghitung tf idf
processedObjects = []

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename == 'HASIL PREPROCESSING.csv':
        with open(filename) as csv_file:
            fileReader = csv.reader(csv_file, delimiter=',')
            hasilReadCSV = ''
            for column in fileReader:
                hasilReadCSV = column[4] + ' '
                tf  = pp.count_words(hasilReadCSV)
                tfw = {}
                idf = {}
                wtd = {}
            for word in BOW:
                #########proses tf###########
                if tf[word] != 0:
                    tfw[word] = 1 + math.log10(tf[word])
                else:
                    tfw[word] = 0
                #########proses idf###########    
                idf[word] = math.log10(totalDocuments/df[word])
                #########proses wtd###########
                wtd[word] = tfw[word] * idf[word]
                
            ########proses instansiasi objek##########
            processedObjects.append(tfidf(tf, tfw, idf, wtd))
            
            
with open('HASIL TF-IDF.csv', mode='w', newline = '') as test_file:
    first_row = True
    for document in processedObjects:
        image_writer = csv.writer(test_file, delimiter=',', quotechar='"', 
                                  quoting=csv.QUOTE_MINIMAL)
        if first_row == True:
            words = sorted(list(BOW))
            image_writer.writerow(words)
            first_row = False
        else:
            wtd_document = document.get_wtd()
            hasil_tfidf_dokumen = [wtd_document[word] for word in sorted(BOW.values())]
            image_writer.writerow(hasil_tfidf_dokumen)
            


print(tf)
print('==============================')
print(tfw)
print('==============================')
print(idf)
print('==============================')
print(wtd)

            


#with open('coba.csv') as csv_file:
#    file_reader = csv.reader(csv_file, delimiter=',')
#    hasil_preprocessing_read = []
#    for column in file_reader:
#        nomor = column[5]
#        hasil_preprocessing_read += column[1].split()
#
#    semua_kata = ' '.join(hasil_preprocessing_read)
#    tf = pp.count_words(semua_kata)
#    print(tf, '<-- tf')
#
#    tfw = {}
#    for key in tf.keys():
#        tfw[key] = 1 + math.log10(tf.get(key))
#
#    print(tfw, '<-- tf weight')
#
#    idf = {}
#    for key in tf.keys():
#        idf[key] = math.log10(1/1)
#    print(idf,'<--- idf')
#
#    wtd = {}
#    for key in tf.keys():
#        wtd[key] = tfw[key] * idf[key]
#
#    print(wtd,'<--- wtd')

