# coding=utf-8
# 用来检查标注结果的每个json文件中是否有对应的image 文件
# 检测结果显示所有第4步的所有json文件都有对应的image文件

import os,sys
import glob
import json
import numpy as np

reload(sys) 
sys.setdefaultencoding("utf8")

json_dir = "/Users/lairf/Documents/LinkfaceTrainingData/标注结果/20170301_linkface_VehicleLicense_第四步_标字_liangding/Label/"
image_dir = "/Users/lairf/Documents/LinkfaceTrainingData/行驶证/行驶证/"

images = set()
img_path = image_dir +  "*.*"
image_file_count = 0
for img_file in glob.glob(img_path):
    file_name = os.path.basename(img_file)[:-4]
    images.add(file_name)
    image_file_count += 1

json_file_count = 0
json_path = json_dir +  "*.json"
for json_file in glob.glob(json_path):
    with open(json_file) as data_file:    
        data = json.load(data_file)
        json_file_count += 1
        image_file_name = data['image']['rawFilename']
        index = image_file_name.find('_')
        if index < 0: index = -4
        file_name = image_file_name[:index]
        if file_name not in images:
            print image_file_name
            
print("json: {}, image: {}".format(json_file_count, image_file_count))