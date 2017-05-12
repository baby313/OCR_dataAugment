# coding: utf-8

import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont 
from PIL import ImageFilter
import pygame
import math
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
position=[(random.gauss(122,2),random.gauss(99,1)),    
          (random.gauss(350,2),random.gauss(99,1)),
          (random.gauss(122,2),random.gauss(143,1)),
          (random.gauss(122,2),random.gauss(187,1)),
          (random.gauss(122,2),random.gauss(230,1)),
          (random.gauss(315,2),random.gauss(230,1)),
          (random.gauss(290,2),random.gauss(272,1)),
          (random.gauss(270,2),random.gauss(315,1)),
          (random.gauss(260,2),random.gauss(358,1)),
          (random.gauss(460,2),random.gauss(358,1))]

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

def drawText(text, filename):
    try:
        pygame.init()        
        backgroundName = "./assets/background.jpg"
        background = Image.open(backgroundName)
        image = ImageDraw.Draw(background)
        
        myFont1 = ImageFont.truetype("./fonts/Songti.ttc", 19)
        myFont2 = ImageFont.truetype("./fonts/xingshi1.ttf", 19)
        
        word = split(text)
        
        f = open(filename + '_box.txt', 'w') 
        box = []     #拉框标注
        for index in range(len(word)):
            s=unicode(word[index],'utf-8')
            len_c = (len(word[index])-len(s))//2
            len_en = len(s)-len_c
            if index == 3:
                box_tmp = (position[index][0]-3,position[index][1]-3,
                           position[index][0]+20*len_c+7*len_en,position[index][1]+25)
                box.append(box_tmp)
                f.write(str(box_tmp)+'\n')
            elif index == 7:
                box_tmp = (position[index][0]-3,position[index][1]-3,
                           position[index][0]+20*len_c+12*len_en+6,position[index][1]+25)
                box.append(box_tmp)
                f.write(str(box_tmp)+'\n')
            elif index >= 0 and index <= 6:
                box_tmp = (position[index][0]-3,position[index][1]-3,
                           position[index][0]+20*len_c+12*len_en,position[index][1]+25)
                box.append(box_tmp)
                f.write(str(box_tmp)+'\n')
            else:
                box_tmp = (position[index][0]-3,position[index][1]-3,
                       position[index][0]+20*len_c+10*len_en,position[index][1]+25)
                box.append(box_tmp)
                f.write(str(box_tmp)+'\n')
        #allBox.append(box)
        f.close()
        
        
        #渲染每行字体
        for index in range(len(word)):   
            if   index == 0:
                 s=unicode(word[index],'utf-8')
                 image.text(position[index],s[0:1],(30,30,30),font = myFont1)    #模拟打印机墨不足情况可将所有30调成50
                 image.text(np.array((21,5))+np.array(position[index]),s[1:],(0,0,0),font = myFont2)                
                 
            elif index >=1 and index <=4:
                 s=unicode(word[index],'utf-8')
                 image.text(position[index],s,(30,30,30),font = myFont1)
       
            elif index == 5:
                 s=unicode(word[index],'utf-8')
                 n=(len(word[index])-len(s))//2
                 image.text(position[index],s[0:n],(30,30,30),font = myFont1)
                 image.text(np.array((19*n+2,5))+np.array(position[index]),s[n:],(0,0,0),font = myFont2)
                 
            else:
                 s=unicode(word[index],'utf-8') 
                 image.text(np.array((0,5))+np.array(position[index]),s,(0,0,0),font = myFont2)
             
        #存储每个抠图    
        for index in range(len(word)):
             region = background.crop(box[index])
             region.save(filename + '_'+str(index)+'.jpg')
            
        background.save(filename + '.jpg')
        
        #模糊
        #image1 = background.filter(MyGaussianBlur(radius=1,sigma=150))
        #image1.save(filename + '_blur1.jpg')
        
        #image2 = background.filter(MyGaussianBlur(radius=1,sigma=120))
        #image2.save(filename + '_blur2.jpg')
        
        #image3 = background.filter(MyGaussianBlur(radius=2,sigma=250))
        #image3.save(filename + '_blur3.jpg')
         
        #将每行信息存储成txt文件
       
            #f.write(text)
            #f.close()
    except:
        print("Unexpected error:", sys.exc_info()[0])

if __name__ == '__main__':
    if not os.path.isdir('./address/'):
        os.mkdir('./address/')
    #file = open("./assets/address.txt");
    #file = open("/Users/xiuxiuzhang/Downloads/list1.txt")
    file = open("./list.txt")
    i = 0
    #allBox = []

    for line in file:
        i += 1
        filename = './address/' + str(i)
        drawText(line, filename) 
        if i % 1000 == 0:
            print(i)
    pass
