# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 15:32:24 2017
新增矩形中心点比较去重功能
新增自动色阶滤波，效果有较大提升
经反复试验，多阈值大津法效果没有显著提示，暂时不采用
新增切割细胞并保存功能
@author: weir
"""
import skimage
from skimage.morphology import disk
import os
import cv2
import numpy as np
import time


# 均衡化+二值化
# 均衡化后表现更佳
def preprocess_equ_threshold(gray):
    # 直方图均衡化
    equ = cv2.equalizeHist(gray)
    # 二值化，下一步cv2.findContours()函数接受的参数为二值图
    # 通过直方图分析，120为阈值较为合适
    # 单单使用大津法（OTSU）或者（THRESH_BINARY_INV）效果均不好
    # 将简单阈值法和otsu阈值法得到的结果按位或，效果较好
    ret_otsu, binary_otsu = cv2.threshold(equ, 120, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)
    cv2.waitKey(0)
    #print("均衡化+二值化预处理完成")
    return binary_otsu
    
    
def preprocess_sobel_threshold(gray):
    x = cv2.Sobel(gray,cv2.CV_16S,1,0)  
    y = cv2.Sobel(gray,cv2.CV_16S,0,1)  
    absX = cv2.convertScaleAbs(x)   # 转回uint8  
    absY = cv2.convertScaleAbs(y)    
    dst = cv2.addWeighted(absX,0.5,absY,0.5,0)  
    ret_otsu, binary_otsu = cv2.threshold(dst, 120, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)
    cv2.waitKey(0)
    #print("sober算子+二值化预处理完成")
    return binary_otsu

# 自动色阶滤波+均衡化+中值滤波+二值化
# 均衡化后表现更佳
def preprocess_equ_median_threshold(gray):
    # 自动色阶，用局部直方图来对图片进行滤波分级。
    # 该滤波器局部地拉伸灰度像素值的直方图，以覆盖整个像素值范围。
    # 半径为5的圆形滤波器
    # 如果叠加高斯平滑，效果变差！
    # 叠加bottomhat和tophat滤波器效果较差 
    # 叠加对比度增强滤波器效果不佳
    # 叠加modal滤波器效果不佳
    gray = skimage.filters.rank.autolevel(gray, disk(5))   
    # 直方图均衡化
    equ = cv2.equalizeHist(gray)
    median = cv2.medianBlur(equ,9)
    # 二值化，下一步cv2.findContours()函数接受的参数为二值图
    # 通过直方图分析，140为阈值较为合适
    # ret, binary = cv2.threshold(equ, 140, 255, cv2.THRESH_BINARY_INV)
    ret_otsu, binary_otsu = cv2.threshold(median, 120, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)
    cv2.waitKey(0)
    #print("均衡化+中值滤波+二值化预处理完成")
    return binary_otsu   
    

# 高斯平滑+二值化   
def preprocess_gaussian_threshold(gray):
    # 高斯平滑
    gaussian = cv2.GaussianBlur(gray, (3, 3), 0, 0, cv2.BORDER_DEFAULT)
    ret_otsu, binary_otsu = cv2.threshold(gaussian, 120, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)
    cv2.waitKey(0)
    #print("高斯平滑+二值化预处理完成")
    return binary_otsu
   
# 高斯平滑+中值滤波+二值化      
# 增加均衡化后效果变差，不采用
def preprocess_gaussian_median_threshold(gray):
    # 高斯平滑
    gaussian = cv2.GaussianBlur(gray, (3, 3), 0, 0, cv2.BORDER_DEFAULT)
    # 中值滤波
    median = cv2.medianBlur(gaussian, 5)
    ret_otsu, binary_otsu = cv2.threshold(median, 100, 255, cv2.THRESH_BINARY_INV)   
    cv2.waitKey(0)    
    #print("高斯平滑+中值滤波+二值化预处理完成")
    #cv2.imshow("binary_otsu ",binary_otsu )
    return binary_otsu 

# 均衡化+高斯平滑+二值化+膨胀腐蚀预处理
def preprocess_equ_gaussian_median_dilation_erosion_threshold(gray):
    # 直方图均衡化
    equ = cv2.equalizeHist(gray)
    # 高斯平滑
    gaussian = cv2.GaussianBlur(equ, (3, 3), 0, 0, cv2.BORDER_DEFAULT)
    # 中值滤波
    median = cv2.medianBlur(gaussian, 5)
    # 二值化，下一步cv2.findContours()函数接受的参数为二值图
    # 通过直方图分析，140为阈值较为合适
    ret_otsu, binary_otsu = cv2.threshold(median, 100, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)
    # 膨胀和腐蚀操作的核函数
    element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
    element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 7))  
    # 膨胀一次，让轮廓突出
    dilation_otsu = cv2.dilate(binary_otsu, element2, iterations = 1)
    # 腐蚀一次，去掉细节
    erosion_otsu = cv2.erode(dilation_otsu, element1, iterations = 1)
    dilation_otsu_2 = cv2.dilate(erosion_otsu, element2, iterations = 1)
    cv2.waitKey(0)
    #print("均衡化+高斯平滑+二值化+膨胀腐蚀预处理完成")
    #cv2.imshow("dilation_otsu",dilation_otsu_2)
    return dilation_otsu_2
    
# 去除重复标记    
def region_process(region):   
    #print(region)
    center=[]
    # 用于存储需去除元素序号
    delete_list=[]
    # 去除方法1：寻找矩形中心点，删除中心点靠近的矩形
    for box in region:
        #print(box)
        xs = [box[0, 0], box[1, 0], box[2, 0], box[3, 0]]
        #print(xs)
        ys = [box[0, 1], box[1, 1], box[2, 1], box[3, 1]]
        #print(ys)    
        xs.sort()
        #print(xs)
        ys.sort()
        #print(ys)
        x1 = xs[0]
        #print(x1)
        x2 = xs[3]
        #print(x2)
        y1 = ys[0]
        #print(y1)
        y2 = ys[3]        
        #print(y2)
        x = (x1+x2)/2
        y = (y1+y2)/2
        center.append((x,y))
        #print(center)
    #print("center:")
    #print(center)
    for i in range(len(center)):
        for j in range(i+1,len(center)):
            # 去除标准
            if abs(center[j][0]-center[i][0])<8 and abs(center[j][1]-center[i][1])<8:
                delete_list.append(j)
    delete_list = list(set(delete_list))
    delete_list.sort()
    delete_list.reverse()
    # 去除重影
    for x in delete_list:
        del region[x]
    #print("region:")
    #print(region)    
    return region
    
def findCellRegion(img):
    region=[]
    img,contours,hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # 筛选面积小的
    #print(len(contours))
    for i in range(len(contours)):
        cnt = contours[i]
        # 计算该轮廓的面积
        area = cv2.contourArea(cnt)
        # print(area)
        if area<1000 or area>8000:
            continue
        # 找到最小的矩形，该矩形可能有方向
        rect = cv2.minAreaRect(cnt)
        # print ("rect is: ")
        # print (rect)
        # box是四个点的坐标
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        region.append(box)
    #print("region length")
    #print(len(region))
    return region
    
def gamma_trans(img, gamma):
    # 具体做法是先归一化到1，然后gamma作为指数值求出新的像素值再还原
    gamma_table = [np.power(x/255.0, gamma)*255.0 for x in range(256)]
    gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
    
    # 实现这个映射用的是OpenCV的查表函数
    # cv2.LUT函数只有两个参数，分别为输入图像和查找表，其返回处理的结果
    return cv2.LUT(img, gamma_table)

def detect(img,file_name,result_dir,result_dir2):
    # 执行Gamma矫正，小于1的值让暗部细节大量提升，同时亮部细节少量提升，对于当前处理图片有很大帮助！
    img_corrected = gamma_trans(img, 0.5)
    gray = cv2.cvtColor(img_corrected, cv2.COLOR_BGR2GRAY)
    print("hhh")
    # 选择bottomhat和uphat滤波器效果都不好
    # gray = skimage.filters.rank.bottomhat(gray, disk(5))
    # 形态学变换的预处理
    result_equ_threshold = preprocess_equ_threshold(gray)
    result_sobel_threshold = preprocess_sobel_threshold(gray)
    result_equ_median_threshold=preprocess_equ_median_threshold(gray)
    result_gaussian_threshold = preprocess_gaussian_threshold(gray)
    result_gaussian_median_threshold = preprocess_gaussian_median_threshold(gray)
    result_equ_gaussian_median_dilation_erosion_threshold = preprocess_equ_gaussian_median_dilation_erosion_threshold(gray)
    
    region_equ_threshold = findCellRegion(result_equ_threshold)
    region_sobel_threshold = findCellRegion(result_sobel_threshold)
    region_equ_median_threshold = findCellRegion(result_equ_median_threshold)
    region_gaussian_threshold = findCellRegion(result_gaussian_threshold)
    region_gaussian_median_threshold = findCellRegion(result_gaussian_median_threshold)
    region_equ_gaussian_median_dilation_erosion_threshold = findCellRegion(result_equ_gaussian_median_dilation_erosion_threshold)
    region = []
    if region_equ_threshold==[]:
        region = []
    else:
        region = region_equ_threshold
    if region_sobel_threshold==[]:
        region = region
    else:
        region.extend(region_sobel_threshold)
    if region_equ_median_threshold==[]:
        region = region
    else:
        region.extend(region_equ_median_threshold)
    if region_gaussian_threshold==[]:
        region = region
    else:
        region.extend(region_gaussian_threshold)
    if region_gaussian_median_threshold==[]:
        region = region
    else:
        region.extend(region_gaussian_median_threshold)   
    if region_equ_gaussian_median_dilation_erosion_threshold ==[]:
        region = region
    else:
        region.extend(region_equ_gaussian_median_dilation_erosion_threshold) 
        
    region = region_process(region)
    i = 0    
    for box in region:  
        i+=1      
        # 生成带轮廓的图片   
        #print(i)
        xs = [box[0, 0], box[1, 0], box[2, 0], box[3, 0]]
        #print(xs)
        ys = [box[0, 1], box[1, 1], box[2, 1], box[3, 1]]
        #print(ys)    
        x_min = 0
        x_max = img.shape[0]
        y_min = 0
        y_max = img.shape[1]
        xs.sort()
        #print(xs)
        ys.sort()
        #print(ys)
        x1 = xs[0]
        if x1<x_min:
            x1 = x_min
        #print(x1)
        x2 = xs[3]
        if x2>x_max-1:
            x2 = x_max-1
        #print(x2)
        y1 = ys[0]
        if y1<y_min:
            y1 = y_min
        #print(y1)
        y2 = ys[3]        
        if y2>y_max-1:
            y2 = y_max-1
        #print(y2)
        # 注意参数顺序，y轴在前
        crop_img_original = img[y1:y2+1,x1:x2+1]
        crop_img = cv2.resize(crop_img_original,(64,64))
        cv2.imwrite(result_dir2+"\\"+file_name.split(".")[-2]+"_"+str(i)+".jpg",crop_img)
    for box in region:
        cv2.drawContours(img, [box], 0, (0, 255, 0), 2)  
    cv2.imwrite(result_dir+'\\'+file_name, img) 
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return len(region)

if __name__=="__main__":
    start_time = time.time()
    target_dir = r"C:\Users\Unknow\Desktop\data\201704\1"
    result_dir = r"C:\Users\Unknow\Desktop\result1"
    result_dir2 = r"C:\Users\Unknow\Desktop\result2"
    if os.path.exists(result_dir):
        pass
    else:
        os.makedirs(result_dir)
    if os.path.exists(result_dir2):
        pass
    else:
        os.makedirs(result_dir2)
    file_list = os.listdir(target_dir)
    picture_number_account=[]
    for file_name in file_list:
        if file_name.endswith(".jpg"):
            print(file_name)
            #print(file_name.split("."))
            imagePath=target_dir+'\\'+file_name
            # print(imagePath)
            img = cv2.imread(imagePath)
            number = detect(img,file_name,result_dir,result_dir2)
            picture_number_account.append(number)
            print("done")
        else:
            pass
    print("图片标记个数依次为：")
    print(picture_number_account)
    print("总处理图片数为：")
    print(len(picture_number_account))
    end_time = time.time()
    last_time = end_time-start_time
    print("耗时：%s second"%(last_time))
    