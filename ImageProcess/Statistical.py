# coding:utf-8
import os
import sys
import json
import codecs
import glob
import os.path
import numpy as np
import traceback
from PIL import Image

reload(sys)
sys.setdefaultencoding('utf8')  # 2.7



global filenum
global checkbox
filenum = 0
checkbox = 0
isDebug = False
def choice(isGPU,isTrain):
    if isTrain:
        if isGPU:
            homedir = '/data/linkface/OcrData/标注结果/20170301_linkface_VehicleLicense_第四步_标字_liangding/TrainLabel'  # TrainLabel,TestLabel
        else:
            homedir = '/Users/gouwei/Downloads/testData/标注结果/20170301_linkface_VehicleLicense_第四步_标字_liangding/Label'
    else:
        if isGPU:
            homedir = '/data/linkface/OcrData/标注结果/20170301_linkface_VehicleLicense_第四步_标字_liangding/TestLabel'  # TrainLabel,TestLabel
        else:
            homedir = '/Users/gouwei/Downloads/testData/标注结果/20170301_linkface_VehicleLicense_第四步_标字_liangding/Label'
    return homedir



def mark(path):
    global filenum
    global checkbox
    path = path + '/*.json'
    for filepath in glob.glob(path):
        try:
            #print(filepath)
            filenum += 1
            jsf = codecs.open(filepath, 'r', 'utf-8')
            Res = json.load(jsf)
            f0 = Res['objects']['ocr']
            #print(filenum)
            checkbox = checkbox + len(f0)
            #print(checkbox)
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



if __name__ == '__main__':
    #train data
    print('TrainData')
    homedir = choice(isGPU=True,isTrain=True)
    mark(homedir)
    print('json文件数'+str(filenum))
    print(checkbox)

    #test data
    print('TestData')
    checkbox = 0
    filenum = 0
    homedir = choice(isGPU=True, isTrain=False)
    mark(homedir)
    print('json文件数' + str(filenum))
    print(checkbox)




#scp /Users/gouwei/OCR/ImageProcess/Statistical.py dp@192.168.2.105:~/OCR/ImageProcess

# ls | wc -w


