# coding=utf-8
import os,sys
import glob
import numpy as np
import tensorflow as tf
import cv2
from PIL import Image

reload(sys) 
sys.setdefaultencoding("utf8")

def __int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[x for x in value]))

def __bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


input_dir = "/Users/lairf/AI-projects/ocr/Data/address_train_/"
output_dir = "/Users/lairf/AI-projects/ocr/Data/address_train_tfrecord/"

SPACE_INDEX=0
SPACE_TOKEN=''
encode_maps={}
decode_maps={}
def loadDict(dictPath):
    pos = len(encode_maps)
    with open(dictPath) as file:
        for line in file:
            char = line.decode("utf-8").strip()
            if char not in encode_maps:
                encode_maps[char]=pos
                decode_maps[pos]=char
                pos += 1

encode_maps[SPACE_TOKEN]=SPACE_INDEX
decode_maps[SPACE_INDEX]=SPACE_TOKEN
loadDict("../Dicts/Chars.txt")
loadDict("../Dicts/GB2312.txt")

index = 0
batch_size = 1000
image_height = 28
output_file = output_dir  + '0.tfrecords'
writer = tf.python_io.TFRecordWriter(output_file)

in_path = input_dir +  "*.jpg"
for img_file in glob.glob(in_path):
    label_file = img_file[:-3] + "txt"
    if os.path.exists(label_file):
        img = np.array(Image.open(img_file))
        height = img.shape[0]
        width = img.shape[1]
        img_raw = img.tostring()

        # im = cv2.imread(img_file).astype(np.int32)

        # # resize to same height(image_height=28)
        # # image_width = im.shape[0] * im.shape[1] / image_height
        # # im = cv2.resize(im,(image_width, image_height))
        # image_raw = im.tostring()

        # # swap x, y;  each row as feature sequence which inputs in bi-lstm
        # im = im.swapaxes(0,1)

        # read labels
        label = []
        with open(label_file) as file:
            code = file.read().decode("utf-8").strip()
            if code == SPACE_TOKEN:
                label = [SPACE_INDEX]
            else:
                for i in range(len(code)):
                    if code[i] in encode_maps:
                        label.append(encode_maps[code[i]])
                    else:
                        label.append(SPACE_INDEX)
                        print(code[i])
        
        example = tf.train.Example(features=tf.train.Features(feature={
            'shape':  __int64_feature(img.shape),
            'image_raw': __bytes_feature(img_raw),
            'lable': __int64_feature(label)
        }))

        writer.write(example.SerializeToString())
        index += 1

        # create a new file
        if index % batch_size == 0:
            writer.close()
            output_file = '%s%d.tfrecords' % (output_dir,index / batch_size )
            writer = tf.python_io.TFRecordWriter(output_file)

writer.close()


            