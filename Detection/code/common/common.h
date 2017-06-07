
#ifndef _COMMON_H
#define _COMMON_H

#include <vector>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

#include "big_rect.h"
#include "connect_comp.h"

#ifdef _WIN32
#include "io.h"
#include "direct.h"
#else
#include <sys/stat.h>
#include <dirent.h>
#include<unistd.h>
#endif

#define SCALE 3.0

namespace Common
{
	static bool readDir(std::string strDir, std::vector<std::string> &vecFile)
	{
#ifdef _WIN32
		strDir += "*.*";
		struct _finddata_t file;
		long fileHandle;
		if ((fileHandle = _findfirst(strDir.c_str(), &file)) == -1)
		{
			return false;
		}
		do
		{
			if (strcmp(file.name, "..") != 0 && strcmp(file.name, ".") != 0)
			{
				if (_A_SUBDIR == file.attrib)
				{
					continue;
				}
				else
				{
					std::string str = strDir.substr(0, strDir.rfind("\\") + 1);
					if (str.empty())
					{
						str = strDir.substr(0, strDir.rfind("/") + 1);
					}
					str += file.name;
					vecFile.push_back(str);
				}
			}
		} while (!(_findnext(fileHandle, &file)));
		_findclose(fileHandle);
		return true;
#else
		DIR *dp;
		if ((dp = opendir(strDir.c_str())) == NULL)
			return false;
		struct dirent *dirp;
		int n = 0;
		while ((dirp = readdir(dp)) != NULL)
		{
			if (strcmp(dirp->d_name, "..") != 0 && strcmp(dirp->d_name, ".") != 0)
			{
				string str = strDir + dirp->d_name;
				vecFile.push_back(str);
				n++;
			}
		}
#endif
	}
	static bool CreatDir(std::string pszDir)
	{
#ifdef _WIN32
		int i = 0;
		int iRet = 0;
		int iLen = pszDir.length();

		if (pszDir[iLen - 1] != '\\')
		{
			pszDir += "\\";
		}
		iLen = pszDir.length();

		for (i = 0; i < iLen; i++)
		{
			if (pszDir[i] == '\\')
			{
				iRet = _access(pszDir.c_str(), 0);   //���ڷ�����
				//����������,����
				if (iRet != 0)
				{
					iRet = _mkdir(pszDir.c_str());
					if (iRet != 0)
					{
						return false;
					}
				}
			}
		}
		return true;

#else
		int res = access(pszDir.c_str(), F_OK);
		if (res == 0)
		{
			return true;
		}
		res = mkdir(pszDir.c_str(), S_IRWXU);
		if (0 != res)
		{
			return false;
		}
		return true;
#endif
	}

	static bool dividePathFile(std::string fullPath, std::string &strPath, std::string &strFileName, std::string &strFileExt)
	{
		int pos1 = fullPath.rfind("\\");
		int pos2 = fullPath.rfind("/");
		if ((pos1 < 0 || pos1 >= fullPath.length()) && (pos2 < 0 || pos2 >= fullPath.length()))
		{
			return false;
		}
		strPath = fullPath.substr(0, max(pos1, pos2) + 1);
		int pos3 = fullPath.rfind(".");
		strFileName = fullPath.substr(max(pos1, pos2) + 1, pos3 - max(pos1, pos2) - 1);
		strFileExt = fullPath.substr(pos3 + 1, fullPath.length());
		return true;
	}

	static string getFilePath(std::string fullPath)
	{
		int pos1 = fullPath.rfind("\\");
		int pos2 = fullPath.rfind("/");
		if ((pos1 < 0 || pos1 >= fullPath.length()) && (pos2 < 0 || pos2 >= fullPath.length()))
		{
			return "";
		}
		return fullPath.substr(0, max(pos1, pos2) + 1);
	}

	static string getFileFullName(string fullPath)
	{
		int pos1 = fullPath.rfind("\\");
		int pos2 = fullPath.rfind("/");
		if ((pos1 < 0 || pos1 >= fullPath.length()) && (pos2 < 0 || pos2 >= fullPath.length()))
		{
			return "";
		}
		return fullPath.substr(max(pos1, pos2) + 1, fullPath.length());
	}

