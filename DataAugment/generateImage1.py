# coding: utf-8

import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont 
from PIL import ImageFilter
import pygame
import traceback
import numpy as np
import math
import sys
import os

def textrotate(Path,Path1,x,y,degree):
    region = Path1
    im = Path
    im = im.rotate(-1 * degree)
    (w, h) = im.size
    if x < w / 2:
        if y < h/2:
            r = math.sqrt((h / 2 - y) * (h / 2 - y) + (w / 2 - x) * (w / 2 - x))
            a = math.atan((h / 2 - y) / (w / 2 - x))
            a1 = a + degree * 3.1416 / 180  # 弧度
            x1 = w / 2 - math.cos(a1) * r
            y1 = h / 2 - math.sin(a1) * r
        else:
            r = math.sqrt((h / 2 - y) * (h / 2 - y) + (w / 2 - x) * (w / 2 - x))
            a = math.atan((-h / 2 + y) / (w / 2 - x))
            a1 = a + degree * 3.1416 / 180  # 弧度
            x1 = w / 2 - math.cos(a1) * r
            y1 = h / 2 + math.sin(a1) * r
    else:
        r = math.sqrt((h / 2 - y) * (h / 2 - y) + (w / 2 - x) * (w / 2 - x))
        a = math.atan((h / 2 - y) / math.fabs(w / 2 - x))
        a1 = a + degree * 3.1416 / 180  # 弧度
        x1 = w / 2 + math.cos(a1) * r
        y1 = h / 2 - math.sin(a1) * r
    '''
    if x< w/2:
        r = math.sqrt((h / 2 - y) * (h / 2 - y) + (w / 2 - x) * (w / 2 - x))
        a = math.atan((h / 2 - y) / (w / 2 - x))
        a1 = a + degree * 3.1416 / 180  # 弧度
        x1 = w / 2 - math.cos(a1) * r
        y1 = h / 2 - math.sin(a1) * r
    else:
        r = math.sqrt((h / 2 - y) * (h / 2 - y) + (w / 2 - x) * (w / 2 - x))
        a = math.atan((h / 2 - y) / math.fabs(w / 2 - x))
        a1 = a + degree * 3.1416 / 180  # 弧度
        x1 = w / 2 + math.cos(a1) * r
        y1 = h / 2 - math.sin(a1) * r
    '''
    return(x1,y1)

def split(line):      #将文本每行分割出十个信息
    allWords = []     
    list = line.split(',')  
    for word in list:  
        if word[-1]=='\n':  
           allWords.append(word[:-1])  #去掉行末的'\n'  
        else:  
           allWords.append(word)     
    return allWords

#存储每行信息所放位置                
position_new = [(random.gauss(122,5),random.gauss(99,2)),    
                (random.gauss(350,5),random.gauss(99,2)),
                (random.gauss(122,5),random.gauss(143,2)),
                (random.gauss(122,5),random.gauss(187,2)),
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
                (random.gauss(122,5),random.gauss(186,2)),
                (random.gauss(122,5),random.gauss(230,2)),
                (random.gauss(388,5),random.gauss(230,2)),
                (random.gauss(285,5),random.gauss(270,2)),
                (random.gauss(285,5),random.gauss(315,2)),
                (random.gauss(285,5),random.gauss(358,2)),
                (random.gauss(460,5),random.gauss(358,2))]

#高斯模糊
class MyGaussianBlur(ImageFilter.Filter):
    name = "GaussianBlur"

    def __init__(self, radius=2.0,sigma=2.0):
        self.radius = radius
        #self.bounds = bounds
        self.sigma  = sigma
        
    def filter(self, background):
        return background.gaussian_blur(self.radius,self.sigma)

# how many pictures to generate
num = 10
if len(sys.argv) > 1:
    num = int(sys.argv[1])

