#ifndef CV_UTILS_H
#define CV_UTILS_H

#ifdef _MSC_VER
#	ifdef CV_STATIC_LIB
#		define CV_SDK_API_
#	elif defined SDK_EXPORTS
#		define CV_SDK_API_ __declspec(dllexport)
#	else
#		define CV_SDK_API_ __declspec(dllimport)
#	endif
#else /* _MSC_VER */
#	ifdef SDK_EXPORTS
#		define CV_SDK_API_ __attribute__((visibility ("default")))
#	else
#		define CV_SDK_API_
#	endif
#endif

typedef int cv_errcode;

#define CV_ERR_PACK(lib, module, reason)	\
	((int)( 0x80000000 | ((unsigned int)(lib) & 0x7ff) << 20 | ((unsigned int)(module) & 0xf) << 16 | ((unsigned int)(reason) & 0xffff)))

#define CV_ERR_GETLIB(error_code)	\
	((unsigned int)(error_code) >> 20 & 0x7ff)

#define CV_ERR_GETMODULE(error_code)	\
	((unsigned int)(error_code) >> 16 & 0xf)
	
#define CV_ERR_GETREASON(error_code)	\
	((unsigned int)(error_code) & 0xffff)

///====================global error definition==========================================
#define CV_E_GLOBAL_LIB 0x7ff
#define CV_E_GLOBAL_MODULE 0xf

#define	CV_OK 0					///< 正常运行
#define	CV_E_INVALIDARG               CV_ERR_PACK(CV_E_GLOBAL_LIB, CV_E_GLOBAL_MODULE, 0xffff)		///< 无效参数
#define	CV_E_HANDLE                   CV_ERR_PACK(CV_E_GLOBAL_LIB, CV_E_GLOBAL_MODULE, 0xfffe)		///< 句柄错误
#define	CV_E_OUTOFMEMORY              CV_ERR_PACK(CV_E_GLOBAL_LIB, CV_E_GLOBAL_MODULE, 0xfffd)		///< 内存不足
#define	CV_E_FAIL                     CV_ERR_PACK(CV_E_GLOBAL_LIB, CV_E_GLOBAL_MODULE, 0xfffc)		///< 运行失败，内部错误
#define	CV_E_DELNOTFOUND              CV_ERR_PACK(CV_E_GLOBAL_LIB, CV_E_GLOBAL_MODULE, 0xfffb)		///< 定义缺失
#define	CV_E_INVALID_PIXEL_FORMAT     CV_ERR_PACK(CV_E_GLOBAL_LIB, CV_E_GLOBAL_MODULE, 0xfffa)			///< 不支持的图像格式
#define	CV_E_FILE_NOT_FOUND           CV_ERR_PACK(CV_E_GLOBAL_LIB, CV_E_GLOBAL_MODULE, 0xfff9)		///<. 文件不存在
#define	CV_E_INVALID_FILE_FORMAT      CV_ERR_PACK(CV_E_GLOBAL_LIB, CV_E_GLOBAL_MODULE, 0xfff8)		///< 模型格式不正确导致加载失败
#define	CV_E_UNSUPPORTED              CV_ERR_PACK(CV_E_GLOBAL_LIB, CV_E_GLOBAL_MODULE, 0xfc18)		///< 不支持的函数调用方式

#define	CV_E_FILE_EXPIRE                 CV_ERR_PACK(CV_E_GLOBAL_LIB, CV_E_GLOBAL_MODULE, 0xfff7)		///< 模型文件过期
#define	CV_E_INVALID_AUTH                CV_ERR_PACK(CV_E_GLOBAL_LIB, CV_E_GLOBAL_MODULE, 0xfff3)		///< license不合法
#define	CV_E_INVALID_APPID               CV_ERR_PACK(CV_E_GLOBAL_LIB, CV_E_GLOBAL_MODULE, 0xfff2)		///< 包名错误
#define	CV_E_AUTH_EXPIRE                 CV_ERR_PACK(CV_E_GLOBAL_LIB, CV_E_GLOBAL_MODULE, 0xfff1)		///< SDK过期
#define	CV_E_UUID_MISMATCH               CV_ERR_PACK(CV_E_GLOBAL_LIB, CV_E_GLOBAL_MODULE, 0xfff0)		///< UUID不匹配
#define	CV_E_ONLINE_AUTH_CONNECT_FAIL    CV_ERR_PACK(CV_E_GLOBAL_LIB, CV_E_GLOBAL_MODULE, 0xffef)		///< 在线验证连接失败
#define	CV_E_ONLINE_AUTH_TIMEOUT         CV_ERR_PACK(CV_E_GLOBAL_LIB, CV_E_GLOBAL_MODULE, 0xffee)		///< 在线验证超时
#define	CV_E_ONLINE_AUTH_INVALID         CV_ERR_PACK(CV_E_GLOBAL_LIB, CV_E_GLOBAL_MODULE, 0xffed)		///< 在线验证失败
#define	CV_E_LICENSE_IS_NOT_ACTIVABLE    CV_ERR_PACK(CV_E_GLOBAL_LIB, CV_E_GLOBAL_MODULE, 0xffec)		///< license不可激活
#define	CV_E_ACTIVE_FAIL                 CV_ERR_PACK(CV_E_GLOBAL_LIB, CV_E_GLOBAL_MODULE, 0xffeb)		///< license激活失败
#define	CV_E_ACTIVE_CODE_INVALID         CV_ERR_PACK(CV_E_GLOBAL_LIB, CV_E_GLOBAL_MODULE, 0xffea)		///< 激活码无效

///=======================protector errors===========================================
#define CV_E_PROTECTOR_LIB 0x1
#define CV_E_PROTECTOR_MODULE_ONLINEAUTH_MODULE 0x1		///< protector 在线验证返回错误码mask

#endif