	static string getFileName(std::string fullPath)
	{
		int pos1 = fullPath.rfind("\\");
		int pos2 = fullPath.rfind("/");
		if ((pos1 < 0 || pos1 >= fullPath.length()) && (pos2 < 0 || pos2 >= fullPath.length()))
		{
			return "";
		}
		int pos3 = fullPath.rfind(".");
		return fullPath.substr(max(pos1, pos2) + 1, pos3 - max(pos1, pos2) - 1);
	}

	static string getFileExtName(std::string fullPath)
	{
		int pos1 = fullPath.rfind("\\");
		int pos2 = fullPath.rfind("/");
		if ((pos1 < 0 || pos1 >= fullPath.length()) && (pos2 < 0 || pos2 >= fullPath.length()))
		{
			return "";
		}
		int pos3 = fullPath.rfind(".");
		return fullPath.substr(pos3 + 1, fullPath.length());
	}


	static bool sortbyArea(const Rect r1, const Rect r2)
	{
		return r1.area() > r2.area();
	}
	static void sortRectsByArea(vector<Rect> &recs)
	{
		if (recs.size() > 0) {
			sort(recs.begin(), recs.end(), sortbyArea);
		}
	}

	static bool sortbyX(const Rect r1, const Rect r2)
	{
		return r1.x < r2.x;
	}
	static bool sortbyY(const Rect r1, const Rect r2)
	{
		return r1.y < r2.y;
	}

	static float llcv_stddev_of_abs_c(Mat src)
	{
		int ch[] = { 0, 0 };
		Mat single(src.size(), CV_8U);
		mixChannels(&src, 1, &single, 1, ch, 1);
		CvMat image = single;
		cvAbs(&image, &image);
		CvScalar stddev;
		cvAvgSdv(&image, NULL, &stddev, NULL);
		return (float)stddev.val[0];
	}

	/*
	Combines two images by scacking one on top of the other

	@param img1 top image
	@param img2 bottom image

	@return Returns the image resulting from stacking \a img1 on top if \a img2
	*/
	static IplImage* stack_imgs(IplImage* img1, IplImage* img2)
	{
		IplImage* stacked = cvCreateImage(cvSize(MAX(img1->width, img2->width),
			img1->height + img2->height),
			IPL_DEPTH_8U, img2->nChannels);

		cvZero(stacked);
		cvSetImageROI(stacked, cvRect(0, 0, img1->width, img1->height));
		cvAdd(img1, stacked, stacked, NULL);
		cvSetImageROI(stacked, cvRect(0, img1->height, img2->width, img2->height));
		cvAdd(img2, stacked, stacked, NULL);
		cvResetImageROI(stacked);

		return stacked;
	}

	static float focus(Mat src)
	{
		Mat dst;
		Sobel(src, dst, 2 * src.depth(), 1, 1);
		return llcv_stddev_of_abs_c(dst);
	}
	static double getFocus(Mat &src)
	{
		Mat color;
		//used to calculate brightness and focus
		cvtColor(src, color, COLOR_BGR2YCrCb);
		return focus(color);
	}

	static bool getMaxChannle(IplImage * src, IplImage * dst)
	{
		for (int i = 0; i < src->height; i++)
		{
			for (int j = 0; j < src->width; j += 3)
			{
				unsigned b = src->imageData[i * src->widthStep + j * 3];
				unsigned g = src->imageData[i * src->widthStep + j * 3 + 1];
				unsigned r = src->imageData[i * src->widthStep + j * 3 + 2];
				dst->imageData[i * dst->widthStep + j] = max(max(b, g), r);
			}
		}
		return true;
	}
    
/*    static Mat getMaxChannle(Mat & src)
    {
        Mat res(src.rows, src.cols, CV_32UC, Scalar(255));
        for (i = 0; i < src.rows; i++) {
            p = src.ptr<uchar>(i);
            q = res.ptr<uchar>(i)
            for (int j = 0; j < src.cols; j += 3) {
                q[j] = max(p[j], p[j + 1], p[j + 2]);
            }
        }
        return res;
    }

*/	static Mat getRedChannel(Mat src)
	{
		if (src.channels() == 3) {
			vector<Mat> channels;
			cv::split(src, channels);
			return  channels[2];
		}
		else{
			return  src;
		}
	}

