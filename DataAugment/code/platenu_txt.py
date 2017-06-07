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

district1=['京','津','冀','晋','蒙','辽','吉','黑','沪','苏','浙','皖','闽','赣',
          '鲁','豫','鄂','湘','粤','桂','琼','渝','川','黔','滇','藏','陕','甘',
          '青','宁','新','台','港','澳']

#车牌号生成
def random_platenu(district1):
    district1="".join(random.sample(district1,1))
    Cap = random.randint(65,90) #大写字母
    district2="".join(random.sample(['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'], 5))
    m_platenu = district1+chr(Cap)+district2
    return m_platenu


if __name__ == '__main__':
    file = open('./assets/platenu_txt.txt','w')
    for i in range(500000):
        try:
            text = random_platenu(district1) 
            file.write(text+'\n')
            if i % 5000==0:
                print(i),
        except:
            print('Error')

    file.close()