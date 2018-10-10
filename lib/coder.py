#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: lib/coder.py
#
# Docx 文档的解析类 / HTML 文档的编码类
#

import os
import re
from datetime import date
from zipfile import ZipFile
from lxml import etree

from tags import *
from utils import Logger, Config, Stack
from errors import (
        ContradictoryZoneError, UnmatchZoneError, UnregisteredZoneError, MultiCountConflictError,
        StaticServerTypeError, IllustrationTypeError, MultiPictureConflictError, ParamKeyError,
        ParamValueError, ParamDefineTooLateError
    )


Root_Dir = os.path.join(os.path.dirname(__file__), '../')   # 项目根目录
Illustration_Dir = os.path.join(Root_Dir, "illustration/")  # 插图目录


__all__ = ['HTMLCoder',]


class DocxParser(object):
    """ [docx 文档解析类]
        用于解压和解析 docx 中的关键 xml 文件，为 HTMLCoder 类提供信息

        Attributes:
            class:
                logger                  Logger            日志实例
                config                  Config            配置文件实例
                illustration            tuple             统一插图（编者按/记者手记）
            instance:
                staticServer            StaticAPI         静态文件 api 类的实例
                docx                    zipfile.ZipFile   docx 文件的 zipfile 对象
                imgLinks                dict              存放 docx 文档中图片的外链信息
                styleMap                dict              存放 docx 文档中样式表信息
                documentXml             bytes             记录 docx 文档结构的 xml 文件
                filename                str               去扩展名的 docx 文件名
                Output_Dir              str               HTML 文档的生成目录
            Raises:
                StaticServerTypeError   非法的静态服务器类型
    """
    logger = Logger('docxparser')
    config = Config('coder.ini')
    illustration = ("editornote","reporternote")

    def __init__(self, file, output, **kwargs):
        """
            Args:
                file        str      docx 文件的路径
                output      str      html 文档的输出路径
                **kwargs             来自命令行的参数设置
        """

        self.logger.info('parse %s' % os.path.abspath(file)) # 打日志

        self.Output_Dir = output
        self.staticServer = self.__get_static_server(kwargs.get('static_server_type'))
        self.docx = ZipFile(file)
        self.imgLinks = self.__get_img_links()
        self.styleMap = self.__get_style_map()
        self.filename = os.path.basename(self.docx.filename)
        self.documentXml = self.docx.read("word/document.xml")

    def __get_static_server(self, static_server_type=None):
        """ 确定图床类型，构造图床实例
        """
        sType = static_server_type or self.config.get('static.server', 'type')
        if sType == 'SM.MS':
            from smms import SMMSAPI as StaticAPI
        elif sType == 'Tietuku':
            from tietuku import TietukuAPI as StaticAPI
        elif sType == 'Elimage':
            from elimage import ElimageAPI as StaticAPI
        else:
            raise StaticServerTypeError("no such static server '%s' !" % sType)
        return StaticAPI()

    def __get_img_links(self):
        """ 构造 imgLinks 属性

            Raises:
                IllustrationTypeError    未注册的插图类型
        """
        imgLinks = {}

        """ 上传文内图片 """
        root = etree.fromstring(self.docx.read("word/_rels/document.xml.rels"))
        for eRel in root.findall("Relationship", namespaces=root.nsmap):
            if eRel.get('Target')[:11] != 'media/image':
                continue
            else:
                _id, target = eRel.get('Id'), eRel.get('Target')
                file = 'word/' + target # ZipFile 内部路径统一为 '/' 连接，此处不可用 os.path.join 连接，否则可能由于系统不同导致路径
                imgBytes = self.docx.read(file)
                filename = os.path.basename(file)
                links = self.staticServer.upload(filename, imgBytes, log=True)
                imgLinks[_id] = links

        """ 上传通用插图 """
        for filename in os.listdir(Illustration_Dir):
            key, ext = os.path.splitext(filename)
            if key not in self.illustration:
                raise IllustrationTypeError("unregisted illustration type '%s' !" % key)
            with open(os.path.join(Illustration_Dir, filename), "rb") as fp:
                imgBytes = fp.read()
            links = self.staticServer.upload(filename, imgBytes, log=True)
            imgLinks[key] = links

        return imgLinks

    def __get_style_map(self):
        styleMap = {}
        root = etree.fromstring(self.docx.read("word/styles.xml"))
        for eStyle in root.findall("w:style", namespaces=root.nsmap):
            ns_w = "{%s}" % root.nsmap['w']
            styleId = eStyle.get(ns_w+'styleId')
            styleMap[styleId] = eStyle
        return styleMap

    """
        以下函数用于通过 imgLinks 映射表获取信息

        Args:
            rId       str    图片在 docx 文件中的 id
        Returns:
            result    str    图片的相应数据
    """

    def get_img_src(self, rId):
        """ 获得图片外链
        """
        return self.imgLinks[rId]['url']

    def get_img_md5(self, rId):
        """ 获得图片 md5 值
        """
        return self.imgLinks[rId]['md5']

    def get_img_sha1(self, rId):
        """ 获得图片 sha1 值
        """
        return self.imgLinks[rId]['sha1']



