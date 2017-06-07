#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#Created on Fri May 12 10:43:40 2017

#@author: xiuxiuzhang


import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont 
from PIL import ImageFilter
import pygame
import numpy as np
import shutil
import sys
import os

#存储每行信息所放位置                
position_new = [(random.gauss(122,5),random.gauss(99,2)),    
                (random.gauss(350,5),random.gauss(99,2)),
                (random.gauss(122,5),random.gauss(143,2)),
                [(122,165),(122,189)],
                (random.gauss(122,5),random.gauss(230,2)),
                (random.gauss(315,5),random.gauss(230,2)),
                (random.gauss(290,5),random.gauss(272,2)),
                (random.gauss(270,5),random.gauss(315,2)),
                (random.gauss(260,5),random.gauss(358,2)),
                (random.gauss(460,5),random.gauss(358,2))]

#旧版每行位置               
position_old = [(random.gauss(122,5),random.gauss(100,2)),    
                (random.gauss(350,5),random.gauss(100,2)),
                (random.gauss(122,5),random.gauss(143,2)),
                [(122,165),(122,189)],
                (random.gauss(122,5),random.gauss(230,2)),
                (random.gauss(388,5),random.gauss(230,2)),
                (random.gauss(285,5),random.gauss(270,2)),
                (random.gauss(285,5),random.gauss(315,2)),
                (random.gauss(285,5),random.gauss(358,2)),
                (random.gauss(460,5),random.gauss(358,2))]

#字体
pygame.init() 
theFont = pygame.font.Font("./fonts/STSongti-SC-Bold.ttf", 19)     
myFont = ImageFont.truetype("./fonts/STSongti-SC-Bold.ttf", 19)

#参数
def config():
    m = random.random()               #定义像素值
    if m < 0.5:
        pixel = (0,0,0)
    elif m >= 0.5 and m <0.7:
        pixel = (30,30,30)
    elif m >= 0.7 and m<0.9:
        pixel = (60,60,60)            
    else:
        pixel = (100,100,100)
       
    n = random.random()            #定义模糊的概率    
    if n < 0.2:
        is_blur = True
    else:
        is_blur = False
        
    return [pixel,is_blur]
    

#高斯模糊
class MyGaussianBlur(ImageFilter.Filter):
    name = "GaussianBlur"

    def __init__(self, radius=2.0,bounds=None,sigma=2.0):
        self.radius = radius
        #self.bounds = bounds
        self.sigma  = sigma
        
    def filter(self, background):
        return background.gaussian_blur(self.radius,self.sigma)


def split(line):      #将文本每行分割出十个信息
    allWords = []     
    list = line.split(',')  
    for word in list:  
        if word[-1]=='\n':  
           allWords.append(word[:-1])  #去掉行末的'\n'  
        else:  
           allWords.append(word)     
    return allWords


def generateNewText():
    file = open("./assets/list.txt")       #输入信息
    file_new = open('./assets/longtext.txt','w')
    for line in file:
        word = split(line)
        s = unicode(word[3],'utf-8')
        [width,height] = theFont.size(s)
        if width > 600-122:
            #print("width:",width)
            file_new.write(line)
        else:
           pass
    file.close()                                         
    file_new.close()
            
