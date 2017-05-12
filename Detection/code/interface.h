#include<python2.7/Python.h>
#include<opencv2/opencv.hpp>
#include<string>
#include<stdio.h>
using namespace cv;
using namespace std;

#include"LFocr.h"
using namespace LF;

extern "C" 
{
	PyObject* textCrop(const char* loc, const char* tem, const char* img );
        PyObject* test(const char* loc, const char*tem, const char* pathJson, const char* pathImgd);
}


