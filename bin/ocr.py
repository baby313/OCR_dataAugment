from ctypes import *
import sys
import cv2
import os.path
import numpy as np
sys.path.append("../Recognizition")
import predict as pred
import utils

print "=== Detection ==="

imagePath = sys.argv[1]
print imagePath

LFocr = CDLL("/home/linkface/OCR/bin/LFocr.so")
LFocr.textCrop.restype = py_object
positions = LFocr.textCrop("/home/linkface/OCR/bin/locate/title.jpg","/home/linkface/OCR/bin/template/DriveLicense_0.json",imagePath)
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
