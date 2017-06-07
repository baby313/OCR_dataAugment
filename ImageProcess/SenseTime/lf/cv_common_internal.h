#ifndef STSDK_CVCOMMONINTERNAL_H_
#define STSDK_CVCOMMONINTERNAL_H_

#include "cv_common.h"

/// @addtogroup cv_common
/// @{

// ====================== feature ========================
/// @defgroup cv_feature cv feature
/// @brief feature processing internface for cv libs
/// @{

/// @brief 特征信息编码成字符串, 编码后的字符串用于保存
/// @param[in] feature 输入的特征信息
/// @param[in] feature_str 输出的编码后的字符串, 由用户分配和释放, 长度使用CV_ENCODE_FEATURE_SIZE(pf)获取
CV_SDK_API
cv_result_t
cv_feature_serialize(
	const cv_feature_t *feature,
	char *feature_str
);

/// @brief 解码字符串成特征信息
/// @param[in] feature_str 输入的待解码的字符串
/// @return 返回解码后的feature, 需要用户使用 cv_common_feature_release() 释放
CV_SDK_API
cv_feature_t *
cv_feature_deserialize(
	const char *feature_str
);

/// @brief 释放提取特征时分配的空间
/// @param[out] feature 提取到的特征信息
/// @return 成功返回CV_OK, 否则返回错误类型
CV_SDK_API
cv_result_t
cv_common_feature_release(
	cv_feature_t *feature
);

/// @brief 获取feature的raw data
/// @param[in] feature 输入的特征
/// @return 返回feature的raw data
CV_SDK_API
float*
cv_feature_rawdata(
	const cv_feature_t* feature
);
/// @}

// ====================== common detect =======================
/// @defgroup cv_detector cv detector
/// @brief common detector definitions and interface
/// @{

/// @brief 进行目标检测
/// @param[in] handle 已初始化的目标检测句柄
/// @param[in] image 用于检测的图像, 推荐BGR格式
/// @param[out] targets 检测到的目标信息数组, api负责分配内存
/// @param[out] scores 检测到的目标分值, api负责分配内存
/// @param[out] count 检测到的目标数量
/// @return 成功返回CV_OK
CV_SDK_API
cv_result_t
cv_common_detection_detect(
	cv_handle_t handle,
	const cv_image *image,
	cv_rect_t **targets,
	float **scores,
	int *count
);

/// @brief 获取目标检测阈值
/// @param[in] handle 已初始化的目标检测句柄
/// @param[out] threshold 输出检测阈值
/// @return 正常返回CV_OK, 否则返回错误类型
CV_SDK_API
cv_result_t
cv_common_detection_get_threshold(
	cv_handle_t handle,
	float *threshold
);

/// @brief 释放目标检测返回结果时分配的空间
/// @param[in] targets 检测到的目标数组
/// @param[in] scores 检测到的目标分值
/// @param[in] count 检测到的目标数量
CV_SDK_API
void
cv_common_detection_release_result(
	cv_rect_t *targets,
	float *scores,
	int count
);

/// @brief 销毁已初始化目标检测句柄
/// @param[in] handle 已初始化的目标检测句柄
CV_SDK_API
void
cv_common_detection_destroy(
	cv_handle_t handle
);

/// @}

// ====================== spider detect ========================
/// @defgroup cv_detector_spider cv spider detector
/// @brief spider detector definitions & interface
/// @{

/// @brief 创建spider模型目标检测句柄
/// @param[in] model 载入spider模型
/// @param[out] handle 输出spider句柄
/// @return 正常返回CV_OK, 否则返回错误类型
CV_SDK_API
cv_result_t
cv_common_detection_spider_create(
	cv_model_t model,
	cv_handle_t *handle
);

#define cv_common_detection_spider_detect		cv_common_detection_detect
#define cv_common_detection_spider_release_result	cv_common_detection_release_result
#define cv_common_detection_spider_get_threshold	cv_common_detection_get_threshold
#define cv_common_detection_spider_destroy		cv_common_detection_destroy

