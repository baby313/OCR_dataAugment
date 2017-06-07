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

