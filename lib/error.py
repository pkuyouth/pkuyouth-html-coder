#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: error.py
#
# 自定义错误类
#


try:
    from simplejson.errors import JSONDecodeError
except (ImportError, SystemError):
    from json.decoder import JSONDecodeError


__all__ = [
    'UnregisteredZoneError',
    'ContradictoryZoneError',
    'UnmatchZoneError',
    'TietukuError',
    'JSONDecodeError',
    'NoConfigFileError',
    'NoConfigOptionError',
    'NoConfigSectionError',
    'NoDocxFileError',
    'StaticServerTypeError',
    'MultiCountError',
    'SMMSUploadError',
    'SMMSGetListError',
    'SMMSClearError',
]



class ConfigError(BaseException):
    """配置文件错误"""
    pass

class NoConfigFileError(ConfigError):
    """没有找到配置文件"""
    pass

class NoConfigOptionError(ConfigError):
    """没有找到配置项"""
    pass

class NoConfigSectionError(ConfigError):
    """没有找到配置节"""
    pass



class CoderError(BaseException):
    """编码器错误"""
    pass

class NoDocxFileError(CoderError):
    """没有找到docx文件"""
    pass

class StaticServerTypeError(CoderError):
    """未注册的图床类型"""
    pass

class MultiCountError(CoderError):
    """同时统计字数和图片数"""
    pass


class ZoneError(CoderError):
    """模板区域错误"""
    pass

class UnregisteredZoneError(ZoneError):
    """未注册的区域名"""
    pass

class ContradictoryZoneError(ZoneError):
    """读取的区域信息冲突，可能是区域名称不配对，或是区域标识符防止不合理"""
    pass

class UnmatchZoneError(ZoneError):
    """区域未闭合"""
    pass



class TietukuError(BaseException):
    """贴图库api错误"""
    pass

class TietukuUploadError(TietukuError):
    """调用上传图片的 api ，请求状态码非 200"""
    pass


'''
    贴图库错误码汇总

    4001    上传凭证无效。 检查生成Token的参数
    4002    资源不存在。
    4003    关闭上传
    4004    请求方式错误，非预期的请求方式。
    4005    验证Token返回值为空
    4006    无法创建存储目录或目录不可写
    4007    缺少图片链接
    4008    获取本地上传图片信息失败
    4009    获取网络上传图片信息失败
    4010    打开临时文件失败
    4011    存储临时文件失败
    4012    不支持此类图片上传
    4013    图片太大超过上传限制
    4014    未能获取图片信息
    4015    存储图片失败
    4016    没有上传本地图片
    4017    上传本地图片失败
    4018    上传文件不存在
    4019    达到用户每小时上传数量上限   请升级套餐服务
    4020    达到用户单个IP每小时上传数量上限   请升级套餐服务
    4021    没有购买基础版服务或服务已到期 请开通套餐服务
    4022    图片数量达到非专业版用户数量限制    请开通专业版
    4500    缺失Token参数
    4501    Token参数值为空
    4502    Token参数值无效
    4503    公钥无效
    4504    路径参数无效
    4505    上传公钥等级低
    4506    用户提供Token参数值无效
    4507    公钥不存在或无效
    4510    用户账户不存在或被封
    4511    相册不存在或已经删除
    4512    不是你的相册，无权操作
    4513    写入数据失败
    4516    写入图片数据失败
    4517    更新图片数量失败
    4518    保存已存在图片信息到数据库失败
    4519    缺失UID参数
    4520    会员账号无效
    4521    相册数量不能超过100个
    4522    相册名称无效
    4523    相册名称长度为3-20字符
    4524    只有一个相册时，无法删除
    4525    相册ID无效或该用户无权限操作该相册
    4526    该相册内有照片，无法删除
    4527    相册aid参数无效
    4528    插入findurl失败
    4529    图片不存在
    4530    权限不足
    4531    删除图片失败
    4532    缺失图片ID
    4533    没有找到相关信息
    4534    修改图片名称失败
'''


class SMMSError(BaseException):
    """SM.MS api 错误"""
    pass

class SMMSUploadError(SMMSError):
    """SM.MS 上传文件错误"""
    pass

class SMMSGetListError(SMMSError):
    """SM.MS 获取文件列表错误"""
    pass

class SMMSClearError(SMMSError):
    """SM.MS 清除文件列表错误"""
    pass


'''
    错误列表

    Access Denied.
    Upload file count limit.
    Upload file frequency limit.
    Server error. Upload directory isn't writable.
    No files were uploaded.
    File is empty.
    File is too large.
    File has an invalid extension.
    Could not save uploaded file.
'''