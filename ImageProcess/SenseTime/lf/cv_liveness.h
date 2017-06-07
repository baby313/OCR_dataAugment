#ifndef INCLUDE_CVLIVENESS_API_CV_LIVENESS_H_
#define INCLUDE_CVLIVENESS_API_CV_LIVENESS_H_

#include "cv_common.h"

/// @defgroup cv_liveness_hackness cvliveness hackness
/// @brief liveness hackness definitions and interface
///
/// This set of interfinances processing liveness hackness detection.
///
/// @{

/// @brief 创建防hack检测句柄
/// @param[in] hackness_model 指定防hack模型
/// @param[out] hackness_handle 返回防hack句柄
/// @return 成功返回CV_OK, 否则返回错误码
CV_SDK_API
cv_result_t
cv_liveness_hackness_create(
	cv_model_t hackness_model,
	cv_handle_t* hackness_handle
);

/// @brief 销毁防hack句柄
/// @param[in] hackness_handle 待销毁的句柄
CV_SDK_API
void
cv_liveness_hackness_destroy(
	cv_handle_t hackness_handle
);

/// @brief 输入一帧图片,进行防hack检测
/// @param[in] hackness_handle 已初始化的句柄
/// @param[in] image 当前帧图片数据
/// @param[in] landmarks 当前帧关键点信息
/// @param[out] score 返回该帧得分,分数越大越可能是hack
/// @return 成功返回CV_OK, 否则返回错误码
CV_SDK_API
cv_result_t
cv_liveness_hackness_detect(
	cv_handle_t hackness_handle,
	const cv_image *image,
	const cv_landmarks_t *landmarks,
	float *score
);

/// @}

#endif  // INCLUDE_CVLIVENESS_API_CV_LIVENESS_H_
