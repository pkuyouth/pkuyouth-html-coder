#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: const.py
# modified: 2019-03-30
"""
常数表
"""

__all__ = [

    "PROJECT_DIR",
    "PACKAGE_DIR",
    "CACHE_DIR",
    "CONFIG_DIR",
    "STATIC_DIR",
    "LOG_DIR",
    "INPUT_DIR",
    "OUTPUT_DIR",
    "OUTPUT_SRC_DIR",

    "STYLE_CSS",

    "CLIENT_DEFAULT_TIMEOUT",
    "CLIENT_USER_AGENT",

    "TIETUKU_TOKEN",
    "TIETUKU_AID",
    "TIETUKU_CACHE_EXPIRED",
    "TIETUKU_LINKS_CACHE_JSON",

    "ELIMAGE_LINKS_CACHE_JSON",

    "SMMS_LINKS_CACHE_JSON",

    ]


import os


def __mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)

__Base_dir = os.path.dirname(__file__)
__absP = lambda *path: os.path.abspath(os.path.join(__Base_dir, *path))


PROJECT_DIR    = __absP("../../")
PACKAGE_DIR    = __absP("../")
CACHE_DIR      = __absP("../cache/")
CONFIG_DIR     = __absP("../config/")
STATIC_DIR     = __absP("../static/")
LOG_DIR        = __absP("../../logs/")
INPUT_DIR      = __absP("../../input/")
OUTPUT_DIR     = __absP("../../output/")
OUTPUT_SRC_DIR = __absP("../../output/src/")

STYLE_CSS      = __absP(CONFIG_DIR, "style.css")


__mkdir(LOG_DIR)
__mkdir(CACHE_DIR)
__mkdir(INPUT_DIR)
__mkdir(OUTPUT_DIR)
__mkdir(OUTPUT_SRC_DIR)


CLIENT_DEFAULT_TIMEOUT   = 15
CLIENT_USER_AGENT        = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.122 Safari/537.36"

TIETUKU_TOKEN            = "305b1ec69ae2dfd54076a3f648931b9ac51a414b:EkuHTpQkLlK07Ocf69_VxR3anu8=:eyJkZWFkbGluZSI6MTUzMzI4ODMyNCwiYWN0aW9uIjoiZ2V0IiwidWlkIjoiNjU2NTU0IiwiYWlkIjoiMTQ3ODU1NSIsImZyb20iOiJmaWxlIn0="
TIETUKU_AID              = 1478555
TIETUKU_CACHE_EXPIRED    = 12*60*60  # 12 h
TIETUKU_LINKS_CACHE_JSON = "tietuku.links.json"

ELIMAGE_LINKS_CACHE_JSON = "elimage.links.json"

SMMS_LINKS_CACHE_JSON    = "sm.ms.links.json"
