#encoding=utf-8
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
from functools import reduce

'''
so_path = ""
locate_path = ""
template_path = ""
img_dir = ""
json_dir = ""
img_Result = ""
img_test = ""
'''


#def init(filepath):
#global so_path, locate_path, template_path, img_dir, json_dir, img_Result, img_test
jsfile = codecs.open(os.getcwd() + '/path.json', 'r', 'utf-8')
jsStr = json.load(jsfile)
so_path = jsStr["so_path"]
LF_ocr = CDLL(so_path)
locate_path = jsStr["locate_path"]
template_path = jsStr["template_path"]
img_dir = jsStr["img_dir"]
json_dir = jsStr["json_dir"]
img_Result = jsStr["img_Result"]
img_test = jsStr["img_test"]
jsfile.close()

def str2float(s):
  return reduce(lambda x,y:(x+int2dec(y)),map(str2int,s.split('.')))
def char2num(s):
  return {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}[s]
def str2int(s):
  return reduce(lambda x,y:(x*10+y),map(char2num,s))
def intLen(i):
  return len('%d'%i)
def int2dec(i):
  return i/(10**intLen(i))

def getTextRectangle(LF_ocr, img_path):
    LF_ocr.textCrop.restype = py_object
    res = LF_ocr.textCrop(str(locate_path), str(template_path), str(img_path) )
    return np.array(res).reshape( (len(res)/4, 4) )

def overlapRate( t1,  l1,  b1,  r1,  t2,  l2,  b2,  r2):
	iner = max(0, min(r1, r2) - max(l1, l2)) * max(0, min(b1, b2) - max(t1, t2))
	outer = max(r1, r2) - min(l1, l2) * max(b1, b2) - min(t1, t2)
	res = iner / oute
	return res

def overlapRateByList(l1, l2):  
    iner = max(0, min(l1[3], l2[3]) - max(l1[1], l2[1])) * max(0, min(l1[2], l2[2]) - max(l1[0], l2[0]))
    outer = (max(l1[3], l2[3]) - min(l1[1], l2[1])) * (max(l1[2], l2[2]) - min(l1[0], l2[0]))
    #res = iner / outer
    s1 = (l1[2] - l1[0]) * (l1[3] - l1[1])
    s2 = (l2[2] - l2[0]) * (l2[3] - l2[1])
    return iner / (s1 + s2 - iner), iner / s1, iner / s2

def readJsonDir():
    json_list = []
    json_dict = {}
    #parent是父文件夹;dirnames是dirroot所含文件夹;
    for parent, dirnames, filenames in os.walk(json_dir):
        for filename in filenames:
            if os.path.splitext(filename)[1] == '.json':
                jsonfile = json_dir + filename
                json_list.append(jsonfile)
                jsfile = codecs.open(jsonfile, 'r', 'utf-8')
                jsStr = json.load(jsfile)
                imgname = jsStr['image']['rawFilename']
                json_dict[imgname] = jsonfile
                jsfile.close()
    print("josn file count : ", len(json_list))
    return json_list, json_dict

def readImgDir():
    img_list = []
    for parent,dirnames,filenames in os.walk(img_dir):
        for filename in filenames:
            if os.path.splitext(filename)[1] == '.jpg':
                imgfile = img_dir + filename
                img_list.append(imgfile)
    print("img file count : ", len(img_list))
    return img_list

def readDir(dir_path):
    json_list_tem = []
    in_path = dir_path + "*.json"
    for img_file in glob.glob(in_path):
        json_list_tem.append(img_file)
    print(len(json_list_tem))

