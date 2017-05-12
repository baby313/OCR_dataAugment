
#ifndef BigRect_h
#define BigRect_h

#include <opencv2/opencv.hpp>
#include <vector>

using namespace cv;
using namespace std;

class BigRect{
public:
    BigRect();
    BigRect(Rect rect, vector<Rect> subrec);
    ~BigRect();

	static bool sortbyX(const Rect r1, const Rect r2);
	void sortRectsByX(vector<Rect> &recs);
	static bool sortbyArea(const Rect r1, const Rect r2);
	void sortRectsByArea(vector<Rect> &recs);
	void mergeRects(vector<Rect>  &zone);

    void split(int offset=2);
    void adjustWidth(int width);
    void eraseByIndex(int index);
    void eraseByRatio(double ratio=0.5);
    void adjustOffset(int offset=2);
    void eraseIntersect();
    void filterSubRects(Rect tmp);
    void mergeSubRects(double ratio=0.8, int offset=5);

    Rect rc;
    vector<Rect> vSubRc;
};

#endif /* HejinBigRect_hpp */
