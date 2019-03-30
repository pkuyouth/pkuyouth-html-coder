#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: tietuku.py
# modified: 2019-03-30
"""
贴图库 api 类
"""

__all__ = [

    "TietukuClient",

    ]


import os
import time
from io import BytesIO
from .base import BaseClient
from .utils import get_links_cache_json, save_links_cache_json
from ..utils.log import cout
from ..utils.funcs import xMD5, xSHA1
from ..utils.meta import Singleton
from ..utils.decorator import cached_property
from ..const import TIETUKU_TOKEN, TIETUKU_AID, TIETUKU_CACHE_EXPIRED, TIETUKU_LINKS_CACHE_JSON
from ..exceptions import TietukuUploadError


class TietukuClient(BaseClient, metaclass=Singleton):
    """
    贴图库客户端类
    """

    def __init__(self):
        super().__init__()
        self._imgLinks = get_links_cache_json(TIETUKU_LINKS_CACHE_JSON)


    def upload(self, filename, imgBytes):
        """
        图片上传接口

        Args:
            filename    str     图片名
            imgBytes    bytes   图片的 bytes
        Return:
            links       dict    该文件的外链信息
            {
               'url': 图片链接
               'md5': 图片 MD5
               'sha1': 图片 SHA1
               'expire_time': 图片过期的 Unix 时间/s
            }
        Raise:
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

        imgMD5  = xMD5(imgBytes)
        imgSHA1 = xSHA1(imgBytes)

        links = self._imgLinks.get(imgSHA1)

        if links is not None and links['expire_time'] > time.time():

            cout.info('Get image %s from cache' % filename)
            return links

        else:

            cout.info('uploading image %s' % filename)

            key = "{basename}{ext}".format(
                        basename=imgSHA1,
                        ext=os.path.splitext(filename)[1]
                        )

            r = self._post('http://up.imgapi.com/',

                    data={
                        'Token': TIETUKU_TOKEN,
                        'deadline': int(time.time() + 60), # 官方要求的参数，不清楚什么用
                        'aid': TIETUKU_AID,
                        'from': 'file', # 可选项 file 或 web ，表示上传的图片来自 本地/网络
                        },

                    files={
                        'file': (key, BytesIO(imgBytes)),
                        }
                )

            respJson = r.json()

            if "code" in respJson:
                raise TietukuUploadError("[%s] %s" % ( respJson['code'], respJson['info'] ) )

            links = {
                "url": respJson['linkurl'],
                # "o_url": respJson['linkurl'], # 原始图
                # "s_url": respJson['s_url'],   # 展示图
                # "t_url": respJson['t_url'],   # 缩略图
                "md5": imgMD5,
                "sha1": imgSHA1,
                "expire_time": int(time.time() + TIETUKU_CACHE_EXPIRED) # 用于校验图片有效性
                }

            self._imgLinks[imgSHA1] = links

            save_links_cache_json(TIETUKU_LINKS_CACHE_JSON, self._imgLinks)

            return links
