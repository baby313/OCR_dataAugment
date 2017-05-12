
#ifndef MSER_H
#define MESR_H

#include <vector>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

#include "mser_detector.h"
#include "../common/big_rect.h"

class Mser
{
public:
	Mser();
	~Mser();

public:

	static vector<BigRect> detect_mser(Mat src, Mat mask, int maxHeight, double delta, int off, bool redchannel);

};

#endif //MESR_H
