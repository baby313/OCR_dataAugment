
#include "LFocr.h"
#include "json/json.h"

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

	DriveLience dl0;
        dl0.init(strTemplateFile);
}

double overlapRate(int t1, int l1, int b1, int r1, int t2, int l2, int b2, int r2)
{
	double iner = (cv::max(0, cv::min(r1, r2) - cv::max(l1, l2)) * (cv::max(0, cv::min(b1, b2) - cv::max(t1, t2));
	double outer = (cv::max(r1, r2) - cv::min(l1, l2)) * (cv::max(b1, b2) - cv::min(t1, t2));
	return int / outer;
}

int OCR::testDetectAccuracy(string strdirJson, string strdirImg, vector<double> &vdAl)
{
	vector<string> vstrImg;
	Common::readDir(strdirImg, vstrImg);
	vector<string> vstrJson;
	Common::readDir(strdirJson, vstrJson);
	for (int i = 0; i < vstrImg.size(); i++)
	{
		vector<int> vrcImg;
		textCrop(vstrImg[i], vrcImg);
		vector<int> vrcJson;
		bool finded = false;
		for (int j = 0; j < vstrJson.size(); j++)
		{
			Json::Reader jsonReader;
			Json::Value jsonRoot;
			Json::Value jsonValue;
			std::ifstream inFile;
			inFile.open(vstrJson[j], std::ios::binary);
			if (jsonReader.parse(inFile, jsonRoot))
			{
				if (vstrImg[i] == jsonRoot["image"]["rawFilename"].asString())
				{
					int ocr_size = jsonRoot["objects"]["ocr"].size();
					for (int k = 0 ; k < ocr_size; k++)
					{
						 vrcJson.push_back(jsonRoot["objects"]["ocr"][k]["top"].asInt());
						 vrcJson.push_back(jsonRoot["objects"]["ocr"][k]["left"].asInt());
						 vrcJson.push_back(jsonRoot["objects"]["ocr"][k]["bottom"].asInt());
						 vrcJson.push_back(jsonRoot["objects"]["ocr"][k]["right"].asInt());
					}
					inFile.close();
					finded = true;
					break;
				}
				else
				{
					inFile.close();
					continue;
				}
			}
		}
		if (finded)
		{
			for (int j = 0 ; j < vrcImg.size(); j += 4)
			{
				double maxRate = 0.0;
				for (int k = 0 ; k < vrcJson.size(); k+= 4)
				{
					double tem = overlapRate(vrcImg[j], vrcImg[j+1], vrcImg[j+2], vrcImg[j+3], vrcImg[k], vrcImg[k+1], vrcImg[k+2], vrcImg[k+3]);
					if(temp > maxRate)
						maxRate = tem;
				}
				vdAl.push_back(maxRate);
			}
		}
	}
}

int OCR::printAccuracy(string strJson, vector<int> &vrc)
{
        
}

int OCR::textCrop(string strImgPath, vector<int> &vrc)
{
	IplImage* imgLocate = 0;
	imgLocate = cvLoadImage(strLocateImg.c_str());
	if (imgLocate == 0)
		return 1;
	IplImage* imgSrc = 0;
	imgSrc = cvLoadImage(strImgPath.c_str());
	std::vector<cv::Point> vpt_start;
	std::vector<cv::Point> vpt_end;
	sift_calc(imgLocate, imgSrc, vpt_start, vpt_end);
	
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
