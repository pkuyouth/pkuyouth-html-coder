#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: tags.py
#
# 自定义的 HTML 节点类
#


from lxml import etree
from lxml.builder import E

from util import Config


config = Config('style.ini')


__all__ = [
    'span',\
    'Br','Hr','Img','H1','R15','R16','NSyb',\
    'P','PRNote','ImgNote','PEndNote','PCount','PRpt','PRef','PHr',\
    'HeadBox','BodyBox','TailBox','CountBox','RefBox','WrapBox',\
    'HTML',\
]


class Node(object):
    ''' [基础的 DOM 节点类]

        Methods:
            render      返回与该节点模型等价的 lxml.etree._Element 对象
                return    lxml.etree._Element
            print_out   以特定的 lxml.etree.tostring 函数输出的 html ，utf-8 编码
                return    str
    '''
    def __init__(self, *args, **kwargs):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError

    def print_out(self):
        raise NotImplementedError

    def __str__(self):
        return self.print_out()


class Text(Node):
    """ [文字节点类]
    """
    def __init__(self, text, *args, bold=False):
        """
            Args:
                text    str     文字内容
                *args           无意义，为了保证 bold 为 kwargs
                bold    bool    是否加粗
        """
        if isinstance(text, (str,int,float)):
            self.text = str(text)
            self.bold = bold
        else:
            raise TypeError("invalid type '%s' for Text Node !" % type(text))

    def render(self):
        """ 渲染成对应的 lxml 对象

            Returns:
                bold = True   =>  lxml.etree._Element
                bold = False  =>  str
        """
        if not self.bold:
            return self.text
        else:
            return E('strong', self.text)

    def print_out(self, **kwargs):
        """ 渲染成 html 文档输出

            Args:
                **kwargs    传入 lxml.etree.tostring ，例如 pretty_print = True
            Returns:
                str         html 字符串，utf-8 编码
        """
        ele = self.render()
        return ele if isinstance(ele, str) \
            else etree.tostring(ele, method='html', encoding='UTF-8', **kwargs).decode('utf-8')


class Tag(Node):
    """ [DOM 标签节点类]

        Attributes:
            class:
                tag       str    标签名
                class_    str    标签类名
            instance:
                attrib    dict   标签属性值，包含 class 和 style
                children  list   以 Node 为基础类定义的子节点列表
    """


    tag = ''
    class_ = ''


    def __init__(self, *args, bold=False):
        """
            Args:
                *args    str / Node   顺序添加的子节点
                bold     bool         是否加粗，传给所有 Text 节点
        """
        if self.__class__ == Tag: # 是 Tag 类
            raise NotImplementedError
        else:
            self.attrib = {} if self.class_ == '' else {
                "class": self.class_,
                "style": ' '.join('%s: %s;' % (k,v) for k,v in config[self.class_].items()),
            }
            self.children = []
            for child in args:
                self.append(child, bold=bold)


    def __to_child_node(self, child, *args, bold=False):
        """ 将 __init__ 传入节点解析为 Node 节点

            Args:
                child   str / Node   子节点
                *args                无意义，为了保证 bold 为 kwargs
                bold    bool         是否加粗，对应传给 Text 节点
            Returns:
                Node  返回一个 Node 对象
        """
        if isinstance(child, Node):
            return child
        elif isinstance(child, (str,int,float)):
            return Text(child, bold=bold)
        else:
            raise TypeError("children of Tag must be a (int,str,float) or Node type, not %s !" % type(child))


    def insert(self, *args, index=0, bold=False):
        """ 类似于 list.insert ，在 children 列表中特定位置顺序添加若干子节点

            Args:
                *args   str / Node   顺序添加的子节点
                index   int          插入点索引值
                bold    bool         是否加粗，对应传给 Text 节点
            Returns:
                self    Node         返回本身，用于进行连续操作
        """
        for child in args:
            self.children.insert(index, self.__to_child_node(child, bold=bold))
        return self


    def append(self, *args, bold=False):
        """ 类似于 list.append ，在 children 列表后顺序插入若干子节点

            Args:
                *args   str / Node   顺序添加的子节点
                bold    bool         是否加粗，对应传给 Text 节点
            Returns:
                self    Node         返回本身，用于进行连续操作
        """
        for child in args:
            self.children.append(self.__to_child_node(child, bold=bold))
        return self


    def pop(self, node=None):
        """ 类似于 list.pop ，从 children 列表中删除特定类型的 Node

            Args:
                node    None / class Node    需要删除的节点类型，如果为 None 则删除 children 列表最后一个节点
            Returns:
                self    Node                 返回本身，用于进行连续操作
        """
        if node is None:
            self.children.pop()
        else:
            if not issubclass(node, Node):
                raise TypeError("'node' must be a subclass of Node, not a '%s' type !" % type(node))
            else:
                for (idx, _node) in enumerate(reversed(self.children)):
                    if _node.__class__ == node:
                        self.children.pop(-idx-1)
                        return self


    def __add__(self, child):
        """ 操作符 + 重载，append 的快捷方式

            Args:
                *args   str / Node   顺序添加的子节点
                bold    bool         是否加粗，对应传给 Text 节点
            Returns:
                self    Node         返回本身，用于进行连续操作
        """
        return self.append(child)


    def __sub__(self, node=None):
        """ 操作符 - 重载，pop 的快捷方式

            Args:
                node    None / class Node    需要删除的节点类型，如果为 None 则删除 children 列表最后一个节点
            Returns:
                self    Node                 返回本身，用于进行连续操作
        """
        return self.pop(node=node)


    def render(self):
        """ 渲染成对应的 lxml 对象

            Returns:
                lxml.etree._Element
        """
        return E(self.tag, self.attrib, *list(child.render() for child in self.children))


    def print_out(self, **kwargs):
        """ 渲染成 html 文档输出

            Args:
                **kwargs    传入 lxml.etree.tostring ，例如 pretty_print = True
            Returns:
                str         html 字符串，utf-8 编码
        """
        return etree.tostring(self.render(), method='html', encoding='UTF-8', **kwargs).decode('utf-8')


