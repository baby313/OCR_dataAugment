#include <string>
#include <vector>

using namespace std;

#include "mser/mser.h"
#include "common/big_rect.h"
#include "common/common.h"
#include "sift/match.h"

#include "drive_license.h"

namespace LF
{
    class OCR
    {
    public:
       OCR(string strLocate, string strTemplate);
       ~OCR();
    public:
	int textCrop(string strImgPath, vector<int> &vrc);
    public:
	string strLocateImg;
	string strTemplateFile;
    };
}
