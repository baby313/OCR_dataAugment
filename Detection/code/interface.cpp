#include "interface.h"

PyObject* textCrop(const char* loc, const char* tem, const char* img )
{
	LF::OCR ooo(loc, tem);
	vector<int> vrc;
	ooo.textCrop(img, vrc);
	PyObject* res = PyList_New(vrc.size());
	for(int i = 0 ; i < vrc.size(); i++)
	{
		PyList_SetItem(res, i, Py_BuildValue("i", vrc[i]));
	}
	return res;
}

PyObject* test(const char* loc, const char*tem, const char* pathJson, const char* pathImg)
{
	printf("%s", loc);
	printf("%s", tem);
	printf("%s", pathJson);
	printf("%s", pathImg);
	LF::OCR ooo(loc, tem);
	vector<double> vdA;
	ooo.testDetectAccuracy(pathJson, pathImg, vdA);
	PyObject* res = PyList_New(vdA.size() + 1);
	for(int i = 0 ; i < vdA.size(); i++)
	{
		PyList_SetItem(res, i, Py_BuildValue("i", vdA[i]));
	}
	return res;
}

