#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: run.py


import sys
sys.path.append('../lib/')

import os
from datetime import datetime

from util import Config
from tietuku import TietukuAPi
from coder import HTMLCoder
from error import NoDocxFileError


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
	for file in sorted(os.listdir(folder), key=lambda f: os.path.getmtime(f), reverse=True):
		if not os.path.isdir(file) and os.path.splitext(file)[1] == '.docx':
			return file
		else:
			continue
	raise NoDocxFileError('*.docx file is missing in %s !' % os.path.abspath(folder))


def main():

	htmlcoder = HTMLCoder(file=__get_docx_file(), output=Build_Dir)
	htmlcoder.work()

	with open(os.path.join(Static_Dir, "preview.template.html"), "r") as rfp:
		with open(os.path.join(Build_Dir, "preview.html"), "w") as wfp:
			wfp.write(rfp.read().format(
				title = htmlcoder.filename,
				src = "./%s.html" % htmlcoder.filename,
				timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
			))


if __name__ == '__main__':
	main()

