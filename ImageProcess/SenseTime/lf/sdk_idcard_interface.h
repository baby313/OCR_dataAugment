#ifndef INCLUDE_IDCARD_API_H_
#define INCLUDE_IDCARD_API_H_

#include "cv_common_internal.h"

#define CV_IDCARD_MAX_INFO_LENGTH 256			///< 内容描述最大长度

#define CV_IDCARD_KEY_MASK_NAME (1<<0)			///< 姓名
#define CV_IDCARD_KEY_MASK_SEX (1<<1)			///< 性别
#define CV_IDCARD_KEY_MASK_NATION (1<<2)		///< 民族
#define CV_IDCARD_KEY_MASK_BIRTHDAY (1<<3)		///< 生日
#define CV_IDCARD_KEY_MASK_ADDR (1<<4)			///< 地址
#define CV_IDCARD_KEY_MASK_NUM (1<<5)			///< 身份证号
#define CV_IDCARD_KEY_MASK_AUTHORITY (1<<6)		///< 签发机关
#define CV_IDCARD_KEY_MASK_TIMELIMIT (1<<7)		///< 有效期限
#define CV_IDCARD_CLASSIFY_THRESHOLD 0.99		///< 身份证type,side分类概率阈值

/// @brief 身份证类型
typedef enum cv_idcard_type {
	CV_IDCARD_TYPE_UNKNOWN = 0,	///< 未知
	CV_IDCARD_TYPE_NORMAL,		///< 正常身份证
	CV_IDCARD_TYPE_TEMP,		///< 临时身份证
	CV_IDCARD_TYPE_RESERVE		///< 预留
} cv_idcard_type;

/// @brief 身份证旋转朝向
typedef enum cv_idcard_orient {
	CV_IDCARD_ORIENT_UNKNOWN = 0,	///< 未知,程序将会自动判断
	CV_IDCARD_ORIENT_TOP,		///< 身份证向上,即身份证中人脸朝向正常
	CV_IDCARD_ORIENT_LEFT,		///< 身份证向左,即身份证被逆时针旋转了90度
	CV_IDCARD_ORIENT_BOTTOM,	///< 身份证向下,即身份证被逆时针旋转了180度
	CV_IDCARD_ORIENT_RIGHT,		///< 身份证向右,即身份证被逆时针旋转了270度
} cv_idcard_orient;

/// @brief 身份证正背面
typedef enum cv_idcard_side {
	CV_IDCARD_SIDE_UNKNOWN = 0,	///< 未知,程序将会自动判断
	CV_IDCARD_SIDE_FRONT,		///< 身份证正面
	CV_IDCARD_SIDE_BACK,		///< 身份证背面
} cv_idcard_side;

/// @brief 身份证信息顺序
typedef enum cv_idcard_info_idx {
	CV_IDCARD_INFO_IDX_NAME = 0,			///< 姓名
	CV_IDCARD_INFO_IDX_SEX,				///< 性别
	CV_IDCARD_INFO_IDX_NATION,			///< 民族
	CV_IDCARD_INFO_IDX_YEAR,			///< 出生年
	CV_IDCARD_INFO_IDX_MONTH,			///< 出生月
	CV_IDCARD_INFO_IDX_DAY,				///< 出生日
	CV_IDCARD_INFO_IDX_ADDR,			///< 地址
	CV_IDCARD_INFO_IDX_NUM,				///< 身份证号
	CV_IDCARD_INFO_IDX_AUTHORITY,			///< 签发机关
	CV_IDCARD_INFO_IDX_TIMELIMIT,			///< 有效期限
	CV_IDCARD_INFO_COUNT				///< 身份证上信息个数
} cv_idcard_info_idx;

/// @brief 单个文字条目信息
typedef struct cv_idcard_item {
	int valid;					///< 本条目识别结果是否有效
	cv_rect_t keyword_region;			///< 关键词位置(在返回的剪裁过的图像中)
	cv_rect_t text_region;				///< 信息内容的位置(在返回的剪裁过的图像中)
	char text[CV_IDCARD_MAX_INFO_LENGTH];		///< 信息内容
} cv_idcard_item;

/// @brief 身份证识别结果
typedef struct cv_idcard_info {
	int valid;					///< 整体识别结果是否有效
	cv_idcard_type type;				///< 身份证类型
	cv_idcard_orient orient;			///< 身份证旋转方向信息
	cv_idcard_side side;				///< 身份证正背面信息
	cv_pointf_t corners[4];				///< 检测到身份证的四个角点:左上、右上、左下、右下
	cv_idcard_item info[CV_IDCARD_INFO_COUNT];	///< 信息条目数组,顺序见cv_idcard_info_idx
} cv_idcard_info;

// ====================== idcard still ocr =======================
/// @defgroup cv_idcard_still cv_idcard still ocr interface
/// @brief idcard still ocr definitions and interface，different from the mobile interface
/// @{

/// @brief 创建身份证识别句柄
/// @param[in] model 载入身份证模型
/// @param[out] handle 输出id card句柄
/// @return 正常返回CV_OK, 否则返回错误类型
CV_SDK_API
cv_result_t
cv_idcard_ocr_create(
	cv_composite_model_t model,
	cv_handle_t* handle
);

/// @brief 身份证静态图像识别
/// @param[in] handle 已完成初始化的身份证句柄
/// @param[in] input_image 输入的待识别的图像,推荐BGR格式
/// @param[in] type 身份证类型,still支持临时身份证区分，不支持识别
/// @param[in] orient 输入图像中身份证的旋转方向
/// @param[in] side 输入图像中身份证的正背面
/// @param[in] key_require 指定需要识别的信息,值为0时对所有信息都识别,其他比如只需要识别姓名和号码信息是设置key_require=CV_IDCARD_KEY_MASK_NAME+CV_IDCARD_KEY_MASK_NUM
/// @param[out] card 身份证识别结果,用户负责分配内存
/// @param[out] output_image 如果不为null则输出剪裁过的的只包含身份证的图像,图像数据像素格式固定为CV_PIX_FMT_BGR888,api负责分配内存,需要调用cv_image_release释放
/// @return 正常返回CV_OK, 否则返回错误类型
CV_SDK_API
cv_result_t
cv_idcard_ocr(
	cv_handle_t handle,
	const cv_image* input_image,
	cv_idcard_type type,
	cv_idcard_orient orient,
	cv_idcard_side side,
	int key_require,
	cv_idcard_info* card,
	cv_image** output_image
);

/// @brief 销毁已初始化的身份证句柄
/// @param[in] handle 已完成初始化的身份证句柄
CV_SDK_API
void
cv_idcard_ocr_destroy(
	cv_handle_t handle
);

/// @}

#endif  // INCLUDE_IDCARD_API_H_
