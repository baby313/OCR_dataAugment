//////////////////////////////////////////////////////////////////////////

#ifndef DRIVE_LICENSE_H
#define DRIVE_LICENSE_H

#include <string>
#include <vector>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

typedef struct ProjLocale 
{
	string key;//label
	Rect rc;
};

typedef struct ProjNode
{
	string key;//label
	Rect rc;
}NODE;

class DriveLicense
{
public:
	DriveLicense();
	~DriveLicense();

public:
	int init(string tempFile);

private:
	int readTemplate(string tempFile);

public:
	int DLtype;//行驶证类型 
	vector<ProjLocale> vLocate;
	vector<ProjNode> vNode;
	
	//ProjNode title;//标题 
	//ProjNode NO;//号牌号码 
	//ProjNode vehicleType;//车辆类型 
	//ProjNode owner;//所有人 
	//ProjNode address;//住址 
	//ProjNode property;//使用性质：非营运等 
	//ProjNode brand;//品牌型号 
	//ProjNode IDCode;//车辆识别代码 
	//ProjNode engineID;//发动机代码 
	//ProjNode registerData;//注册日期 
	//ProjNode issueData;//发证日期 
};

#endif //DRIVE_LICENSE_H
