# coding=utf-8
# 使用传统方法做字符串检测

import _init_paths
from ctypes import *
import sys
import cv2
import os.path
import numpy as np
import Recognition.predict as pred
import Recognition.utils as utils


print "=== Detection ==="

imagePath = sys.argv[1]
print imagePath

LFocr = CDLL("/home/linkface/OCR/Assemble/LFocr.so")
LFocr.textCrop.restype = py_object
positions = LFocr.textCrop("/home/linkface/OCR/Assemble/locate/title.jpg","/home/linkface/OCR/Assemble/template/DriveLicense_0.json",imagePath)
regions = np.asarray(positions)
regions = regions.reshape((-1, 4))
print regions


print "=== Recognizition ==="
images = []
image_height = 28

img = cv2.imread(imagePath).astype(np.float32)/255.
for region in regions:    
    top, left, bottom, right = region 
    region = img[top:bottom,left:right]
    image_width = int((right-left)*image_height/(bottom-top))
    regImg = cv2.resize(region, (image_width, image_height))

    regImg = regImg.swapaxes(0,1)
    images.append(regImg)

batch_inputs, batch_seq_len = utils.pad_input_sequences(images)

 # after pooling, the feature length or the height of the image is resize to height/4
results, costTime = pred.predict(batch_inputs, batch_seq_len/4)

print("Recognition Cost Time: ", costTime)
for res in results:
    print res
