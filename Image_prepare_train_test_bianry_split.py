# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 09:34:55 2017

@author: Unknow
"""
import os
import random
import shutil

train_test_split = 0.2
path = r"C:\Users\Unknow\Desktop\data\v0.2\cell_result_multi_binary_total"

filenames = [os.path.join(path,filename) for filename in os.listdir(path) if filename.endswith("jpg")]
random.shuffle(filenames)

filenames_0 = [os.path.join(path,filename) for filename in filenames if (int(filename.split(".")[-2].split("_")[-1])==0)]
filenames_1 = [os.path.join(path,filename) for filename in filenames if (int(filename.split(".")[-2].split("_")[-1])==1)]  
"""
print(filenames)
print(filenames_0)
print(filenames_1)
"""
total_num = len(filenames)
total_num_0 = len(filenames_0)
total_num_1 = len(filenames_1)

print("total number of cell is:")
print(total_num)
print("total number of class-0 cell is:")
print(total_num_0)
print("total number of class-1 cell is:")
print(total_num_1)

test_num_0  = int(total_num_0*train_test_split)
train_num_0 = int(total_num_0)-int(total_num_0*train_test_split)   
test_num_1  = int(total_num_1*train_test_split)
train_num_1 = int(total_num_1)-int(total_num_1*train_test_split)   
print("total number of test set of class-0 cell is:")
print(test_num_0)
print("total number of train set of class-0 cell is:")
print(train_num_0)
print("total number of test set of class-1 cell is:")
print(test_num_1)
print("total number of train set of class-1 cell is:")
print(train_num_1)


filenames_0_train = filenames_0[:train_num_0]
filenames_0_test  = filenames_0[train_num_0:]
filenames_1_train = filenames_1[:train_num_1]
filenames_1_test  = filenames_1[train_num_1:]
filenames_train   = filenames_0_train+filenames_1_train
filenames_test    = filenames_0_test+filenames_1_test

for sourceF in filenames_train:
    sourceF = sourceF
    filename = sourceF.split("\\")[-1]
    target_folder = r"C:\Users\Unknow\Desktop\cell_result_binary_train"
    if not os.path.exists(target_folder):
        os.mkdir(target_folder)
    targetF = os.path.join(target_folder,filename)
    if os.path.isfile(sourceF):
        if not os.path.exists(targetF) or (os.path.exists(targetF) and (os.path.getsize(targetF) != os.path.getsize(sourceF))):
            shutil.copy(sourceF,targetF) 
            
for sourceF in filenames_test:
    sourceF = sourceF
    filename = sourceF.split("\\")[-1]
    target_folder = r"C:\Users\Unknow\Desktop\cell_result_binary_test"
    if not os.path.exists(target_folder):
        os.mkdir(target_folder)
    targetF = os.path.join(target_folder,filename)
    if os.path.isfile(sourceF):
        if not os.path.exists(targetF) or (os.path.exists(targetF) and (os.path.getsize(targetF) != os.path.getsize(sourceF))):
            shutil.copy(sourceF,targetF) 