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

Multiday=random.randint(0,365*17)
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
#print(random_platenu(district1))
#桥车型号：
'''
A1:大型客车（大型载客汽车）
A2:牵引车（重型中型全挂，半挂汽车）
A3:城市公交车（荷载10人以上的城市公交车）
B1:中型客车（中型载客汽车，含载10人以上19人以下的城市公交车）
B2：大型货车（重型中型载货汽车，大重中型专项作业车）
C1：小型汽车（小型微型载客汽车以及轻型微型载货汽车：轻小微型专项作业车）
C2：小型自动挡汽车
'''

car_sty = ['轿车','小型普通客车','中型普通客车', '中型普通货车','大型普通客车', '重型半挂牵引车', '普通二轮摩托车', '小型越野客车', '微型普通客车', '小型轿车', '中型半挂牵引','重型普通货车', '重型厢式货车',
 '重型自卸货车', '中型封闭货车', '中型集装厢车', '中型自卸货车', '轻型普通货车','轻型厢式货车', '轻型自卸货车', '微型普通货车', '微型厢式货车', '微型自卸货车', '重型普通半挂车', '中型普通半挂车',
 '轻型普通半挂车', '重型普通全挂车', '中型普通全挂车','大型专项作业车', '中型专项作业车', '小型专项作业车']

def random_district(car_sty):
    m_car = "".join(random.sample(car_sty,1))
    return m_car
#print(random_district(car_sty))

#姓名：
def random_name():
    try:
        with open(r'../Dicts/Name.txt') as file:
            num=0
            name=[]
            for line in file:
                temp = line.strip('\n')
                name.append(temp)
                #name[num]=temp
                num+=1
                #print(temp)
    except:
        print('the Name.txt is not find')
    return name


#k=random.randint(1,len(m_name))
#print(m_name[k])
#地址：
def random_Address():
    with open(r'../Dicts/Address.txt') as file:
        num=0
        Address=[]
        for line in file:
            temp = line.strip('\n')
            Address.append(temp)
            #name[num]=temp
            num+=1
            #print(temp)
    return Address

#k=random.randint(1,len(m_address))
#print(m_address[k])



#使用性质  非营运 货运 出租车 租赁 公路客运 公交客运 出租客运 旅游客运 教练 危险品运输


usage = ['非营运','货运', '出租车', '租赁', '公路客运', '公交客运', '出租客运', '旅游客运', '教练', '危险品运输']
def random_usage(usage):
    m_usage = "".join(random.sample(usage,1))
    return m_usage
#print(random_usage(usage))

#车型号

def random_sty():
    with open(r'../Dicts/Bands.txt') as file:
        num=0
        sty=[]
        for line in file:
            temp = line.strip('\n')
            sty.append(temp)
            num+=1
    return sty

#m_sty=random_sty()
#k=random.randint(1,len(m_sty))
#print(m_sty[k]+str(random_str(9)))


#车辆识别代号

def random_carid():
    m_carid = random_str(17)
    return m_carid
#print(random_carid())



#发动机号码 7-14
def random_carid():
    m_motorid=random_str(random.randint(7,14))
    return m_motorid
#print(random_carid())



#注册日期 2009-09-03
def random_regist_time():
    #先获得时间数组格式的日期
    threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days = Multiday))#365*17
    #转换为时间戳:
    timeStamp = int(time.mktime(threeDayAgo.timetuple()))
    #转换为其他字符串格式:
    m_regist_time = threeDayAgo.strftime("%Y-%m-%d")
    return m_regist_time
#print(random_regist_time())

#发证日期 2014-12-29
def random_issue_time():
    threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days = random.randint(0,Multiday)))#365*17
    #转换为时间戳:
    timeStamp = int(time.mktime(threeDayAgo.timetuple()))
    #转换为其他字符串格式:
    m_issue_time = threeDayAgo.strftime("%Y-%m-%d")
    return m_issue_time
#print(random_issue_time())


if __name__ == '__main__':
    #os.remove('list3.txt')
    m_address = random_Address()
    m_name = random_name()
    m_sty = random_sty()
    file = open('../DataAugment/assets/list.txt','w')
    for i in range(200000):
        try:
            k = random.randint(0, len(m_name)-1)
            k1 = random.randint(0,len(m_address)-1)
            k2 = random.randint(0, len(m_sty)-1)
            text = random_platenu(district1) + ','+ random_district(car_sty)+','+m_name[k]+','+m_address[k1]+','+\
               random_usage(usage)+','+m_sty[k2]+str(random_str(9))+','+random_carid()+','+random_carid()+ ','+\
               random_regist_time()+','+random_issue_time()
            file.write(text+'\n')
            if i % 5000==0:
                print(i),
        except:
            print('Error')

    file.close()