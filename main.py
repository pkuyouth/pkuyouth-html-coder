#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: main.py
# modified: 2019-03-30

import os
import re
import time
from lxml import etree
from collections import deque
from htmlcoder.core.tags import *
from htmlcoder.core.docx import DocxParser
from htmlcoder.core.client import TietukuClient
from htmlcoder.core.utils.log import cout, ferr
from htmlcoder.core.const import INPUT_DIR, OUTPUT_DIR, OUTPUT_SRC_DIR, STATIC_DIR
from htmlcoder.core.exceptions import HTMLCoderError


def _get_docx_file(folder=INPUT_DIR):
    """
    返回目标文件夹下修改日期最新的 docx 文件路径

    Args:
        folder    str    目标文件夹路径，此处即为输入文件夹路径
    Return:
        file      str    docx 文件路径
    """
    files = [os.path.join(folder, f) for f in os.listdir(folder)]
    files.sort(key=lambda f: os.path.getmtime(f), reverse=True)
    for file in files:
        filename = os.path.basename(file)
        if not os.path.isdir(file) and os.path.splitext(filename)[1] == '.docx':
            return file
    else:
        raise HTMLCoderError("在 %s 下未找到任何 *.docx 文件" % os.path.abspath(folder))


docx = DocxParser(file=_get_docx_file())
client = TietukuClient()

imgLinks = {}  # rId -> links 的映射


def task_upload_images():
    """
    上传 docx 文件内的插图
    """
    for id_, file in docx.images.items():
        imgBytes = docx.read(file)
        filename = os.path.basename(file)
        links = client.upload(filename, imgBytes)
        imgLinks[id_] = links


def task_upload_illustrations():
    """
    上传通用的插图
    """
    ILLUSTRATIONS = ("editornote","reporternote")  # 插图文件名 basename

    for filename in os.listdir(STATIC_DIR):
        key, ext = os.path.splitext(filename)
        if key in ILLUSTRATIONS:
            with open(os.path.join(STATIC_DIR, filename), "rb") as fp:
                imgBytes = fp.read()
            links = client.upload(filename, imgBytes)
            imgLinks[key] = links


