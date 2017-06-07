#coding:utf-8

import os
import sys
import json
import codecs
import cv2
import os.path
import shutil
import numpy as np
import random
import string
import binascii
import time
import datetime

reload(sys)
sys.setdefaultencoding('utf8')  # 2.7

def random_str(randomlength=8):
    str = ''
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    length = len(chars) - 1
    #random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str
'''
define: 闽CF0792,小型轿车,吴培辉,福建省安溪县剑斗镇剑斗村西在范28号,非营运,比亚迪牌QCJ7200E3,LGXC16DG046621,0909366,2009-09-03,2014-12-29
'''

#发动机号码 7-14
def random_enginenu():
    m_motorid=random_str(random.randint(7,14))
    return m_motorid
#print(random_carid())



if __name__ == '__main__':
    file = open('./assets/enginenu_txt.txt','w')
    for i in range(500000):
        try:
            text = random_enginenu()
            file.write(text+'\n')
            if i % 5000==0:
                print(i),
        except:
            print('Error')

    file.close()