	static Mat getGreenChannel(Mat src)
	{
		if (src.channels() == 3) {
			vector<Mat> channels;
			cv::split(src, channels);
			return  channels[1];
		}
		else{
			return  src;
		}
	}

	static Mat getBlueChannel(Mat src)
	{
		if (src.channels() == 3) {
			vector<Mat> channels;
			cv::split(src, channels);
			return  channels[0];
		}
		else{
			return  src;
		}
	}

	static void colorFilter(Mat inmat, Mat& outmat)
	{
		int i, j;
		//IplImage* image = cvCreateImage(cvGetSize(inmat), 8, 3);
		//cvGetImage(inmat, image);
		//IplImage* hsv = cvCreateImage(cvGetSize(image), 8, 3);
		Mat image;
		inmat.copyTo(image);
		Mat hsv;

		cvtColor(inmat, hsv, CV_BGR2HSV);
		int width = hsv.cols;
		int height = hsv.rows;
		for (i = 0; i < height; i++)
		{
			uchar *udata = hsv.ptr<uchar>(i);
			for (j = 0; j < width; j++)
			{
				//��ȡ���ص�Ϊ��j, i������HSV��ֵ 
				/*opencv ��H��Χ��0~180����ɫ��H��Χ������(0~8)��(160,180)
				S�Ǳ��Ͷȣ�һ���Ǵ���һ��ֵ,S���;��ǻ�ɫ���ο�ֵS>80)��
				V�����ȣ����;��Ǻ�ɫ�����߾��ǰ�ɫ(�ο�ֵ220>V>50)��*/
				//if (!(((udata[j * 3]>0) && (udata[j * 3]<8)) || (udata[j * 3]>120) && (udata[j * 3] < 180)))
				if (!((udata[j * 3]>160) && (udata[j * 3] < 250)))
				{
					udata[j * 3 + 1] = 0;
					udata[j * 3 + 2] = 255;
				}
			}
		}
		cvtColor(hsv, outmat, CV_HSV2BGR);
	}

	static void bin(IplImage * src, IplImage * dst)
	{
		int minpix = 255;
		for (int i = 0; i < src->height; i++)
		{
			for (int j = 0; j < src->width; j++)
			{
				int tmp = (unsigned char)(src->imageData[i * src->widthStep + j]);
				if (minpix > tmp)
				{
					minpix = tmp;
				}
			}
		}
		cvThreshold(src, dst, minpix + 50, 255, CV_THRESH_BINARY);
		int xxx = 1;
		while (true)
		{
			int nCount = 0;
			for (int i = 0; i < dst->height; i++)
			{
				for (int j = 0; j < dst->width; j++)
				{
					if ((unsigned char)(dst->imageData[i * dst->widthStep + j]) < 128)
					{
						nCount++;
					}
				}
			}
			if (nCount < (dst->height * dst->width) / 12)
			{
				cvThreshold(src, dst, minpix + 50 + xxx * 10, 255, CV_THRESH_BINARY);
				xxx++;
				//cvShowImage("dst" , dst);
				//cvWaitKey(0);
			}
			else
			{
				break;
			}
		}
	}

	static void filterRectsByHeight(vector<Rect>  &zone, int minHeight, int maxHeight)
	{
		for (vector<Rect>::iterator it = zone.begin(); it != zone.end();) {
			Rect rec = *it;
			if ((rec.height > maxHeight) || (rec.height <= minHeight)) {
				it = zone.erase(it);
			}
			else
				it++;
		}
	}

	static void mergeOnHor(vector<Rect>  &zone)
	{
		sort(zone.begin(), zone.end(), sortbyX);
	}
	static void mergeOnVer(vector<Rect>  &zone)
	{
		sort(zone.begin(), zone.end(), sortbyY);
	}

