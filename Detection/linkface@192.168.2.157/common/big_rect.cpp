
#include "big_rect.h"

BigRect::BigRect()
{
    rc = Rect(0,0,0,0);
}

BigRect::BigRect(Rect rect, vector<Rect> subrec)
{
	rc = rect;
	vSubRc.clear();
	for (int i = 0; i<subrec.size(); i++) {
		Rect tmp = subrec[i];
		if ((tmp & rc) == tmp)
		{
			tmp.y = rc.y;
			tmp.height = rc.height;
			vSubRc.push_back(tmp);
		}
	}
	if (vSubRc.size() >0) {
		/*HJUtil::*/sortRectsByArea(vSubRc);
		/*HJUtil::*/mergeRects(vSubRc);
		/*HJUtil::*/sortRectsByX(vSubRc);
		this->mergeSubRects();
	}
}

BigRect::~BigRect()
{

}

bool BigRect::sortbyX(const Rect r1, const Rect r2) {
	return r1.x < r2.x;
}


void BigRect::sortRectsByX(vector<Rect> &recs)
{
	if (recs.size() > 0) {
		sort(recs.begin(), recs.end(), sortbyX);
	}
}

bool BigRect::sortbyArea(const Rect r1, const Rect r2) {
	return r1.area() > r2.area();
}

void BigRect::sortRectsByArea(vector<Rect> &recs)
{
	if (recs.size() > 0) {
		sort(recs.begin(), recs.end(), sortbyArea);
	}
}

void BigRect::mergeRects(vector<Rect>  &zone)
{
	vector<Rect>  ret;
	vector<Rect>  remain;
	vector<Rect>  tmpremain;

	sort(zone.begin(), zone.end(), sortbyArea);
	Rect tmp;
	remain = zone;
	while (remain.size() > 0) {
		tmp = remain[0];
		tmpremain.clear();
		for (int j = 1; j < remain.size(); j++) {
			Rect rec = remain[j];
			Rect inter = tmp & rec;
			Rect outer = tmp | rec;
			if (inter == tmp || inter == rec){
				tmp = outer;
			}
			else{
				tmpremain.push_back(rec);
			}
		}
		ret.push_back(tmp);
		remain = tmpremain;
	}
	zone = ret;
}

void BigRect::split(int offset)
{
    vector<Rect> tmp;
    for (vector<Rect>::iterator it=vSubRc.begin(); it!= vSubRc.end(); it++) {
        Rect rec = Rect(it->tl(), it->size());
        if ((double)it->width > it->height +offset) {
            rec.width = (it->width)/2+1;
            tmp.push_back(rec);
            rec.x = it->x + (it->width)/2;
            tmp.push_back(rec);
        }else
        {
            tmp.push_back(rec);
        }
    }
    vSubRc = tmp;
}


void BigRect::adjustWidth(int width)
{
    vector<Rect> tmp;
    for (vector<Rect>::iterator it=vSubRc.begin(); it!= vSubRc.end(); it++) {
        Rect rec = Rect(it->tl(), it->size());
        if (it->width <width) {
            rec.width =width;
        }
        tmp.push_back(rec);
    }
    vSubRc = tmp;
}

void BigRect::eraseByIndex(int index)
{
    int cnt=0;
    for (vector<Rect>::iterator it=vSubRc.begin(); it!= vSubRc.end(); it++) {
        if (cnt == index) {
            vSubRc.erase(it);
            break;
        }
        cnt++;
    }
}

void BigRect::eraseIntersect()
{
    vector<Rect> tmp;

    for (vector<Rect>::iterator itfirst=vSubRc.begin(); itfirst!= vSubRc.end(); itfirst++) {
        int cnt=0;
        for (vector<Rect>::iterator it=vSubRc.begin(); it!= vSubRc.end(); it++) {
            if (itfirst == it) {
                continue;
            }
            Rect inter=(*itfirst)&(*it);
            if (inter.area() > 0) {
                cnt++;
            }
        }
        if (cnt<=1) {
            tmp.push_back(*itfirst);
        }
    }
    vSubRc=tmp;
}

void BigRect::eraseByRatio(double ratio)
{
    for (vector<Rect>::iterator it=vSubRc.begin(); it!= vSubRc.end(); ) {
        if ((double)it->width/it->height < 0.5) {
            it = vSubRc.erase(it);
        }else
            it++;
    }
}

void BigRect::adjustOffset(int offset)
{
    int preX= vSubRc[0].br().x;
    for (int i=1; i< vSubRc.size(); i++) {
        Rect rec = vSubRc[i];
        int delta = rec.x - preX;
        if (delta > offset ) {
            rec.width = rec.br().x-preX-offset;
            rec.x = preX+offset;
        }
        vSubRc[i] = rec;
        preX=vSubRc[i].br().x;
    }
}

void BigRect::filterSubRects(Rect tmp)
{
    for (vector<Rect>::iterator it = vSubRc.begin(); it != vSubRc.end(); ) {
        Rect inter = *it & tmp;
        if (inter.area() > 0) {
            it = vSubRc.erase(it);
        }else{
            it++;
        }
    }
    /*HJUtil::*/sortRectsByX(vSubRc);
    // reform outter rec
    rc = Rect(0,0,0,0);
    for (vector<Rect>::iterator it = vSubRc.begin(); it != vSubRc.end(); it++) {
        Rect inter = *it;
        if (rc.area() == 0) {
            rc = inter;
        }else{
            rc |= *it;
        }
    }

}

void BigRect::mergeSubRects(double ratio, int offset)
{
    vector<Rect> ret;
    /*HJUtil::*/sortRectsByX(vSubRc);
    // filter the rects already more than ratio
    for (vector<Rect>::iterator it = vSubRc.begin(); it != vSubRc.end(); ) {
        double Rt = (double)it->width/it->height;
        if (Rt >= ratio) {
            ret.push_back(*it);
            it = vSubRc.erase(it);
        }else{
            it++;
        }
    }

    if (vSubRc.size()>=2) {
        for (int i=0; i< vSubRc.size()-1; i++) {
            Rect first = vSubRc[i];
            Rect second = vSubRc[i+1];
            if ((second.x-first.br().x) < offset) {
                Rect outer = first | second;
                double Rt = (double)outer.width/outer.height;
                if (Rt >= ratio){
                    ret.push_back(outer);
                    i++;
                }else{
                    vSubRc[i+1] = outer;
                }
            }
        }
    }

        for (int i=0; i< vSubRc.size(); i++) {
            Rect first = vSubRc[i];
			if (first.width >=5) {
			ret.push_back(first);
			}
        }

    mergeRects(ret);
    vSubRc = ret;
    sortRectsByX(vSubRc);
}
