#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: base.py
# modified: 2019-03-30
"""
客户端抽象基类
"""

__all__ = [

    "BaseClient",

    ]


import requests
from .utils import _hook_check_status
from ..const import CLIENT_DEFAULT_TIMEOUT, CLIENT_USER_AGENT


class BaseClient(object):

    timeout = CLIENT_DEFAULT_TIMEOUT
    headers = {
        "User-Agent": CLIENT_USER_AGENT,
        }

    def __init__(self):
        if __class__ is self.__class__:
            raise NotImplementedError

        self._session = requests.session()
        self._session.headers.update(self.__class__.headers)
        self._session.hooks["response"].append(_hook_check_status)

    def _request(self, method, url, **kwargs):
        kwargs.setdefault("timeout", self.__class__.timeout)
        return self._session.request(method, url, **kwargs)

    def _get(self, url, params=None, **kwargs):
        return self._request('GET', url, params=params, **kwargs)

    def _post(self, url, data=None, json=None, **kwargs):
        return self._request('POST', url, data=data, json=json, **kwargs)