	static void mergeRects(vector<Rect>  &zone)
	{
#if 0
		char *pLa = new char[zone.size()];
		memset(pLa, 0, sizeof(char)* zone.size());
		while (true)
		{
			bool merged = false;
			for (int i = 0; i < zone.size(); i++)
			{
				if (*(pLa + i) != 0)
					continue;
				for (int j = i + 1; j < zone.size(); j++)
				{
					if (*(pLa + j) != 0)
						continue;
					Rect temp = zone[i] & zone[j];
					if (temp.height > 0 && temp.width > 0)
					{
						zone[i] = zone[i] | zone[j];
						*(pLa + j) = 1;
						merged = true;
						//continue;
					}
				}
			}
			if (merged == false)
				break;
		}

		vector<Rect>  ret;
		for (int i = 0; i < zone.size(); i++)
		{
			if (*(pLa + i) == 0)
			{
				ret.push_back(zone[i]);
			}
		}
		zone = ret;
#endif

#if 1
		vector<Rect>  ret;
		vector<Rect>  remain;
		vector<Rect>  tmpremain;

		sort(zone.begin(), zone.end(), sortbyArea);
		Rect tmp;
		remain = zone;
		while (remain.size() > 0) {
			tmp = remain[0];
			tmpremain.clear();
			for (int j = 1; j < remain.size(); j++) {
				Rect rec = remain[j];
				Rect inter = tmp & rec;
				Rect outer = tmp | rec;
				if (inter == tmp || inter == rec){
					tmp = outer;
				}
				else{
					tmpremain.push_back(rec);
				}
			}
			ret.push_back(tmp);
			remain = tmpremain;
		}
		zone = ret;
#endif
	}

	static void mergeInterectRects(vector<Rect>  &zone)
	{
		vector<Rect>  ret;
		vector<Rect>  remain;
		vector<Rect>  tmpremain;

		sort(zone.begin(), zone.end(), sortbyArea);
		Rect tmp;
		remain = zone;
		while (remain.size() > 0) {
			tmp = remain[0];
			tmpremain.clear();
			for (int j = 1; j< remain.size(); j++) {
				Rect rec = remain[j];
				Rect inter = tmp & rec;
				Rect outer = tmp | rec;
				if (inter.area() >0){
					connectComp comp(tmp, rec);
					if (comp.empty()) {
						tmpremain.push_back(rec);
					}
					else
						tmp = outer;
				}
				else{
					tmpremain.push_back(rec);
				}
			}
			ret.push_back(tmp);
			remain = tmpremain;
		}
		zone = ret;
	}
	static void MergeConnectComp(vector<Rect> &zone, double delta, int off)
	{
		vector<connectComp> comps;
		bool hasconnect = false;

		sort(zone.begin(), zone.end(), sortbyX);
		//get all connected info and remove all has connected;
		for (vector<Rect>::iterator it = zone.begin(); it != zone.end();)
		{
			hasconnect = false;
			for (vector<Rect>::iterator itsecond = zone.begin(); itsecond != zone.end(); itsecond++)
			{
				if (it == itsecond)
					continue;
				connectComp tmp(*it, *itsecond, delta, off);
				if (tmp.empty())
					continue;
				comps.push_back(tmp);
				hasconnect = true;
			}
			if (hasconnect)
				it = zone.erase(it);
			else
				it++;
		}

		while (comps.size() > 0)
		{
			for (vector<connectComp>::iterator it = comps.begin(); it != comps.end();)
			{
				hasconnect = false;
				for (vector<connectComp>::iterator itsecond = comps.begin(); itsecond != comps.end(); itsecond++)
				{
					if (it == itsecond)
						continue;
					if (it->sharesame(*itsecond) && !(it->same(*itsecond)))
					{
						if (it->start.x < itsecond->start.x)
						{
							itsecond->start = it->outter;
							itsecond->outter = itsecond->start | itsecond->end;
						}
						else
						{
							itsecond->start = itsecond->outter;
							itsecond->end = it->end;
							itsecond->outter = itsecond->start | itsecond->end;
						}
						hasconnect = true;
					}
				}
				if (hasconnect)
				{
					it = comps.erase(it);
				}
				else
				{
					zone.push_back(it->outter);
					it = comps.erase(it);
				}
			}
		}
		mergeRects(zone);
		mergeInterectRects(zone);
	}

