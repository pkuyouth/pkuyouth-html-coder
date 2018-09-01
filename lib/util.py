#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: util.py
#
# 通用的 function / class
#


import os
import sys
import logging
import hashlib
from configparser import RawConfigParser, NoSectionError, NoOptionError


try:
    import simplejson as json
except (ImportError, SystemError):
    import json

from error import NoConfigFileError, NoConfigOptionError, NoConfigSectionError


Root_Dir = os.path.join(os.path.dirname(__file__), '../') # 文件夹根目录
Config_Dir = os.path.join(Root_Dir, "config/") # 配置文件夹


__all__ = [

    'json_load',
    'json_dump',
    'MD5',

    'Logger',
    'Config',
]



def __to_hash(hashlib_fn, data):
    """ hashlib 函数的通用模板

        Args:
            hashlib_fn    function    hashlib 的函数接口
            data          bytes/str/int/float    待 hash 化的数据
        Returns:
            str     32 位的 MD5 hash 值
        Raises:
            TypeError     data 类型非法
    """
    if isinstance(data, bytes):
        pass
    elif isinstance(data, (str, int, float)):
        data = str(data).encode('utf-8')
    else:
        raise TypeError('unsupported type %s' % type(data))
    return hashlib_fn(data).hexdigest()


""" hashlib.md5 函数的封装

    Args:
        data    bytes/str/int/float    待 hash 化的数据
    Returns:
        str     32 位的 MD5 hash 值
    Raises:
        TypeError     data 类型非法
"""
MD5 = lambda data: __to_hash(hashlib.md5, data)



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
    return json.load(open(file, 'r'), **kwargs)

def json_dump(folder, filename, data, **kwargs):
    """ json.dump 函数的封装

        Args:
            folder      str      文件夹路径
            filename    str      文件名
            data        object
            **kwargs             传给 json.dump 函数的参数，例如 indent = 4
    """
    file = os.path.join(folder, filename)
    json.dump(data, open(file, 'w'), ensure_ascii=True, **kwargs)



class Logger(object):
    """ [日志类，logging 模块的封装]

        Attributes:
            class:
                Default_Name     str                    缺省的日志名
            instance:
                logger           logging.Logger         logging 的 Logger 对象
                format           logging.Formatter      日志格式
                console_headler  logging.StreamHandler  控制台日志 handler
    """

    Default_Name = 'htmlcoder'

    def __init__(self, name=None):
        self.logger = logging.getLogger(name or self.Default_Name)
        self.logger.setLevel(logging.DEBUG)
        self.add_handler(self.console_headler)

    @property
    def format(self):
        fmt = ("[%(levelname)s] %(name)s, %(asctime).19s, %(message)s", "%H:%M:%S")
        return logging.Formatter(*fmt)

    @property
    def console_headler(self):
        console_headler = logging.StreamHandler(sys.stdout)
        console_headler.setLevel(logging.DEBUG)
        console_headler.setFormatter(self.format)
        return console_headler

    def add_handler(self, handler):
        """ logging.addHander 函数的封装，非重复地添加 handler

            Args:
                handler    logging.Handler    logging 的 Handler 对象
            Returns:
                None
        """
        for hd in self.logger.handlers:
            if hd.__class__.__name__ == handler.__class__.__name__:
                return # 不重复添加
        self.logger.addHandler(handler)

    """
        以下是对 logging 的五种 level 输出函数的封装
        并定义 __call__ = logging.info
    """

    def debug(self, *args, **kwargs):
        return self.logger.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        return self.logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        return self.logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        return self.logger.error(*args, **kwargs)

    def critical(self, *args, **kwargs):
        return self.logger.critical(*args, **kwargs)

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
            self.__config.read(file, encoding="utf-8")

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