/// @}

// ====================== craft detect ========================
/// @defgroup cv_detector_craft cv craft detector
/// @brief craft detector definitions and interface
/// @{

/// @brief 创建craft模型目标检测句柄
/// @param[in] model 载入craft模型
/// @param[out] handle 输出craft句柄
/// @return 正常返回CV_OK, 否则返回错误类型
CV_SDK_API
cv_result_t
cv_common_detection_craft_create(
	cv_model_t model,
	cv_handle_t *handle
);

#define cv_common_detection_craft_detect		cv_common_detection_detect
#define cv_common_detection_craft_release_result	cv_common_detection_release_result
#define cv_common_detection_craft_get_threshold		cv_common_detection_get_threshold
#define cv_common_detection_craft_destroy		cv_common_detection_destroy

/// @}

// ====================== hunter detect ========================
/// @defgroup cv_detector_hunter cv hunter detector
/// @brief hunter detctor definitions and interface
/// @{

/// @brief 创建hunter模型目标检测句柄
/// @param[in] model 载入hunter模型
/// @param[out] p_hunter_handle 输出hunter句柄
/// @return 成功返回CV_OK, 否则返回错误代码
CV_SDK_API
cv_result_t
cv_common_detection_hunter_create(
	cv_model_t model,
	cv_handle_t *p_hunter_handle
);

#define cv_common_detection_hunter_detect			cv_common_detection_detect
#define cv_common_detection_hunter_detect_with_label		cv_common_detection_detect_with_label
#define cv_common_detection_hunter_release_result_with_label	cv_common_detection_release_result_with_label
#define cv_common_detection_hunter_release_result		cv_common_detection_release_result
#define cv_common_detection_hunter_get_threshold		cv_common_detection_get_threshold
#define cv_common_detection_hunter_destroy			cv_common_detection_destroy

/// @}

// ====================== alignemnt ========================
/// @defgroup cv_align_deep cv deep align
/// @brief deep align definitions and interface
/// @{

/// @brief 通过deep模型创建目标关键点检测句柄
/// @param[in] model 载入的deep模型
/// @param[out] handle 输出deep alignment句柄
/// @return 成功返回CV_OK
CV_SDK_API
cv_result_t
cv_common_alignment_deep_create(
	cv_model_t model,
	cv_handle_t *handle
);

/// @brief 获取模型支持的关键点数
/// @param [in] handle 已初始化的目标关键点检测句柄
/// @return 返回关键点数. 如果出现错误则返回-1(例如传入参数为NULL)
CV_SDK_API
cv_result_t
cv_common_alignment_get_points_count(
	cv_handle_t handle,
	int *count
);

/// @brief 获取模型输入关键点数
/// @param [in] handle 已初始化的目标关键点检测句柄
/// @return 返回关键点数. 如果出现错误则返回-1(例如传入参数为NULL)
CV_SDK_API
cv_result_t
cv_common_alignment_get_input_points_count(
	cv_handle_t align_handle,
	int *count
);

/// @brief 通过deep模型进行面部关键点检测
/// @param[in] handle 已初始化的目标关键点检测句柄
/// @param[in] image 用于配准的图像, 推荐灰度格式
/// @param[in] rect 输入的目标面部矩形区域
/// @param[out] output_points_array 检测到的关键点坐标
/// @param[out] output_points_count 目标的关键点数, 由模型决定是21p还是106p
/// @param[out] score 检测到的关键点置信度
/// @return 正常返回CV_OK, 否则返回错误类型
CV_SDK_API
cv_result_t
cv_common_alignment_align_by_rect(
	cv_handle_t handle,
	const cv_image *image,
	cv_rect_t rect,
	cv_pointf_t **output_points_array,
	int *output_points_count,
	float *score
);

/// @brief 释放目标关键点检测返回结果时分配的空间
/// @param [in] points_array 检测到的目标关键点
/// @param [in] points_count 检测到的目标关键点数量
CV_SDK_API
void
cv_common_alignment_release_result(
	cv_pointf_t *points_array,
	int points_count
);

