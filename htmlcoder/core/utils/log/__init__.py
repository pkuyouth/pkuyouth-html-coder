#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: __init__.py
# modified: 2019-03-30

__all__ = [

    "cout",
    "ferr",

    ]


import os
import time
from .logger import ConsoleLogger, ErrorLogger
from ...const import LOG_DIR


_Error_log_filename = "%s.error.log" % time.strftime("%Y-%m-%d", time.localtime(time.time()))
_Error_log_file = os.path.join(LOG_DIR, _Error_log_filename)


cout = ConsoleLogger("htmlcoder.stdout")
ferr = ErrorLogger("htmlcoder.stderr", _Error_log_file)
