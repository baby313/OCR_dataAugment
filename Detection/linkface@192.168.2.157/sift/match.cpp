
#include "sift.h"
#include "imgfeatures.h"
#include "kdtree.h"
#include "utils.h"
#include "xform.h"
#include "../common/common.h"
#include "match.h"

#ifdef _WIN32
#include "io.h"
#include "direct.h"
#else
#include <sys/stat.h>
#include <dirent.h>
#include<unistd.h>
#endif
#include <stdio.h>

#include <vector>
#include <string>

using namespace std;

/* the maximum number of keypoint NN candidates to check during BBF search */
#define KDTREE_BBF_MAX_NN_CHKS 200

/* threshold on squared ratio of distances between NN and 2nd NN */
#define NN_SQ_DIST_RATIO_THR 0.4

void sift_calc(IplImage *imgS, IplImage *imgB, vector<Point>& vpt_start, vector<Point>& vpt_end)
{
	struct feature* feat1, *feat2, *feat;
	struct feature** nbrs = nullptr;
	struct kd_node* kd_root;
	CvPoint pt1, pt2;
	double d0, d1;
	int n1, n2, k, i, m = 0;

	//fprintf(stderr, "Finding features in %s...\n", argv[1]);
	n1 = sift_features(imgS, &feat1);
	//fprintf(stderr, "Finding features in %s...\n", argv[2]);
	n2 = sift_features(imgB, &feat2);
	//fprintf(stderr, "Building kd tree...\n");
	kd_root = kdtree_build(feat2, n2);
	for (i = 0; i < n1; i++)
	{
		feat = feat1 + i;
		k = kdtree_bbf_knn(kd_root, feat, 2, &nbrs, KDTREE_BBF_MAX_NN_CHKS);
		if (k == 2)
		{
			d0 = descr_dist_sq(feat, nbrs[0]);
			d1 = descr_dist_sq(feat, nbrs[1]);
			if (d0 < d1 * NN_SQ_DIST_RATIO_THR)
			{
				pt1 = cvPoint(cvRound(feat->x), cvRound(feat->y));
				vpt_start.push_back(pt1);
				pt2 = cvPoint(cvRound(nbrs[0]->x), cvRound(nbrs[0]->y));
				vpt_end.push_back(pt2);
				m++;
				feat1[i].fwd_match = nbrs[0];
			}
		}
		free(nbrs);
	}

	kdtree_release(kd_root);
	free(feat1);
	free(feat2);
}
