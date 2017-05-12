//////////////////////////////////////////////////////////////////////////

#include <fstream> 
#include <iostream> 

using namespace std;

#include "drive_license.h"
#include "json/json.h"


DriveLicense::DriveLicense()
{
}


DriveLicense::~DriveLicense()
{
}

int DriveLicense::init(string tempFile)
{
	int res = readTemplate(tempFile);
	return res;
}

int DriveLicense::readTemplate(string tempFile)
{
	Json::Reader jsonReader;
	Json::Value jsonRoot;
	Json::Value jsonValue;
	std::ifstream inFile;
	inFile.open(tempFile, std::ios::binary);

	if (jsonReader.parse(inFile, jsonRoot))
	{
		//type 
		DLtype = jsonRoot["type"].asInt();

		//get locate mark
		int locCount = jsonRoot["locate"].size();
		for (int i = 0; i < locCount; i++)
		{
			ProjLocate lc;
			lc.key = jsonRoot["locate"][i]["label"].asString();
			lc.rc.x = jsonRoot["locate"][i]["x"].asInt();
			lc.rc.y = jsonRoot["locate"][i]["y"].asInt();
			lc.rc.width = jsonRoot["locate"][i]["w"].asInt();
			lc.rc.height = jsonRoot["locate"][i]["h"].asInt();
			vLocate.push_back(lc);
		}

		//get node infomation
		int nodeCount = jsonRoot["node"].size();
		for (int i = 0; i < nodeCount; i++)
		{
			ProjNode nod;
			nod.key = jsonRoot["node"][i]["label"].asString();
			nod.rc.x = jsonRoot["node"][i]["x"].asInt();
			nod.rc.y = jsonRoot["node"][i]["y"].asInt();
			nod.rc.width = jsonRoot["node"][i]["w"].asInt();
			nod.rc.height = jsonRoot["node"][i]["h"].asInt();
			vNode.push_back(nod);
		}

		inFile.close();
		return 0;
	}
	return 1;
}