
#ifndef MSERDetector_hpp
#define MSERDetector_hpp

#include <vector>
#include <opencv2/opencv.hpp>

using namespace cv;
using namespace std;

class MserDetector
{
public:
	MserDetector(int _delta = 4, int _min_area = 3, int _max_area = 1000,
		double _max_variation = 2, double _min_diversity = 2, bool _pass2Only = false,
		int _max_evolution = 200, double _area_threshold = 1.01,
		double _min_margin = 0.003, int _edge_blur_size = 5);
	~MserDetector();
	int delta;
	int minArea;
	int maxArea;
	double maxVariation;
	double minDiversity;
	bool pass2Only;

	int maxEvolution;
	double areaThreshold;
	double minMargin;
	int edgeBlurSize;

	bool detect(Mat img, Mat mask, vector<Rect>  &zone, vector<vector <Point> >  &region);

};


#endif /* MSERDetector_hpp */
