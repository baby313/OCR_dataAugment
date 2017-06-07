#ifndef INCLUDE_BANKCARD_API_H_
#define INCLUDE_BANKCARD_API_H_

#include "cv_common_internal.h"

#define CV_BANKCARD_DIGIT_MAXCOUNT 32				///< 卡号最大个数
#define CV_BANKCARD_MAX_INFO_LENGTH 256				///< 内容描述最大长度

#define CV_BANKCARD_KEY_MASK_NUM (1<<0)				///< 卡号key_require mask
#define CV_BANKCARD_KEY_MASK_BANK (1<<1)			///< 银行卡片信息key_require mask
#define CV_BANKCARD_KEY_MASK_NAME (1<<2)			///< 卡主姓名key_require mask
#define CV_BANKCARD_KEY_MASK_DATE (1<<3)			///< 卡片有效日期key_require mask

/// @brief 银行卡方向
typedef enum cv_bankcard_layout{
	CV_BANKCARD_LAYOUT_UNKNOWN = 0,				///< 未知方向(保留字段)
	CV_BANKCARD_LAYOUT_HORIZONTAL,				///< 水平方向(常见版式)
	CV_BANKCARD_LAYOUT_VERTICAL				///< 垂直方向
} cv_bankcard_layout;

/// @brief 单个卡号条目信息
typedef struct cv_bankcard_item_number {
	int valid;						///< 卡号是否有效
	int  digit_count;					///< 卡号个数
	char digit_content[CV_BANKCARD_DIGIT_MAXCOUNT];		///< 卡号内容
	cv_rect_t digit_pos[CV_BANKCARD_DIGIT_MAXCOUNT];	///< 每个数字位置(相对于矫正后图像)
	cv_rect_t rect;						///< 卡号所在区域（相对于矫正后图像）
} cv_bankcard_item_number;

/// @brief 银行卡识别结果
typedef struct cv_bankcard_info {
	int valid;						///< 可识别结果是否全部有效
	cv_bankcard_layout layout;				///< 银行卡方向
	cv_bankcard_item_number num_item;			///< 卡号
	char bankname[CV_BANKCARD_MAX_INFO_LENGTH];		///< 银行名称
	char bankid[CV_BANKCARD_MAX_INFO_LENGTH];		///< 银行编号
	char cardname[CV_BANKCARD_MAX_INFO_LENGTH];		///< 卡片名称
	char cardtype[CV_BANKCARD_MAX_INFO_LENGTH];		///< 卡片类型
	char holder[CV_BANKCARD_MAX_INFO_LENGTH];		///< 持卡人（暂时无效）
	char date[CV_BANKCARD_MAX_INFO_LENGTH];			///< 有效日期（暂时无效）
	cv_pointf_t corners[4];					///< 检测到银行卡的四个角点:左上、右上、左下、右下
} cv_bankcard_info;

// ====================== bankcard still ocr =======================
/// @defgroup cv_bankcard_still cv_bankcard still ocr interface
/// @brief bankcard still ocr definitions and interface，different from the mobile interface
/// @{

/// @brief 创建银行卡检测句柄
/// @param[in] model 载入银行卡模型
/// @param[out] handle 输出bank card句柄
/// @return 正常返回CV_OK, 否则返回错误类型
CV_SDK_API
cv_result_t
cv_bankcard_ocr_create(
	cv_composite_model_t model,
	cv_handle_t* handle
);

/// @brief 银行卡静态图像识别，支持竖卡识别
/// @param[in] handle 已完成初始化的银行卡句柄
/// @param[in] input_image 输入的待识别的图像,推荐BGR格式
/// @param[in] layout 银行卡方向，不支持传入“未知方向”
/// @param[in] key_require 指定需要识别的信息,值为0时识别全部可支持内容,其它比如key_require=CV_BANKCARD_KEY_MASK_NUM + CV_BANKCARD_KEY_MASK_BANK为识别卡号和银行名
/// @param[out] card 银行卡识别结果,用户负责分配内存
/// @param[out] output_image 如果不为null则输出剪裁过的的只包含银行卡的图像,图像数据像素格式固定为CV_PIX_FMT_BGR888,api负责分配内存,需要调用cv_image_release释放
/// @return 正常返回CV_OK, 否则返回错误类型
CV_SDK_API
cv_result_t
cv_bankcard_ocr(
	cv_handle_t handle,
	const cv_image* input_image,
	cv_bankcard_layout layout,
	int key_require,
	cv_bankcard_info* card,
	cv_image** output_image
);

/// @brief 销毁已初始化的银行卡句柄
/// @param[in] handle 已完成初始化的银行卡句柄
CV_SDK_API
void
cv_bankcard_ocr_destroy(
	cv_handle_t handle
);

/// @}

#endif  // INCLUDE_BANKCARD_API_H_
