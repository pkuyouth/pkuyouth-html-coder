#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: logger.py
# modified: 2019-03-30

__all__ = [

    "ConsoleLogger",
    "ErrorLogger",

    ]


import logging
from .handler import StreamHandlerMixin, FileHandlerMixin


class BaseLogger(object):
    """
    logging 模板的封装，基类
    """

    LEVEL = logging.DEBUG

    def __init__(self, name):
        if __class__ is self.__class__:
            raise NotImplementedError
        self._logger = logging.getLogger(name)
        self._logger.setLevel(self._get_level())

    def _get_level(self):
        return self.__class__.LEVEL

    def log(self, level, msg, *args, **kwargs):
        return self._logger.log(level, msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        return self._logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        return self._logger.info(msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        return self._logger.warn(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        return self._logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        return self._logger.error(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        kwargs.setdefault("exc_info", True)
        return self._logger.exception(msg, *args, **kwargs)

    def fatal(self, msg, *args, **kwargs):
        return self._logger.fatal(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        return self._logger.critical(msg, *args, **kwargs)


class ConsoleLogger(BaseLogger, StreamHandlerMixin):
    """
    控制台日志
    """
    def __init__(self, name):
        BaseLogger.__init__(self, name)
        StreamHandlerMixin.__init__(self)


class ErrorLogger(BaseLogger, FileHandlerMixin):
    """
    错误日志
    """
    LEVEL = logging.ERROR

    def __init__(self, name, file):
        BaseLogger.__init__(self, name)
        FileHandlerMixin.__init__(self, file)
