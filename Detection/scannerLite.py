# coding=utf-8

import sys, glob
import cv2
import numpy as np
from matplotlib import pyplot as plt


class Line:

    def __init__(self, l):
        self.point = l
        x1, y1, x2, y2 = l
        self.c_x = (x1 + x2) / 2
        self.c_y = (y1 + y2) / 2


def show(im):
    msg = 'press any key to continue'
    cv2.namedWindow(msg, cv2.WINDOW_NORMAL)
    cv2.imshow(msg, im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def intersection(l1, l2):
    x1, y1, x2, y2 = l1.point
    x3, y3, x4, y4 = l2.point
    a1, b1 = y2 - y1, x1 - x2
    c1 = a1 * x1 + b1 * y1
    a2, b2 = y4 - y3, x3 - x4
    c2 = a2 * x3 + b2 * y3
    det = a1 * b2 - a2 * b1
    assert det, "lines are parallel"
    return (1. * (b2 * c1 - b1 * c2) / det, 1. * (a1 * c2 - a2 * c1) / det)


def scannerLite(im, debug=False):
    # resize
    print(im.shape)
    h, w, _ = im.shape
    min_w = 300
    scale = min(10., w * 1. / min_w)
    h_proc = int(h * 1. / scale)
    w_proc = int(w * 1. / scale)
    im_dis = cv2.resize(im, (w_proc, h_proc))
    print(im_dis.shape)

    # gray
    gray = cv2.cvtColor(im_dis, cv2.COLOR_BGR2GRAY)
    
    # blur
    # gray = cv2.blur(gray, (3, 3))
    # gray = cv2.GaussianBlur(gray, (3,3), 0)

    if debug:
        show(gray)

    # canny edges detection
    high_thres = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[0]
    low_thres = high_thres * 0.33
    canny = cv2.Canny(gray, low_thres, high_thres)
    if debug:
        show(canny)

    # lines detection
    lines = cv2.HoughLinesP(
        canny, 1, np.pi / 180, h_proc / 4, None, h_proc / 4, 40)

    if debug:
        t = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)

    # classify lines
    hori, vert = [], []
    for l in lines[0]:
        x1, y1, x2, y2 = l
        if abs(x1 - x2) > abs(y1 - y2):
            hori.append(Line(l))
        else:
            vert.append(Line(l))
        if debug:
            cv2.line(t, (x1, y1), (x2, y2), (0, 0, 255), 1)
    if debug:
        show(t)

    # not enough
    if len(hori) < 2:
        if not hori or hori[0].c_y > h_proc / 2:
            hori.append(Line((0, 0, w_proc - 1, 0)))
        if not hori or hori[0].c_y <= h_proc / 2:
            hori.append(Line((0, h_proc - 1, w_proc - 1, h_proc - 1)))

    if len(vert) < 2:
        if not vert or vert[0].c_x > w_proc / 2:
            vert.append(Line((0, 0, 0, h_proc - 1)))
        if not vert or vert[0].c_x <= w_proc / 2:
            vert.append(Line((w_proc - 1, 0, w_proc - 1, h_proc - 1)))

    hori.sort(key=lambda l: l.c_y)
    vert.sort(key=lambda l: l.c_x)

    # corners
    if debug:
        for l in [hori[0], vert[0], hori[-1], vert[-1]]:
            x1, y1, x2, y2 = l.point
            cv2.line(t, (x1, y1), (x2, y2), (0, 255, 255), 1)

    img_pts = [intersection(hori[0], vert[0]), intersection(hori[0], vert[-1]),
               intersection(hori[-1], vert[0]), intersection(hori[-1], vert[-1])]

    for i, p in enumerate(img_pts):
        x, y = p
        img_pts[i] = (x * scale, y * scale)
        if debug:
            cv2.circle(t, (int(x), int(y)), 1, (255, 255, 0), 3)
    if debug:
        show(t)

    # perspective transform
    # w_a4, h_a4 = 1654, 2339
    w_a4, h_a4 = 620, 420
    dst_pts = np.array(
        ((0, 0), (w_a4 - 1, 0), (0, h_a4 - 1), (w_a4 - 1, h_a4 - 1)),
        np.float32)
    img_pts = np.array(img_pts, np.float32)
    transmtx = cv2.getPerspectiveTransform(img_pts, dst_pts)
    return cv2.warpPerspective(im, transmtx, (w_a4, h_a4))


def detect(img): 
    img_copy = img.copy()

    # 转成灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 将灰度图像转成二值图像
    #ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)


    # img1 = cv2.GaussianBlur(gray, (5, 5), 0)
    # canny = cv2.Canny(img1, 50, 150)
    #
    # cv2.imshow('Canny', canny)

    #高斯模糊
    img1 = cv2.GaussianBlur(img, (1, 1), 0)
    # cv2.imshow("img1", img1)
    show(img1)

    #OpenCV定义的结构元素
    kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))

    # 开运算
    opened = cv2.morphologyEx(img1, cv2.MORPH_OPEN, kernel1)
    #显示腐蚀后的图像
    # cv2.imshow("Open", opened)
    show(opened)

    #OpenCV定义的结构元素
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))

    # 闭运算
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel2)
    # 显示腐蚀后的图像
    # cv2.imshow("Close", closed)
    show(closed)

    # 转成灰度图像
    # gray2 = cv2.cvtColor(closed, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('gray2', gray2)

    # canny = cv2.Canny(gray, 50, 150)
    canny = cv2.Canny(closed, 20, 80)

    # cv2.imshow('Canny', canny)
    show(canny)




    # #OpenCV定义的结构元素
    # kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT,(20, 20))

    # # 开运算
    # opened2 = cv2.morphologyEx(canny, cv2.MORPH_OPEN, kernel1)
    # #显示腐蚀后的图像
    # cv2.imshow("Open2", opened2);

    # 将灰度图像转成二值图像
    # ret, binary = cv2.threshold(canny, 127, 255, cv2.THRESH_BINARY)

    # 查找轮廓
    # aa,contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 查找轮廓
    _, contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(img_copy, contours, -1, (0, 0, 255), -1)

    # cv2.imshow("img_copy", img_copy)
    show(img_copy)



    maxarea = 0
    for i in range(1,len(contours)):
        area = cv2.contourArea(contours[i])

        if area > maxarea :
            maxarea = area
            contmax = contours[i]
            print(area)

    # # 用粉色(177, 156, 242)来画出最小的矩形框架
    # x, y, w, h = cv2.boundingRect(contmax)
    # cv2.rectangle(img, (x, y), (x+w, y+h), (177, 156, 242), 2);
    # cv2.imshow("img_d", img)

    # 用红色(0, 0, 255)表示有旋转角度的矩形框架
    rect = cv2.minAreaRect(contmax)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
    # cv2.imshow("img_d", img)
    show(img)
    # cv2.imwrite("ID_D4.jpg", img)

    # cv2.waitKey(0)    

if __name__ == '__main__':
    # imagePath = sys.argv[1]
    in_path = "/Users/lairf/Documents/LinkfaceTrainingData/行驶证&驾驶证&营业执照OCR/行驶证/*.jpg"
    for img_file in glob.glob(in_path):
        print(img_file)
        im = cv2.imread(img_file)
        show(im)
        # dst = scannerLite(im, debug=True)
        # show(dst)
        detect(im)