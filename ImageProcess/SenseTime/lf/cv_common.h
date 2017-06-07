#ifndef CV_COMMON_H_
#define CV_COMMON_H_

#include "cv_utils.h"

#ifdef __cplusplus
#	define CV_SDK_API extern "C" CV_SDK_API_
#else
#	define CV_SDK_API CV_SDK_API_
#endif

/// cv handle declearation
typedef void *cv_handle_t;

/// cv result declearation
typedef cv_errcode cv_result_t;

/// cv rectangle definition
typedef struct cv_rect_t {
	int left;	///< 矩形最左边的坐标
	int top;	///< 矩形最上边的坐标
	int right;	///< 矩形最右边的坐标
	int bottom;	///< 矩形最下边的坐标
} cv_rect_t;

/// cv float type point definition
typedef struct cv_pointf_t {
	float x;	///< 点的水平方向坐标, 为浮点数
	float y;	///< 点的竖直方向坐标, 为浮点数
} cv_pointf_t;

/// cv landmark array struct
typedef struct cv_landmarks_t {
	cv_pointf_t *points_array;
	int points_count;
} cv_landmarks_t;

/// @brief 关键点跟踪结果结构体
typedef  struct cv_target_t {
	cv_rect_t rect;			///< 代表面部的矩形区域
	cv_pointf_t *points_array;	///< 目标关键点坐标
	int points_count;		///< 目标关键点长度
	float score;			///< 目标置信度
	int id;				///< 目标ID, 用于表示在目标跟踪中的相同目标在不同帧多次出现
} cv_target_t;

typedef struct cv_feature_header_t {
	int ver;		///< 版本信息
	int idx;		///< 数组下标索引
	int len;		///< CV_FEATURE全部内容的长度, 包括feature_header和特征数组, 按字节计算, 与sizeof(cv_feature_header_t)定义不同
} cv_feature_header_t;

/// @brief 特征格式定义
typedef struct cv_feature_t {
	int ver;	///< 特征版对应模型本号
	int idx;	///< 特征索引序号
	int len;	///< CV_FEATURE全部内容的长度, 包括feature_header和特征数组, 按字节计算, 与sizeof(cv_feature_header_t)定义不同
	float feat[0];	///< 特征数组
} cv_feature_t;

#define CV_FEATURE_HEADER(pf) ((cv_feature_header_t*)(pf))
#define CV_FEATURE_SIZE(pf)   (CV_FEATURE_HEADER(pf)->len)
#define CV_FEATURE_LENGTH(pf)   ((CV_FEATURE_HEADER(pf)->len-sizeof(cv_feature_header_t))/sizeof(float))
#define CV_ENCODE_FEATURE_SIZE(pf) ((CV_FEATURE_HEADER(pf)->len+2)/3*4 + 1)

/// cv pixel format definition
typedef enum {
	CV_PIX_FMT_GRAY8,	///< Y    1       8bpp ( 单通道8bit灰度像素 )
	CV_PIX_FMT_YUV420P,	///< YUV  4:2:0   12bpp ( 3通道, 一个亮度通道, 另两个为U分量和V分量通道, 所有通道都是连续的 )
	CV_PIX_FMT_NV12,	///< YUV  4:2:0   12bpp ( 2通道, 一个通道是连续的亮度通道, 另一通道为UV分量交错 )
	CV_PIX_FMT_NV21,	///< YUV  4:2:0   12bpp ( 2通道, 一个通道是连续的亮度通道, 另一通道为VU分量交错 )
	CV_PIX_FMT_BGRA8888,	///< BGRA 8:8:8:8 32bpp ( 4通道32bit BGRA 像素 )
	CV_PIX_FMT_BGR888	///< BGR  8:8:8   24bpp ( 3通道24bit BGR 像素 )
} cv_pixel_format;

/// @brief 时间戳定义
typedef struct cv_time_t {
	long int tv_sec;	///< 秒
	long int tv_usec;	///< 微妙
}cv_time_t;

/// 图像格式定义
typedef struct cv_image {
	unsigned char *data;		///< 图像数据指针
	cv_pixel_format pixel_format;	///< 像素格式
	int width;			///< 宽度(以像素为单位)
	int height;			///< 高度(以像素为单位)
	int stride;			///< 跨度, 即每行所占的字节数
	cv_time_t time_stamp;		///< 时间戳
} cv_image;

// ====================== image utilities ========================
/// @defgroup image_utils image utilities
/// @brief common APIs for image utilities
/// @{

/// @brief 创建图像指针并分配内存
/// @param[in] width 输入宽度
/// @param[in] height 输入高度
/// @param[in] pixel_format 输入像素格式
/// @param[out] image 输出图像指针所在地址
/// @return 成功返回CV_OK, 否则返回错误码
CV_SDK_API
cv_result_t cv_image_allocate(
	int width,
	int height,
	cv_pixel_format pixel_format,
	cv_image ** image
);

/// @brief 释放图像数据
/// @param[in] image 图像指针
CV_SDK_API void
cv_image_release(cv_image* image);

/// @brief 进行颜色格式转换
/// @param[in] image_src 用于待转换的图像数据
/// @param[out] image_dst 转换后的图像数据, 目标图像由用户分配内存, 需提前定义宽, 高, PixelFormat等信息, 像素值初始化为0
/// @return 正常返回CV_OK, 否则返回错误类型
CV_SDK_API cv_result_t
cv_common_color_convert(
	const cv_image* image_src,
	cv_image* image_dst
);

