#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: utils.py
# modified: 2019-03-30
"""
图床客户端相关的通用函数
"""

__all__ = [

    "_get_hooks",
    "_hook_check_status",

    "get_links_cache_json",
    "save_links_cache_json",

    ]


from requests.compat import json
from ..utils.funcs import json_load, json_dump
from ..const import CACHE_DIR


def _get_hooks(*fn):
    return {"response": fn}

def _hook_check_status(r, **kwargs):
    if r.status_code != 200:
        r.raise_for_status()


def get_links_cache_json(file):
    try:
        imgLinks = json_load(CACHE_DIR, file)
    except (FileNotFoundError, json.JSONDecodeError):
        imgLinks = {}
    return imgLinks

def save_links_cache_json(file, data):
    json_dump(CACHE_DIR, file, data)