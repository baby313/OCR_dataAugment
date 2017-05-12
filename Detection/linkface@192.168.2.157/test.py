from ctypes import *
import numpy as np

LFocr = CDLL("/home/dp/OCR/Detection/code/LFocr.so")
LFocr.textCrop.restype = py_object
res = LFocr.textCrop("/home/dp/OCR/Detection/locate/title.jpg","/home/dp/OCR/Detection/template/DriveLicense_0.json","/home/dp/OCR/Detection/img_correct/3425581_0.jpg")
np.array(res).reshape((len(res)/4, 4))
print res
