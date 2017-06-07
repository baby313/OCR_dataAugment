#pragma once
#include "cv_common.h"
#include "cv_common_internal.h"
/// 图像格式定义
typedef struct cv_image_ex:cv_image {
    inline cv_image_ex():orientation(CV_ORIENTATION_0){}
    cv_orientation orientation;
} cv_image_ex;