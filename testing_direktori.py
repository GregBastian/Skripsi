# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 16:45:22 2019

@author: User
"""
import os
directory = r'G:\My Drive\Skripsi Jaya!\DATASET\Training Data'
dic_food = {
        '001' : 'Donut',
'002' : 'Roti Gandum',
'003' : 'Roti Tawar',
'004' : 'Mie Goreng',
'005' : 'Mie Goreng',
'006' : 'Telor Ceplok',
'007' : 'Telur Dadar',
'008' : 'Ayam Goreng Tepung', 
'009' : 'Dendeng', 
'010' : 'Timun', 
'011' : 'Bayam', 
'012' : 'Kol', 
'013' : 'Selada', 
'014' : 'Kemangi', 
'015' : 'Tomat', 
'016' : 'Stroberi', 
'017' : 'Pisang Hijau', 
'018' : 'Pisang Kuning', 
'019' : 'Jeruk', 
'020' : 'Jeruk Kehijauan', 
'021' : 'Nasi Kuning', 
'022' : 'Nasi Merah', 
'023' : 'Oreo', 
'024' : 'Beng-Beng', 
'025' : 'Snack Kentang', 
'026' : 'Biskuit Coklat', 
'027' : 'Happytos', 
'028' : 'Wafer Cokelat', 
'029' : 'Biskuit Biskuat',
'030' : 'Chocolate Drops', 
'032' : 'Strudel Kismis'
        }

#for filename in os.listdir(directory):
#    folder = filename
#    all_testing_location = r'G:\My Drive\Skripsi Jaya!\DATASET\ALL Training Data'
#    new_directory = directory+'\\'+folder
#    for filename in os.listdir(new_directory):
#        src = new_directory + '\\' + filename
#        dst = all_testing_location + '\\' + filename
#        os.rename(src ,dst)
#    print('Done Moving', filename)

directory = r'G:\My Drive\Skripsi Jaya!\DATASET - Original\ALL Testing Data'

for filename in os.listdir(directory):
    new_name = 'testing_' + filename
    src = directory + '\\' + filename
    dst = directory + '\\' + new_name
    os.rename(src ,dst)
    print('Finished Renaming', filename)


#for filename in os.listdir(directory):
#    i = 0
#    folder = filename
#    num = folder.split(' ')[0]
#    new_directory = directory+'\\'+folder
#    for filename in os.listdir(new_directory):
#        food_name = dic_food[num]
#        dst = food_name+'_' + str(i) + ".jpeg"
#        src = new_directory + '\\' + filename
#        dst = new_directory + '\\' + dst
#        os.rename(src ,dst)
#        i += 1
#    print(food_name,'Done Renaming!')

