#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: lib/smms.py
#
# SM.MS api 类
#
# 上传速度较慢
#

import os
import time
from io import BytesIO
from functools import partial
import requests

from utils import json_dump, json_load, MD5, SHA1, Logger, Config
from errors import JSONDecodeError, SMMSUploadError, SMMSGetListError, SMMSClearError


Root_Dir = os.path.join(os.path.dirname(__file__), '../') # 项目根目录
Cache_Dir = os.path.join(Root_Dir, "cache/") # 缓存文件目录

json_dump = partial(json_dump, Cache_Dir)
json_load = partial(json_load, Cache_Dir)


__all__ = ['SMMSAPI',]


class SMMSAPI(object):
    """ [SM.MS api 类] 为图片提供外链

        Attributes:
            class:
                logger                   Logger    日志实例
                config                   Config    配置文件实例
                api                      dict      API 接口
                Image_Links_Cache_JSON   str       图片外链 json 缓存文件名
                imgLinks                 dict      图片 sha1 与图片外链的映射
    """
    logger = Logger('SM.MS')
    config = Config('smms.ini')

    api = {
        'list': 'https://sm.ms/api/list',
        'upload': 'https://sm.ms/api/upload',
        'clear': 'https://sm.ms/api/clear',
    }

    Image_Links_Cache_JSON = config.get('cache', 'image_links_json')

    try:
        imgLinks = json_load(Image_Links_Cache_JSON)
    except (FileNotFoundError, JSONDecodeError): # 说明文件不存在或者为空，应当至少为 {}
        imgLinks = {}


    def upload(self, filename, imgBytes, log=True):
        """ 图片上传接口

            Args:
                filename    str     图片名
                imgBytes    bytes   图片的 bytes
                log         bool    是否输出日志
            Returns:
                links       dict    该文件的外链信息 {
                                       'url': 图片链接
                                       'md5': 图片 MD5
                                       'sha1': 图片 SHA1
                                       'delete': 删除图片链接
                                    }
            Raises:
                SMMSUploadError      code 字段非 'success'

            -----------------------------------------------------
            返回数据说明

            名称  类型  示例值 描述
            code    String  success 上传文件状态。正常情况为 success。出现错误时为 error
            filename    String  smms.jpg    上传文件时所用的文件名
            storename   String  561cc4e3631b1.png   上传后的文件名
            size    Int 187851  文件大小
            width   Int 1157    图片的宽度
            height  Int 680 图片的高度
            hash    String  nLbCw63NheaiJp1 随机字符串，用于删除文件
            delete  String  https://sm.ms/api/delete/nLbCw63NheaiJp1    删除上传的图片文件专有链接
            url String  https://ooo.0o0.ooo/2015/10/13/561cfc3282a13.png    图片服务器地址
            path    String  /2015/10/13/561cfc3282a13.png   图片的相对地址
            msg String  No files were uploaded. 上传图片出错时将会出现
        """
        imgMD5 = MD5(imgBytes)
        imgSHA1 = SHA1(imgBytes)
        links = self.imgLinks.get(imgSHA1)
        if links is not None:
            if log:
                self.logger.info('get image %s from cache' % filename)
            return links
        else:
            if log:
                self.logger.info('uploading image %s' % filename)

            respJson = requests.post(self.api['upload'], files={
                    'smfile': (imgSHA1 + os.path.splitext(filename)[1], BytesIO(imgBytes)),
                }).json()

            code = respJson.get('code')

            if code == 'success':
                data = respJson['data']
                links = {
                    'url': data['url'],
                    'md5': imgMD5,
                    'sha1': imgSHA1,
                    'delete': data['delete'],
                }
                self.imgLinks[imgSHA1] = links
                json_dump(self.Image_Links_Cache_JSON, self.imgLinks) # 缓存
                return links
            elif code == 'error':
                raise SMMSUploadError(respJson.get('msg'))
            else:
                raise SMMSUploadError('unexcepted return code ! %s' % respJson)


    def list(self):
        """ 获得过去一小时内上传的文件列表

            Returns:
                links       list    图片信息 dict 的列表，格式如 upload 返回值

            Raises:
                SMMSGetListError    code 字段非 'success'
        """
        respJson = requests.get(self.api['list']).json()
        code = respJson.get('code')
        if code == 'success':
            return respJson['data']
        elif code == 'error':
            raise SMMSGetListError(respJson.get('msg'))
        else:
            raise SMMSGetListError('unexcepted return code ! %s' % respJson)


    def clear(self):
        """ 将历史上传的文件列表移除

            Raises:
                SMMSClearError    code 字段非 'success'
        """
        respJson = requests.get(self.api['clear']).json()
        code = respJson.get('code')
        if code == 'success':
            self.logger.info(respJson.get('msg'))
        elif code == 'error':
            raise SMMSClearError(respJson.get('msg'))
        else:
            raise SMMSClearError('unexcepted return code ! %s' % respJson)

