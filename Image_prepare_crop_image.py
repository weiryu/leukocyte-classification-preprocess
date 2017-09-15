# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import cv2
import sys
import os

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
 
# build folder to save target image that belog to predefined_classes.txt
def target_folder_build(predefinded_classes_text,target_folder): 
    if os.path.exists(target_folder):
        if os.path.isdir(target_folder):
            pass
        else:
            os.mkdir(target_folder)
    else:
        os.mkdir(target_folder)
    with open(predefinded_classes_text,'rb') as f:
        cell_classes = []
        for line in f:
            cell_classes.append(line.decode("utf-8").replace("\r\n",""))
        for cell_class in cell_classes:
            print(cell_class)
            cell_class_folder = os.path.join(target_folder,cell_class)
            if os.path.exists(cell_class_folder):
                if os.path.isdir(cell_class_folder):
                    pass
                else:
                    os.mkdir(cell_class_folder)
            else:
                os.mkdir(cell_class_folder)   
    return cell_classes

def get_file_list(original_file_folder):
    Image_Format = [".jpg",".jpeg",".bmp",".png"]
    Xml_Format = [".xml"]
    Image_file_list = []
    Xml_file_list = []
    for s in os.listdir(original_file_folder):
        newDir = os.path.join(original_file_folder,s)
        if os.path.isfile(newDir):
            if newDir and (os.path.splitext(newDir)[1] in Image_Format):
                Image_file_list.append(newDir)
            elif newDir and (os.path.splitext(newDir)[1] in Xml_Format):
                Xml_file_list.append(newDir)                
            else:
                pass
        else:
            pass
    return Image_file_list,Xml_file_list
 
# cut picture according to xml file and save it to target folder
def xml_read_pic_crop(target_file_folder,xml_file_path,cell_classes):
    try:
        # open file
        tree = ET.parse(xml_file_path)
        # get root point
        root = tree.getroot()
    except Exception as e:
        print("Error:cannot parse xml file")
        sys.exit(1)
    print(root.tag,"---",root.attrib)
    print("------")
    for child in root:
        print(child.tag,"---",child.attrib)
    """
    print('*'*10)
    print("folder is:")
    folder_name = root[0].text 
    print(root[0].text)
    print("filename is:")
    """
    filename = root[1].text  
    """    
    print(root[1].text)
    print('*'*10)      
    """
    img_file_path = os.path.splitext(xml_file_path)[0]+".jpg"
    print(img_file_path)
    image = cv2.imread(img_file_path)
    """
    cv2.imshow("original",image)
    cv2.waitKey(0)
    """
    i = 0
    for objectname in root.findall("object"):
        name = objectname.find("name").text
        new_cell_class_path = os.path.join(target_folder,name)
        if name not in cell_classes:
            cell_classes.append(name)
            new_cell_class_path = os.path.join(target_folder,name)
            if os.path.exists(new_cell_class_path):
                if os.path.isdir(new_cell_class_path):
                    pass
                else:
                    os.mkdir(new_cell_class_path)
            else:
                os.mkdir(new_cell_class_path)   
        print(name)
        for rect in objectname.findall("bndbox"):
            xmin = int(rect.find("xmin").text)
            print(xmin)
            ymin = int(rect.find("ymin").text)
            print(ymin)
            xmax = int(rect.find("xmax").text)
            print(xmax)
            ymax = int(rect.find("ymax").text)
            print(ymax)
        cropImg = image[ymin:ymax,xmin:xmax].copy()
        # 解决cv2.imwrite无法保存到中文路径问题
        cv2.imencode(".jpg",cropImg)[1].tofile(os.path.join(target_folder,name)+"\\"+filename+"_"+str(i)+".jpg")
        i = i+1      
        
if __name__=="__main__":
    original_file_folder = r"C:\Users\Unknow\Desktop\data\201704\4--label"
    target_folder = r"C:\Users\Unknow\Desktop\cell_result"
    predefinded_classes_text = r"C:\Users\Unknow\Desktop\data\201704\predefined_classes.txt"
    cell_classes = target_folder_build(predefinded_classes_text,target_folder)
    Image_file_list,Xml_file_list = get_file_list(original_file_folder)
    for xml_file_path in Xml_file_list:
        xml_read_pic_crop(target_folder,xml_file_path,cell_classes)
    
