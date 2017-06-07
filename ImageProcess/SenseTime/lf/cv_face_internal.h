#ifndef INCLUDE_CVFACE_API_CV_FACE_INTERNAL_H_
#define INCLUDE_CVFACE_API_CV_FACE_INTERNAL_H_

#include "cv_common.h"
#include "cv_common_internal.h"

#define CV_E_INVALID_POINTS_COUNT	0x101 ///< 输入的点数无效
#define CV_E_INVALID_MODEL		0x102 ///< 无效的model文件
#define CV_E_INVALIDARG_MODEL		0x103 ///< model句柄指针为空
#define CV_E_INVALID_MODEL_CONFIG	0x104 ///< model的名字与要求的不符
//#define CV_E_INVALID_MODEL_FILE		0x105 ///< model中缺少文件
#define CV_E_INVALID_MODEL_FILE		-8 ///< model中缺少文件 为了和sdk_common兼容
#define CV_E_FAIL_ALGORITHM		0x106 ///< 算法内部错误
#define CV_E_INVALID_WATERMARK_IMAGE 0x107 ///< 不是有效的watermarked图片

/// @addtogroup cv_common
/// @{

// ====================== calc pose ========================
/// @defgroup cv_calcpose cv calcpose
/// @brief head_pose calculator definitions and interface
/// @{

/// @brief 创建head pose计算句柄
/// @param [in] model 载入AnnHeadPose模型
/// @param [out] handle 返回的创建好的句柄指针
/// @return 成功返回CV_OK, 否则返回错误码
CV_SDK_API
cv_result_t
cv_face_calcpose_ann_create(
	cv_model_t model,
	cv_handle_t *handle
);

/// @brief 通过关键点位置确定人脸三维旋转角度和两眼球距离，先计算roll角度，后计算yaw和pitch
/// @param [in] handle 已初始化的head pose计算句柄
/// @param [in] points_array 输入的人脸关键点坐标
/// @param [in] points_count 输入的人脸关键点个数, 现支持21点和106点
/// @param [out] yaw 水平角角度, 真实度量的左负右正，范围-90°,90°
/// @param [out] pitch 俯仰角角度, 真实度量的上负下正，范围-90°,90°
/// @param [out] roll 旋转角, 真实度量的左负右正，范围-180°,180°
/// @param [out] eye_dist 两眼间距
/// @return 正常返回CV_OK, 否则返回错误类型
CV_SDK_API
cv_result_t
cv_face_calcpose_ann_pose(
	cv_handle_t handle,
	const cv_pointf_t *points_array,
	int points_count,
	float *yaw, float *pitch, float *roll,
	float *eye_dist
);

/// @brief 销毁已初始化的AnnHeadPose模型
/// @param [in] handle 已初始化的head pose计算句柄
CV_SDK_API
void
cv_face_calcpose_ann_destroy(
	cv_handle_t handle
);

/// @}

//========================= utils =============================
/// @defgroup cv_utils cv utils
/// @brief utils definitions and interface
/// @{

/// @brief 通过关键点位置来确定人脸面部矩形区域
/// @param [in] points_array 输入的人脸关键点坐标
/// @param [in] points_count 输入的人脸关键点个数, 现支持21点和106点
/// @param [out] rect 得到人脸面部矩形区域
CV_SDK_API
cv_result_t
cv_face_utils_points_to_rect(
	const cv_pointf_t *points_array,
	int points_count,
	cv_rect_t *rect
);

/// @}

//=================== face feautre extractor ======================
/// @defgroup cv_face_feature cv face feature extractor
/// @brief face feature extractor definitions and interface
/// @{

#define cv_face_feature_extractor_create cv_common_feature_extractor_create

#define cv_face_feature_extractor_duplicate cv_common_feature_extractor_duplicate

#define cv_face_feature_extractor_get_version cv_common_feature_extractor_get_version

#define cv_face_feature_extractor_get_length cv_common_feature_extractor_get_length

#define cv_face_feature_extractor_destroy cv_common_feature_extractor_destroy

/// @brief 通过关键点位置提取人脸面部特征信息
/// @param [in] handle 由 cv_face_feature_extractore_create() 创建的句柄
/// @param [in] input_image 包含人脸的输入图像
/// @param [in] points_array 输入的人脸关键点坐标
/// @param [in] points_count 输入的人脸关键点个数, 现支持21点和106点
/// @param [out] feautre 得到人脸面部特征信息结构体, 需要使用 cv_common_feature_release() 释放
/// @return 正确执行返回CV_OK, 否则返回错误码
CV_SDK_API
cv_result_t
cv_face_feature_extractor_extract(
	cv_handle_t handle,
	const cv_image* input_image,
	const cv_pointf_t* points_array,
	int points_count,
	cv_feature_t** feature
);

/// @}

// ==================== pattern watermark ========================
/// @defgroup cv_demask_pattern cv dewatermark pattern
/// @brief dewatermark pattern definitions and interface
/// @{

/// @brief 通过pattern模型创建去水印句柄
/// @param [in] model 载入pattern模型
/// @param [out] handle 输出已初始化的去水印句柄地址
/// @return 成功返回CV_OK, 否则返回错误码
CV_SDK_API
cv_result_t
cv_face_watermark_pattern_create(
	cv_model_t model,
	cv_handle_t* handle
);

/// @brief 通过pattern模型去水印
/// @param [in] handle 已初始化的pattern去水印句柄
/// @param [in] input_image 用于待去水印的输入图像,推荐的图像格式：CV_PIX_FMT_BGR888
/// @param [out] output_image 去完水印后的输出图像数据
/// @return 成功返回CV_OK, 否则返回错误码
CV_SDK_API
cv_result_t
cv_face_watermark_pattern_remove(
	cv_handle_t handle,
	const cv_image* input_image,
	cv_image* output_image
);

/// @brief 销毁已初始化的pattern模型去水印句柄
/// @param [in] handle 已初始化的pattern去水印句柄
CV_SDK_API
void
cv_face_watermark_pattern_destroy(
	cv_handle_t handle
);

/// @}

#endif  // INCLUDE_CVFACE_API_CV_FACE_INTERNAL_H_