def testPosition(LF_ocr):
    json_list, json_dict = readJsonDir()
    img_list = readImgDir()
    rectRateAll=[]
    #检测图片上的文本区域 
    j = 0
    for i in range(len(img_list)):
        print('*****************************************   start  *************************************************')
        if j >= 10:
            break
        if img_list[i].find('_1') > 0:
            print(str(img_list[i])+ '-----副页')
            continue
        if json_dict.has_key(os.path.basename(img_list[i])) == False:
            print('-----Image ' + os.path.basename(img_list[i]) + ' donot find Json')
            continue

        print(j)
        print(img_list[i])
        rectImg = getTextRectangle(LF_ocr, img_list[i])

        if len(rectImg) == 0 :
            print('-----Image ', img_list[i], ' text detect failed')
            continue

        j += 1

        rectRate=[]
        imgSrc = cv2.imread(img_list[i])
        print("Get json : ", json_dict[os.path.basename(img_list[i])])
        jsfile = codecs.open(json_dict[os.path.basename(img_list[i])], 'r', 'utf-8')
        jsStr = json.load(jsfile)
        #寻找此图像对应的标记json 
        rectJs_file=[]
        rectJs_ori =[]
        rectJs=[]
        for rcjsocr in range(len(jsStr["objects"])):
            for rcjs in range(len(jsStr["objects"]["ocr"])):
                rectJs_file.append(jsStr["objects"]["ocr"][rcjs]["position"]["top"])
                rectJs_file.append(jsStr["objects"]["ocr"][rcjs]["position"]["left"])
                rectJs_file.append(jsStr["objects"]["ocr"][rcjs]["position"]["bottom"])
                rectJs_file.append(jsStr["objects"]["ocr"][rcjs]["position"]["right"])
            rectJs_ori = np.array(rectJs_file).reshape((len(rectJs_file)/4, 4))
        #为每个rect寻找最合适的标记区域  
        for imrc in range(len(rectImg)):
            maxRate = 0.0
            maxPos = 0
            recall = 0.0
            prec = 0.0
            if len(rectJs_ori) > 0:
                for jsrc in range(len(rectJs_ori)):
                    temp, recall_tem, prec_tem = overlapRateByList(rectImg[imrc], rectJs_ori[jsrc])
                    if temp > maxRate :
                        maxRate = temp
                        maxPos = jsrc
                        recall = recall_tem
                        prec = prec_tem
                rectJs.append(rectJs_ori[maxPos])
                rectRate.append(maxRate)
            else:
                rectJs.append(rectImg[imrc])
                rectRate.append(1.0)
        for ct in range(len(rectRate)):
            print(rectRate[ct])
            cv2.rectangle(imgSrc, (rectImg[ct][1], rectImg[ct][0]), (rectImg[ct][3], rectImg[ct][2]), (255, 0, 0), 1)
            cv2.rectangle(imgSrc, (int(rectJs[ct][1]), int(rectJs[ct][0])), (int(rectJs[ct][3]), int(rectJs[ct][2])), (0, 0, 255), 1)
        cv2.imwrite(img_Result + os.path.basename(img_list[i]), imgSrc)
        rectRateAll.append(rectRate)
    return rectRateAll

def analyzeResult(file_path):
    lr = []
    file_object = open(str(file_path),'rU')
    try: 
        for line in file_object:
            if float(str(line.strip('\n'))) != 0.0:
                lr.append(float(str(line.strip('\n'))))
    finally:
        file_object.close()
    print lr


if __name__ == '__main__':
    #init(os.getcwd() + '/path.json')
    #LF_ocr = CDLL(so_path)
    #getTextRectangle(LF_ocr, img_test)

    rectRateAll = testPosition(LF_ocr)

    resultfilename = "/data/OCR/Detection/code/result.txt"
    with open(resultfilename, "w") as rf:
        for rateImg in rectRateAll:
            for rateText in rateImg:
                rf.write(str(rateText))
                rf.write('\t')
            rf.write('\n')
    if rf:
        rf.close()

    resultfilename_1r = "/data/OCR/Detection/code/result_1r.txt"
    with open(resultfilename_1r, "w") as rf:
        for rateImg in rectRateAll:
            for rateText in rateImg:
                rf.write(str(rateText))
                rf.write('\n')
            rf.write('\n')
    if rf:
        rf.close()

    analyzeResult(resultfilename_1r)
