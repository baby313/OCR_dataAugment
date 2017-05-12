# coding:utf-8
import numpy as np
from PIL import Image
from PIL import ImageDraw
import matplotlib.pyplot as plt

from pylab import *
reload(sys)
sys.setdefaultencoding('utf8')  # 2.7
'''
#img = Image.open('/Users/gouwei/Downloads/test/background.jpg')
img = np.array(Image.open('/Users/gouwei/Downloads/test/background.jpg'))
print img.shape

fore = Image.open('/Users/gouwei/Downloads/test/1_0.jpg')
fore = fore.rotate(2)
fore.save("/Users/gouwei/Downloads/test/rotate.jpg")# 保存灰度图像
img1 = np.array(fore)
print img1.shape

rect = [118, 101, 217, 130]

row,col,dim = img1.shape
rows, cols,dims = img.shape

for i in range(rows):
    for j in range(cols): #h=29,w=99
        if i>=rect[1] and i<min(row+rect[1],rect[3]) and j>=rect[0] and j<min(col+rect[0],rect[2]) and all(img1[i-rect[1],j-rect[0],:]) !=0:
            #print (i,j)
            img[i, j,:] = img1[i-rect[1],j-rect[0],:]
        else:
            img[i, j,:] = img[i,j,:]


img11=Image.fromarray(uint8(img))
img11.save("/Users/gouwei/Downloads/test/rest.jpg")# 保存灰度图像
'''
def picrotate(src,region,rect,degree):
    region = region.rotate(degree)
    srcimg = np.array(src)
    regionimg = np.array(region)
    rows, cols, dims = srcimg.shape
    row, col, dim = regionimg.shape
    for i in range(rows):
        for j in range(cols):  # h=29,w=99
            if i >= rect[1] and i < min(row+rect[1], rect[3]) and j >= rect[0] and j < min(col + rect[0],rect[2]) and\
                            all(regionimg[i-rect[1],j-rect[0],:]) != 0:
                srcimg[i,j,:] = regionimg[i-rect[1], j-rect[0],:]
            else:
                srcimg[i,j,:] = srcimg[i,j,:]
    img11 = Image.fromarray(uint8(srcimg))
    return img11

if __name__ == '__main__':
    img = Image.open('/Users/gouwei/Downloads/test/background.jpg')
    fore = Image.open('/Users/gouwei/Downloads/test/1_0.jpg')
    rect = [118, 101, 217, 130]
    dest = picrotate(img,fore,rect,3)
    dest.save("/Users/gouwei/Downloads/test/rest.jpg")  # 保存灰度图像

    #dest.transform((100,100),'EXTENT',(0,0,620,240))