class HTMLCoder(object):
    """ [HTML 文档编码类]

        Attributes:
            class:
                logger           Logger              日志实例
                config           Config              配置文件实例
                zones            tuple               注册的合法区域
                params           tuple               注册合法参数名
                trueValues       tuple               注册参数真值
                falseValues      tuple               注册参数非真值
                regex_comment    _sre.SRE_Pattern    正则表达式，匹配注释
                regex_param      _sre.SRE_Pattern    正则表达式，匹配参数设置符
                regex_zone       _sre.SRE_Pattern    正则表达式，匹配区域定义符
                regex_zoneEnd    _sre.SRE_Pattern    正则表达式，匹配区域结尾定义符
            instance:
                docx             DocxParser          DocxParser 实例
                filename         str                 去拓展名的 docx 文件名
                Output_Dir       str                 HTML 文档的生成目录
                Count_Word       bool                编码参数：是否统计字数，不可与 Count_Picture 同时为 True
                Count_Picture    bool                编码参数：是否统计图片，不可与 Count_Word 同时为 True
    """
    logger = Logger('htmlcoder')
    config = Config('coder.ini')

    zones = ("ignore","reporter","body","ending","editornote","reporternote","reference")
    params = ("No_Reporter","Count_Picture")
    trueValues = ("True","true","1")
    falseValues = ("False","false","0")

    regex_comment = re.compile(r"^[#|＃]") # 匹配注释 # ...
    regex_param = re.compile(r"^[@|＠]\s*(\S+)\s*=\s*(\S+).*$", re.I) # 匹配参数设置符 @ key = value
    regex_zone = re.compile(r"^\s*{%\s*(\S+)\s*%}.*$", re.I) # 匹配区域定义符 {% xxx %}
    regex_zoneEnd = re.compile(r"^END(\S+)$") # 匹配 {% ENDxxxx %} ，大小写敏感

    def __init__(self, file, output, **kwargs):
        """
            Args:
                file      str      docx 文件的路径
                output    str      html 文档的输出路径
                **kwargs           来自命令行的参数设置
            Raises:
                MultiCountConflictError    同时统计字数和图片数
        """

        self.docx = DocxParser(file, output=output, **kwargs)
        self.filename = os.path.splitext(self.docx.filename)[0]
        self.Output_Dir = output

        """ 编码参数"""

        if kwargs.get('count_picture'):
            self.Count_Word = False
            self.Count_Picture = True
        else:
            self.Count_Word = self.config.getboolean('params', 'count_word')
            self.Count_Picture = self.config.getboolean('params', 'count_picture')

        """ 过程变量"""
        self.__head = HeadBox()                  # 开头部分 box
        self.__body = BodyBox()                  # 正文部分 box
        self.__ending = EndingBox()              # 结尾部分 box
        self.__reporter = ReporterBox()          # 记者信息 box
        self.__editorNote = EditorNoteBox()      # 编者按 box
        self.__reporterNote = ReporterNoteBox()  # 记者手记 box
        self.__reference = ReferenceBox()        # 参考文献框 box
        self.__count = CountBox()                # 字数统计框 box
        self.__html = HTML(title=self.filename)  # 整体 HTML 文档
        self.__wordSum = 0                       # 字数统计
        self.__pictSum = 0                       # 图片统计
        self.__zoneSt = Stack()                  # 区域符堆栈
        self.__inPreZone = True                  # 是否尚未进入任何区域

    """
        Args:
            以下所有参数 p, ele, ...    均为 docx 段落的 lxml.etree._Element
    """

    def __is_bold(self, p):
        """ 判断当前段落是否为加粗段，同时考虑样式表的定义和段落内定义

            Returns:
                True/False    bool
        """
        bold = False # 默认为 False
        w_ns = "{%s}" % p.nsmap['w']
        for eStyle in p.xpath('.//w:pStyle | .//w:rStyle', namespaces=p.nsmap):
            styleId = eStyle.get(w_ns+'val')
            eStyle = self.docx.styleMap[styleId]
            _bold = self.__real_is_bold(eStyle)
            bold = _bold if _bold is not None else bold
        _bold = self.__real_is_bold(p)
        return _bold if _bold is not None else bold # 如果 p 定义了加粗则返回 p 的定义，否则返回 style 的定义

    def __real_is_bold(self, ele):
        """ 真正用来判断传入元素是否将该段落定义为加粗

            Returns:
                True/False/None    bool/None    如果没有找到 w:b 字段，则返回 None 否则 bool
        """
        bs = ele.xpath('.//w:rPr/w:b', namespaces=ele.nsmap) # w:b 位于 w:rPr 内
        if bs == []:
            return None
        else: # 还需判断其 w:val 是否为 'false'
            ns_w = "{%s}" % ele.nsmap['w']
            bold = True # 默认为 True
            for b in bs: # w:rPr 类似于 span 标签，一段内不一定唯一，但此处只考虑最后一个 w:b
                val = b.get(ns_w+'val')
                bold = False if val == 'false' else True
            return bold

    def __get_align(self, p):
        """ 获得当前段落的对齐方式，同时考虑样式表定义和段落内定义

            Returns:
                align    str    返回值有 left/right/justify ...
        """
        align = "left" # 默认左对齐
        w_ns = "{%s}" % p.nsmap['w']
        for eStyle in p.xpath('.//w:pStyle', namespaces=p.nsmap): # w:jc 位于 w:pStyle 内
            styleId = eStyle.get(w_ns+'val')
            eStyle = self.docx.styleMap[styleId]
            align = self.__real_get_align(eStyle) or align
        return self.__real_get_align(p) or align

    def __real_get_align(self, ele):
        """ 真正用来判断当前段落

            Returns:
                align    str/None    无 w:jc 返回 None ，否则 left/right/justify ...
        """
        jc = ele.xpath('.//w:pPr/w:jc', namespaces=ele.nsmap) # w:jc 位于 w:pPr 内
        if jc == []:
            return None
        else: # w:pPr 类似于 p 标签属性，段内唯一
            w_ns = "{%s}" % ele.nsmap['w']
            return jc[0].get(w_ns+'val') # 因此，如果找到，则必定只有一个

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

    def __find_img(self, p):
        """ 获得当前段落的图片节点

            因为不同版本 word 编码出的 docx 中，对于图片的定义方式差别较大，因此这里单独将其列出

            Returns:
                None  or  list => [lxml.etree._Element,]     lxml.etree.xpath 的搜索结果
        """
        return p.xpath('.//w:drawing//*[@r:embed] | .//w:pict//*[@r:id]', namespaces=p.nsmap)

    def __get_img_src(self, p):
        """ 获得当前段落图片的外链

            这里对应于上一个获得图片的函数

            Returns:
                src    str    当前段落图片的外链
            Raises:
                MultiPictureConflictError    多行图片共存一行
        """
        imgs = self.__find_img(p) # 实际上应该唯一
        r_ns = "{%s}" % p.nsmap['r']
        rIds = set(img.get(r_ns+'embed') or img.get(r_ns+'id') for img in imgs) # 可能有多个图片，但可能是相同的 rId，代表同一张图
        imgsSHA1 = set(self.docx.get_img_sha1(rId) for rId in rIds) # 或是不同 rId，但是指向的图片相同，此处通过 sha1 校验
        if len(imgsSHA1) > 1: # 不允许多张图共存于一行
            raise MultiPictureConflictError("don't place %s pictrues in the same paragraph !" % len(imgsSHA1))
        else:
            return self.docx.get_img_src(rIds.pop())

    def __is_next_to_img(self, p):
        """ 判断当前段落之前是否是图片段

            用于判断图片间是否相邻，如果相邻，则不空行

            Returns:
                True / False    bool
        """
        for i in range(p.getparent().index(p)-1, -1, -1): # 从当前节点开始往前找
            _p = self.__ps[i] # 注意！ __ps 和 p.getparent() 的匹配结果数不同！这会导致索引错误！
            if _p is p: # 由于原始 parent 必定多余 p 标签，因此此处多做一次校验，如果不是就往前寻找
                continue
            elif _p.text: # 是正文段
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
            return (self.__wordSum + 300) // 600 # 每 600字 （四舍五入）
        elif self.Count_Picture:
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
            elif self.regex_param.match(p.text): # 匹配参数定义符
                self.__handle_param(p)
            elif self.regex_zone.match(p.text):  # 再匹配区域定义符
                self.__handle_zone(p)
            elif self.__zoneSt.empty(): # 当前不在任何区域内
                pass
            elif self.__zoneSt.peek() == 'ignore': # 处在忽略段落
                pass
            elif self.__zoneSt.peek() == 'reporter': # 记者信息是唯一需要自定义的头部信息
                self.__handle_reporter(p)
            elif self.__zoneSt.peek() == 'body':
                self.__handle_body(p)
            elif self.__zoneSt.peek() == 'ending':
                self.__handle_ending(p)
            elif self.__zoneSt.peek() == 'editornote':
                self.__handle_editornote(p)
            elif self.__zoneSt.peek() == 'reporternote':
                self.__handle_reporternote(p)
            elif self.__zoneSt.peek() == 'reference':
                self.__handle_ref(p)
            else: # 非注释，非区域定义符，堆栈非空，但不能匹配任何一种情况
                raise Exception # 这种情况不应该出现

        """校验过程变量合理性"""
        if not self.__zoneSt.empty(): # 区域未闭合
            raise ContradictoryZoneError("{%% end%s %%} is missing" % self.__zoneSt.peek())

        if all([self.Count_Picture, self.Count_Word]): # 校验参数合理性
            raise MultiCountConflictError("you can't count words and pictures at the same time !")

        """构造记者信息"""
        if len(self.__reporter) > 2: # 含有除了标题外的其他元素，由于标题前还有空行，故最小值为 2
            self.__head + self.__reporter

        """构造字数统计框"""
        if self.Count_Word:
            self.__count + PCount(span("全文共"), R16(self.__wordSum), span("字，阅读大约需要"),\
                 R16(self.__get_read_time()), span("分钟。"))
        elif self.Count_Picture:
            self.__count + PCount(span("全文共"), R16(self.__pictSum), span("张图，阅读大约需要"),\
                 R16(self.__get_read_time()), span("分钟。"))
        if self.Count_Word or self.Count_Picture: # 可以都不选，则都不构造
            self.__head.insert(self.__count, Br()) # 头插一行

        """完成 head-box 的构造"""
        self.__head.insert(Br()) # 头插一行留放顶图
        self.__head.append(PHr(Hr()))  # 构造分割线

        """构造参考文献框"""
        if len(self.__reference) > 1: # 含有除了标题外的其他元素
            self.__ending.insert(Br(), self.__reference) # 先插一行

        self.__ending + Br() # 最后插一行

        """先构造记者手记"""
        if self.__reporterNote.has_child():
            self.__reporterNote.insert(Img(self.docx.get_img_src("reporternote"))) # 记者手记四个字
            self.__reporterNote + PHr(Hr()) # 加一条分割线

        """再构造编者按"""
        if self.__editorNote.has_child():
            self.__editorNote.insert(Img(self.docx.get_img_src("editornote"))) # 编者按三个字
            self.__editorNote + PHr(Hr()) # 加一条分割线

        """最后合并 box ，构造 HTML 文档"""
        self.__html + WrapBox(self.__head)
        if self.__editorNote.has_child():
            self.__html + WrapBox(self.__editorNote)
        if self.__reporterNote.has_child():
            self.__html + WrapBox(self.__reporterNote)
        self.__html + WrapBox(self.__body) + WrapBox(self.__ending)

    def __handle_zone(self, p):
        """ 区域定义符段 """
        zoneText = self.regex_zone.match(p.text).group(1)
        if self.regex_zoneEnd.match(zoneText): # 区域结尾
            zone = self.regex_zoneEnd.match(zoneText).group(1)
            if zone not in self.zones: # 非法区域
                raise UnregisteredZoneError("unregisted zone '%s' in {%% %s %%}" % (zone, zoneText))
            elif self.__zoneSt.empty(): # 不在任何区域内
                raise ContradictoryZoneError("unexpected {%% END%s %%} , not in any zone now !" % zone)
            elif self.__zoneSt.peek() != "ignore" and zone != self.__zoneSt.peek(): #不配对
                raise UnmatchZoneError("{%% END%s %%} doesn't match current zone '%s' !" % (zone, self.__zoneSt.peek()))
            else:
                if self.__zoneSt.peek() == "ignore" and zone != "ignore":
                    pass
                else:
                    item = self.__zoneSt.pop() # 离开该区域
                    # self.logger.debug("<- %s" % item)
        else: # 区域开始
            zone = zoneText
            if zone not in self.zones: # 非法区域
                raise UnregisteredZoneError("unregisted zone '%s' in {%% %s %%}" % (zone, zoneText))
            else:
                if self.__zoneSt.peek() == "ignore":
                    pass
                else:
                    # self.logger.debug("-> %s" % zone)
                    self.__zoneSt.push(zone) # 进入该区域
                    self.__inPreZone = False # 已进入其他区域

    def __handle_param(self, p):
        """ 参数定义符 """
        key, value = self.regex_param.match(p.text).group(1,2)
        if not self.__inPreZone:
            raise ParamDefineTooLateError("you should define param '%s' at the beginning of the *.docx document !" % key)
        if key not in self.params:
            raise ParamKeyError("unregisted param '%s' !" % key)
        if value in self.trueValues:
            self.__setattr__(key, True)
            if key == "Count_Picture":
                self.Count_Word = False # 特别指定 Count_Pictrue 与 Count_Word 互斥
        elif value in self.falseValues:
            self.__setattr__(key, False)
        else:
            raise ParamValueError("set param '%s' to %s or %s" % (key, self.trueValues, self.falseValues))

    def __handle_reporter(self, p):
        """ 记者信息 """
        if p.text: # 记者信息，需转义半角
            if self.__is_bold(p): #加粗，为记者信息标题
                self.__reporter + Br() + PRpt(self.__to_SBC_case(p.text), bold=True) # 前加一行，其后不空行
            else:
                self.__reporter + PRpt(self.__to_SBC_case(p.text)) # 其后不空行
        else:
            pass

    def __handle_body(self, p):
        """ 正文段 """
        if self.__find_img(p) != []: # 先找图
            if self.__is_next_to_img(p):
                self.__body - Br + Img(self.__get_img_src(p)) + Br() # 连续图片不空行
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
            self.__wordSum += len(p.text) # 正文段的文字计入字数统计
        else:
            pass

    def __handle_ending(self, p):
        """ 文末段 """
        if p.text: # 所有文字均视为尾注
            self.__ending + PEndNote(self.__to_SBC_case(p.text)) # 不空行
        else:
            pass

    def __handle_editornote(self, p):
        """ 编者按 """
        if p.text:
            align = self.__get_align(p)
            if align == "right": # 记者署名
                self.__editorNote + PRNote(p.text) + Br()
            else: # 其他是正文
                self.__editorNote + P(p.text) + Br()
        else:
            pass

    def __handle_reporternote(self, p):
        """ 记者手记 """
        if p.text:
            align = self.__get_align(p)
            if align == "right": # 记者署名
                self.__reporterNote + PRNote(p.text) + Br()
            else: # 其他是正文
                self.__reporterNote + P(p.text) + Br()
        else:
            pass

    def __handle_ref(self, p):
        """ 参考文献 """
        if p.text:
            if self.__is_bold(p): # 标题
                self.__reference + PRef(R15(p.text))
            else:
                self.__reference + PRef(p.text)
        else:
            pass

    def work(self):
        """ 编码的外部接口函数 """
        self.__code()

        file = '%s.html' % self.filename
        with open(os.path.join(self.Output_Dir, file), 'w', encoding='utf-8') as fp:
            fp.write(self.__html.print_out())

        self.logger.info('build %s in %s' % (file, os.path.abspath(self.Output_Dir))) # 打日志

