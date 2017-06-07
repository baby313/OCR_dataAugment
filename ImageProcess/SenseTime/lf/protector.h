#ifndef PROTECTOR_H
#define PROTECTOR_H

#include "cv_utils.h"

#ifdef __cplusplus
extern "C" {
#endif

// ======================= UDID API ==========================
/// @defgroup sdk_protector sdk protector
/// @brief protector base on license
/// @{

/// @brief 获取设备的UDID（主板号），移动端可正常使用，PC端需要SUDO权限
/// @param [in] buf_size udid分配的内存大小
/// @param [out] udid 返回的udid字符串
/// @return 失败返回CV_OK
CV_SDK_API_ cv_errcode sdk_protector_udid(char *udid, int buf_size);

/// @}

// ======================= License API ===========================
/// @defgroup license_loader license api
/// @brief protector base on license
/// @{

/// @brief 添加一个license到环境中, 并做检查（AppId / 在线验证 / 设备ID / 激活码 / 时间限制），不调用或失败后无法加载模型
/// 		如License中设置AppId字段，则会检查当前SDK所在的AppId是否可用
/// 		如License中设置在线验证字段，则会通过互联网与公司服务器连接作验证，即该SDK可随时被停用
/// @note 在license相关函数中，该函数不是线程安全的
/// @param [in] product 所签发License对应的产品名称
/// @param [in] license_string 所签发的License字符串
/// @param [in] uuid 获取的uuid
/// 		如license中未写入UDID字段，则不会对UUID作检查；否则会验证传入的UUID是否与License中写入的一致
/// @param [in] signed_code 激活码为通过激活接口获取的code
/// 		如传NULL，则会检查License中的时间限制；否则，跳过时间限制检查转而检查license对应的激活码
/// @return 成功返回CV_OK, 否则返回错误码
CV_SDK_API_ cv_errcode sdk_protector_add_license(
	const char *product,
	const char *license_string,
	const char *uuid,
	const char *signed_code
);

/// @brief 测试当前是否已经加入一个有效的license
/// @param [in] product_name 如果传入NULL, 则检查是否有任一个有效的license；否则，检查是否有对应名字的有效license
CV_SDK_API_ cv_errcode sdk_protector_has_license(
	const char* product_name
);

/// @brief 验证License中的自定义限制内容
/// @param [in] product 所签发License对应的产品名称
/// @param [in] item 需要获取的限制项名称
/// @return 失败返回-1, 成功返回获取的值
CV_SDK_API_ int sdk_protector_get_limit(
	const char *product_name,
	const char *item
);

/// @brief 验证License中的自定义能力控制内容
/// @param [in] product 所签发License对应的产品名称
/// @param [in] item 需要获取的能力控制项名称
/// @return 能力可得返回CV_OK, 否则返回错误码
CV_SDK_API_ cv_errcode sdk_protector_has_capability(
	const char *product_name,
	const char *capability
);

/// @}

// ======================= Encypted API ==========================
/// @defgroup model_protector model protector
/// @brief protector for model files
/// @{

/// @brief 加密内存数据
/// @param [in] start 待加密内容起始位置
/// @param [in] fill 待加密内容结束位置
/// @param [out] output_buf 返回的加密后数据, 需要用户使用free释放
/// @warning 该接口并不具有CV_SDK_API_ 属性，因此只能以静态链接库方式使用，如果需要作为动态链接库接口需要外层封装
/// @return 成功返回加密后数据大小, 否则返回-1
int STEF_encrypt2mem(
	unsigned char *start, unsigned char *fill,
	unsigned char **output_buf
);

/// @}

// ===============================================================

#ifdef __cplusplus
}
#endif

#endif