/// @brief 销毁已初始化的simple模型目标关键点检测句柄
/// @param [in] handle 已初始化的目标关键点检测句柄
CV_SDK_API
void cv_common_alignment_destroy(
	cv_handle_t handle
);

#define cv_common_alignment_deep_get_points_count	cv_common_alignment_get_points_count
#define cv_common_alignment_deep_get_mean_pose		cv_common_alignment_get_mean_pose
#define cv_common_alignment_deep_align_by_rect		cv_common_alignment_align_by_rect
#define cv_common_alignment_deep_align_by_pose		cv_common_alignment_align_by_pose
#define cv_common_alignment_deep_release_result		cv_common_alignment_release_result
#define cv_common_alignment_deep_destroy		cv_common_alignment_destroy

#define cv_common_alignment_simple_get_points_count	cv_common_alignment_get_points_count
#define cv_common_alignment_simple_get_mean_pose	cv_common_alignment_get_mean_pose
#define cv_common_alignment_simple_align_by_rect	cv_common_alignment_align_by_rect
#define cv_common_alignment_simple_align_by_pose	cv_common_alignment_align_by_pose
#define cv_common_alignment_simple_release_result	cv_common_alignment_release_result
#define cv_common_alignment_simple_destroy		cv_common_alignment_destroy

/// @}

// ==================== align based track ========================
/// @defgroup cv_track_landmark cv landmark tracker
/// @brief landmark tracker definitions and interface
/// @{

/// @}

// ==================== random dewatermark ========================
/// @defgroup cv_demask cv dewatermark
/// @brief dewatermark definitions and interface
/// @{

/// @brief 通过rand模型创建去水印句柄
/// @param[in] model 已初始化的rand模型
/// @param[out] handle 已初始化的去水印句柄所在的地址
/// @return 成功返回CV_OK, 否则返回错误码
CV_SDK_API cv_result_t
cv_common_dewatermark_rand_create(
	cv_model_t model,
	cv_handle_t *handle
);

/// @brief 通过rand模型去水印
/// @param[in] handle 已初始化的去水印句柄
/// @param[in] input_image 待去水印的图片, 不支持灰度图像, 推荐BGR格式
/// @param[out] output_image 去除水印后的图片
/// @return 正常返回CV_OK, 否则返回错误类型
CV_SDK_API cv_result_t
cv_common_dewatermark_rand_wipe(
	cv_handle_t handle,
	const cv_image* input_image,
	cv_image* output_image
);

/// @brief 销毁已初始化的rand模型去水印句柄
/// @param[in] handle 已初始化的去水印句柄
CV_SDK_API void
cv_common_dewatermark_rand_destroy(
	cv_handle_t handle
);

/// @}

// ======================= feature extractor =======================
/// @defgroup cv_feature_extractor cv feature extractor
/// @brief feature extractor definitions and interface
/// @{

/// @brief 创建特征提取句柄
/// @param[in] model 载入特征模型
/// @param[out] handle 保存输出的特征提取句柄
/// @return 正常返回CV_OK, 否则返回错误类型
CV_SDK_API
cv_result_t
cv_common_feature_extractor_create(
	cv_model_t model,
	cv_handle_t* handle
);

/// @brief 创建特征提取句柄的副本, 与旧的句柄共享内存, 可用于多线程调用
/// @param[in] old_handle 旧的特征验证句柄, 新句柄释放后才能释放旧句柄
/// @param[out] new_handle 保存输出的新的特征验证句柄
/// @return 正常返回CV_OK, 否则返回错误类型
CV_SDK_API
cv_result_t
cv_common_feature_extractor_duplicate(
	cv_handle_t old_handle,
	cv_handle_t* new_handle
);

/// @brief 销毁已初始化的特征提取句柄
/// @param[in] handle 已初始化的特征提取句柄
/// @return 正常返回CV_OK, 否则返回错误类型
CV_SDK_API
cv_result_t
cv_common_feature_extractor_destroy(
	cv_handle_t handle
);

