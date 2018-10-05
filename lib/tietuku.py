#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: lib/tietuku.py
#
# 贴图库 api 类
#

import os
import time
from io import BytesIO
from functools import partial
import requests

from utils import json_dump, json_load, MD5, SHA1, Logger, Config
from errors import JSONDecodeError, TietukuUploadError


Root_Dir = os.path.join(os.path.dirname(__file__), '../') # 项目根目录
Cache_Dir = os.path.join(Root_Dir, "cache/") # 缓存文件目录

json_dump = partial(json_dump, Cache_Dir)
json_load = partial(json_load, Cache_Dir)


__all__ = ['TietukuAPI',]


class TietukuAPI(object):
    """ [贴图库 api 类] 为图片提供外链

        Attributes:
            class:
                logger                   Logger    日志实例
                config                   Config    配置文件实例
                token                    str       贴图库 api 接口的 token
                aid                      int       图库 ID
                Validity_Period          int       图片有效期
                Image_Links_Cache_JSON   str       图片外链 json 缓存文件名
                imgLinks                 dict      图片 sha1 与图片外链的映射
    """

    logger = Logger('tietuku')
    config = Config('tietuku.ini')

    token = config.get('account', 'token')
    aid = config.getint('account', 'aid')

    Validity_Period = config.getint('cache', 'cache_time')
    # Validity_Period = 24*60*60*(7-1) # 实际 7 天过期，自定义 6 天即不能用
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
                                       'expire_time': 图片过期的 Unix 时间/s
                                    }
            Raises:
                TietukuUploadError   图片上传错误，请求状态码非 200 可以查询 code 字段的信息

            -------------------------------------------------
            请求成功的返回 json 包
            {
                "width": 1280,
                "height": 711,
                "type": "jpg",
                "size": 24640,
                "ubburl": "[img]http://i1.bvimg.com/656554/0cf57e9173c0acaf.jpg[/img]",
                "linkurl": "http://i1.bvimg.com/656554/0cf57e9173c0acaf.jpg",
                "htmlurl": "<img src='http://i1.bvimg.com/656554/0cf57e9173c0acaf.jpg' />",
                "markdown": "![Markdown](http://i1.bvimg.com/656554/0cf57e9173c0acaf.jpg)",
                "s_url": "http://i1.bvimg.com/656554/0cf57e9173c0acafs.jpg",
                "t_url": "http://i1.bvimg.com/656554/0cf57e9173c0acaft.jpg",
                "findurl": "7cbf06538e66e772"
            }

            请求失败的返回 json 包，可通过 code 查询相应错误类型，错误信息 == info
            {
                "code": "4511",
                "info": "\u76f8\u518c\u4e0d\u5b58\u5728\u6216\u5df2\u7ecf\u5220\u9664"
            }
        """
        imgMD5 = MD5(imgBytes)
        imgSHA1 = SHA1(imgBytes)
        links = self.imgLinks.get(imgSHA1)
        if links is not None and links['expire_time'] > time.time():
            if log:
                self.logger.info('get image %s from cache' % filename)
            return links
        else:
            if log:
                self.logger.info('uploading image %s' % filename)
            resp = requests.post('http://up.imgapi.com/', data={
                'Token': self.token,
                'deadline': int(time.time() + 60), # 官方要求的参数，不清楚什么用
                'aid': self.aid,
                'from': 'file', # 可选项 file 或 web ，表示上传的图片来自 本地/网络
            }, files={
                'file': (imgSHA1 + os.path.splitext(filename)[1], BytesIO(imgBytes)),
            })
            if resp.status_code != requests.codes.ok:
                raise TietukuUploadError('[status %d] %s' % (resp.status_code, resp.text))
            else:
                respJson = resp.json()
                links = {
                    "url": respJson['linkurl'],
                    # "o_url": respJson['linkurl'], # 原始图
                    # "s_url": respJson['s_url'],   # 展示图
                    # "t_url": respJson['t_url'],   # 缩略图
                    "md5": imgMD5,
                    "sha1": imgSHA1,
                    "expire_time": int(time.time() + self.Validity_Period) # 用于校验图片有效性
                }
                self.imgLinks[imgSHA1] = links
                json_dump(self.Image_Links_Cache_JSON, self.imgLinks) # 缓存
                return links
