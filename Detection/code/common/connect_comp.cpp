
#include "connect_comp.h"

connectComp::~connectComp()
{
}

connectComp::connectComp(Rect r1, Rect r2, double delta, int off)
{
    if (connected(r1, r2,delta,off)) {
        outter = start | end;
        inner = start & end;
    }else{
        start = end = Rect(0,0,0,0);
    }
}

bool connectComp::same(connectComp in)
{
    if (start == in.start && end == in.end)
    {
        return true;
    }
    return false;
}

bool connectComp::sharesame(connectComp in)
{
    if (start == in.start || end == in.end || start == in.end || end == in.start)
    {
        return true;
    }
    return false;
}

bool connectComp::empty(){
    if (start.area() ==0 || end.area() == 0) {
        return true;
    }
    return false;
}

bool connectComp::connected(Rect r1, Rect r2, double delta, int off)
{
    Rect t1= r1-Point(r1.x,0);
    Rect t2 = r2-Point(r2.x,0);
    Rect inter = t1 & t2;
//  Rect outer = t1 | t2;

    int minW = fmin(r1.width, r2.width);
    int maxW = fmax(r1.width, r2.width);
    int minH = fmin(r1.height, r2.height);
    int maxH = fmax(r1.height, r2.height);

    int offset =0;
    if ((((minH >= maxH*delta) || (minW >= maxW*delta)) && ((inter.height >= maxH*delta) || (inter.height == minH)))
		|| inter == t1 || inter == t2)
	{
        if (r1.x < r2.x) 
		{
            start = r1;
            end = r2;
        }
		else
		{
            start = r2;
            end = r1;
        }
        offset = end.x - start.br().x;
        if (offset <= off) 
		{
            return true;
        }
    }

    return false;
}
