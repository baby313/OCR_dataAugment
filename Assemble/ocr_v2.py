# coding=utf-8
# 使用faster rcnn做字符串检测

import _init_paths
from ctypes import *
import sys, time
import cv2
import math
import os.path
import numpy as np
import tensorflow as tf
import Recognition.predict as pred
import Recognition.utils as utils
import FasterRCNN.tools.text_detector as text_detector
import layout

reload(sys) 
sys.setdefaultencoding("utf8")

print "========Init session========="
# set config
tfconfig = tf.ConfigProto(allow_soft_placement=True)
tfconfig.gpu_options.allow_growth=True
sess = tf.Session(config=tfconfig)

print "========Load Faster RCNN models========="

NETS = {'vgg16': ('vgg16_faster_rcnn_iter_70000.ckpt',),'res101': ('res101_faster_rcnn_iter_70000.ckpt',), 'res50': ('res50_faster_rcnn_iter_70000.ckpt',)}
demonet = 'res101'
detector_model = os.path.join('/home/linkface/tf-faster-rcnn/output', demonet, 'vechile_2017_trainval', 'default',
                              NETS[demonet][0])
detector = text_detector.TextDetector(sess, demonet, detector_model)


print "========Load CNN+LSTM+CTC models========="

recognizer_model = '/home/linkface/OCR/Recognition/checkpoint_bilstm_dropout_0.5/'
recognizer = pred.Predictor(sess, recognizer_model)

image_folder = '/data/linkface/OcrData/VechileLicense2017/Vechile2017/JPEGImages/'
while True:
    path = raw_input("Image full path:")
    if path == 'exit' or path == '0': break
    if path[0] != '/': path = image_folder + path
    if not os.path.isfile(path):
        print("Image not exists!")
        continue

    # print "=== Detection ==="

    im = cv2.imread(path)
    
    detect_start = time.time()
    regions = detector.detect(im)
    detect_end = time.time()
    regions = layout.align(regions, 0)
    print regions
    print("Detection cost time: {0}".format(detect_end-detect_start))

    # print "=== Recognizition ==="

    image_height = 28

    img = im.astype(np.float32)/255.

    images = []
    for region in regions:    
        # top, left, bottom, right, score = region 
        left = int(math.floor(region[0]))
        top = int(math.floor(region[1]))
        right = int(math.ceil(region[2]))
        bottom = int(math.ceil(region[3]))
        
        region = img[top:bottom,left:right]
        image_width = int((right-left)*image_height/(bottom-top))
        regImg = cv2.resize(region, (image_width, image_height))

        regImg = regImg.swapaxes(0,1)
        images.append(regImg)
        # images = [regImg]
        # seq_len = [image_width / 4]
        # text = recognizer.predict(np.asarray(images), np.asarray(seq_len))
        # print text[0]
    
    batch_inputs, batch_seq_len = utils.pad_input_sequences(images)


    results = recognizer.predict(batch_inputs, batch_seq_len/4)
    for res in results:
        print res

    rec_end = time.time()
    print("Recognizition cost time: {0}".format(rec_end-detect_end))
    print("Totally cost time: {0}".format(rec_end-detect_start))