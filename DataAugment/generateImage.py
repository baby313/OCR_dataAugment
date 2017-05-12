# coding: utf-8

import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont 
from PIL import ImageFilter
import pygame
import numpy as np

import sys
import os


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

    def __init__(self, radius=2.0,bounds=None,sigma=2.0):
        self.radius = radius
        #self.bounds = bounds
        self.sigma  = sigma
        
    def filter(self, background):
        return background.gaussian_blur(self.radius,self.sigma)

# how many pictures to generate
num = 10
if len(sys.argv) > 1:
    num = int(sys.argv[1])

def drawText(text, filename,i,version):     #每幅图
    try:
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
        #n = 0
        if n < 0.2:
            is_blur = True
        else:
            is_blur = False
        
        #字体初始化
        pygame.init() 
        theFont = pygame.font.Font("./fonts/STSongti-SC-Bold.ttf", 19)     
        myFont = ImageFont.truetype("./fonts/STSongti-SC-Bold.ttf", 19)
        #将一行信息分割开
        word = split(text)    
        
        if version == 'new':
            #加载字体和背景
            backgroundName = "./assets/background.jpg"
            background = Image.open(backgroundName)
            image = ImageDraw.Draw(background)
            
            for index in range(len(word)):       #每行
                angel = random.gauss(0,1)     #旋转角度
                rangel = np.deg2rad(angel)
                s = unicode(word[index],'utf-8')             
                #image = ImageDraw.Draw(background)
                region = list(position_new[index])
                
                for letter in s:               #每字
                    image.text(region,letter,pixel,font = myFont)                    
                    [w,h] = theFont.size(letter)
                    region[0] = region[0] + w
                    region[1] = region[1] - np.tan(rangel)*w
                   
                #获得每行字体所占宽度和高度                     
                [width,height] = theFont.size(s)
             
                box = [0]*4    #偏移的抠图
                box[0] = int(random.gauss(position_new[index][0],1))
                box[1] = int(random.gauss(position_new[index][1],2))
                box[2] = int(box[0] + width)
                box[3] = int(box[1] + height) 
                
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
                
                if box[2] < 600:                    
                    #存储每小格坐标信息
                    f_box = open(filename + '/regionImage/' + str(i) + '_' + str(index) + '_box.txt', 'w')   #存储边框信息
                    f_box.write(str(box))
                    f_box.close()   
                    #存储每小格抠图
                    region = background.crop(box)
                    region.save(filename + '/regionImage/' + str(i) + '_' + str(index) + '.jpg')
                                  
                    #存储每小格文字信息
                    f_region_box = open(filename + '/regionImage/'+str(i) +'_'+str(index)+'.txt','w')
                    f_region_box.write(word[index])        
                    f_region_box.close()
                else:
                    pass
            
            #存储整图
            background.save(filename + '/wholeImage/'+str(i) + '.jpg') 
            
            #模糊
            if is_blur == True:
                j = random.randrange(1,3)
                if j == 1:
                    image1 = background.filter(MyGaussianBlur(radius=2,sigma=150))
                    image1.save(filename + '/wholeImage/'+str(i) + '.jpg')
                elif  j == 2:
                    image1 = background.filter(MyGaussianBlur(radius=2,sigma=120))
                    image1.save(filename + '/wholeImage/'+str(i) + '.jpg')
                else :
                    image1 = background.filter(MyGaussianBlur(radius=2,sigma=250))
                    image1.save(filename + '/wholeImage/'+str(i) + '.jpg')
                for index in range(len(word)):         #存储模糊抠图
                    s = unicode(word[index],'utf-8') 
                    [width,height] = theFont.size(s)
                    
                    box = [0]*4    #偏移的抠图
                    box[0] = int(random.gauss(position_new[index][0],1))
                    box[1] = int(random.gauss(position_new[index][1],2))
                    box[2] = int(box[0] + width)
                    box[3] = int(box[1] + height)
                    
                    if box[2] < 600:
                        #存储每小格坐标信息
                        f_box = open(filename + '/regionImage/' + str(i) + '_' + str(index) + '_box.txt', 'w')   #存储边框信息
                        f_box.write(str(box))
                        f_box.close() 
                                       
                        region = image1.crop(box)
                        region.save(filename + '/regionImage/' + str(i) + '_' + str(index) + '.jpg')
                    else:
                        pass
            else:
                pass
                

        elif version == 'old':
            #加载字体和背景
            backgroundName = "./assets/background_old.jpg"
            background = Image.open(backgroundName)
            image = ImageDraw.Draw(background)
            
            for index in range(len(word)):       #每行
                angel = random.gauss(0,1)     #旋转角度
                rangel = np.deg2rad(angel)
                s = unicode(word[index],'utf-8')             
                region = list(position_old[index])
                
                for letter in s:               #每字
                    image.text(region,letter,pixel,font = myFont)                    
                    [w,h] = theFont.size(letter)
                    region[0] = region[0] + w
                    region[1] = region[1] - np.tan(rangel)*w                   
                #获得每行字体所占宽度和高度                     
                [width,height] = theFont.size(s) 
               
                box = [0]*4    #偏移的抠图
                box[0] = int(random.gauss(position_old[index][0],1))
                box[1] = int(random.gauss(position_old[index][1],2))
                box[2] = int(box[0] + width)
                box[3] = int(box[1] + height)                  
                if box[2] < 600:
                    #存储每小格坐标信息
                    f_box = open(filename + '/regionImage/' + str(i) + '_' + str(index) + '_old_box.txt', 'w')   #存储边框信息
                    f_box.write(str(box))
                    f_box.close()   
                    #存储每小格抠图
                    region = background.crop(box)
                    region.save(filename + '/regionImage/' + str(i) + '_' + str(index) + '_old.jpg')
                                  
                    #存储每小格文字信息
                    f_region_box = open(filename + '/regionImage/'+str(i) +'_'+str(index)+'_old.txt','w')
                    f_region_box.write(word[index])        
                    f_region_box.close()
                else:
                    pass
            #存储整图
            background.save(filename + '/wholeImage/'+str(i) + '_old.jpg') 
            
            #模糊
            if is_blur == True:
                j = random.randrange(1,3)
                if j == 1:
                    image2 = background.filter(MyGaussianBlur(radius=2,sigma=150))
                    image2.save(filename + '/wholeImage/'+str(i) + '_old.jpg')
                elif  j == 2:
                    image2 = background.filter(MyGaussianBlur(radius=1,sigma=120))
                    image2.save(filename + '/wholeImage/'+str(i) + '_old.jpg')
                else :
                    image2 = background.filter(MyGaussianBlur(radius=2,sigma=250))
                    image2.save(filename + '/wholeImage/'+str(i) + '_old.jpg')
                for index in range(len(word)):         #存储模糊抠图
                    s = unicode(word[index],'utf-8') 
                    [width,height] = theFont.size(s)
                    
                    box = [0]*4    #偏移的抠图
                    box[0] = int(random.gauss(position_old[index][0],1))
                    box[1] = int(random.gauss(position_old[index][1],2))
                    box[2] = int(box[0] + width)
                    box[3] = int(box[1] + height)                  
                    if box[2] < 600:
                        #存储每小格坐标信息
                        f_box = open(filename + '/regionImage/' + str(i) + '_' + str(index) + '_old_box.txt', 'w')   #存储边框信息
                        f_box.write(str(box))
                        f_box.close() 
                                       
                        region = image2.crop(box)
                        region.save(filename + '/regionImage/' + str(i) + '_' + str(index) + '_old.jpg')
                    else:
                        pass
            else:
                pass
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

    file = open("./assets/list.txt")       #输入信息
    i = 0
    
    for line in file:
        i += 1             #生成第i个文件
        
        #生成文件存放位置
        #filename = '/data/linkface/OcrFakeData/'
        #filename = '/Users/gouwei/Desktop/OcrFakeData/'        
        filename = './address/' 

        a = random.random()
        if a < 0.7:
            version = 'new'
        else:
            version = 'old'
        drawText(line, filename,i,version)
        if i % 5000 == 0:
            print(i)
