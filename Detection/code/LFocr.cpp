
#include <fstream>

using namespace std; 

#include "LFocr.h"
#include "json/json.h"
//#include "layout/layout.h"

#define OUTPUT_IMAGE
#define SIFT_MATCH_MIN 16

#ifdef _WIN32
string img_path = "D:\\code\\code\\img\\";
string temp_path = "D:\\code\\code\\template\\";
#else
string img_path = "/home/liyd/img/DriveLicense/img/";
string temp_path = "/home/liyd/img/DriveLicense/template/";
#endif

#ifdef _WIN32
#define SEPARATE_LINE "\\"
#else
#define SEPARATE_LINE "/"
#endif

using namespace LF;

OCR::OCR(string strLocate, string strTemplate)
{
	init(strLocate, strTemplate);
}

OCR::~OCR()
{
}

int OCR::init(string strLocate, string strTemplate)
{
	strLocateImg = strLocate;
    strTemplateFile = strTemplate;

	
    dl0.init(strTemplateFile);
}

int OCR::textCrop(string strImgPath, vector<int> &vrc)
{
	IplImage* imgLocate = 0;
	//printf("Image is : %s\n ", strImgPath.c_str());
	imgLocate = cvLoadImage(strLocateImg.c_str());
	if (imgLocate == 0)
	{
		printf("Load locate image %s failed.", strLocateImg.c_str());
		return 1;
	}
	//printf("Load locate image %s succeed. \n", strLocateImg.c_str());
	IplImage* imgSrc = 0;
	imgSrc = cvLoadImage(strImgPath.c_str());
	if (imgSrc == 0)
	{
		printf("Load image %s failed.", strImgPath.c_str());
		return 1;
	}
	//printf("Load %s succeed. \n", strImgPath.c_str());
	std::vector<cv::Point> vpt_start;
	std::vector<cv::Point> vpt_end;
	sift_calc(imgLocate, imgSrc, vpt_start, vpt_end);
	//printf("Sift cal end.");

	bool sift_match = false;
	if (vpt_end.size() >= SIFT_MATCH_MIN)
	{
		sift_match = true;
	}

	Mat mask;
	Mat src = imread(strImgPath);
	vector<BigRect> bigrects = Mser::detect_mser(src, mask, 70, 0.7, 10, true);

	for (int i = 0; i < dl0.vNode.size(); i++)
	{
		Rect rc;
		bool bGet = false;
		for (int j = 0; j < bigrects.size(); j++)
		{
			double temp = Common::rcOverlapRat(dl0.vNode[i].rc, bigrects[j].rc);
			Rect rctmp = (dl0.vNode[i].rc & bigrects[j].rc);
			if (temp > 0 && rctmp.width > 2 && rctmp.height > 2)
			{
				rc = bGet ? (rc | (dl0.vNode[i].rc & bigrects[j].rc)) : (dl0.vNode[i].rc & bigrects[j].rc);
				bGet = true;
			}
		}
		vrc.push_back(rc.y);
		vrc.push_back(rc.x);
		vrc.push_back(rc.y + rc.height);
		vrc.push_back(rc.x + rc.width);
	}
}






