
#include "mser_detector.h"
#include "../common/common.h"

MserDetector::MserDetector(int _delta, int _min_area, int _max_area,
	double _max_variation, double _min_diversity, bool _pass2Only,
	int _max_evolution, double _area_threshold,
	double _min_margin, int _edge_blur_size)
{
	delta = _delta;
	minArea = _min_area;
	maxArea = _max_area;
	maxVariation = _max_variation;
	minDiversity = _min_diversity;
	maxEvolution = _max_evolution;
	areaThreshold = _area_threshold;
	minMargin = _min_margin;
	edgeBlurSize = _edge_blur_size;
	pass2Only = _pass2Only;
}

MserDetector::~MserDetector()
{
}

bool MserDetector::detect(cv::Mat img, cv::Mat mask, vector<Rect> &zone, vector<vector<Point> > &region)
{
	if (!mask.empty()) {
		if (img.size() != mask.size()) {
			cout << "img size and mask size not match" << endl;
			return false;
		}
		Mat newimg = Mat::zeros(img.size(), img.type());
		img.copyTo(newimg, mask);
		newimg.copyTo(img);
	}

	Ptr<Feature2D> b;
	if (img.type() == CV_8UC3)
	{
		b = MSER::create(this->delta, this->minArea, this->maxArea, this->maxVariation, this->minDiversity, this->maxEvolution,
			this->areaThreshold, this->minMargin, this->edgeBlurSize);
	}
	else
	{
		b = MSER::create(this->delta, this->minArea, this->maxArea, this->maxVariation, this->minDiversity);
		b.dynamicCast<MSER>()->setPass2Only(this->pass2Only);

	}
	try
	{
		Mat desc;
		if (b.dynamicCast<MSER>() != NULL)
		{
			Ptr<MSER> sbd = b.dynamicCast<MSER>();
			sbd->detectRegions(img, region, zone);
			return  true;
		}
		else
			return false;
	}
	catch (Exception& e)
	{
		cout << e.msg << endl;
	}
	return false;
}

