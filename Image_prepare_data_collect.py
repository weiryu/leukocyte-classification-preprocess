# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 16:59:36 2017

命名规则：
中性分叶核粒细胞      0_xx_0.jpg
中性杆状核粒细胞      1_xx_1.jpg
中性多分叶核粒细胞    2_xx_1.jpg
淋巴细胞             3_xx_1.jpg
嗜酸粒细胞           4_xx_1.jpg
嗜碱粒细胞           5_xx_1.jpg
异型淋巴细胞         6_xx_1.jpg
单核细胞             7_xx_1.jpg
其他细胞             8_xx_1.jpg
@author: Unknow
"""

import os
import shutil

def binary_folder_create(original_folder,binary_target_folder):    
    for parent,dirnames,filenames in os.walk(original_folder):  
        count = 0  
        for dirname in dirnames:
            if dirname != u"中性分叶核粒细胞":
                if dirname == u"中性杆状核粒细胞":
                    count = 1
                    sourceDir = os.path.join(original_folder,dirname)
                    for f in os.listdir(sourceDir):
                        filename = f.split(".")[0]
                        sourceF = os.path.join(sourceDir,f)
                        targetF = os.path.join(binary_target_folder,str(count)+"_"+filename+"_1.jpg")
                        if os.path.isfile(sourceF):
                            if not os.path.exists(targetF) or (os.path.exists(targetF) and (os.path.getsize(targetF) != os.path.getsize(sourceF))):
                                shutil.copy(sourceF,targetF)
                elif dirname == u"中性多分叶核粒细胞":
                    count = 2
                    sourceDir = os.path.join(original_folder,dirname)
                    for f in os.listdir(sourceDir):
                        filename = f.split(".")[0]
                        sourceF = os.path.join(sourceDir,f)
                        targetF = os.path.join(binary_target_folder,str(count)+"_"+filename+"_1.jpg")
                        if os.path.isfile(sourceF):
                            if not os.path.exists(targetF) or (os.path.exists(targetF) and (os.path.getsize(targetF) != os.path.getsize(sourceF))):
                                shutil.copy(sourceF,targetF) 
                elif dirname == u"淋巴细胞":
                    count = 3
                    sourceDir = os.path.join(original_folder,dirname)
                    for f in os.listdir(sourceDir):
                        filename = f.split(".")[0]
                        sourceF = os.path.join(sourceDir,f)
                        targetF = os.path.join(binary_target_folder,str(count)+"_"+filename+"_1.jpg")
                        if os.path.isfile(sourceF):
                            if not os.path.exists(targetF) or (os.path.exists(targetF) and (os.path.getsize(targetF) != os.path.getsize(sourceF))):
                                shutil.copy(sourceF,targetF) 
                elif dirname == u"嗜酸粒细胞":
                    count = 4
                    sourceDir = os.path.join(original_folder,dirname)
                    for f in os.listdir(sourceDir):
                        filename = f.split(".")[0]
                        sourceF = os.path.join(sourceDir,f)
                        targetF = os.path.join(binary_target_folder,str(count)+"_"+filename+"_1.jpg")
                        if os.path.isfile(sourceF):
                            if not os.path.exists(targetF) or (os.path.exists(targetF) and (os.path.getsize(targetF) != os.path.getsize(sourceF))):
                                shutil.copy(sourceF,targetF) 												
                elif dirname == u"嗜碱粒细胞":
                    count = 5
                    sourceDir = os.path.join(original_folder,dirname)
                    for f in os.listdir(sourceDir):
                        filename = f.split(".")[0]
                        sourceF = os.path.join(sourceDir,f)
                        targetF = os.path.join(binary_target_folder,str(count)+"_"+filename+"_1.jpg")
                        if os.path.isfile(sourceF):
                            if not os.path.exists(targetF) or (os.path.exists(targetF) and (os.path.getsize(targetF) != os.path.getsize(sourceF))):
                                shutil.copy(sourceF,targetF) 	
                elif dirname == u"异型淋巴细胞":
                    count = 6
                    sourceDir = os.path.join(original_folder,dirname)
                    for f in os.listdir(sourceDir):
                        filename = f.split(".")[0]
                        sourceF = os.path.join(sourceDir,f)
                        targetF = os.path.join(binary_target_folder,str(count)+"_"+filename+"_1.jpg")
                        if os.path.isfile(sourceF):
                            if not os.path.exists(targetF) or (os.path.exists(targetF) and (os.path.getsize(targetF) != os.path.getsize(sourceF))):
                                shutil.copy(sourceF,targetF) 
                elif dirname == u"单核细胞":
                    count = 7
                    sourceDir = os.path.join(original_folder,dirname)
                    for f in os.listdir(sourceDir):
                        filename = f.split(".")[0]
                        sourceF = os.path.join(sourceDir,f)
                        targetF = os.path.join(binary_target_folder,str(count)+"_"+filename+"_1.jpg")
                        if os.path.isfile(sourceF):
                            if not os.path.exists(targetF) or (os.path.exists(targetF) and (os.path.getsize(targetF) != os.path.getsize(sourceF))):
                                shutil.copy(sourceF,targetF)       
                else:
                    count = 8
                    sourceDir = os.path.join(original_folder,dirname)
                    for f in os.listdir(sourceDir):
                        filename = f.split(".")[0]
                        sourceF = os.path.join(sourceDir,f)
                        targetF = os.path.join(binary_target_folder,str(count)+"_"+filename+"_1.jpg")
                        if os.path.isfile(sourceF):
                            if not os.path.exists(targetF) or (os.path.exists(targetF) and (os.path.getsize(targetF) != os.path.getsize(sourceF))):
                                shutil.copy(sourceF,targetF) 																			
            else:
                sourceDir = os.path.join(original_folder,dirname)
                for f in os.listdir(sourceDir):
                    filename = f.split(".")[0]
                    sourceF = os.path.join(sourceDir,f)
                    targetF = os.path.join(binary_target_folder,"0_"+filename+"_0.jpg")
                    if os.path.isfile(sourceF):
                        if not os.path.exists(targetF) or (os.path.exists(targetF) and (os.path.getsize(targetF) != os.path.getsize(sourceF))):
                            shutil.copy(sourceF,targetF) 
                    

if __name__=="__main__":
    original_folder = r"C:\Users\Unknow\Desktop\data\v0.2\cell_result"
    binary_target_folder = r"C:\Users\Unknow\Desktop\cell_result_binary"
    if not os.path.exists(binary_target_folder):
        os.mkdir(binary_target_folder)
    binary_folder_create(original_folder,binary_target_folder)