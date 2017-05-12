
#include "mser.h"
#include "../common/common.h"

Mser::Mser()
{
}


Mser::~Mser()
{
}

vector<BigRect> Mser::detect_mser(Mat src, Mat mask, int maxHeight, double delta, int off, bool redchannel)
{
	Mat imgOrig, img;

	vector<BigRect> ret;
	vector<Rect>  zone;
	vector<Rect>  mergedzone;
	vector<Rect>  bigzone;
	vector<vector <Point> >  region;

	if (src.empty()) {
		cout << "file is empty" << endl;
		return ret;
	}

	double focus = Common::getFocus(src);
	cout << "focus " << focus << endl;

	int kern = (focus) / 3;
	Size blurSize(kern, kern);

	if (redchannel) {
		imgOrig = Common::getRedChannel(src);
	}
	else {
		if (src.channels() == 3) {
			cvtColor(src, imgOrig, COLOR_BGR2GRAY);
		}
		else{
			imgOrig = src;
		}
	}

	if (kern > 0) {
		blur(imgOrig, img, blurSize);
	}
	else{
		img = imgOrig;
	}

	if (!mask.empty()) {
		if (mask.size() != imgOrig.size()) {
			cout << "mask size " << mask.size() << " not match imgOrig " << imgOrig.size() << endl;
			return ret;
		}
	}


	MserDetector mser = MserDetector();
	mser.maxArea = 600;
	mser.minArea = 5;

	if (mser.detect(img, mask, zone, region))
	{
		//Mat result1;
		//src.copyTo(result1);
		//Common::drawrects(result1, zone, Scalar(255, 0, 0), 1);
		//imwrite("D:\\code\\code\\img\\temp\\3425838_1.jpg", result1);

		Common::filterRectsByHeight(zone, 0, maxHeight);
		Common::mergeRects(zone);
		for (int i = 0; i < zone.size(); i++) 
		{
			mergedzone.push_back(zone[i]);
		}

		//Mat result2;
		//src.copyTo(result2);
		//Common::drawrects(result2, zone, Scalar(255, 0, 0), 1);
		//imwrite("img_mser/3425838_2.jpg", result2);

		Common::MergeConnectComp(zone, delta, off);

		//Mat result3;
		//src.copyTo(result3);
		//Common::drawrects(result3, zone, Scalar(255, 0, 0), 1);
		//imwrite("img_mser/3425838_3.jpg", result3);

		Common::mergeRects(zone);

		//Mat result4;
		//src.copyTo(result4);
		//Common::drawrects(result4, zone, Scalar(255, 0, 0), 1);
		//imwrite("img_mser/3425838_4.jpg", result4);

		Common::MergeConnectComp(zone, delta, off);
		Common::filterRectsByHeight(zone, 8, maxHeight);
		bigzone = zone;

		//Mat result5;
		//src.copyTo(result5);
		//Common::drawrects(result5, zone, Scalar(255, 0, 0), 1);
		//imwrite("img_mser/3425838_5.jpg", result5);

		//saveDebugFile("detect_mser", result1, true);
		//saveDebugFile("merged_mser", result2, true);
		//saveDebugFile("newmerged_mser", result3, true);

		Common::sortRectsByArea(bigzone);

		//        bool frontface=true;
		//        if (bigzone.size() > 1) {
		//            if ((bigzone[0].width < 210)
		//                && (bigzone[0].width > 120) ){
		//                frontface = false;
		//            }
		//        }

		for (int i = 0; i < bigzone.size(); i++) 
		{
			BigRect tmp = BigRect(bigzone[i], mergedzone);
			ret.push_back(tmp);
			//if ((frontface == false) && (i== 1)
			//{
			//	break;
			//}
		}
	}
	return ret;
}
