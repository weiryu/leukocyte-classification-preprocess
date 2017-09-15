# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 09:35:29 2017

@author: weir
"""

import os
import shutil
import glob

result = r"C:\Users\Unknow\Desktop\cell"
file_list = glob.glob(r"C:\Users\Unknow\Desktop\data\v0.4\*\*.jpg")
count = 0

if not os.path.exists(result):
    os.makedirs(result)
    
for i in file_list:
    if os.path.isfile(i):        
        dst = result+"\\"+str(count)+".jpg"
        shutil.copy(i,dst)
        count+=1
    else:
        pass