	static void drawrects(Mat result, vector<Rect> zone, Scalar color, int thickness)
	{
		for (int i = 0; i < zone.size(); i++) {
			rectangle(result, zone[i], color, thickness);
		}
	}

	static void drawBigRects(Mat result, vector<BigRect>  &zone, bool subrc = true)
	{
		for (int i = 0; i < zone.size(); i++) {
			Rect rec = zone[i].rc;
			rec -= Point(2, 2);
			rec += Size(4, 4);
			rectangle(result, rec, Scalar(0, 0, 255));
			if (subrc)
			{
				drawrects(result, zone[i].vSubRc, Scalar(255, 0, 0), 1);
			}
		}
	}

	static void drawBigRect(Mat result, BigRect bigrec)
	{
		Rect rec = bigrec.rc;
		rec -= Point(2, 2);
		rec += Size(4, 4);
		rectangle(result, rec, Scalar(0, 0, 255));
		drawrects(result, bigrec.vSubRc, Scalar(255, 0, 0), 1);
	}

	static Rect multiRC(Rect param, double scale)
	{
		Rect rc;
		rc.x = param.x * scale;
		rc.y = param.y * scale;
		rc.width = param.width * scale;
		rc.height = param.height * scale;
		return rc;
	}

	static double rcOverlapRat(Rect rc1, Rect rc2)
	{
		Rect inte = rc1 & rc2;
		return max( ((double)inte.area()) / ((double)rc1.area()), ((double)inte.area()) / ((double)rc2.area()) );
	}

	static void getMidPT(vector<Point> &vpt, Point &pt)
	{
		vector<vector<Point> > vvpt;
		vector<Point> vpt_tmp;
		vpt_tmp.push_back(vpt[0]);
		vpt_tmp.push_back(vpt[0]);
		vvpt.push_back(vpt_tmp);
		for (int mm = 1; mm < vpt.size(); mm++)
		{
			int maxSame = -1;
			int minDis = 10000;
			for (int nn = 0; nn < vvpt.size(); nn++)
			{
				int x_dis = abs(vvpt[nn][0].x - vpt[mm].x);
				int y_dis = abs(vvpt[nn][0].y - vpt[mm].y);
				if (x_dis <= SCALE * 30 && y_dis <= SCALE * 30 && (x_dis + y_dis) < minDis)
				{
					minDis = abs(vvpt[nn][0].x - vpt[mm].x) + abs(vvpt[nn][0].y - vpt[mm].y);
					maxSame = nn;
				}
			}
			if (maxSame >= 0)//�ҵ������ʵ��飬���ҽ����´��� 
			{
				vvpt[maxSame].push_back(vpt[mm]);
				vvpt[maxSame][0].x = 0;  vvpt[maxSame][0].y = 0;
				for (int ww = 1; ww < vvpt[maxSame].size(); ww++)
				{
					vvpt[maxSame][0].x += vvpt[maxSame][ww].x;
					vvpt[maxSame][0].y += vvpt[maxSame][ww].y;
				}
				vvpt[maxSame][0].x /= (vvpt[maxSame].size() - 1);
				vvpt[maxSame][0].y /= (vvpt[maxSame].size() - 1);
			}
			else
			{
				std::vector<cv::Point> vpt_tmp2;
				vpt_tmp2.push_back(vpt[mm]);
				vpt_tmp2.push_back(vpt[mm]);
				vvpt.push_back(vpt_tmp2);
			}
		}
		int maxCount = 0;
		int maxPos = 0;
		for (int nn = 0; nn < vvpt.size(); nn++)
		{
			if (vvpt[nn].size() > maxCount)
			{
				maxCount = vvpt[nn].size();
				maxPos = nn;
			}
		}
		pt = vvpt[maxPos][0];
	}

};

#endif //_COMMON_H