/// @brief 进行仿射变换
/// @param[in] image_src 用于待转换的图像数据
/// @param[in] src_points_array 源图的仿射点数组
/// @param[in] src_points_count 源图仿射点的数目
/// @param[in] dst_points_array 目标图的仿射点数组
/// @param[in] dst_points_count 目标图仿射点的数目
/// @param[out] image_dst 转换后的图像数据, 必须是BGR格式图像，目标图像需要由用户分配内存, 需提前定义宽, 高, PixelFormat等信息
/// @return 正常返回CV_OK, 否则返回错误类型
CV_SDK_API
cv_result_t
cv_common_image_affine_transfer(
	const cv_image *image_src,
	const cv_pointf_t *src_points_array,
	const int src_points_count,
	const cv_pointf_t *dst_points_array,
	const int dst_points_count,
	cv_image *image_dst
);

/// @brief 图片调整方法
typedef enum {
       CV_IMAGE_RESIZE_BILINEAR,	///< 双线性插值
       CV_IMAGE_RESIZE_AREA		///< 区域插值
} cv_image_resize_method;

/// @brief 进行缩放变换
/// @note 该函数目前不支持stride参数, 所以stride参数应等于 width * elemSize
/// @param[in] image_src 用于待转换的图像数据
/// @param[out] image_dst 转换后的图像数据, 目标图像由用户分配内存, 需提前定义宽, 高, PixelFormat等信息
/// @param[in] method 缩放转换的方法
/// @return 正常返回CV_OK, 否则返回错误类型
CV_SDK_API
cv_result_t
cv_common_image_resize(
       const cv_image *image_src,
       cv_image *image_dst,
       cv_image_resize_method method
);

/// @brief 进行图像裁剪
/// @param[in] image_src 用于待裁剪的图像数据
/// @param[in] crop_area 图像裁剪的区域
/// @param[out] image_dst 裁剪后的图像数据, 目标图像由用户分配内存, 需提前定义宽, 高, PixelFormat等信息
/// @return 正常返回CV_OK, 否则返回错误类型
CV_SDK_API
cv_result_t
cv_common_image_crop(
       const cv_image *image_src,
       const cv_rect_t *crop_area,
       cv_image *image_dst
);

/// @brief 进行图像旋转
/// @note 该函数目前不支持stride参数, 所以stride参数应等于 width * elemSize
/// @param[in] image_src 用于待旋转的图像数据
/// @param[out] image_dst 旋转后的图像数据, 目标图像由用户分配内存, 需提前定义宽, 高, PixelFormat等信息
/// @param[in] rotate_degree 图像顺时针旋转的角度, 现在只支持0, 90, 180, 270
/// @return 正常返回CV_OK, 否则返回错误类型
CV_SDK_API
cv_result_t
cv_common_image_rotate(
       const cv_image *image_src,
       cv_image *image_dst,
       unsigned int rotate_degree
);

/// @}

// ====================== model loader ========================
/// @defgroup model_loader model loader
/// @brief common APIs for model loader
/// @{

/// 模型指针
typedef void * cv_model_t;

/// 组合模型指针
typedef void * cv_composite_model_t;

/// @brief 加载外部模型
/// @param[in] file 输入模型文件路径
/// @param[out] model 输出已初始化的模型指针
/// @return 成功返回CV_OK
CV_SDK_API cv_result_t
cv_common_load_model(
	const char *file,
	cv_model_t *model
);

/// @brief 获取模型名称
/// @param[in] model 模型指针
/// @param[out] name 输出模型名称
CV_SDK_API
void
cv_common_model_name(
	cv_model_t m,
	char name[128]
);

/// @brief 获取模型名称
/// @param[in] model 模型指针
/// @param[out] ver 输出模型版本， 格式: <major>.<minor>
CV_SDK_API
void
cv_common_model_version(
	cv_model_t m,
	char ver[128]
);

/// @brief 销毁已加载的模型
/// @param[in] model 模型指针
CV_SDK_API
void cv_common_unload_model(
	cv_model_t model
);

/// @brief 加载内部模型
/// @param[in] model_start 内部模型指针头
/// @param[in] model_end 内部模型指针尾
/// @param[out] model 输出已初始化的模型指针
/// @return 成功返回CV_OK
CV_SDK_API cv_result_t
cv_common_load_resource(
	const unsigned char *model_start,
	const unsigned char *model_end,
	cv_model_t *model
);

/// @brief 加载组合模型
/// @param[in] file 组合模型文件路径， 文件是由多个子模型文件组成tar包
/// @param[out] model 输出已初始化的组合模型指针
/// @return 成功返回CV_OK
CV_SDK_API cv_result_t
cv_common_load_composite_model(
	const char *file,
	cv_composite_model_t *model
);

/// @brief 销毁已加载的组合模型
/// @param[in] model 将销毁的模型
CV_SDK_API cv_result_t
cv_common_unload_composite_model(
       cv_composite_model_t model
);

/// @brief 获取子模型
/// @param[in] model 组合模型
/// @param[in] name 子模型名字
/// @param[in] 成功返回CV_OK
CV_SDK_API cv_result_t
cv_common_composite_model_get_submodel(
       cv_composite_model_t model,
       const char *name,
       cv_model_t *submodel
);

/// @}

#endif  // INCLUDE_CV_COMMON_H_