def is_bold(p):
    """
    判断当前段落是否为加粗段
    """

    def _real_is_bold(ele):
        """
        从 xml 中判断是否为加粗段
        真正用来判断传入元素是否将该段落定义为加粗

        Return:
            bool/None    如果没有找到 w:b 字段，则返回 None 否则 bool
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

    bold = False # 默认为 False
    w_ns = "{%s}" % p.nsmap['w']
    for eStyle in p.xpath('.//w:pStyle | .//w:rStyle', namespaces=p.nsmap):
        styleId = eStyle.get(w_ns+'val')
        eStyle = docx.styles[styleId]
        _bold = _real_is_bold(eStyle)
        bold = _bold if _bold is not None else bold
    _bold = _real_is_bold(p)
    return _bold if _bold is not None else bold # 如果 p 定义了加粗则返回 p 的定义，否则返回 style 的定义


def get_align(p):
    """
    获得当前段落的对齐方式

    Return:
        align    str    返回值有 left/right/justify ...
    """

    def _real_get_align(ele):
        """
        从 document.xml 中判断当前段落的对齐方式

        Return:
            align    str/None    无 w:jc 返回 None ，否则 left/right/justify ...
        """
        jc = ele.xpath('.//w:pPr/w:jc', namespaces=ele.nsmap) # w:jc 位于 w:pPr 内
        if jc == []:
            return None
        else: # w:pPr 类似于 p 标签属性，段内唯一
            w_ns = "{%s}" % ele.nsmap['w']
            return jc[0].get(w_ns+'val') # 因此，如果找到，则必定只有一个

    align = "left" # 默认左对齐
    w_ns = "{%s}" % p.nsmap['w']
    for eStyle in p.xpath('.//w:pStyle', namespaces=p.nsmap): # w:jc 位于 w:pStyle 内
        styleId = eStyle.get(w_ns+'val')
        eStyle = docx.styles[styleId]
        align = _real_get_align(eStyle) or align
    return _real_get_align(p) or align


def DBC_to_SBC(text):
    """
    转义 半角竖线/半角空格 -> 全角竖线/全角空格
    """
    rules = (
        (" ", "\u3000"), #全角空格
        ("|", "\uFF5C"), #全角竖线
        )
    for DBC, SBC in rules:
        text = SBC.join(w for w in text.split(DBC) if w != '') # 合并连续空格
    return text


def find_img(p):
    """
    获得当前段落的图片节点
    因为不同版本 word 编码出的 docx 中，对于图片的定义方式差别较大，因此这里单独将其列出
    """
    return p.xpath('.//w:drawing//*[@r:embed] | .//w:pict//*[@r:id]', namespaces=p.nsmap)


def get_img_src(p):
    """
    获得当前段落中图片的外链
    """
    imgs = find_img(p)  # 应当唯一
    r_ns = "{%s}" % p.nsmap['r']
    rIds = set(img.get(r_ns+'embed') or img.get(r_ns+'id') for img in imgs)  # 可能有多个图片，但可能是相同的 rId，代表同一张图
    imgSHA1s = set(imgLinks[rId]["sha1"] for rId in rIds) # 或是不同 rId，但是指向的图片相同，此处通过 sha1 校验
    if len(imgSHA1s) > 1: # 不允许多张图共存于一行
        raise HTMLCoderError("不可以将 %s 张图片置于同一段落内" % len(imgSHA1s))
    return imgLinks[rIds.pop()]["url"]


def is_next_to_img(p):
    """
    判断当前段落之前是否是图片段
    用于判断图片间是否相邻，如果相邻，则不空行
    """
    ps = docx.paragraphs
    for i in range(p.getparent().index(p)-1, -1, -1): # 从当前节点开始往前找
        _p = ps[i] # 注意！ __ps 和 p.getparent() 的匹配结果数不同！这会导致索引错误！
        if _p is p: # 由于原始 parent 必定多余 p 标签，因此此处多做一次校验，如果不是就往前寻找
            continue
        elif _p.text: # 是正文段
            return False
        elif find_img(_p) != []: # 无字，但找到图，说明相邻
            return True
        else:
            continue
    return False # 找到头都是空行，这种情况理论上不会发生，因为并不会将图片放在文档开头


regex_comment  = re.compile(r"^[#|＃]") # 匹配注释 # ...
regex_param    = re.compile(r"^[@|＠]\s*(\S+)\s*=\s*(\S+).*$", re.I) # 匹配参数设置符 @ key = value
regex_zone     = re.compile(r"^\s*{%\s*(\S+)\s*%}.*$", re.I) # 匹配区域定义符 {% xxx %}
regex_zoneEnd  = re.compile(r"^END(\S+)$") # 匹配 {% ENDxxxx %} ，大小写敏感

## 常数 ##
ZONES          = ("ignore", "reporter", "body", "ending", "editornote", "reporternote", "reference")
PARAMS         = ("Count_Picture")
TRUE_VALUES    = ("True", "true", "1")
FALSE_VALUES   = ("False", "false", "0")

## 参数 ##
Count_Word     = True
Count_Picture  = False

## 过程变量 ##
head           = HeadBox()                 # 开头部分 box
body           = BodyBox()                 # 正文部分 box
ending         = EndingBox()               # 结尾部分 box
reporter       = ReporterBox()             # 记者信息 box
editorNote     = EditorNoteBox()           # 编者按 box
reporterNote   = ReporterNoteBox()         # 记者手记 box
reference      = ReferenceBox()            # 参考文献框 box
count          = CountBox()                # 字数统计框 box
html           = HTML(title=docx.filename) # 整体 HTML 文档
wordSum        = 0                         # 字数统计
pictSum        = 0                         # 图片统计
zoneSt         = deque()                   # 区域符堆栈
inPreviousZone = True                      # 是否尚未进入任何区域


def handle_param(p):
    """
    参数定义符
    """
    global inPreviousZone
    key, value = regex_param.match(p.text).group(1,2)
    if not inPreviousZone:
        raise HTMLCoderError("'必须要在 *.docx 文档的头部定义参数 %r" % key)
    if key not in PARAMS:
        raise HTMLCoderError("未知的参数名 %r" % key)
    if value in TRUE_VALUES:
        exec("global %s" % key)
        exec("%s = True" % key)
        if key == "Count_Picture":
            global Count_Word
            Count_Word = False  # 特别指定 Count_Pictrue 与 Count_Word 互斥
    elif value in FALSE_VALUES:
        exec("global %s" % key)
        exec("%s = False" % key)
    else:
        raise HTMLCoderError("参数 %r 的值只能设为 %s 或 %s" % (key, TRUE_VALUES, FALSE_VALUES) )


def handle_zone(p):
    """
    区域定义符
    """
    global inPreviousZone
    zoneText = regex_zone.match(p.text).group(1)
    if regex_zoneEnd.match(zoneText): # 区域结尾
        zone = regex_zoneEnd.match(zoneText).group(1)
        if zone not in ZONES: # 非法区域
            raise HTMLCoderError("未知的区域名 %r <- {%% %s %%}" % (zone, zoneText) )
        if len(zoneSt) == 0: # 不在任何区域内
            raise HTMLCoderError("意外的 {%% END%s %%}, 当前不处在任何区域内" % zone)
        elif zoneSt[-1] != "ignore" and zone != zoneSt[-1]: # 不配对
            raise HTMLCoderError("{%% END%s %%} 与当前区域 %r 不匹配" % (zone, zoneSt[-1]) )
        elif zoneSt[-1] == "ignore" and zone != "ignore":
            pass
        else:
            item = zoneSt.pop() # 离开该区域
    else: # 区域开始
        zone = zoneText
        if zone not in ZONES: # 非法区域
            raise HTMLCoderError("未知的区域名 %r <- {%% %s %%}" % (zone, zoneText) )
        elif len(zoneSt) > 0 and zoneSt[-1] == "ignore":
            pass
        else:
            zoneSt.append(zone) # 进入该区域
            inPreviousZone = False # 已进入其他区域


def handle_reporter(p):
    """
    记者信息
    """
    if p.text: # 记者信息，需转义半角
        if is_bold(p): #加粗，为记者信息标题
            reporter + Br() + PRpt(DBC_to_SBC(p.text), bold=True) # 前加一行，其后不空行
        else:
            reporter + PRpt(DBC_to_SBC(p.text)) # 其后不空行
    else:
        pass


def handle_body(p):
    """
    正文段
    """
    global wordSum, pictSum
    if find_img(p) != []: # 先找图
        if is_next_to_img(p):
            body - Br + Img(get_img_src(p)) + Br() # 连续图片不空行
        else:
            body + Img(get_img_src(p)) + Br()
        pictSum += 1
    elif p.text:
        if is_bold(p): # 加粗定义的标题
            body + H1(p.text) + Br()
        else:
            align = get_align(p)
            if align == 'center': # 图注
                body - Br + ImgNote(NSyb(), span(p.text)) + Br() # 先减删去前一空行
            elif align == 'right': # 右引用
                body + PRNote(p.text) + Br()
            else: # 左对齐/两端对齐，正文
                body + P(p.text) + Br()
        wordSum += len(p.text) # 正文段的文字计入字数统计
    else:
        pass


def handle_ending(p):
    """
    文末段
    """
    if p.text: # 所有文字均视为尾注
        ending + PEndNote(DBC_to_SBC(p.text)) # 不空行
    else:
        pass


def handle_editornote(p):
    """
    编者按
    """
    if p.text:
        align = get_align(p)
        if align == "right": # 记者署名
            editorNote + PRNote(p.text) + Br()
        else: # 其他是正文
            editorNote + P(p.text) + Br()
    else:
        pass


def handle_reporternote(p):
    """
    记者手记
    """
    if p.text:
        align = get_align(p)
        if align == "right": # 记者署名
            reporterNote + PRNote(p.text) + Br()
        else: # 其他是正文
            reporterNote + P(p.text) + Br()
    else:
        pass


def handle_ref(p):
    """
    参考文献
    """
    if p.text:
        if is_bold(p): # 标题
            reference + PRef(R16(p.text))
        else:
            reference + PRef(p.text)
    else:
        pass



def main():

    global Count_Word, Count_Picture, wordSum, pictSum


    ## 上传资源 ##
    task_upload_images()
    task_upload_illustrations()


    ## 初步编码 ##
    for p in docx.paragraphs:
        p.text = ''.join(t.text for t in p.xpath('.//w:t', namespaces=p.nsmap)).strip() # 段落正文，写入属性

        ## 按段落类型情况分类处理 ##
        if regex_comment.match(p.text): # 先匹配注释
            continue
        elif regex_param.match(p.text): # 匹配参数定义符
            handle_param(p)
        elif regex_zone.match(p.text):  # 再匹配区域定义符
            handle_zone(p)
        elif len(zoneSt) == 0: # 当前不在任何区域内
            pass
        else:
            top = zoneSt[-1]
            if top == 'ignore': # 处在忽略段落
                pass
            elif top == 'reporter': # 记者信息是唯一需要自定义的头部信息
                handle_reporter(p)
            elif top == 'body':
              handle_body(p)
            elif top == 'ending':
                handle_ending(p)
            elif top == 'editornote':
                handle_editornote(p)
            elif top == 'reporternote':
                handle_reporternote(p)
            elif top == 'reference':
                handle_ref(p)
            else: # 非注释，非区域定义符，堆栈非空，但不能匹配任何一种情况
                raise Exception # 这种情况不应该出现


    ## 校验过程变量合理性 ##
    if len(zoneSt) > 0: # 区域未闭合
        raise HTMLCoderError("区域符未闭合，缺失 {%% end%s %%}" % zoneSt[-1])

    if all([Count_Picture, Count_Word]): # 校验参数合理性
        raise HTMLCoderError("不能同时输出文字统计信息和图片统计信息")


    ## 构造记者信息 ##
    if len(reporter) > 2: # 含有除了标题外的其他元素，由于标题前还有空行，故最小值为 2
        head + reporter


    ## 构造字数统计框 ##
    if Count_Word:
        """
        计算规则：
            + 600 字   ->  + 1 分钟
        """
        readTime = (wordSum + 300) // 600  # 每 600字 （四舍五入）

        count + PCount(span("全文共"),
                       R16(wordSum),
                       span("字，阅读大约需要"),
                       R16(readTime),
                       span("分钟。"))

    elif Count_Picture:
        """
        计算规则：
            0  ~ 20 图  ->    3 分钟
            20 ~ 30 图  ->    4 分钟
                 30 图  ->    5 分钟
            > 30 图：
               + 20 图  ->  + 1 分钟
        """
        if 0 <= pictSum < 20:
            readTime = 3
        elif 20 <= pictSum < 30:
            readTime = 4
        elif pictSum == 30:
            readTime = 5
        else: #图片数量多于30
            readTime = 5 + (pictSum - 31) // 20

        count + PCount(span("全文共"),
                       R16(pictSum),
                       span("张图，阅读大约需要"),
                       R16(readTime),
                       span("分钟。"))

    if Count_Word or Count_Picture:  # 可以都为 False ，则都不构造
        head.insert(count, Br()) # 头插一行


    ## 完成 head-box 的构造 ##
    head.insert(Br()) # 头插一行留放顶图
    head.append(PHr(Hr()))  # 构造分割线


    ## 构造参考文献框 ##
    if len(reference) > 1: # 含有除了标题外的其他元素
        ending.insert(Br(), reference) # 先插一行

    ending + Br() # 最后插一行


    ## 先构造记者手记 ##
    if reporterNote.has_child():
        reporterNote.insert(Img(imgLinks["reporternote"]["url"])) # 记者手记四个字
        reporterNote + PHr(Hr()) # 加一条分割线


    ## 再构造编者按 ##
    if editorNote.has_child():
        editorNote.insert(Img(imgLinks["editornote"]["url"])) # 编者按三个字
        editorNote + PHr(Hr()) # 加一条分割线


    ## 最后合并 box ，构造 HTML 文档 ##
    html + WrapBox(head)
    if editorNote.has_child():
        html + WrapBox(editorNote)
    if reporterNote.has_child():
        html + WrapBox(reporterNote)
    html + WrapBox(body) + WrapBox(ending)


    ## 输出文件 ##
    file = '%s.html' % docx.filename
    with open(os.path.join(OUTPUT_SRC_DIR, file), 'w', encoding='utf-8') as fp:
        fp.write(html.print_out())

    with open(os.path.join(STATIC_DIR, "preview.template.html"), "r", encoding="utf-8-sig") as rfp:
        with open(os.path.join(OUTPUT_DIR, file), "w", encoding="utf-8") as wfp:
            wfp.write(rfp.read().format(
                title = docx.filename,
                src = "./src/%s" % file,
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                ))

    cout.info('Build %s in %s' % (file, os.path.abspath(OUTPUT_DIR))) # 打日志



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt: # Ctrl + C 则正常退出，不写日志
        pass
    except Exception as e:
        ferr.exception(e)
        raise e
