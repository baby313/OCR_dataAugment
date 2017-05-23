# coding: utf-8

import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont 
from PIL import ImageFilter
import pygame
import numpy as np
import cv2
import math
from pylab import *

#pygame.init()
#white_background = Image.new("RGB",[400,100],'white')
#myFont = ImageFont.truetype("./STSongti-SC-Bold.ttf", 20)
#word = "你还是nhabce你的话"
#text = unicode(word,'utf-8')
#theFont = pygame.font.Font("./STSongti-SC-Bold.ttf", 20)                       
#[width,height] = theFont.size(text)
#image = ImageDraw.Draw(white_background)
#image.text([10,10],text,(0,0,0),font = myFont)
#image1 = white_background.rotate(5)
#image2 = image1.crop([10,10,10+width,10+height])
#
#image1.show()
#print width,height

def rotate_about_center(src, angle, scale=1.):
  w = src.shape[1]
  h = src.shape[0]
  rangle = np.deg2rad(angle) # angle in radians
  # now calculate new image width and height
  nw = (abs(np.sin(rangle)*h) + abs(np.cos(rangle)*w))*scale
  nh = (abs(np.cos(rangle)*h) + abs(np.sin(rangle)*w))*scale
  # ask OpenCV for the rotation matrix
  rot_mat = cv2.getRotationMatrix2D((nw*0.5, nh*0.5), angle, scale)
  # calculate the move from the old center to the new center combined
  # with the rotation
  rot_move = np.dot(rot_mat, np.array([(nw-w)*0.5, (nh-h)*0.5,0]))
  # the move only affects the translation, so update the translation
  # part of the transform
  rot_mat[0,2] += rot_move[0]
  rot_mat[1,2] += rot_move[1]
  return cv2.warpAffine(src, rot_mat, (int(math.ceil(nw)), int(math.ceil(nh))), flags=cv2.INTER_LANCZOS4)


if __name__ == '__main__':
    src = Image.open("./1.jpg")
    src = np.array(src)
    angel = 5
    image = rotate_about_center(src,angel,scale=1.)
    img_rotate = Image.fromarray(uint8(image))
    img_rotate.save('3.jpg')
    #print img_rotate