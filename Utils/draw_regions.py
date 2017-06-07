# coding=utf-8
# 将faster-rcnn检测出来的字符框坐标，画到原图上

import os,sys
import glob
import fileinput
from PIL import Image
from PIL import ImageDraw

reload(sys) 
sys.setdefaultencoding("utf8")

label_dir = "/Users/lairf/Documents/LinkfaceTrainingData/VechileLicense2017/results/VechileLicense2017/Main/"
image_dir = "/Users/lairf/Documents/LinkfaceTrainingData/VechileLicense2017/Vechile2017/JPEGImages/"
output_dir = "/Users/lairf/Documents/LinkfaceTrainingData/VechileLicense2017/results/MarkedImage/"

def getColor(score):
    if score >= 1.0:
        return (255, 0, 0, 128)
    elif score >= 0.98:
        return (128, 0, 0, 128)
    elif score >= 0.95:
        return (0, 255, 0, 128)
    elif score >= 0.9:
        return (0, 128, 0, 128)
    else:
        return (0, 0, 255, 128)

im = None
draw = None
previous_image_name = ''
label_path = label_dir +  "*.txt"
for label_file in glob.glob(label_path):
    for line in fileinput.input(label_file):
        image_name, score, left, top, right, bottom = line.split()
        if previous_image_name != image_name:
            if im != None:
                output_image_path = output_dir + previous_image_name + '.jpg'
                print(output_image_path)
                im.save(output_image_path, "JPEG")

            image_path = image_dir + image_name + '.jpg'
            im = Image.open(image_path)
            draw = ImageDraw.Draw(im)
            previous_image_name = image_name
        
        color = getColor(float(score))
        draw.rectangle([(float(left), float(top)), (float(right), float(bottom))], outline=color)

    if im != None:
        output_image_path = output_dir + previous_image_name + '.jpg'
        im.save(output_image_path, "JPEG")