def drawText(text, filename,i,version,per_blur,per_light):
    try:
        if version == 'new':
            #加载字体和背景
            pygame.init()        
            backgroundName = "./assets/background.jpg"
            background = Image.open(backgroundName)
            im = background
            image = ImageDraw.Draw(background)
            
            #myFont = tkFont.Font(family="STMerge",size=19,weight="bold")
            myFont = ImageFont.truetype("./fonts/STSongti-SC-Bold.ttf", 20)
        
            word = split(text)
      
            for index in range(len(word)): 
                #渲染每行字体
                s = unicode(word[index],'utf-8')
                
                if i%100 < per_light:                
                    image.text(position_new[index],s,(60,60,60),font = myFont)
                else:
                    image.text(position_new[index],s,(0,0,0),font = myFont)
                
                #获得每行字体所占宽度和高度
                theFont = pygame.font.Font("./fonts/STSongti-SC-Bold.ttf", 20)                       
                [width,height] = theFont.size(s)
 
                #存储每小格坐标信息
                f_box = open(filename + '/regionImage/' + str(i) + '_' + str(index) + '_box.txt', 'w')   #存储边框信息
                box = [0]*4
                box[0] = int(random.gauss(position_new[index][0]-2,1))
                box[1] = int(random.gauss(position_new[index][1]-2,4))
                box[2] = int(box[0] + width)
                box[3] = int(box[1] + height)
                f_box.write(str(box))
                f_box.close()
                
                #存储每小格抠图
                region = background.crop(box)
                region.save(filename + '/regionImage/' + str(i) + '_' + str(index) + '.jpg')
                
                #存储每小格文字信息
                f_region_box = open(filename + '/regionImage/'+str(i) +'_'+str(index)+'.txt','w')
                f_region_box.write(word[index])        
                f_region_box.close()
            
            #存储整图
            background.save(filename + '/wholeImage/'+str(i) + '.jpg') 
            
            #模糊
            '''
            if i%100 < per_blur:
                j = random.randrange(1,3)
                if j == 1:
                #模糊
                    image1 = background.filter(MyGaussianBlur(radius=1,sigma=150))
                    print('**********')
                    print(image1)
                    image1.save(filename + '/wholeImage/'+str(i) + '_blur.jpg')
                elif  j == 2:
                    image2 = background.filter(MyGaussianBlur(radius=1,sigma=120))
                    image2.save(filename + '/wholeImage/'+str(i) + '_blur.jpg')
                else :
                    image3 = background.filter(MyGaussianBlur(radius=2,sigma=250))
                    image3.save(filename + '/wholeImage/'+str(i) + '_blur.jpg')
            '''
        elif version == 'old':
            #加载字体和背景
            pygame.init()        
            backgroundName = "./assets/background_old.jpg"
            background = Image.open(backgroundName)
            im = background
            image = ImageDraw.Draw(background)

            myFont = ImageFont.truetype("./fonts/STSongti-SC-Bold.ttf", 20)

            word = split(text)
      
            for index in range(len(word)): 
                #渲染每行字体
                s = unicode(word[index],'utf-8')
                if i%100 < per_light:                
                    image.text(position_old[index],s,(80,80,80),font = myFont)
                else:
                    image.text(position_old[index],s,(0,0,0),font = myFont)
                
                #获得每行字体所占宽度和高度
                theFont = pygame.font.Font("./fonts/STSongti-SC-Bold.ttf", 20)                       
                [width,height] = theFont.size(s)
 
                #存储每小格坐标信息
                f_box = open(filename + '/regionImage/' + str(i) + '_' + str(index) + '_old_box.txt', 'w')   #存储边框信息
                box = [0]*4
                box[0] = int(random.gauss(position_old[index][0]-2,1))
                box[1] = int(random.gauss(position_old[index][1]-2,4))
                box[2] = int(box[0] + width)
                box[3] = int(box[1] + height)
                f_box.write(str(box))
                f_box.close()
                
                #存储每小格抠图
                region = background.crop(box)
                print('*************')
                backgroundName = "./assets/background_old.jpg"
                im = Image.open(backgroundName)
                region1 = region#im.crop(box)
                (x1,y1) = textrotate(im,region,box[0],box[1],3)
                im.paste(region1, (int(x1), int(y1)))
                im.save(filename + '/regionImage/' + str(i) + '_' + str(index) + '_oldrotate.jpg')
                if index==0:
                    print (box[0], box[1])
                    print (x1,y1)
                #im.save(filename + '/wholeImage/' + str(i) + '_rotate.jpg')
                print('*************')
                region.save(filename + '/regionImage/' + str(i) + '_' + str(index) + '_old.jpg')
                
                #存储每小格文字信息
                f_region_box = open(filename + '/regionImage/'+str(i) +'_'+str(index)+'_old.txt','w')
                f_region_box.write(word[index])        
                f_region_box.close()
            
            #存储整图
            background.save(filename + '/wholeImage/'+str(i) + '_old.jpg')
            '''
            #模糊
            if i%100 < per_blur:
                j = random.randrange(1,3)
                if j == 1:
                #模糊
                    image1 = background.filter(MyGaussianBlur(radius=1,sigma=150))
                    image1.save(filename + '/wholeImage/'+str(i) + '_old_blur.jpg')
                elif  j == 2:
                    image2 = background.filter(MyGaussianBlur(radius=1,sigma=120))
                    image2.save(filename + '/wholeImage/'+str(i) + '_old_blur.jpg')
                else :
                    image3 = background.filter(MyGaussianBlur(radius=2,sigma=250))
                    image3.save(filename + '/wholeImage/'+str(i) + '_old_blur.jpg')
            '''
        else:
            print("input error")
            
         
    except:
        info = sys.exc_info()
        for file, lineno, function, text in traceback.extract_tb(info[2]):
            print(file, "line:", lineno, "in", function)
            print(text)
        print("** %s: %s" % info[:2])
        #print("Unexpected error:", sys.exc_info()[0])

if __name__ == '__main__':

    #file = open("./assets/address.txt");
    file = open("./assets/list.txt")
    i = 0
            
    per_blur = raw_input("please input the percentage of blurred picture:(for example:10) ")
    per_light = raw_input("please input the percentage of lighted picture:(for example:20) ")

    for line in file:
        i += 1             #生成第i个文件
        
        #生成文件存放位置
        #filename = '/data/linkface/OcrFakeData/'
        #filename = '/Users/gouwei/Desktop/OcrFakeData/'        
        filename = './address/' 

        version = 'new'
        drawText(line, filename,i,version,per_blur,per_light)
        version = 'old'
        drawText(line, filename,i,version,per_blur,per_light)
        if i % 5000 == 0:
            print(i)
    pass
