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
	int DLtype;//��ʻ֤���� 
	vector<ProjLocale> vLocate;
	vector<ProjNode> vNode;
	
	//ProjNode title;//���� 
	//ProjNode NO;//���ƺ��� 
	//ProjNode vehicleType;//�������� 
	//ProjNode owner;//������ 
	//ProjNode address;//סַ 
	//ProjNode property;//ʹ�����ʣ���Ӫ�˵� 
	//ProjNode brand;//Ʒ���ͺ� 
	//ProjNode IDCode;//����ʶ����� 
	//ProjNode engineID;//���������� 
	//ProjNode registerData;//ע������ 
	//ProjNode issueData;//��֤���� 
};

#endif //DRIVE_LICENSE_H
