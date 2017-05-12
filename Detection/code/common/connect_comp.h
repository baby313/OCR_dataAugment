
#ifndef connectComp_h
#define connectComp_h

#include <vector>
#include <opencv2/opencv.hpp>

using namespace cv;
using namespace std;

class connectComp{
public:
    connectComp(Rect r1, Rect r2, double delta=0.7, int off = 10);
    ~connectComp();
    bool connected(Rect r1, Rect r2, double delta=0.7, int off = 10);
    bool same(connectComp in);
    bool sharesame(connectComp in);
    bool empty();
    Rect start;
    Rect end;
    Rect outter;
    Rect inner;
};

#endif // connectComp_h 
