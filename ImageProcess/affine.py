# coding:utf-8
import os
import sys
import json
import codecs
import cv2
import os.path
import shutil
import numpy as np
import traceback
from PIL import Image
import math
#from PIL import Image
reload(sys)
sys.setdefaultencoding('utf8')  # 2.7



Path = '/Users/gouwei/Downloads/test/background.jpg'
Path1 = '/Users/gouwei/Downloads/test/1_0.jpg'

'''
img = cv2.imread(Path,-1)
cv2.namedWindow("Image")
cv2.imshow("Image", img)
for row in range(img.shape[0]):
    for col in range(img.shape[1]):
        alpha = img[row / 3 * 4 + 3]
        print(alpha)
cv2.waitKey(0)
cv2.destroyAllWindows()


path2 ='/data/linkface/OcrData/行驶证/行驶证/5132969.jpg'
img = cv2.imread(Path)
cv2.namedWindow("Image")
cv2.imshow("Image", img)
cv2.waitKey(0)
#cv2.destroyAllWindows()
'''
'''
from PIL import Image


def transPNG(srcImageName, dstImageName):
    img = Image.open(srcImageName)
    (x, y) = img.size
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = list()
    num=0
    for item in datas:
        num+=1
        if item[0] > 220 and item[1] > 220 and item[2] > 220:
            newData.append((0, 0, 0, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(dstImageName, "PNG")
    #img.save(dstImageName, "PNG")
    print(x*y)



if __name__ == '__main__':
    transPNG(Path, Path1)
    '''


import Image
import ImageDraw
region = Image.open(Path1)
im = Image.open(Path)
degree = -3
im = im.rotate(-1*degree)
(w,h) = im.size
x = 118
y = 101
r = math.sqrt((h/2-y)*(h/2-y)+(w/2-x)*(w/2-x))
a = math.atan((h/2.0-y)/(w/2.0-x))
a1 = a + degree*3.1416/180  #弧度
x1 = w/2-math.cos(a1)*r
y1 = h/2-math.sin(a1)*r

im.paste(region,(int(x1), int(y1)))
#im.paste(region, (122, 101-8))
#im = im.rotate(10)
'''
im = im.convert("RGBA")
transparent_area = (118,101,217,130)
transparent=1000  #用来调透明度，具体可以自己试
mask=Image.new('L', im.size, color=transparent)
draw=ImageDraw.Draw(mask)
draw.rectangle(transparent_area, fill=0)
im.putalpha(mask)#
'''
im = im.rotate(degree)
im.save('/Users/gouwei/Downloads/test/1.png')

'''
import Image

Im = Image.open(Path)
Im = Im.convert("RGBA")
Im.show()

'''

'''
import Image

Im = Image.open('/data/linkface/OcrData/行驶证/行驶证/5132969.jpg')
#Im = Im.convert("RGBA")
Im.show()
'''


'''
Im1 = Image.open(Path1).convert(Im.mode)
bounds = (0, 0, 250, 100)
Im1 = Im1.crop(bounds)
Im1 = Im1.resize(Im.size)
print Im.mode,Im.size,Im.format
Im1.show()


#img = Image.blend(Im,Im1,0.5)
#img = Image.paste(Im1,Im,None)

<<<<<<< HEAD
#img=Image.alpha_composite(Im,Im1)

img3=Image.new("RGBA",Im.size,"black")
img=Image.composite(Im1,Im,img3)
img.show()
=======
img=Image.alpha_composite(Im,Im1)

#img3=Image.new("RGBA",Im.size,"black")
#img=Image.composite(Im1,Im,img3)
img.show()
'''

