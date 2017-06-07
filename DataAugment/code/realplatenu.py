#coding:utf-8
import os
import sys
import json
import codecs
import cv2
import os.path
import shutil
import traceback
import numpy as np
import re
import chardet
reload(sys)
sys.setdefaultencoding('utf8')#2.7

#需要修改大小写问题

#from time import sleep
#from tqdm import tqdm
isDebug=False
field=['人','kg','mm']
#temp ='/Users/gouwei/Downloads/4/'+ori_image[0:-4]
global num
global k
global falsepic
k=0
num = 0
falsepic = 0

def isAlnum(word):
    try:
        return word.encode('ascii').isalnum()
    except UnicodeEncodeError:
        return False

def walk_dir(homedir,fileinfo,isGPU,topdown=True):
    #print(dir,fileinfo,topdown)
    filenum=0
    for root, dirs, files in os.walk(homedir, topdown):
        for name in files:
            if os.path.splitext(name)[1] == '.json':
              #print(os.path.join(name))
              mark(homedir,os.path.join(name),isGPU)
              filenum=filenum+1
              if filenum%1000==0:
                print(str(filenum)),


def mark(homedir,path,isGPU):
    path =homedir+'/'+path
    jsf=codecs.open(path,'r','utf-8')
    Res = json.load(jsf)
    try:
        ori_image = Res['image']['rawFilename']
    except:
        ori_image = ''
    file =ori_image[0:-4]
    jsf.close()
    if isGPU:
        picdir='/data/linkface/OcrData/OcrPrpData/'#扣取的图片路径
    else:
        picdir = '/Users/gouwei/Downloads/testData/pretreatment/'  # 扣取的图片路径

    Path = picdir + file + '.jpg'

    img = cv2.imread(Path)
    special = False
    if img is None and len(file)==7:
        Path = picdir + file + '_0.jpg'
        img = cv2.imread(Path)
        special = True
    global num
    global falsepic
    font = True #正面
    num += 1
    if img is not None:
        try:
            f0 = Res['objects']['ocr']
        except:
            f0 = ''
        global k
        k+=1
        if f0 is not None:
            for i in range(len(f0)):
                try:
                    top = int(Res['objects']['ocr'][i]['position']['top'])
                    bottom = int(Res['objects']['ocr'][i]['position']['bottom'])
                    left = int(Res['objects']['ocr'][i]['position']['left'])
                    right = int(Res['objects']['ocr'][i]['position']['right'])

                    try:
                        value=Res['objects']['ocr'][i]['attributes']['content']['value']
                        m = re.match(r'(\d+)', value)
                        if ((value[-1]=='人' and len(m.group())>0) or (value[-2:]=='kg' and len(m.group())>2) or (value[-2:]=='mm' and len(m.group())>3)):  #负面标志
                            #print(m.group())
                            #print(value)
                            front = False
                            break

                    except:
                        value=''
                    
                    if not(isAlnum(value[0]) == False and len(value)==7 and isAlnum(value[1:])):
                        #print (len(value))
                        #print(isAlnum(value))
                        continue
                        
                    #print(len(s))
                    #print(top,bottom,left,right)
                    print value
                    dest = img[top:bottom,left:right]#截取top:bottom行,left:right列
                    res2 = cv2.resize(dest,(int((right-left)*28/(bottom-top)),28),interpolation=cv2.INTER_CUBIC)
                    #if not special:
                    cv2.imwrite(temp+'/'+file+'_'+str(i)+'.jpg', res2)#dest)
                    txtpath = temp+'/'+file+'_'+str(i)+'.txt'
                    print(temp+'/'+file+'_'+str(i)+'.jpg')
                    with open(txtpath,"w") as f:
                        f.write(value)
                    f.close()
                except:
                    if isDebug:
                        info = sys.exc_info()
                        for file, lineno, function, text in traceback.extract_tb(info[2]):
                            print(file, "line:", lineno, "in", function)
                            print(text)
                        print("** %s: %s" % info[:2])
                    else:
                        f = open("log.txt", 'a')
                        traceback.print_exc(file=f)
                        f.flush()
                        f.close()
    else:
        falsepic+=1
        #print('not find the picture!')

if __name__ == '__main__':

    isGPU=True
    print('Begin TrainData:')
    if isGPU:
        homedir = '/data/linkface/OcrData/VechileLicense2017/label'  # TrainLabel,TestLabel
        temp = '/data/linkface/OcrData/platenu_realdata'  # 结果路径 OcrTrainData  OcrTestData
    else:
        homedir = '/Users/gouwei/Downloads/testData/标注结果/20170301_linkface_VehicleLicense_第四步_标字_liangding/Label'
        temp = '/Users/gouwei/Downloads/testData/result'  # 结果路径
    if os.path.exists(temp) == False:
        os.makedirs(temp)
    else:
        shutil.rmtree(temp)
        os.makedirs(temp)
    fileinfo = open('list.txt', 'w')
    walk_dir(homedir, fileinfo,isGPU)
    fileinfo.close()
    print('TrainData文件总数：' + str(num))
    print('可读取的图片数' + str(k))
    print('End TrainData:')
