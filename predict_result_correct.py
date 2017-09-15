# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 19:32:23 2017

程序说明:用于细胞预测结果修正后按细胞类别重新划分

@author: Unknow
"""

import os
import glob
import shutil
import sys
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

original_dir_1 = r"C:\Users\Unknow\Desktop\0629\*"
original_dir = r"C:\Users\Unknow\Desktop\0629"
target_dir = r"C:\Users\Unknow\Desktop\celll"
dirnames = []
xml_dirnames = []

if os.path.exists(target_dir):
    shutil.rmtree(target_dir)
os.mkdir(target_dir)


for original_dirname in glob.glob(original_dir_1):
    dirname = original_dirname.split("\\")[-1]
    dirnames.append(dirname)
    if not os.path.exists(os.path.join(target_dir,dirname)):
        print(dirname)
        os.mkdir(os.path.join(target_dir,dirname))
   

print(dirnames)
for dirname in dirnames:
    for filename in os.listdir(os.path.join(original_dir,dirname)):
        if filename.endswith("jpg"):
            filename_xml = filename.split(".")[0]+".xml"
            if not os.path.exists(os.path.join(os.path.join(original_dir,dirname),filename_xml)):
                #print(os.path.join(os.path.join(target_dir,dirname),filename))
                shutil.copy(os.path.join(os.path.join(original_dir,dirname),filename),os.path.join(os.path.join(target_dir,dirname),filename))
            else:
                try:
                    tree = ET.parse(os.path.join(os.path.join(original_dir,dirname),filename_xml))
                    root = tree.getroot()
                except Exception as e:
                    print("Error:can not parse xml file")
                    sys.exit(1)
                for objectname in root.findall("object"):
                    name = objectname.find("name").text
                    print(name)
                    if name not in dirnames:
                        xml_dirnames.append(name)
                        if not os.path.exists(os.path.join(target_dir,name)):
                            os.mkdir(os.path.join(target_dir,name))
                    shutil.copy(os.path.join(os.path.join(original_dir,dirname),filename),os.path.join(os.path.join(target_dir,name),filename))
                    
        else:
            pass

dirnames.extend(xml_dirnames)
print(dirnames)
                    