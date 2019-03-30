#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: meta.py
# modified: 2019-03-30
"""
通用 metaclass
"""

__all__ = [

    "Singleton",

    ]


class Singleton(type):
    """
    Singleton Metaclass
    @link https://github.com/jhao104/proxy_pool/blob/428359c8dada998481f038dbdc8d3923e5850c0e/Util/utilClass.py
    """
    _inst = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._inst:
            cls._inst[cls] = super(Singleton, cls).__call__(*args)
        return cls._inst[cls]