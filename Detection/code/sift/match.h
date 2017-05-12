
#ifndef MATCH_H
#define MATCH_H

#include <opencv/cv.h>
#include <opencv/cxcore.h>
#include <opencv/highgui.h>

using namespace cv;

/*************************** Function Prototypes *****************************/

/**
Creates a new minimizing priority queue.
*/
extern void sift_calc(IplImage *imgS, IplImage *imgB, vector<cv::Point>& vpt_start, vector<Point>& vpt_end);


#endif
