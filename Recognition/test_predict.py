from ctypes import *
import sys
import cv2
import os.path
import numpy as np
import predict as pred

images = []
seq_lens =[]
imagePath = "/data/linkface/OcrTestData/3945623_1_4.jpg"
image_height = 28

print('loading validation data, please wait---------------------')
val_feeder=utils.DataIterator(data_dir="/data/linkface/OcrTestData_s/")
print('get image: ',val_feeder.size)

val_inputs,val_seq_len,val_labels,val_lab_len=val_feeder.input_index_generate_batch_warp()
val_feed = {
    g.inputs: val_inputs,
    g.labels: val_labels,
    g.seq_len: val_seq_len,
    g.label_len: val_lab_len
}

img = cv2.imread(imagePath).astype(np.float32)/255.
shape = img.shape
image_width = shape[0] * shape[1] / image_height
img = cv2.resize(img,(image_width, image_height))
img = img.swapaxes(0,1)
images.append(img)

# after pooling, the feature length or the height of the image is resize to height/4
seq_lens.append(image_width / 4)

results, costTime = pred.predict(np.asarray(images), np.asarray(seq_lens))

print("Cost Time: ", costTime)
for res in results:
    print res
