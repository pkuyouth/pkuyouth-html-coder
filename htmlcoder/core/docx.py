#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: docx.py
# modified: 2019-03-30
"""
docx 文档解析
"""

__all__ = [

    "DocxParser",

    ]


import os
from zipfile import ZipFile
from lxml import etree
from .utils.log import cout
from .utils.decorator import cached_property
from .const import STATIC_DIR


class DocxParser(object):
    """
    docx 文档解析类
    用于解压和解析 docx 中的关键 xml 文件

    """

    def __init__(self, file):
        cout.info("Parse %s" % file)
        self._docxFile = ZipFile(file)


    def _parse_images(self):
        """
        解析图片在 docx 中的路径

        Return: id(str) -> file(str)
        """
        images = {}
        root = etree.fromstring(self._docxFile.read("word/_rels/document.xml.rels"))
        for eRel in root.findall("Relationship", namespaces=root.nsmap):
            if not eRel.get('Target').startswith('media/image'):
                continue
            id_ = eRel.get('Id')
            target = eRel.get('Target')
            file = 'word/' + target  # 注：ZipFile 内部路径统一为 '/' 连接
            images[id_] = file
        return images


    def _parse_styles(self):
        """
        解析文档样式的映射关系

        Return: id(str) -> eStyle(lxml.etree._Element)
        """
        styles = {}
        root = etree.fromstring(self._docxFile.read("word/styles.xml"))
        for eStyle in root.findall("w:style", namespaces=root.nsmap):
            ns_w = "{%s}" % root.nsmap['w']
            id_ = eStyle.get(ns_w+'styleId')
            styles[id_] = eStyle
        return styles


    def read(self, file):
        """
        ZipFIle.read 函数的代理
        """
        return self._docxFile.read(file)


    @cached_property
    def filename(self):
        """
        去除后缀的文件名
        """
        filename = os.path.basename(self._docxFile.filename)
        return os.path.splitext(filename)[0]

    @cached_property
    def document(self):
        """
        document.xml 的 lxml 对象，记录了文档的内容
        """
        return etree.fromstring(self.read("word/document.xml"))

    @cached_property
    def paragraphs(self):
        """
        document.xml 中所有的 <w:p> 元素
        """
        document = self.document
        return document.xpath('//w:p', namespaces=document.nsmap)

    @cached_property
    def images(self):
        """
        docx 中所有图片的路径
        """
        return self._parse_images()

    @cached_property
    def styles(self):
        """
        docx 中的样式表
        """
        return self._parse_styles()