def drawText(text, filename,i,version):     #每幅图
    #try:
        [pixel,is_blur] = config()    #配置
        

        #将一行信息分割开
        word = split(text) 
        #将地址行分割成两行
        word3 = unicode(word[3],'utf-8')
        #print word3
        for j in range(len(word3)):
            [w_tmp,h_tmp] = theFont.size(word3[0:j]) 
            #print w_tmp,h_tmp           
            if w_tmp > 580-122:
                #print w_tmp
                s1 = word3[0:j-1]      #序号不包括最后一位
                #print s1
                s2 = word3[j-1:]
                #print s2
                #print '/n'
                break
        
        if version == 'new':
            #加载字体和背景
            backgroundName = "./assets/background.jpg"
            background = Image.open(backgroundName)
            image = ImageDraw.Draw(background)
        
            for index in range(len(word)):       #每行
                angel = random.gauss(0,1)     #旋转角度
                rangel = np.deg2rad(angel)
                s = unicode(word[index],'utf-8')
                #地址行特殊处理
                if index == 3:       
                    image.text(position_new[3][0],s1,pixel,font = myFont)
                    image.text(position_new[3][1],s2,pixel,font = myFont)
                    [w1,h1] = theFont.size(s1) 
                    [w2,h2] = theFont.size(s2)
                    box1 = [122,165,122+w1,160+h1]
                    box2 = [122,189,122+w2,189+h2]
                    
                    
                    # #检测
                    # #存储每小格坐标信息
                    # f_box = open(filename + '/regionImage/' + str(i) + '_' + str(index) + '_box_1.txt', 'w')   #存储边框信息
                    # f_box.write(str(box1))
                    # f_box.close() 
                    # f_box = open(filename + '/regionImage/' + str(i) + '_' + str(index) + '_box_2.txt', 'w')   #存储边框信息
                    # f_box.write(str(box2))
                    # f_box.close() 
                                      

                    #存成一行
                    new_img = Image.new('RGB',(w1+w2,max(h1,h2)), 'white') 
                    #存储每小格抠图
                    region = background.crop(box1)
                    new_img.paste(region, (0, 0))
                    #region.save(filename + '/regionImage/' + str(i) + '_' + str(index) + '_1.jpg')
                    region = background.crop(box2)
                    new_img.paste(region,(w1,0))
                    #region.save(filename + '/regionImage/' + str(i) + '_' + str(index) + '_2.jpg')
                    
                    new_img.save(filename + '/longAddress/' + str(i) + '_3.jpg')      #第三格抠图和文字信息
                    f = open(filename + '/longAddress/'+str(i) +'_3.txt','w')
                    f.write(word[index])        
                    f.close()

                    
                    # #存储每小格文字信息
                    # f_region_box = open(filename + '/regionImage/'+str(i) +'_'+str(index)+'_1.txt','w')
                    # f_region_box.write(s1.encode('utf-8'))        
                    # f_region_box.close()
                    # f_region_box = open(filename + '/regionImage/'+str(i) +'_'+str(index)+'_2.txt','w')
                    # f_region_box.write(s2.encode('utf-8'))        
                    # f_region_box.close()
                    
                #正常的行                                           
                else:
                    box_init = list(position_new[index])
                    #旋转渲染每行字
                    for letter in s:              
                        image.text(box_init,letter,pixel,font = myFont)                    
                        [w,h] = theFont.size(letter)
                        box_init[0] = box_init[0] + w
                        box_init[1] = box_init[1] - np.tan(rangel)*w
                    #获得每行字体所占宽度和高度  
                                      
                    # [width,height] = theFont.size(s)                
                    # #每小格边框信息
                    # box = [0]*4
                    # box[0] = int(random.gauss(position_new[index][0]-2,1))
                    # box[1] = int(random.gauss(position_new[index][1]-2,4))
                    # box[2] = int(box[0] + width)
                    # box[3] = int(box[1] + height)
                    # #存储每小格坐标信息
                    # #print(filename + '/regionImage/' + str(i) + '_' + str(index))
                    # f_box = open(filename + '/regionImage/' + str(i) + '_' + str(index) + '_box.txt', 'w')   #存储边框信息
                    
                    # f_box.write(str(box))
                    # f_box.close()   
                    # #存储每小格抠图
                    # region = background.crop(box)
                    # region.save(filename + '/regionImage/' + str(i) + '_' + str(index) + '.jpg')
                    # #存储每小格文字信息
                    # f_region_box = open(filename + '/regionImage/'+str(i) +'_'+str(index)+'.txt','w')
                    # f_region_box.write(word[index])        
                    # f_region_box.close()
                    
            #存储整图
            background.save(filename + '/wholeImage/'+str(i) + '.jpg') 
            
            #模糊
            if is_blur == True:
                j = random.randrange(1,3)
                if j == 1:
                    image1 = background.filter(MyGaussianBlur(radius=2,sigma=150))
                    image1.save(filename + '/wholeImage/'+str(i) + '.jpg')       #覆盖之前存储的整图
                elif  j == 2:
                    image1 = background.filter(MyGaussianBlur(radius=2,sigma=120))
                    image1.save(filename + '/wholeImage/'+str(i) + '.jpg')
                else :
                    image1 = background.filter(MyGaussianBlur(radius=2,sigma=250))
                    image1.save(filename + '/wholeImage/'+str(i) + '.jpg')
                for index in range(len(word)):         #存储模糊抠图
                    #地址行
                    if index == 3:
                        #存储每小格抠图
                        new_img = Image.new('RGB',(w1+w2,max(h1,h2)), 'white')
                        region = image1.crop(box1)
                        new_img.paste(region, (0, 0))
                        
                        #region.save(filename + '/regionImage/' + str(i) + '_' + str(index) + '_1.jpg')
                        
                        region = image1.crop(box2)
                        new_img.paste(region,(w1,0))
                        
                        #region.save(filename + '/regionImage/' + str(i) + '_' + str(index) + '_2.jpg')
                        
                        new_img.save(filename + '/longAddress/' + str(i) + '_3.jpg')      
                        f = open(filename + '/longAddress/'+str(i) +'_3.txt','w')
                        f.write(word[index])        
                        f.close()
                    
                    # #其他行
                    # else:
                    #     s = unicode(word[index],'utf-8') 
                    #     [width,height] = theFont.size(s)
                    #     #每行的边框信息
                    #     box = [0]*4    #偏移的抠图
                    #     box[0] = int(random.gauss(position_new[index][0],1))
                    #     box[1] = int(random.gauss(position_new[index][1],2))
                    #     box[2] = int(box[0] + width)
                    #     box[3] = int(box[1] + height)
                    #     #存储每小格坐标信息
                    #     f_box = open(filename + '/regionImage/' + str(i) + '_' + str(index) + '_box.txt', 'w')   #存储边框信息
                    #     f_box.write(str(box))
                    #     f_box.close() 
                    #     #存储抠图              
                    #     region = image1.crop(box)
                    #     region.save(filename + '/regionImage/' + str(i) + '_' + str(index) + '.jpg')
                    
            else:
                pass
                

        elif version == 'old':
            #加载字体和背景
            backgroundName = "./assets/background_old.jpg"
            background = Image.open(backgroundName)
            image = ImageDraw.Draw(background)
            
            #旧版本交换顺序
            word[4],word[5] = word[5],word[4]
            word[6],word[7] = word[7],word[6]
            
            for index in range(len(word)):       #每行
                angel = random.gauss(0,1)     #旋转角度
                rangel = np.deg2rad(angel)
                s = unicode(word[index],'utf-8')
                if index == 3:      
                    image.text(position_old[3][0],s1,pixel,font = myFont)
                    image.text(position_old[3][1],s2,pixel,font = myFont)
                    [w1,h1] = theFont.size(s1) 
                    [w2,h2] = theFont.size(s2)
                    box1 = [122,165,122+w1,160+h1]
                    box2 = [122,189,122+w2,189+h2]
                    
                    # #存储每小格坐标信息
                    # f_box = open(filename + '/regionImage/' + str(i) + '_' + str(index) + '_box_1_old.txt', 'w')   #存储边框信息
                    # f_box.write(str(box1))
                    # f_box.close() 
                    # f_box = open(filename + '/regionImage/' + str(i) + '_' + str(index) + '_box_2_old.txt', 'w')   #存储边框信息
                    # f_box.write(str(box2))
                    # f_box.close() 
                    
                    #存成一行
                    new_img = Image.new('RGB',(w1+w2,max(h1,h2)), 'white') 
                    #存储每小格抠图
                    region = background.crop(box1)
                    new_img.paste(region, (0, 0))
                    
                    #region.save(filename + '/regionImage/' + str(i) + '_' + str(index) + '_1_old.jpg')
                    
                    region = background.crop(box2)
                    new_img.paste(region,(w1,0))
                    
                    #region.save(filename + '/regionImage/' + str(i) + '_' + str(index) + '_2_old.jpg')
                    
                    new_img.save(filename + '/longAddress/' + str(i) + '_3_old.jpg')      
                    f = open(filename + '/longAddress/'+str(i) +'_3.txt','w')
                    f.write(word[index])        
                    f.close()
                    
                    # #存储每小格文字信息
                    # f_region_box = open(filename + '/regionImage/'+str(i) +'_'+str(index)+'_1_old.txt','w')
                    # f_region_box.write(s1.encode('utf-8'))        
                    # f_region_box.close()
                    # f_region_box = open(filename + '/regionImage/'+str(i) +'_'+str(index)+'_2_old.txt','w')
                    # f_region_box.write(s2.encode('utf-8'))        
                    # f_region_box.close()
                    
                #正常的行                 
                else:
                    box_init1 = list(position_old[index])
                    #旋转写入每小格
                    for letter in s:               #每字
                        image.text(box_init1,letter,pixel,font = myFont)                    
                        [w,h] = theFont.size(letter)
                        box_init1[0] = box_init1[0] + w
                        box_init1[1] = box_init1[1] - np.tan(rangel)*w                   
                    #获得每行字体所占宽度和高度                     
                    [width,height] = theFont.size(s)
                    
                    # #每格边框信息
                    # box = [0]*4    
                    # box[0] = int(random.gauss(position_old[index][0],1))
                    # box[1] = int(random.gauss(position_old[index][1],2))
                    # box[2] = int(box[0] + width)
                    # box[3] = int(box[1] + height)                  
                    # #存储每小格坐标信息
                    # f_box = open(filename + '/regionImage/' + str(i) + '_' + str(index) + '_old_box.txt', 'w')   #存储边框信息
                    # f_box.write(str(box))
                    # f_box.close()   
                    # #存储每小格抠图
                    # region = background.crop(box)
                    # region.save(filename + '/regionImage/' + str(i) + '_' + str(index) + '_old.jpg')                                  
                    # #存储每小格文字信息
                    # f_region_box = open(filename + '/regionImage/'+str(i) +'_'+str(index)+'_old.txt','w')
                    # f_region_box.write(word[index])        
                    # f_region_box.close()
                    
            #存储整图
            background.save(filename + '/wholeImage/'+str(i) + '_old.jpg')             
            #模糊
            if is_blur == True:
                j = random.randrange(1,3)
                if j == 1:
                    image2 = background.filter(MyGaussianBlur(radius=2,sigma=150))
                    image2.save(filename + '/wholeImage/'+str(i) + '_old.jpg')       #覆盖之前存储的整图
                elif  j == 2:
                    image2 = background.filter(MyGaussianBlur(radius=2,sigma=120))
                    image2.save(filename + '/wholeImage/'+str(i) + '_old.jpg')
                else :
                    image2 = background.filter(MyGaussianBlur(radius=2,sigma=250))
                    image2.save(filename + '/wholeImage/'+str(i) + '_old.jpg')
                for index in range(len(word)):         #存储模糊抠图
                    #地址行
                    if index == 3:
                        #存储每小格抠图
                        new_img = Image.new('RGB',(w1+w2,max(h1,h2)), 'white')
                        region = image2.crop(box1)
                        new_img.paste(region, (0, 0))
                        
                        #region.save(filename + '/regionImage/' + str(i) + '_' + str(index) + '_1_old.jpg')
                        
                        region = image2.crop(box2)
                        new_img.paste(region,(w1,0))
                        
                        #region.save(filename + '/regionImage/' + str(i) + '_' + str(index) + '_2_old.jpg')
                        
                        new_img.save(filename + '/longAddress/' + str(i) + '_3_old.jpg')      #
                        f = open(filename + '/longAddress/'+str(i) +'_3_old.txt','w')
                        f.write(word[index])        
                        f.close()
                    
                    # #其他行
                    # else:
                    #     s = unicode(word[index],'utf-8') 
                    #     [width,height] = theFont.size(s)
                    #     #每行的边框信息
                    #     box = [0]*4    #偏移的抠图
                    #     box[0] = int(random.gauss(position_old[index][0],1))
                    #     box[1] = int(random.gauss(position_old[index][1],2))
                    #     box[2] = int(box[0] + width)
                    #     box[3] = int(box[1] + height)
                    #     #存储每小格坐标信息
                    #     f_box = open(filename + '/regionImage/' + str(i) + '_' + str(index) + '_box_old.txt', 'w')   #存储边框信息
                    #     f_box.write(str(box))
                    #     f_box.close() 
                    #     #存储抠图              
                    #     region = image2.crop(box)
                    #     region.save(filename + '/regionImage/' + str(i) + '_' + str(index) + '_old.jpg')
                    
        else:
            pass
                    
#    except:
#        print("Unexpected error:", sys.exc_info()[0])
    

if __name__ == '__main__':
    #清空生成文件夹
    shutil.rmtree('./address/longAddress')  
    os.mkdir('./address/longAddress')
    shutil.rmtree('./address/regionImage')  
    os.mkdir('./address/regionImage')
    shutil.rmtree('./address/wholeImage')  
    os.mkdir('./address/wholeImage')
    
    generateNewText()
    #print('**************************')
    file = open("./assets/longtext.txt")       #输入信息
    i = 0
    
    filename = './address'
    #filename = '/data/linkface/OcrData/OcrFakeData-2017-05-12' 
    for line in file:
        i += 1
        a = random.random()
        if a < 0.7:
            version = 'new'
        else:
            version = 'old'
        drawText(line, filename,i,version)
       
        if i % 2 == 0:
            print(i)
        
