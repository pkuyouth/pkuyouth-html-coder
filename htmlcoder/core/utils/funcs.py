#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: funcs.py
# modified: 2019-03-30
"""
通用函数
"""

__all__ = [

    "b",

    "xMD5",
    "xSHA1",

    "json_load",
    "json_dump",

    ]


import os
from requests.compat import json  # 使用的 json 库与 requests 一致
import hashlib


def b(s):
    """
    bytes/str/int/float -> bytes
    """
    if isinstance(s, bytes):
        return s
    elif isinstance(s, (str, int, float)):
        return str(s).encode('utf-8')
    else:
        raise TypeError(type(s))


def xMD5(s):
    return hashlib.md5(b(s)).hexdigest()

def xSHA1(s):
    return hashlib.sha1(b(s)).hexdigest()


def json_load(folder, filename, **kwargs):
    """
    json.load 函数的封装
    """
    file = os.path.join(folder, filename)
    with open(file, 'r', encoding="utf-8-sig") as fp:
        return json.load(fp, **kwargs)

def json_dump(folder, filename, data, **kwargs):
    """
    json.dump 函数的封装
    """
    file = os.path.join(folder, filename)
    with open(file, "w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=True, **kwargs)