/// @brief 获取当前特征提取使用的模型版本号
/// @param[in] handle 已初始化的特征提取句柄
/// @param[out] ver 保存输出的模型版本号
/// @return 正常返回CV_OK, 否则返回错误类型
CV_SDK_API
cv_result_t
cv_common_feature_extractor_get_version(
	cv_handle_t handle,
	int* ver
);

/// @brief 提取特征
/// @param[in] handle 已初始化的特征提取句柄
/// @param[in] image 输入的图像, 推荐图像格式BGR888
/// @param[out] feature 保存输出的特征, 需要用户使用cv_common_feature_release释放
/// @return 正常返回CV_OK, 否则返回错误类型
CV_SDK_API
cv_result_t
cv_common_feature_extractor_extract(
	cv_handle_t handle,
	const cv_image *image,
	cv_feature_t** feature
);

/// @brief 获取当前handle处理后提取的feature长度
/// @param[in] handle 已初始化的特征提取句柄
/// @param[out] len 保存输出的当前handle提取的feature长度
/// @return 成功返回CV_OK, 否则返回错误类型
CV_SDK_API
cv_result_t
cv_common_feature_extractor_get_length(
	cv_handle_t handle,
	int* len
);

/// @}

// ==================== feature comparator ========================
/// @defgroup cv_feature_comparator cv compare feature
/// @brief feature comparator definitions and interface
/// @{

/// @brief 创建特征比较句柄
/// @param[in] model 载入特征比较模型
/// @param[out] handle 保存输出的特征比较句柄
/// @return 正常返回CV_OK, 否则返回错误类型
CV_SDK_API
cv_result_t
cv_common_feature_comparator_create(
	cv_model_t model,
	cv_handle_t* handle
);

/// @brief 销毁已初始化的特征比较句柄
/// @param[in] handle 已初始化的特征比较句柄
CV_SDK_API
void cv_common_feature_comparator_destroy(
	cv_handle_t handle
);

/// @brief 根据模型归一化参数将特征相似度得分归一化
/// @param[in] handle 已初始化的特征比较句柄
/// @param[in] original_score 原始相似度得分
/// @param[out] normalized_score 归一化后的相似度得分
/// @return 成功返回CV_OK, 否则返回错误类型
CV_SDK_API
cv_result_t
cv_common_feature_comparator_normalize_score_by_model(
	cv_handle_t handle,
	float original_score,
	float *normalized_score
);

/// @brief 对提取的feature执行归一化
/// @param[in,out] feature 待归一化处理的feature
/// @return 成功返回CV_OK, 否则返回错误类型
CV_SDK_API
cv_result_t
cv_common_feature_comparator_normalize(
	cv_feature_t *feature
);

/// @brief 计算两个特征的相似度
/// @param[in] feature1 第一张特征信息
/// @param[in] feature2 第二张特征信息
/// @param[out] score 特征验证相似度得分, 得分越大相似度越高
/// @return 成功返回CV_OK, 否则返回错误类型
CV_SDK_API
cv_result_t
cv_common_feature_comparator_get_distance(
	const cv_feature_t* feature1,
	const cv_feature_t* feature2,
	float* score
);

/// @brief 根据模型归一化参数将特征相似度得分归一化
/// @param[in] threshold_src 归一化源节点参数
/// @param[in] threshold_dst 归一化目标节点参数
/// @param[in] len 归一化参数数组长度
/// @param[in] original_score 原始相似度得分
/// @param[out] normalized_score 归一化后的相似度得分
/// @return 成功返回CV_OK, 否则返回错误类型
CV_SDK_API
cv_result_t
cv_common_feature_comparator_normalize_score_by_threshold(
	const float* threshold_src,
	const float* threshold_dst,
	const int len,
	float original_score,
	float *normalized_score
);
/// @}

