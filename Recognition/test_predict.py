# coding=utf-8

import os,sys
from ctypes import *
import cv2
import os.path
import numpy as np
import predict as pred
import glob
import utils as utils

reload(sys) 
sys.setdefaultencoding("utf8")
print sys.getdefaultencoding()

images = []
seq_lens =[]
labels = []
image_height = 28
imagePaths = []
imageFolder= '/data/linkface/OcrData/VINData/RealVinTest/'

in_path = imageFolder +  "*.jpg"
#print(in_path)
for img_file in glob.glob(in_path):
    label_file = img_file[:-3] + "txt"
    # print(label_file)
    if os.path.exists(label_file):
        with open(label_file) as file:
            label = file.read().decode("utf-8").strip().upper()
            labels.append(label)

        img = cv2.imread(img_file).astype(np.float32)/255.
        shape = img.shape
        image_width = shape[0] * shape[1] / image_height
        img = cv2.resize(img,(image_width, image_height))
        img = img.swapaxes(0,1)

        images.append(img)
        # after pooling, the feature length or the height of the image is resize to height/4
        seq_lens.append(image_width / 4)
        imagePaths.append(img_file.split('/')[-1])

batch_inputs, batch_seq_len = utils.pad_input_sequences(images)
results, costTime = pred.predict(batch_inputs, batch_seq_len/4)

print("Cost Time: ", costTime)
for i, res in enumerate(results):
    if labels[i] != res:
        print("Image: {0}, label: {1}, predict: {2}".format(imagePaths[i], labels[i], res))

    
