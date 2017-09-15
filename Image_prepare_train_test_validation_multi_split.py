# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 09:34:55 2017

@author: Unknow
"""
import os
import random
import shutil
import math

train_split = 0.6
validation_split = 0.2
test_split = 0.2
classes_number = 9
path = r"C:\Users\Unknow\Desktop\data\v0.6\train"
total_file_list = []
train_file_list = []
validation_file_list = []
test_file_list  = []
for i in range(classes_number):
    total_file_list.append([])

# restore file list by classes
filenames = [os.path.join(path,filename) for filename in os.listdir(path) if filename.endswith("jpg")]
random.shuffle(filenames)
for filename in filenames:
    m = int(filename.split("\\")[-1].split("_")[0])
    total_file_list[m].append(filename)
  
# split file according to file list
for i in range(classes_number):
    length    = int(len(total_file_list[i]))
    validation_num = math.ceil(length*validation_split)
    test_num  = math.ceil(length*test_split)
    train_num = int(length-test_num-validation_num) 
    print("train number of class %d is %d"%(i,train_num))
    print("validation number of class %d is %d"%(i,validation_num))     
    print("test number of class %d is %d"%(i,test_num))    
    train_file_list_by_class = total_file_list[i][:train_num]
    print(train_file_list_by_class)
    validation_file_list_by_class = total_file_list[i][train_num:train_num+validation_num]
    print(validation_file_list_by_class)
    test_file_list_by_class = total_file_list[i][train_num+validation_num:]
    print(test_file_list_by_class)   
    train_file_list = train_file_list + train_file_list_by_class
    test_file_list  = test_file_list + test_file_list_by_class
    validation_file_list  = validation_file_list + validation_file_list_by_class
    print("*"*10)
 
# copy file to train dir
for sourceF in train_file_list:
    filename = sourceF.split("\\")[-1]
    target_folder = r"C:\Users\Unknow\Desktop\cell_result_train"
    if not os.path.exists(target_folder):
        os.mkdir(target_folder)
    targetF = os.path.join(target_folder,filename)
    if os.path.isfile(sourceF):
        if not os.path.exists(targetF) or (os.path.exists(targetF) and (os.path.getsize(targetF) != os.path.getsize(sourceF))):
            shutil.copy(sourceF,targetF)             
 
# copy file to validation dir
for sourceF in validation_file_list:
    filename = sourceF.split("\\")[-1]
    target_folder = r"C:\Users\Unknow\Desktop\cell_result_validation"
    if not os.path.exists(target_folder):
        os.mkdir(target_folder)
    targetF = os.path.join(target_folder,filename)
    if os.path.isfile(sourceF):
        if not os.path.exists(targetF) or (os.path.exists(targetF) and (os.path.getsize(targetF) != os.path.getsize(sourceF))):
            shutil.copy(sourceF,targetF)  
            
# copy file to test dir
for sourceF in test_file_list:
    filename = sourceF.split("\\")[-1]
    target_folder = r"C:\Users\Unknow\Desktop\cell_result_test"
    if not os.path.exists(target_folder):
        os.mkdir(target_folder)
    targetF = os.path.join(target_folder,filename)
    if os.path.isfile(sourceF):
        if not os.path.exists(targetF) or (os.path.exists(targetF) and (os.path.getsize(targetF) != os.path.getsize(sourceF))):
            shutil.copy(sourceF,targetF)         