// ===============================  search brute force  ===========================
/// @defgroup cv_search_brute cv brute search
/// @brief brute search definitions and interface
/// @{

/// @brief 从一组特征数组中搜索最近的若干特征
/// @param[in] handle 已初始化的特征比较句柄
/// @param[in] list_feature 特征信息数组
/// @param[in] list_count 特征信息数量
/// @param[in] query 待搜索的特征信息
/// @param[in] top_k 最大的特征搜索数量
/// @param[out] top_idxs 搜索到的特征数据库索引值数组(由用户分配和释放)
/// @param[out] top_scores 搜索到的特征相似度得分数组(由用户分配和释放), 范围0-1, 得分越接近1越相似
/// @param[out] result_length 实际搜索到的特征数量
/// @return 成功返回CV_OK, 否则返回错误类型
/// @note 返回的结果以1作为起始索引
CV_SDK_API
cv_result_t
cv_common_search_bruteforce_search(
	cv_handle_t handle,
	cv_feature_t* const *list_feature,
	int list_count,
	const cv_feature_t *query,
	unsigned int top_k,
	int *top_idxs,
	float *top_scores,
	unsigned int *result_length
);

/// @}

// ========================== tracking =============================
/// @defgroup cv_track_landmark cv landmark tracker
/// @brief landmark tracker definitions and interface
/// @{

#define CV_COMMON_RESIZE_IMG_320W	0x00000002  ///< resize图像为长边320的图像
#define CV_COMMON_RESIZE_IMG_640W	0x00000004  ///< resize图像为长边640的图像
#define CV_COMMON_RESIZE_IMG_1280W	0x00000008  ///< resize图像为长边1280的图像

/// @brief 图片目标朝向信息
typedef enum {
	CV_ORIENTATION_0   = 0,	///< 不做旋转预处理
	CV_ORIENTATION_90  = 1,	///< 预处理图像, 将输入图像顺时针旋转90度, 再执行后续操作
	CV_ORIENTATION_180 = 2,	///< 预处理图像, 将输入图像顺时针旋转180度, 再执行后续操作
	CV_ORIENTATION_270 = 3,	///< 预处理图像, 将输入图像顺时针旋转270度, 再执行后续操作
} cv_orientation;

/// @brief 指定采用双线程tracking, 并采用默认模式(fixed sample rate)
#define CV_COMMON_TRACKING_ASYNC   		0x00010000

/// @brief 在双线程tracking下, 采用detect deadline模式
#define CV_COMMON_TRACKING_ASYNC_DETECTDEADLINE 0x00100000

/// @brief 创建实时目标跟踪句柄, 目标的ID会增加, 但其并非连续的
/// @param [in] model: 用于alignment的模型, 21点还是106点tracking由该模型决定
/// @param [in] detector: tracker内部需要使用的detector, 该detector必须在tracker被释放后释放
/// @param [in] config: 配置选项, 例如 CV_COMMON_TRACKING_ASYNC | CV_COMMON_RESIZE_IMG_320W | CV_COMMON_TRACKING_ASYNC_DETECTDEADLINE
/// @param [out] p_handle 用于存储返回的tracker句柄指针
/// @return 成功返回CV_OK, 否则返回错误码
CV_SDK_API
cv_result_t
cv_common_tracking_compact_create(
	cv_model_t model,
	cv_handle_t detector,
	unsigned int config,
	cv_handle_t* p_handle
);

/// @brief 销毁已初始化的实时目标跟踪句柄
/// @param [in] handle 已初始化的实时目标跟踪句柄
CV_SDK_API
void
cv_common_tracking_compact_destroy(
	cv_handle_t handle
);

///@brief 设置检测到的最大目标数目N, 持续track已检测到的N个目标直到目标数小于N再继续做detect. 设置为1即是单脸跟踪
///       有效范围为[1, -), 返回的值可能比输入的值要小
#define CV_COMMON_TRACKING_CONF_LIMIT                           0x0001

