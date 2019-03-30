#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: css.py
# modified: 2019-03-30
"""
css 文件解析
"""

__all__ = [

    "parse_css_file",

    ]


import re

_regex_comment = re.compile(r'(/\*.*?\*/)', re.S)
_regex_style   = re.compile(r'\s*([^{}]*?)\s*{(.*?)}', re.S)


def parse_css_file(file):
    """
    解析 css 文件

    Args:
        file   str   css 路径
    Return:
        res   dict
        {
            "selector1": {
                "key1": "value1",
                ......
            },
            ......
        }
    """

    with open(file, "r", encoding="utf-8-sig") as fp:
        s = fp.read()

    s = s.replace("\n", "")
    s = _regex_comment.sub("", s)

    res = {}

    for selector, styles in _regex_style.findall(s):
        selector = selector.strip()
        styles = [ css.strip() for css in styles.split(";") ]
        styles = dict( map( str.strip, css.split(":") ) for css in styles if css )
        res[selector] = styles

    return res