"""
    以下是继承于 Tag 类定义的 HTML Tag 类

    div, section, span, br, img

    其中 section == div （这是因为微信不允许使用 div 标签，所有之后统一用 section 代替 div）

"""

class div(Tag):
    tag = 'section'

class section(Tag):
    tag = 'section'

class span(Tag):
    tag = 'span'

class br(Tag):
    tag = 'br'

class img(Tag):
    tag = 'img'

    def __init__(self, src):
        """
            Args:
                src    str    图片链接
        """
        super().__init__()
        self.attrib["src"] = src


"""
    以下是根据我们公号的推送文章特点定义的 HTML 组件类

    每一组件以 class_ 为 ID
    下面给出个各类的意义，你可以在 style.ini 中找到相同的描述

    div-head        开头部分的 box
    div-body        正文部分的 box
    div-tail        文末部分的 box
    div-count       字数统计框的 box
    div-ref         参考文献框的 box
    div-wrap        水印框的 box （最外层的 section 会被公号去掉 style ，所以这里做一层皮）

    p-normal        正文段落
    p-right-note    右对齐的引用段落
    p-image-note    图注段落
    p-end-note      尾注（微信编辑之类信息）段落
    p-count         字数统计框的文字段落
    p-reporter      记者信息的段落
    p-reference     参考文献的段落
    p-br            空行段落
    p-hr            分割线段落
    p-h1            大标题段落
    p-img           图片段落
    span-red-15     15号加粗红字（参考文献框的标题）
    span-red-16     16号加粗红字（统计框的数字）
    span-note-syb   图注前的红三角
    hr              分割线

"""

class Br(section):
    class_ = 'p-br'

    def __init__(self):
        super().__init__()
        self.children = [br(),]


class P(section):
    class_ = 'p-normal'

class PRNote(section):
    class_ = 'p-right-note'

class ImgNote(section):
    class_ = 'p-image-note'

class PEndNote(section):
    class_ = 'p-end-note'

class PCount(section):
    class_ = 'p-count'

class PRpt(section):
    class_ = 'p-reporter'

class PRef(section):
    class_ = 'p-reference'

class H1(section):
    class_ = 'p-h1'

class Img(section):
    class_ = 'p-img'

    def __init__(self, src):
        super().__init__()
        self.children = [img(src),]

class PHr(section):
    class_ = 'p-hr'

class Hr(section):
    class_ = 'hr'

class R15(span):
    class_ = 'span-red-15'

class R16(span):
    class_ = 'span-red-16'

class NSyb(span):
    class_ = 'span-note-syb'

    def __init__(self):
        super().__init__()
        self.children = [Text('△'),]


class HeadBox(section):
    class_ = 'div-head'

class BodyBox(section):
    class_ = 'div-body'

class TailBox(section):
    class_ = 'div-tail'

class RefBox(section):
    class_ = 'div-ref'

class CountBox(section):
    class_ = 'div-count'

class WrapBox(section):
    class_ = 'div-wrap'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrib['powered-by'] = 'rabbit'


"""
    特殊的组件，HTML 文档的模板组件
"""


class HTML(Tag):
    """
        Attributes:
            title    str    文档的标题
    """

    tag = 'html'

    def __init__(self, *args, title='html-coder', **kwargs):
        """
            Args:
                *args              同 Tag 的定义
                **kwargs           同 Tag 的定义
                title       str    文档的标题
        """
        super().__init__(*args, **kwargs)
        self.title = title


    def render(self):
        """ 额外渲染了基础 HTML 模板"""
        return E.html(
                E.head(
                    E.mata({"charset": "utf-8"}),
                    E.title(self.title),
                ),
                E.body(
                    *list(child.render() for child in self.children)
                ),
            )

    def print_out(self, **kwargs):
        """ 额外设定了一个 doctype 参数"""
        return etree.tostring(self.render(), method='html', \
            encoding='UTF-8', doctype='<!DOCTYPE html>', **kwargs).decode('utf-8')