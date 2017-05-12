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

path = '/data/linkface/OcrNewFakeData/regionImage/*.jpg'
for filepath in glob.glob(path):
    fore = Image.open(filepath)
    img1 = np.array(fore)
    rows, cols, dims = img1.shape
    #print(rows,cols,dims)
    if cols>610:
        print(filepath)

print('***')
