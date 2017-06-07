# coding: utf-8

import shutil
import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont 
from PIL import ImageFilter
import pygame
import numpy as np
import sys
import os
import thread

position_new = [random.gauss(273,5),random.gauss(318,2)]
position_old = [random.gauss(285,5),random.gauss(270,2)]

#高斯模糊
class MyGaussianBlur(ImageFilter.Filter):
    name = "GaussianBlur"

    def __init__(self, radius=2.0,bounds=None,sigma=2.0):
        self.radius = radius
        #self.bounds = bounds
        self.sigma  = sigma
        
    def filter(self, background):
        return background.gaussian_blur(self.radius,self.sigma)

def config():
    m = random.random()               #定义像素值
    if m < 0.5:
        pixel = (0,0,0)
    elif m >= 0.5 and m <0.7:
        pixel = (80,80,80)
    elif m >= 0.7 and m<0.9:
        pixel = (60,60,60)            
    else:
        pixel = (100,100,100)
       
    n = random.random()            #定义模糊的概率
    #n = 0
    if n < 0.2:
        is_blur = True
    else:
        is_blur = False
    return [pixel,is_blur]


def drawText(vin, filename,i,version):     #每幅图
    #try:
       
        [pixel,is_blur] = config()
        #字体初始化
        pygame.init() 
        theFont = pygame.font.Font("./fonts/STSongti-SC-Bold.ttf", 19)     
        myFont = ImageFont.truetype("./fonts/STSongti-SC-Bold.ttf", 19)

        #加载字体和背景
        backgroundName = './assets/background_' + version + '.jpg'
        background = Image.open(backgroundName)
        image = ImageDraw.Draw(background)
            
        angel = random.gauss(0,1)     #旋转角度
        rangel = np.deg2rad(angel)
        if version == 'new':            
            region = list(position_new)
        else:
            region = list(position_old)    
        #旋转效果
        for letter in vin:              
            image.text(region,letter,pixel,font = myFont)                    
            [w,h] = theFont.size(letter)
            region[0] = region[0] + w
            region[1] = region[1] - np.tan(rangel)*w

        #获得每行字体所占宽度和高度                     
        [width,height] = theFont.size(vin)                
        #每小格边框信息
        box = [0]*4
        if version == 'new':
            box[0] = int(random.gauss(position_new[0]-2,1))
            box[1] = int(random.gauss(position_new[1]-2,2))
        else:
            box[0] = int(random.gauss(position_old[0]-2,1))
            box[1] = int(random.gauss(position_old[1]-2,2))
        box[2] = int(box[0] + width)
        box[3] = int(box[1] + height)
            
        #存储
        region = background.crop(box)
        region.save(filename + '/enginenu/' + str(i) + '_' + version + '.jpg')
        file_txt = open(filename + '/enginenu/' + str(i) + '_' + version +'.txt','w')
        file_txt.write(vin)
        file_txt.close()

        #background.save(filename + '/wholeImage/'+str(i) + '_' + version + '.jpg') 
        #模糊
        if is_blur == True:
            j = random.randrange(1,3)
            if j == 1:
                image1 = background.filter(MyGaussianBlur(radius=2,sigma=150))
                #image1.save(filename + '/wholeImage/'+str(i) + '_' + version + '.jpg')       #覆盖之前存储的整图
            elif  j == 2:
                image1 = background.filter(MyGaussianBlur(radius=2,sigma=120))
                #image1.save(filename + '/wholeImage/'+str(i) + '_' + version + '.jpg')
            else :
                image1 = background.filter(MyGaussianBlur(radius=2,sigma=250))
                #image1.save(filename + '/wholeImage/'+str(i) + '_' + version + '.jpg')

            #存储
            region = image1.crop(box)
            region.save(filename + '/enginenu/' + str(i) + '_' + version + '.jpg')
        
    #except:
        #print("Unexpected error:", sys.exc_info()[0])

def generateImage(vins, output_folder, start_index):
    i = start_index
    for vin in vins:
        i += 1

        a = random.random()
        if a < 0.7:
            version = 'new'
        else:
            version = 'old'
        drawText(vin, output_folder,i,version)

        if i % 100 == 0:
            print("Thread: {0} generate {1}".format(start_index, i))

if __name__ == '__main__':
    filename = '/data/linkface/OcrData/EnginenuData'
    #清空生成文件夹
    shutil.rmtree(filename + '/enginenu/')  
    os.mkdir(filename + '/enginenu/')
    #shutil.rmtree(filename + '/wholeImage/')  
    #os.mkdir(filename + '/wholeImage/')
    file = open("./assets/enginenu_txt.txt")       #输入信息
    i = 0
    
    try:
        vins = []
        for vin in file:
            i += 1             #生成第i个文件
            vins.append(vin)

            if i % 50000 == 0:
                thread.start_new_thread(generateImage, (vins, filename, i))
                vins = []
            #生成文件存放位置
            
            #filename = '/Users/gouwei/Desktop/OcrFakeData/'        
            #filename = './address/' 
        
        if i % 50000 != 0:
            thread.start_new_thread(generateImage, (vins, filename, i))
    except:
       print "Error: unable to start thread"
    
    while 1:
        pass