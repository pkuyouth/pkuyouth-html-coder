#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: handler.py
# modified: 2019-03-30

__all__ = [

    "StreamHandlerMixin",
    "FileHandlerMixin",

    ]


import logging


class StreamHandlerMixin(object):
    """
    StreamHandler 封装 Mixin
    """

    def __init__(self):
        assert hasattr(self, "_logger")
        assert hasattr(self, "_get_level")
        _consoleHeadler = logging.StreamHandler()
        _consoleHeadler.setLevel(self._get_level())
        _consoleHeadler.setFormatter(logging.Formatter("[%(levelname)s] %(asctime)s, %(message)s", "%H:%M:%S"))
        self._logger.addHandler(_consoleHeadler)


class FileHandlerMixin(object):
    """
    FileHandler 封装 Mixin
    """

    def __init__(self, file):
        assert hasattr(self, "_logger")
        assert hasattr(self, "_get_level")
        _fileHandler = logging.FileHandler(file, encoding="utf-8")
        _fileHandler.setLevel(self._get_level())
        _fileHandler.setFormatter(logging.Formatter("[%(levelname)s] %(asctime)s, %(message)s", "%Y-%m-%d %H:%M:%S"))
        self._logger.addHandler(_fileHandler)

