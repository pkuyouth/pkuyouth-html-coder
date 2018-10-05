#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: lib/utils.py
#
# 通用的 function / class
#

import os
import time
import logging
import hashlib
from configparser import RawConfigParser, NoSectionError, NoOptionError

try:
    import simplejson as json
except ModuleNotFoundError:
    import json

from errors import NoConfigFileError, NoConfigOptionError, NoConfigSectionError


Root_Dir = os.path.join(os.path.dirname(__file__), '../') # 文件夹根目录
Config_Dir = os.path.join(Root_Dir, "config/") # 配置文件夹
Log_Dir = os.path.join(Root_Dir, "log/") # 日志输出文件夹


__all__ = [

    'json_load',
    'json_dump',
    'MD5',
    'SHA1',

    'Logger',
    'Config',
    'Stack',
]


def to_bytes(data):
    """ str -> bytes

        Args:
            data    bytes/str/int/float    origin
        Returns:
            bytes   bytes
    """
    if isinstance(data, bytes):
        return data
    elif isinstance(data, (str, int, float)):
        return str(data).encode('utf-8')
    else:
        raise TypeError('unsupported type %s' % type(data))


""" hashlib 函数的封装

    Args:
        data    bytes/str/int/float    待 hash 的数据
    Returns:
        hashString    hash 值
    Raises:
        TypeError     data 类型非法
"""
MD5 = lambda data: hashlib.md5(to_bytes(data)).hexdigest()
SHA1 = lambda data: hashlib.sha1(to_bytes(data)).hexdigest()


def json_load(folder, filename, **kwargs):
    """ json.load 函数的封装

        Args:
            folder      str    文件夹路径
            filename    str    文件名
            **kwargs           传给 json.load 函数的参数
        Returns:
            object             json 文件反序列化的 python 序列对象
    """
    file = os.path.join(folder, filename)
    return json.load(open(file, 'r', encoding="utf-8-sig"), **kwargs)


def json_dump(folder, filename, data, **kwargs):
    """ json.dump 函数的封装

        Args:
            folder      str      文件夹路径
            filename    str      文件名
            data        object
            **kwargs             传给 json.dump 函数的参数，例如 indent = 4
    """
    file = os.path.join(folder, filename)
    json.dump(data, open(file, 'w', encoding="utf-8"), ensure_ascii=True, **kwargs)


class Logger(object):
    """ [日志类，logging 模块的封装]

        Attributes:
            class:
                Default_Name     str                    缺省的日志名
            instance:
                _logger          logging.Logger         logging 的 Logger 对象
    """
    Default_Name = __name__

    def __init__(self, name=None):
        self._logger = logging.getLogger(name or self.Default_Name)
        self._logger.setLevel(logging.DEBUG)
        self._logger.addHandler(self.__get_console_headler())
        self._logger.addHandler(self.__get_file_handler())

    @staticmethod
    def __get_console_headler():
        """ 控制台输出 handler """
        console_headler = logging.StreamHandler()
        console_headler.setLevel(logging.DEBUG)
        console_headler.setFormatter(logging.Formatter("[%(levelname)s] %(name)s, %(asctime)s, %(message)s", "%H:%M:%S"))
        return console_headler

    @staticmethod
    def __get_file_handler():
        """ 文件输出 handler ，只输出错误日志 """
        file = "%s.error.log".format() % time.strftime("%Y-%m-%d", time.localtime(time.time()))
        file_headler = logging.FileHandler(os.path.join(Log_Dir, file), encoding="utf-8")
        file_headler.setLevel(logging.ERROR)
        file_headler.setFormatter(logging.Formatter("[%(levelname)s] %(name)s, %(asctime)s, %(message)s", "%Y-%m-%d %H:%M:%S"))
        return file_headler

    """
        以下是对 logging 的五种 level 输出函数的封装
        并定义 __call__ = logging.info
    """
    def debug(self, *args, **kwargs):
        return self._logger.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        return self._logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        return self._logger.warning(*args, **kwargs)

    def exception(self, *args, **kwargs):
        return self._logger.exception(*args, **kwargs)

    def error(self, *args, **kwargs):
        return self._logger.error(*args, **kwargs)

    def critical(self, *args, **kwargs):
        return self._logger.critical(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.info(*args, **kwargs)


class Config(object):
    """ [配置文件类，configparser 模块的封装]

        Attibutes:
            ini        str                            配置文件的文件名
            __config   configparser.RawConfigParser   config 类的实例
    """
    def __init__(self, ini=None):
        file = os.path.join(Config_Dir, ini)
        if not os.path.exists(file):
            raise NoConfigFileError("config file '%s' is missing !" % ini)
        else:
            self.ini = ini
            self.__config = RawConfigParser(allow_no_value=True)
            self.__config.read(file, encoding="utf-8-sig")

    def __getitem__(self, key):
        """ 内部实例 __config 的 __getitem__ 方法的传递

            Args:
                key    str                   section 名称
            Returns:
                configparser.SectionProxy    section 字典
            Raises:
                NoConfigSectionError         未找到 section
        """
        try:
            return self.__config[key]
        except KeyError:
            raise NoConfigSectionError("[%s] section '%s' is missing !" % (self.ini, key))


    def sections(self):
        """ 内部实例 __config 的 section 方法的传递

            Returns:
                list    section 名称的列表
        """
        return self.__config.sections()

    def __get(self, get_fn, section, option, **kwargs):
        """ config.get 方法的模板函数

            Args:
                get_fn     function    具体的 get 函数
                section    str         section 名称
                option     str         option 名称
                **kwargs               传递给 get 函数
            Returns:
                value      str/int/float/bool    根据特定 get 函数返回相应 option 值
            Raises:
                NoConfigSectionError   未找到 section
                NoConfigOptionError    未找到 option
        """
        try:
            return get_fn(section, option, **kwargs)
        except NoSectionError:
            raise NoConfigSectionError("[%s] section '%s' is missing !" % (self.ini, section))
        except NoOptionError:
            raise NoConfigOptionError("[%s] option '%s' in section '%s' is missing !" % (self.ini, option, section))

    """
        下面是对 get/getint/getfloat/getboolean 四种 config.get 函数的封装
    """
    def get(self, section, option):
        return self.__get(self.__config.get, section, option)

    def getint(self, section, option):
        return self.__get(self.__config.getint, section, option)

    def getfloat(self, section, option):
        return self.__get(self.__config.getfloat, section, option)

    def getboolean(self, section, option):
        return self.__get(self.__config.getboolean, section, option)


class Stack(object):
    """ 堆栈类 """

    def __init__(self, *args):
        self._items = list(args)

    def size(self):
        """ 堆栈内元素个数
        """
        return len(self._items)

    def empty(self):
        """ 判断你是否为空
        """
        return self.size() == 0

    def push(self, item):
        """ 压入一个元素
        """
        self._items.append(item)

    def pop(self):
        """ 弹出一个元素
        """
        if self.empty():
            raise StackEmptyError("no element !")
        return self._items.pop()

    def peek(self):
        """ 查看下一个被弹出元素
        """
        if self.empty():
            return None
        return self._items[-1]
