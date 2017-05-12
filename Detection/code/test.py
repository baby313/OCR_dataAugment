#coding:utf-8
import os
import sys
import json
import codecs
import cv2
import os.path
import shutil
import numpy as np
from ctypes import *
import glob


so_path = "/home/dp/OCR/Detection/code/LFocr.so"
LF_ocr = CDLL(so_path)
              #/home/dp/OCR/Detection/locate
locate_path = "/home/dp/OCR/Detection/locate/title.jpg"
template_path = "/home/dp/OCR/Detection/template/DriveLicense_0.json"
#img_path = "/data/linkface/OcrData/OcrPrpData/3984337_0.jpg"
img_dir = "/data/linkface/OcrData/OcrPrpData/"
json_dir = "/data/linkface/OcrData/标注结果/20170301_linkface_VehicleLicense_第三步_拉框_liangding/Label/"

'''
def getTextRectangle(LF_ocr):
    LF_ocr.textCrop.restype = py_object
    res = LF_ocr.textCrop( locate_path, template_path, img_path ) 
    np.array(res).reshape( (len(res)/4, 4) )
    print res
'''
def getTextRectangle(img_path):
    LF_ocr.textCrop.restype = py_object
    res = LF_ocr.textCrop( locate_path, template_path, img_path ) 
    np.array(res).reshape( (len(res)/4, 4) )
    print res

def testPosition():
    #parent是父文件夹;dirnames是dirroot所含文件夹;
    json_list_tem = []
    num=0
    in_path = json_dir + "*.json"
    for img_file in glob.glob(in_path):
        num+=1
        json_list_tem.append(img_file)
    print(num)
    #print("%d-%d\n", len(json_list_tem),num)
    json_list = []
    for parent,dirnames,filenames in os.walk(json_dir):
        for filename in filenames:
            if os.path.splitext(filename)[1] == '.json':
                jsonfile = json_dir + filename
                json_list.append(jsonfile)
    print("josn file count : %d\n", len(json_list))
    img_list = []
    for parent,dirnames,filenames in os.walk(img_dir):
        for filename in filenames:
            if os.path.splitext(filename)[1] == '.jpg':
                imgfile = img_dir + filename
                img_list.append(imgfile)
    print("img file count : %d\n", len(img_list))
    for i, j in zip(range(0, 4000), range(0, len(img_list))):
        res = getTextRectangle(img_list[i])
        print("No : %d\t Name : %s\n", i, img_list[j])
        print(res)
        print("\n")
'''
    LF_ocr.test.restype = py_object
    res = LF_ocr.test(locate_path, template_path, json_dir, img_dir)
    np.array(res).reshape((len(res)/10, 10))
    print res
'''

if __name__ == '__main__':
    #getTextRectangle()
    testPosition()
