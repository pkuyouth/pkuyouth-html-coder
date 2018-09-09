#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: coder.py
#
# Docx 文档的解析类 / HTML 文档的编码类
#


import os
import re
from datetime import date
from zipfile import ZipFile
from lxml import etree

from tags import *
from util import MD5, Logger, Config
from error import ContradictoryZoneError, UnmatchZoneError, UnregisteredZoneError, \
                    MultiCountError, StaticServerTypeError


Root_Dir = os.path.join(os.path.dirname(__file__), '../') # 项目根目录


__all__ = ['HTMLCoder',]



class DocxParser(object):
    """ [docx 文档解析类]
        用于解压和解析 docx 中的关键 xml 文件，为 HTMLCoder 类提供信息

        Attributes:
            class:
                logger                  Logger            日志实例
                config                  Config            配置文件实例
            instance:
                __static                  StaticAPI         静态文件 api 类的实例
                __docx                  zipfile.ZipFile   docx 文件的 zipfile 对象
                __imgMap                dict              存放 docx 文档中图片信息的映射
                                                          rId: {
                                                              filename: MD5文件名
                                                              target: 图片在 docx 中的文件路径
                                                              links: 文件外链
                                                          }
                documentXml             bytes             记录 docx 文档结构的 xml 文件
                filename                str               去扩展名的 docx 文件名
                Output_Dir              str               HTML 文档的生成目录
                Extract_Pict            bool              附加参数：是否按顺序解压图片
            Raises:
                StaticServerTypeError   非法的静态服务器类型
    """

    logger = Logger('docxparser')
    config = Config('coder.ini')


    def __init__(self, file, output, **kwargs):
        """
            Args:
                file        str      docx 文件的路径
                output      str      html 文档的输出路径
                **kwargs             来自命令行的参数设置
        """

        self.logger.info('parse %s' % os.path.abspath(file)) # 打日志

        self.Output_Dir = output
        self.Extract_Pict = kwargs.get('extract_picture') or False
        self.__static = self.__get_static_server(kwargs.get('static_server_type'))
        self.__docx = ZipFile(file)
        self.__imgMap = self.__get_img_map()
        self.documentXml = self.__docx.read("word/document.xml")


    @property
    def filename(self):
        return os.path.basename(self.__docx.filename)


    def __get_static_server(self, static_server_type=None):
        """ 确定图床类型，构造图床实例
        """
        sType = static_server_type or self.config.get('static.server', 'type')
        if sType == 'SM.MS':
            from smms import SMMSAPI
            return SMMSAPI()
        elif sType == 'Tietuku':
            from tietuku import TietukuAPI
            return TietukuAPI()
        elif sType == 'Elimage':
            from elimage import ElimageAPI
            return ElimageAPI()
        else:
            raise StaticServerTypeError("no such static server '%s' !" % sType)

    def __get_img_map(self):
        """ 构造 imgMap 属性
        """
        imgMap = {}
        tree = etree.fromstring(self.__docx.read("word/_rels/document.xml.rels"))
        for rel in tree.findall("Relationship", namespaces=tree.nsmap):
            if rel.get('Target')[:11] != 'media/image':
                continue
            else:
                _id, target = rel.get('Id'), rel.get('Target')
                file = 'word/' + target # ZipFile 内部路径统一为 '/' 连接，此处不可用 os.path.join 连接，否则可能由于系统不同导致路径
                imgBytes = self.__docx.read(file)

                if self.Extract_Pict: # 解压到 images/ 目录
                    imgId, ext = os.path.splitext(os.path.basename(target))
                    imgId = imgId[5:].zfill(3)  # 去掉 image 前缀, 补齐 3 位数
                    imgFile = "{date}_{idx}{ext}".format(date=date.strftime(date.today(),"%y%m%d"),idx=imgId,ext=ext)
                    imagesDir = os.path.abspath(os.path.join(self.Output_Dir, "images/"))
                    if not os.path.exists(imagesDir):
                        os.mkdir(imagesDir)
                    with open(os.path.join(imagesDir, imgFile),"wb") as fp:
                        fp.write(imgBytes)
                    self.logger.info("extract image %s to %s" % (imgFile, imagesDir))

                filename = MD5(imgBytes) + os.path.splitext(file)[1]
                links = self.__static.upload(filename, imgBytes, log=True)
                imgMap[_id] = {"target": target, "filename": filename, "links": links}
        return imgMap


    def get_img_src(self, rId):
        """ 获得图片外链

            Args:
                rId         str    图片在 docx 文件中的 id
            Returns:
                src         str    图片外链
        """
        return self.__imgMap[rId]['links']['url']