///@brief 对于设置每多少帧进行一次detect。
///       对于单线程, 有效范围[1, -)；
///       对于双线程, 有效值为[0, -) （0表示"catch up"后立即开始下一次detect）
#define CV_COMMON_TRACKING_CONF_DETECTINTERVAL             0x0002

///@brief 设置双线程tracking的默认模式(fixed sample)下的sample rate, 有效范围[1, -), 默认值为2
#define CV_COMMON_TRACKING_CONF_ASYNC_DEFAULT_SAMPLERATE        0x0003

///@brief 设置双线程tracking的detect deadline模式中, 最多可以接受每隔多长时间进行一次detect(单位:ms), 默认值为2000
///     有效值为 (0, -)
#define CV_COMMON_TRACKING_CONF_ASYNC_DETECTDEADLINE_DURATION   0x0004

/// @brief (不推荐直接设置) 设置双线程tracker在detect deadline模式中, 可以接受的冗余量(单位: %1), 默认值为90
#define CV_COMMON_TRACKING_CONF_ASYNC_DETECTDEADLINE_TOLERANCE 0x0005

/// @brief 设置双线程tracker的message queue的最大长度. 在detect与摄像头驱动帧率差距较大的情况下，该值可能会影响运行时消耗内存大小
#define CV_COMMON_TRACKING_CONF_ASYNC_MSGQUEUE_SIZE 0x0006

/// @brief 自定义alignment的threshold 单位为0.001， 例如设置为550表示阈值为0.55
#define CV_COMMON_TRACKING_CONF_THRESHOLD                    0x0007

/// @brief 对Tracking handle进行配置i, 该函数必须在tracking开始前调用
/// @note 对于下列参数, 支持在运行时动态调整, 其他参数必须在第一次track开始前设置
///           CV_COMMON_TRACKING_CONF_DETECTINTERVAL
/// @param [in] handle 跟踪句柄
/// @param [in] config 具体要配置的属性ID, 见上
/// @param [in] val 要设置的新的值,人脸跟踪最大数量为32
/// @param [out] new_val 如果为非空指针, 则返回采用的新的值, 注意由于内部的限制, 实际采用的值并不一定等于val. 例如(CV_COMMON_TRACKING_CONF_LIMIT)
/// @return 成功返回CV_OK, 错误则返回错误码
CV_SDK_API
cv_result_t cv_common_tracking_compact_config(
	cv_handle_t handle,
	unsigned int config,
	int val,
	int* new_val
);

/// @brief 对连续视频帧进行实时快速目标跟踪
/// @param [in] handle 已初始化的实时目标跟踪句柄
/// @param [in] p_image 用于检测的图像数据
/// @param [in] orientation 视频中目标的方向
/// @param [out] p_targets_array 检测到的目标信息数组, api负责分配内存, 需要调用 cv_common_tracking_compact_release_result() 函数释放
/// @param [out] p_targets_count 检测到的目标数量, 0表示没有检测到目标()
/// @return 成功返回CV_OK, 否则返回错误类型
/// @note 如果采用的是双线程detect deadline模型, 要求image中设置有效的时间戳, 且精度在ms级的精度。避免采用clock_t clock()函数获得时间戳, 该函数在多线程程序下无效
CV_SDK_API
cv_result_t
cv_common_tracking_compact_track(
	cv_handle_t handle,
	const cv_image* p_image,
	cv_orientation orientation,
	cv_target_t **p_targets_array,
	int *p_targets_count
);

/// @brief 重置目标跟踪
/// @param [in] handle 已初始化的实时目标跟踪句柄
CV_SDK_API
void
cv_common_tracking_compact_reset(
	cv_handle_t handle
);

/// @brief 释放实时目标跟踪返回结果时分配的空间
/// @param [in] target_array 检测到的目标信息数组
/// @param [in] target_count 检测到的目标数量
CV_SDK_API
void
cv_common_tracking_compact_release_result(
	cv_target_t *target_array,
	int target_count
);

/// @}

#endif  // INCLUDE_CV_INTERNAL_H_
