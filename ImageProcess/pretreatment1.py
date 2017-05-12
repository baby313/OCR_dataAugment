# coding:utf-8
import os
import sys
import json
import codecs
import cv2
import os.path
import shutil
import numpy as np
import traceback
from PIL import Image

reload(sys)
sys.setdefaultencoding('utf8')  # 2.7
isGPU=False
isDebug=True
if isGPU:
    homedir = '/data/linkface/OcrData/标注结果/20170301_linkface_VehicleLicense_第二步_liangding/Label'
    temp = '/data/linkface/OcrData/OcrPrpData'  # +ori_image[0:-4]
else:
    homedir = '/Users/gouwei/Downloads/testData/标注结果/20170301_linkface_VehicleLicense_第二步_liangding/Label'
    temp = '/Users/gouwei/Downloads/testData/pretreatment'

global ErrorPic
global Numfile
Numfile = 0
ErrorPic = 0
# homedir1='/Users/gouwei/Downloads/testData/标注结果/20170301_linkface_VehicleLicense_第三步_拉框_liangding/Label'

def walk_dir(dir, fileinfo, topdown=True):
    # print(dir,fileinfo,topdown)
    global num
    num = 0
    for root, dirs, files in os.walk(dir, topdown):
        for name in files:
            if os.path.splitext(name)[1] == '.json':
                # print(os.path.join(name))
                mark(os.path.join(name))
                num = num + 1
                if num % 1000 == 0:
                    print(str(num))
# fileinfo.write(os.path.join(root,name) + '\n')
# for name in dirs:
# print(os.path.join(name))
# fileinfo.write('  ' + os.path.join(root,name) + '\n')

def mark(path):
    global ErrorPic
    global Numfile
    # print('***************************')
    path = homedir + '/' + path
    jsf = codecs.open(path, 'r', 'utf-8')
    # jsf=codecs.open('/Users/gouwei/Downloads/1e5fb03af952c44c0ab7dfbe55d28e7c.json','r','utf-8')
    Res = json.load(jsf)
    try:
        ori_image = Res['image']['rawFilename']
    except:
        ori_image = ''
    jsf.close()
    if isGPU:
        picdir = '/data/linkface/OcrData/行驶证/行驶证/'
    else:
        picdir = '/Users/gouwei/Downloads/testData/行驶证/'
    # Path='/Users/gouwei/Downloads/'
    Path = picdir + ori_image[0:-4]+'.jpg'#全换成小写的jpg文件
    img = cv2.imread(Path)
    if img is not None:
        try:
            f0 = Res['objects']['ocr'][0]['polygonList']
        except:
            f0 = ''
        for i in range(len(f0)):
            try:
                x0 = Res['objects']['ocr'][0]['polygonList'][i][0]['x']
                y0 = Res['objects']['ocr'][0]['polygonList'][i][0]['y']
                
                x1 = Res['objects']['ocr'][0]['polygonList'][i][1]['x']
                y1 = Res['objects']['ocr'][0]['polygonList'][i][1]['y']
                
                x2 = Res['objects']['ocr'][0]['polygonList'][i][2]['x']
                y2 = Res['objects']['ocr'][0]['polygonList'][i][2]['y']
                
                x3 = Res['objects']['ocr'][0]['polygonList'][i][3]['x']
                y3 = Res['objects']['ocr'][0]['polygonList'][i][3]['y']
                
                pts = np.array([[x0, y0], [x1, y1], [x2, y2], [x3, y3]], np.int32)  # 多边形
                # pts = pts.reshape((-1,1,2))
                #cv2.polylines(img, [pts], True, (0, 0, 255))
                rect = cv2.minAreaRect(pts)  # 外接矩形# rect = ((center_x,center_y),(width,height),angle)

                if img is not None:
                    if rect[1][0] > rect[1][1]:
                        res = cv2.getRotationMatrix2D(rect[0], rect[2], 1)  # 第一个参数旋转中心，第二个参数旋转角度，第三个参数：缩放比例
                        f = (int(rect[0][0] - rect[1][0] / 2), int(rect[0][0] + rect[1][0] / 2),
                             int(rect[0][1] - rect[1][1] / 2), int(rect[0][1] + rect[1][1] / 2))
                             # print(rect)
                        RotImg = cv2.warpAffine(img, res, (int(rect[0][0] * 2), int(rect[0][1] * 2)))
                             # print(roiImg)
                        roiImg1 = RotImg[f[2]:f[3], f[0]:f[1]]
                        '''
                    else:
                        
                        f = (int(rect[0][0] - rect[1][1] / 2), int(rect[0][0] + rect[1][1] / 2),
                             int(abs(rect[0][1] - rect[1][0] / 2)), int(rect[0][1] + rect[1][0] / 2))
                        res = cv2.getRotationMatrix2D(rect[0], rect[2] + 90, 1)  # 第一个参数旋转中心，第二个参数旋转角度，第三个参数：缩放比例
                        RotImg = cv2.warpAffine(img, res, (int(rect[0][0] * 2), int(rect[0][1] * 2)))
                        roiImg1 = RotImg[f[2]:f[3], f[0]:f[1]]
                    # print(roiImg1)
                       '''
                    roiImg = img[pts[:, 1].min():pts[:, 1].max(), pts[:, 0].min():pts[:, 0].max()]
                    file = ori_image[0:-4]
                    res2 = cv2.resize(roiImg1, (620, 420), interpolation=cv2.INTER_CUBIC)
                    if len(f0) > 1:
                        #print(temp + '/' + file + '_' + str(i) + '.jpg')
                        cv2.imwrite(temp + '/' + file + '_' + str(i) + '.jpg', res2)  # 有多张图
                        Numfile+=1
                    else:
                        cv2.imwrite(temp + '/' + file + '.jpg', res2)  # 一张图
                        Numfile+=1

                else:
                     ErrorPic += 1
                     #print('Not find the '+ ori_image[0:-4] +' picture')
            except:
                if not isDebug:
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
        ErrorPic += 1



if __name__ == '__main__':
    global num
    if os.path.exists(temp) == False:
        os.makedirs(temp)
    else:
        shutil.rmtree(temp)
        os.makedirs(temp)
    fileinfo = open('list.txt', 'w')
    walk_dir(homedir, fileinfo)
    fileinfo.close()
    print('have find ' + str(Numfile) + ' pictures')
    print('Not find ' + str(ErrorPic) + ' pictures')

