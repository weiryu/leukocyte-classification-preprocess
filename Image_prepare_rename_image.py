# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 16:24:14 2017

@author: Unknow
"""


import os

def file_rename(target_folder):
    for parent,dirnames,filenames in os.walk(target_folder):    
        for dirname in dirnames:
            if dirname != None:
                target_path = os.path.join(target_folder,dirname)
                if os.path.isdir(target_path):
                    count = 0
                    for file in os.listdir(target_path):
                        os.rename(target_path+"\\"+file,target_path+"\\"+str(count)+".jpg")
                        count = count+1
                else:
                    pass

if __name__=="__main__":
    target_folder = r"C:\Users\Unknow\Desktop\cell_result"
    file_rename(target_folder)