class HTMLCoder(object):
    """ [HTML 文档编码类]

        Attributes:
            class:
                logger           Logger              日志实例
                config           Config              配置文件实例
                zones            tuple               注册的合法区域
                regex_comment    _sre.SRE_Pattern    正则表达式，匹配注释
                regex_zone       _sre.SRE_Pattern    正则表达式，匹配区域定义符
                regex_zoneEnd    _sre.SRE_Pattern    正则表达式，匹配区域结尾定义符
            instance:
                docx             DocxParser          DocxParser 实例
                filename         str                 去拓展名的 docx 文件名
                Output_Dir       str                 HTML 文档的生成目录
                No_Rpt           bool                编码参数：是否有记者信息
                No_Ref           bool                编码参数：是否有参考文献
                Count_Word       bool                编码参数：是否统计字数，不可与 Count_Pict 同时为 True
                Count_Pict       bool                编码参数：是否统计图片，不可与 Count_Word 同时为 True
    """

    logger = Logger('htmlcoder')
    config = Config('coder.ini')

    zones = ("head","body","tail")

    regex_comment = re.compile(r"^#") # 匹配注释
    regex_zone = re.compile(r"^[ ]*{%[ ]*(\S+)[ ]*%}.*$", re.I) # 匹配区域定义符 {% xxx %}
    regex_zoneEnd = re.compile(r"^end(\S+)$", re.I) # 匹配 {% endxxxx %}


    def __init__(self, file, output, **kwargs):
        """
            Args:
                file      str      docx 文件的路径
                output    str      html 文档的输出路径
                **kwargs           来自命令行的参数设置
            Raises:
                MultiCountError    同时统计字数和图片数
        """

        self.docx = DocxParser(file, output=output, **kwargs)
        self.filename = os.path.splitext(self.docx.filename)[0]
        self.Output_Dir = output

        """ 编码参数"""
        self.No_Rpt = kwargs.get('no_reporter') or self.config.getboolean('params', 'no_reporter')
        self.No_Ref = kwargs.get('no_reference') or self.config.getboolean('params', 'no_reference')
        self.Count_Word = kwargs.get('count_word') or self.config.getboolean('params', 'count_word')
        self.Count_Pict = kwargs.get('count_picture') or self.config.getboolean('params', 'count_picture')

        """ 过程变量"""
        self.__head = HeadBox()                  # 开头部分 box
        self.__body = BodyBox()                  # 正文部分 box
        self.__tail = TailBox()                  # 结尾部分 box
        self.__ref = RefBox()                    # 参考文献框 box
        self.__count = CountBox()                # 字数统计框 box
        self.__html = HTML(title=self.filename)  # 整体 HTML 文档
        self.__wordSum = 0                       # 字数统计
        self.__pictSum = 0                       # 图片统计
        self.__nowZone = ''                      # 当前所在区域名称

        if all([self.Count_Pict, self.Count_Word]): # 校验参数合理性
            raise MultiCountError("you can't count words and pictures at the same time !")

    """
        Args:
            以下所有参数 p    均为 docx 段落的 lxml.etree._Element
    """

    def __is_bold(self, p):
        """ 判断当前段落是否为加粗段

            Returns:
                True / False    bool
        """
        b = p.xpath('.//w:b', namespaces=p.nsmap)
        if b == []:
            return False
        else:
            ns_w = "{%s}" % p.nsmap['w']
            val = b[0].get(ns_w+'val')
            return True if val is None or val != 'false' else False


    def __to_SBC_case(self, text):
        """ 转义 半角竖线/半角空格 => 全角竖线/全角空格

            Args:
                text    str    段落正文
            Returns:
                text    str    转以后的段落正文
        """
        rules = (
            (" ", "\u3000"), #全角空格
            ("|", "\uFF5C"), #全角竖线
        )
        for DBC, SBC in rules:
            text = SBC.join(w for w in text.split(DBC) if w != '') # 合并连续空格
        return text


    def __get_align(self, p):
        """ 获得当前段落的 对齐方式

            Returns:
                align    str    返回值有 left/right/justify ...
        """
        jc = p.xpath('.//w:jc', namespaces=p.nsmap)
        if jc == []:
            return 'left' # 默认左对齐
        else:
            w_ns = "{%s}" % p.nsmap['w']
            return jc[0].get(w_ns+'val')


    def __find_img(self, p):
        """ 获得当前段落的图片节点

            因为不同版本 word 编码出的 docx 中，对于图片的定义方式差别较大，因此这里单独将其列出

            Returns:
                None  or  list => [lxml.etree._Element,]     lxml.etree.xpath 的搜索结果
        """
        return p.xpath('.//w:drawing | .//w:pict', namespaces=p.nsmap)


    def __get_img_src(self, p):
        """ 获得当前段落图片的外链

            这里对应于上一个获得图片的函数

            Returns:
                src    str    当前段落图片的外链
        """
        img = self.__find_img(p)[0]
        r_ns = "{%s}" % p.nsmap['r']
        if p.xpath('.//w:drawing', namespaces=p.nsmap):
            rId = img.xpath('.//*[@r:embed]', namespaces=p.nsmap)[0].get(r_ns+'embed')
        elif p.xpath('.//w:pict', namespaces=p.nsmap):
            rId = img.xpath('.//*[@r:id]', namespaces=p.nsmap)[0].get(r_ns+'id')
        return self.docx.get_img_src(rId)


    def __is_next_to_img(self, p):
        """ 判断当前段落之前是否是图片段

            用于判断图片间是否相邻，如果相邻，则不空行

            Returns:
                True / False    bool
        """
        for i in range(p.getparent().index(p)-1, -1, -1): # 从当前节点开始往前找
            _p = self.__ps[i]
            if _p.text: # 是正文段
                return False
            elif self.__find_img(_p) != []: # 无字，但找到图，说明相邻
                return True
            else:
                continue
        return False # 找到头都是空行，这种情况理论上不会发生，因为并不会将图片放在文档开头


    def __get_read_time(self):
        """ 根据统计结果计算阅读时间，用于填充字数统计框

            规则：
                正文： + 600 字    =>  + 1 分钟
                图片： 0  ~ 20 图  =>    3 分钟
                      20 ~ 30 图  =>    4 分钟
                           30 图  =>    5 分钟
                      > 30 图：
                         + 20 图  =>  + 1 分钟
            Returns:
                read_time    int    阅读时间
        """
        if self.Count_Word:
            return self.__wordSum // 600 # 每 600字
        elif self.Count_Pict:
            if 0 <= self.__pictSum < 20:
                return 3
            elif 20 <= self.__pictSum < 30:
                return 4
            elif self.__pictSum == 30:
                return 5
            else: #图片数量多于30
                return 5 + (self.__pictSum - 31) // 20


    def __code(self):
        """ 解析和编码的主函数

            Raises:
                UnregisteredZoneError     未注册的区域名
                ContradictoryZoneError    区域信息冲突
                UnmatchZoneError          区域名不匹配
        """
        document = etree.fromstring(self.docx.documentXml)
        self.__ps = document.xpath('//w:p', namespaces=document.nsmap) # 保存一下，用于搜索图片

        """初步编码"""
        for p in self.__ps:
            p.text = ''.join(t.text for t in p.xpath('.//w:t', namespaces=p.nsmap)).strip() # 段落正文，写入属性

            """按段落类型情况分类处理"""
            if self.regex_comment.match(p.text): # 先匹配注释
                continue
            elif self.regex_zone.match(p.text):  # 再匹配区域定义符
                self.__handle_zone(p)
            elif self.__nowZone == 'head':
                self.__handle_head(p)
            elif self.__nowZone == 'body':
                self.__handle_body(p)
            elif self.__nowZone == 'tail':
                self.__handle_tail(p)
            else: # 非注释，非区域定义符，且不在任一区域内
                pass

        """校验过程变量合理性"""
        if self.__nowZone: # 区域未闭合
            raise ContradictoryZoneError("{%% end%s %%} is missing" % self.__nowZone)

        """构造字数统计框"""
        if self.Count_Word:
            self.__count + PCount(span("全文共"), R16(self.__wordSum), span("字，阅读大约需要"),\
                 R16(self.__get_read_time()), span("分钟。"))
        elif self.Count_Pict:
            self.__count + PCount(span("全文共"), R16(self.__pictSum), span("张图，阅读大约需要"),\
                 R16(self.__get_read_time()), span("分钟。"))
        if self.Count_Word or self.Count_Pict: # 可以都不选，则都不构造
            self.__head.insert(self.__count, Br()) # 头插一行

        """完成 head-box 的构造"""
        self.__head.insert(Br(), Br()) # 头插两行留放顶图
        self.__head.append(PHr(Hr()))  # 构造分割线

        """构造参考文献框"""
        if not self.No_Ref:
            self.__tail.insert(Br(), Br(), self.__ref) # 先插两行

        """最后合并三个 box ，构造 HTML 文档"""
        self.__html + WrapBox(self.__head) + WrapBox(self.__body) + WrapBox(self.__tail)


    def __handle_zone(self, p):
        """ 区域定义符段的处理函数 """
        zoneText = self.regex_zone.match(p.text).group(1).lower()
        if self.regex_zoneEnd.match(zoneText): # 区域结尾
            zone = self.regex_zoneEnd.match(zoneText).group(1)
            if zone not in self.zones: # 非法区域
                raise UnregisteredZoneError("unregisted zone %s in {%% %s %%}" % (zone, zoneText))
            elif not self.__nowZone: # 不在该区域内
                raise ContradictoryZoneError("unexpected {%% end%s %%} , not in any zone now !" % zone)
            elif zone != self.__nowZone: #不配对
                raise UnmatchZoneError("{%% end%s %%} doesn't match current zone %s !" % (zone, self.__nowZone))
            else:
                self.__nowZone = '' # 离开该区域
        else: # 区域开始
            zone = zoneText
            if zone not in self.zones: # 非法区域
                raise UnregisteredZoneError("unregisted zone %s in {%% %s %%}" % (zone, zoneText))
            elif self.__nowZone: # 仍在其他区域内
                raise ContradictoryZoneError("{%% end%s %%} is missing above {%% %s %%}" % (self.__nowZone, zone))
            else:
                self.__nowZone = zone # 进入该区域


    def __handle_head(self, p):
        """ 开头段的处理函数 """
        if self.No_Rpt: # 开头段只需要处理记者信息，没有记者信息则直接可以跳过
            pass
        elif p.text: # 记者信息，需转义半角
            if self.__is_bold(p): #加粗，为记者信息标题
                self.__head + Br() + PRpt(self.__to_SBC_case(p.text), bold=True) # 前加一行，其后不空行
            else:
                self.__head + PRpt(self.__to_SBC_case(p.text)) # 其后不空行
        else:
            pass


    def __handle_body(self, p):
        """ 正文段的处理函数 """
        if self.__find_img(p) != []: # 先找图
            if self.__is_next_to_img(p):
                self.__body + Img(self.__get_img_src(p)) # 连续图片不空行
            else:
                self.__body + Img(self.__get_img_src(p)) + Br()
            self.__pictSum += 1
        elif p.text:
            align = self.__get_align(p)
            if align == 'center':
                if self.__is_bold(p): # 加粗定义的标题
                    self.__body + H1(p.text) + Br()
                else: # 图注
                    self.__body - Br + ImgNote(NSyb(), span(p.text)) + Br() # 先减删去前一空行
            elif align == 'right': # 右引用
                self.__body + PRNote(p.text) + Br()
            else: # 左对齐/两端对齐，正文
                self.__body + P(p.text) + Br()
            self.__wordSum += len(p.text) # 只有正文段的文字计入字数统计 ！
        else:
            pass


    def __handle_tail(self, p):
        """ 文末段的处理函数"""
        if p.text:
            align = self.__get_align(p)
            if align == 'right': # 尾注，记者信息，需转义
                self.__tail + PEndNote(self.__to_SBC_case(p.text)) # 不空行
            else: # 其余视为左对齐注释和参考文献
                if not self.No_Ref:
                    if self.__is_bold(p): # 标题
                        self.__ref + PRef(R15(p.text))
                    else:
                        self.__ref + PRef(p.text)
                else: # 目前认为已经没有左对齐注释，因此所有非右对齐文字可以直接略过
                    pass
        else:
            pass


    def work(self):
        """ 编码的外部接口函数"""
        self.__code()

        file = '%s.html' % self.filename
        with open(os.path.join(self.Output_Dir, file), 'w', encoding='utf-8') as fp:
            fp.write(self.__html.print_out())

        self.logger.info('build %s in %s' % (file, os.path.abspath(self.Output_Dir))) # 打日志

