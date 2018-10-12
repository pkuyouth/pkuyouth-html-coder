#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: main.py


__author__  = "Rabbit"
__version__ = "1.1.0"
__date__    = "2018.10.12"


import sys
sys.path.append('../lib/')

import os
from datetime import datetime
from optparse import OptionParser, OptionGroup

from coder import HTMLCoder
from utils import Config, Logger
from errors import NoDocxFileError


logger = Logger("main")

Root_Dir = os.path.join(os.path.dirname(__file__), '../')   # 项目根目录
Static_Dir = os.path.join(Root_Dir, "static/")              # 静态文件夹
Project_Dir = os.path.join(Root_Dir, "project/")            # 工程文件夹
Build_Dir = os.path.join(Project_Dir, 'build/')             # 输出文件夹


def __get_docx_file(folder=Project_Dir):
    """ 返回目标文件夹下修改日期最新的 docx 文件路径

        Args:
            folder    str    目标文件夹路径，此处即为工程文件夹路径
        Returns:
            file      str    docx 文件路径
        Raises:
            NoDocxFileError  未找到任何 docx 文件
    """
    for file in sorted(os.listdir(folder), key=lambda file: os.path.getmtime(file), reverse=True):
        if not os.path.isdir(file) and os.path.splitext(file)[1] == '.docx':
            return file
        else:
            continue
    raise NoDocxFileError('*.docx file is missing in %s !' % os.path.abspath(folder))


def main(**kwargs):

    htmlcoder = HTMLCoder(file=__get_docx_file(), output=Build_Dir, **kwargs)
    htmlcoder.work()

    with open(os.path.join(Static_Dir, "preview.template.html"), "r", encoding="utf-8-sig") as rfp:
        with open(os.path.join(Build_Dir, "preview.html"), "w", encoding="utf-8") as wfp:
            wfp.write(rfp.read().format(
                title = htmlcoder.filename,
                src = "./%s.html" % htmlcoder.filename,
                timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
            ))


if __name__ == '__main__':

    parser = OptionParser(
        version="HTMLCoder %s" % __version__,
        description="HTMLCoder -- A small tool that can convert a '*.docx' file to a '*.html' file, which is in accord with PKUyouth's style.")

    group_base = OptionGroup(parser,
            title="Base Options")
    group_base.add_option("-s", "--static", dest="static_server_type", metavar="TYPE",
                                help="Type of static server. Options: ['Tietuku','SM.MS','Elimage']")

    group_coding_params = OptionGroup(parser,
            title="Parameters of Coding Process",
            description="Or will use default setting from 'config/coder.ini' file.")
    group_coding_params.add_option("--count-picture", action="store_true", dest="count_picture",
                                        help="Output picture's sum. (Default: False)")

    parser.add_option_group(group_base)
    parser.add_option_group(group_coding_params)

    options, args = parser.parse_args()


    try:
        main(**options.__dict__)
    except Exception as err:
        logger.exception(err)
        # raise err
