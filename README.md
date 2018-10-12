# PKUyouthHTMLCoder

《北大青年》微信推送自动排版小工具 v1.1.0


## 环境配置

通过 [Python 官网](https://www.python.org/downloads/) 下载 Python3 安装包，并以默认方式安装即可。安装成功后，打开命令行，输入 `python3 --version` 或 `python --version` 可看到如下输出结果。
```console
debian-9:~# python3 --version
Python 3.6.6
```

pip3 应该已经默认安装了。打开命令行，输入 `pip3 --version` 可看到如下输出结果。
```console
debian-9:~# pip3 --version
pip 9.0.1 from /usr/lib/python3/dist-packages (python 3.6)
```
如果未找到 pip3 命令，Windows 用户可能需要检查一下 pip3 是否已被添加到系统环境变量中。如果是并未附带安装，请手动安装 pip3 ，例如通过 [pip 官网](https://pip.pypa.io/en/stable/reference/pip_install/) 或 [get-pip.py](https://bootstrap.pypa.io/get-pip.py)，安装过程比价简单就不赘述了。

## 下载项目

直接下载该项目的 [zip 文件包](https://github.com/zhongxinghong/PKUyouthHTMLCoder/archive/master.zip) 并解压。
```console
debian-9:~# wget https://github.com/zhongxinghong/PKUyouthHTMLCoder/archive/master.zip
debian-9:~# unzip master.zip
debian-9:~# mv PKUyouthHTMLCoder-master/ PKUyouthHTMLCoder/
debian-9:~# cd PKUyouthHTMLCoder/
debian-9:~/PKUyouthHTMLCoder# ls
LICENSE  README.md  cache  config  illustration  lib  project  requirements.txt  static
```

## 安装依赖包

该项目依赖于 `requests` 和 `lxml` ，可通过下述命令安装。
```console
debian-9:~# pip3 install requests lxml
```

可选择性安装 `simplejson` 。
```console
debian-9:~# pip3 install simplejson
```

你也可以通过项目根目录中的 `requirements.txt` 来安装指定版本的依赖包。进入项目根目录，运行以下命令即可。
```console
debian-9:~# cd PKUyouthHTMLCoder/
debian-9:~/PKUyouthHTMLCoder# pip3 install -r requirements.txt
```

## 项目文件夹结构

```console
debian-9:~/PKUyouthHTMLCoder# tree
.
├── LICENSE
├── README.md
├── cache                           # 存放贴图库的链接缓存
│   ├── elimage.imageLinks.json
│   ├── sm.ms.imageLinks.json
│   └── tietuku.imageLinks.json
├── config                          # 配置文件目录
│   ├── coder.ini                       # 编码参数配置
│   ├── elimage.ini                     # elimage 图床配置
│   ├── smms.ini                        # SM.MS 图床配置
│   ├── style.css                       # 排版的 css 样式表
│   ├── style.ini                       # 排版的 css 样式配置
│   └── tietuku.ini                     # 贴图库 图床配置
├── illustration                    # 文内通用插图
│   ├── editornote.jpeg                 # “编者按” 三个字
│   └── reporternote.jpeg               # “记者手记” 四个字
├── lib                             # 程序包
│   ├── coder.py                        # 编码主程序
│   ├── elimage.py                      # elimage API
│   ├── error.py                        # 错误类型定义
│   ├── smms.py                         # SM.MS API
│   ├── tags.py                         # DOM 节点定义
│   ├── tietuku.py                      # 贴图库 API
│   └── util.py                         # 通用函数/类
├── log                             # 日志输出目录
├── project                         # 项目目录
│   ├── build                           # 排版结果的输出目录
│   ├── old                             # 存放旧工程
│   ├── main.py                         # 主程序
│   └── template                    # 模板和样例
│       ├── template.concise.docx       # 模板-精简版
│       └── template.docx               # 模板-附排版说明
├── requirements.txt
└── static
    ├── favicon.ico
    └── preview.template.html
```

## 使用方法


### 流程简介

1. 进入 `project` 目录，并将 `template` 目录下的 `template.docx` 或 `template.concise.docx` 模板文件复制到该目录下。
```console
debian-9:~/PKUyouthHTMLCoder/project# cp template/template.docx ./today_prj.docx
debian-9:~/PKUyouthHTMLCoder/project# ls -l
total 20
drwxr-xr-x 2 root root    24 Aug  5 10:21 build
-rwxr-xr-x 1 root root  1633 Aug  5 10:21 main.py
drwxr-xr-x 2 root root    24 Aug  5 10:21 old
drwxr-xr-x 2 root root    46 Aug  5 10:21 template
-rw-r--r-- 1 root root 13718 Aug  5 10:47 today_prj.docx
```

2. 按照模板内写好的规则（详细说明见下方 “模板规则”）将文章排版好，并且 **直接保存**，不要另存为，或是新建一个 \*.docx 文件，然后将模板内容复制进去。

> 由于不同版本的 word 编码的 \*.docx 文件，内部使用的 xml 规则不统一，出于兼容性考虑，请直接使用提供好的 \*.docx 文件来排版，确保使用的是 `Microsoft Word 2007-2013 XML (.docx)` 格式，避免出现兼容性问题。但如果仍发现有排版异常，请及时将其与小哥反馈。

3. 运行 `main.py`，即可完成转码。
```console
debian-9:~/PKUyouthHTMLCoder/project# python3 main.py
[INFO] docxparser, 14:51:08, parse /root/PKUyouthHTMLCoder/project/today_prj.docx
[INFO] tietuku, 14:51:08, uploading image image1.jpeg
[INFO] tietuku, 14:51:09, get image image2.jpeg from cache
[INFO] tietuku, 14:51:09, uploading image image3.jpeg
[INFO] tietuku, 14:51:09, uploading image image4.jpeg
[INFO] tietuku, 14:51:10, uploading image image5.jpeg
[INFO] tietuku, 14:51:11, uploading image image6.jpeg
[INFO] tietuku, 14:51:11, uploading image image7.jpeg
[INFO] tietuku, 14:51:12, uploading image image8.jpeg
[INFO] tietuku, 14:51:13, uploading image reporternote.jpeg
[INFO] tietuku, 14:51:13, uploading image editornote.jpeg
[INFO] htmlcoder, 14:51:14, build today_prj.html in /root/PKUyouthHTMLCoder/project/build
```

4. 完成转码后，将会在 `build` 文件夹中输出 `preview.html` 文件和与你当前项目同名的 `today_prj.html` 文件。
```console
debian-9:~/PKUyouthHTMLCoder/project# cd build/
debian-9:~/PKUyouthHTMLCoder/project/build# ls
preview.html  today_prj.html
```

> 如果程序因错误而异常退出，将会在 `log` 文件夹内记录错误日志。

5. 双击 `preview.html` 可以在浏览器中查看编码结果，你可以根据预览结果返回到 `project` 目录中，重新修改和转码 \*.docx 文件，在浏览器中按 `F5` 刷新，即可实时查看修改结果。

> 程序无法识别在 \*.docx 编辑过程中对图片的旋转处理，因此，需要将图片 **预先旋转** 好后再插入，否则在预览中会出现方向错误的图片。

6. 确保排版结果基本满意后，按 `Ctrl + A` 全选网页 iframe 框中已经排版好的推送预览并按 `Ctrl + C` 复制。登录微信公众号后台，新建一个图文素材，然后按 `Ctrl + V` 粘贴，并确保图片均上传成功。（注：安全起见，请使用宽度不小于 **480 px** 的图片！）

> 请使用 **非IE浏览器** 进行复制操作（推荐使用 **Chrome浏览器** ）！实践证明 IE浏览器 在复制过程中可能存在字符编码错误的问题。
>
> 如果发现部分图片未能成功上传，并不需要全部重新上传。可以直接在公号的素材编辑器中删除上传失败的图片，然后从预览结果中单独选中相应图片，重新复制粘贴到相应位置，即可实现上传。

7. 填写标题、作者、摘要、封面、原文链接等其他相关信息（注意：标题竖线用 **全角**；如果有两个及以上记者，则 ”作者“ 写 **北大青年**，如果只有一个记者，就填那个记者的名字），并 **声明原创**（”文章类别“ 填 **其他**）！然后查看 **预览**，确认无误后准备群发。

> 在编辑器中，可能会发现图片过大，右半截超出编辑器可视范围，这是正常情况，只要在预览中图片能够正常显示即可。

### 参数配置

#### 方法一：通过命令行进行配置

在 `project` 目录下，运行 `main.py -h` 或 `main.py --help` ，可查看参数的说明字段。
```console
debian-9:~/PKUyouthHTMLCoder/project# python3 main.py --help
Usage: main.py [options]

HTMLCoder -- A small tool that can convert a '*.docx' file to a '*.html' file,
which is in accord with PKUyouth's style.

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit

  Base Options:
    -s TYPE, --static=TYPE
                        Type of static server. Options:
                        ['Tietuku','SM.MS','Elimage']

  Parameters of Coding Process:
    Or will use default setting from 'config/coder.ini' file.

    --count-picture     Output picture's sum. (Default: False)
```

#### 参数解释：

- **-s/--static** 选择图片外链服务器（通常使用默认值即可）
- **--count-picture** 统计图片数（默认统计字数）


例如，设置为使用 SM.MS 图床，统计图片数：
```console
debian-9:~/PKUyouthHTMLCoder/project# python3 main.py -s SM.MS --count-picture
```


#### 关于图床：

该项目目前提供了 `Tietuku`, `SM.MS`, `Elimage` 三款免费图床的 API 接口封装，默认使用 `Tietuku` ，因为其上传速度较快，且并发下载速度较快，复制过程中不容易掉图。后两款图床的服务器在境外，相较之下速度较慢。不过需要注意 Tietuku 存在较多限制，比如图片自动过期（7 天）和上传频率限制（<= 100 张/小时）等。本项目对其上传图片的默认缓存时间是 12 小时 。（注：过期不代表推送中的图片过期，推送中的图片一经复制上传成功后将永久有效）


#### 方法二：通过 \*.docx 文档进行配置

为了方便起见，该项目还提供了直接在 \*.docx 文档中配置常用参数的方法。在模板文档上方的参数定义区内已预先设定好了三个支持的参数，其含义同上，如果需要指定相应参数，只需要将相应语句前的注释符 **#** 去掉即可。此处的参数定义优先级高于命令行的参数定义优先级。请确保在 **文案开始前** 的位置就将参数定义完毕。


### 模板规则

#### 符号说明

| Symbol        | Meaning |
| :------------ | :------ |
| #             | 注释符，该行内容全部忽略 |
| @ key = value | 参数设置符 |
| {% xxx %}     | 区域定义符 -- 起始边界 |
| {% ENDxxx %}  | 区域定义符 -- 终止边界 |

#### 区域划分

| Zone         | Range |
| :----------- | :---- |
| ignore       | 忽略该区域内的所有内容 |
| reporter     | 文前部分，包含 记者信息 |
| body         | 正文部分，包含 正文、段落大标题、图片、图注 |
| ending       | 尾注部分，包含 参考资料、尾注（左）、微信编辑、图片来源 |
| editornote   | 编者按 |
| reporternote | 记者手记 |
| reference    | 参考资料 |

#### \*.docx 文档排版样式规定

| Zone             | Component | Style |
| :--------------- | :-------- | :---- |
| **reporter**     | | |
| reporter         | “记者信息”标题 | 加粗，任意对齐 |
| reporter         | “记者信息”正文 | 不加粗，任意对齐，（默认） |
| **body**         | | |
| body             | 正文 | 左对齐/两端对齐，不加粗（默认） |
| body             | 正文（右） | 右对齐，不加粗 |
| body             | 标题 | 加粗，任意对齐 |
| body             | 图片 | 嵌入型版式，**单独成行**（否则同段落的文字将被忽略） |
| body             | 图注 | 居中，不加粗 |
| **ending**       | | |
| ending           | 微信编辑｜图片来源 | 任意格式（建议右对齐） |
| **editornote**   | | |
| editornote       | 正文 | 非右对齐 |
| editornote       | 署名 | 右对齐 |
| **reporternote** | | |
| reporternote     | 正文 | 非右对齐 |
| reporternote     | 署名 | 右对齐 |
| **reference**    | | |
| reference        | “参考资料”标题 | 加粗，任意对齐 |
| reference        | “参考资料”正文 | 不加粗，任意对齐（默认） |

#### 几点说明：

1. \*.docx 文档中的任何多余空行均不会影响实际输出（事实上空行只起到分段作用）。
2. 除以上必要样式外，其他任意样式均不影响实际输出（颜色、字体、字号、斜体、下划线等）。
3. 如果原文档存在修订，请选择`全部接受`。通过选项卡 `审阅 > 修订 > 所有标记/简单标记` ，选择 `接受 > 接受所有修订` 。


### 小贴士

#### 图片导出

有时插图文件体积过大，难以通过复制粘贴自动上传，而需要手动上传。这时可以方便地通过直接解压缩 \*.docx 文件的方式拿到编好号的原图：
```console
debian-9:~/PKUyouthHTMLCoder/project# unzip -d docx_unzip today_prj.docx
Archive:  today_prj.docx
  inflating: docx_unzip/_rels/.rels
  inflating: docx_unzip/word/theme/theme1.xml
  ......
  inflating: docx_unzip/word/settings.xml
  inflating: docx_unzip/word/media/image1.jpeg
  inflating: docx_unzip/word/media/image4.jpeg
  inflating: docx_unzip/word/media/image3.jpeg
  inflating: docx_unzip/word/media/image2.jpeg
  inflating: docx_unzip/word/media/image5.jpeg
  inflating: docx_unzip/word/media/image6.jpeg
  inflating: docx_unzip/word/media/image7.jpeg
  inflating: docx_unzip/word/media/image8.jpeg
  inflating: docx_unzip/word/media/image9.jpeg
  inflating: docx_unzip/word/document.xml
debian-9:~/PKUyouthHTMLCoder/project# tree docx_unzip/word/media/
docx_unzip/word/media/
├── image1.jpeg
├── image2.jpeg
├── image3.jpeg
├── image4.jpeg
├── image5.jpeg
├── image6.jpeg
├── image7.jpeg
├── image8.jpeg
└── image9.jpeg

0 directories, 9 files
```
以 \*.zip 文件格式进行解压，解压得到的图片位于 `<docx_folder>/word/media` 目录内，已自动编好号。

#### 图片压缩

[TinyPNG](https://tinypng.com/) 是一个方便、实用的图片压缩网站，支持 `*.png` 和 `*.jpg` 文件，通过转化 24 位色为 8 位色来实现图片的压缩，可以在不改变图片尺寸的情况下，大幅度减少图片文件的体积（对于 adobe 图片，官方宣称可以减小 70% 以上的文件体积），并且压缩前后几乎看不出差别。因此，也可以将体积过大的图片通过 TinyPNG 进行压缩，重新插入 \*.docx 文档进行编码，这样可以大幅度提高成功上传的概率。


## 北青推送排版规则与秀米排版流程

参考自 [视觉｜北青排版规范2.1][ref-1]


### 样式说明


#### 颜色定义：

| Color | RGB |
| :---- | :-- |
| 红色 | ![#993a3a](https://placehold.it/12/993a3a/000000?text=+) #993A3A |
| 黑色 | ![#3e3e3e](https://placehold.it/12/3e3e3e/000000?text=+) #3E3E3E |
| 灰色 | ![#a5a5a5](https://placehold.it/12/a5a5a5/000000?text=+) #A5A5A5 |

#### 基础样式：

| Name | Style |
| :--- | :---- |
| 字号 | 14 px |
| 文字颜色 | 黑色 |
| 对齐方式 | **两端对齐** |
| 行高 | 2 |
| 字符间距 | 0 |
| 左页边距 | 10 px |
| 右页边距 | 10 px |

#### 组件样式：

| Name | Style |
| :--- | :---- |
| 正文（默认） | 14 px，**两端对齐**，黑色 |
| 图注 | 12 px，两端对齐，灰色，前有红色三角（宽度 10%）|
| 段落大标题 | 20 px，两端对齐，黑色，加粗 |
| 统计框红字 | 16 px，红色，加粗 |
| 正文（右） | 14 px，右对齐，黑色 |
| “本报记者”标题 | 16 px，两端对齐/左对齐，灰色，加粗 |
| “本报记者”正文 | 14 px，两端对齐，灰色，空格用**全角** |
| “参考资料”标题 | **15 px**，两端对齐/左对齐，红色，加粗 |
| “参考资料”正文 | 12 px，两端对齐，灰色 |
| 尾注(左) | 12 px，两端对齐，灰色 |
| 微信编辑｜图片来源 | 12 px，右对齐，灰色，竖线用**全角** |
| 编者按｜勘误｜... | 见参考资料 [视觉｜北青排版规范2.1][ref-1] |
| 分割线 | 14 px，灰色，高度 1 px，上下边距 0.5 em |
| **空行** | **14 px** |

### 空行说明

1. 头图前不空行，底图后不空行。
2. 记者信息（或字数统计，如果没有记者信息）与下方的分割线间不空行。
3. 编者按、记者手记的正文与其下的分割线间空一行。
4. 各种组件间如果存在空行，那么应该是 **一行** 。例如，段落与段落、头图与字数统计、字数统计与记者信息、正文与参考资料、正文与尾注、微信编辑与底图等组件之间的空行均为 **一行** 。需要注意空行的字号应当统一为 **14 px** ，否则会出现空行高度不一致的情况。


### 秀米排版详细流程

1. 利用我们的 **官方秀米账号** 登录，打开 **图文收藏**，里面保存有预设的排版组件，请仔细阅读其内的说明。
2. 务必 **充分利用** 预设的组件进行排版！并严格遵守 [视觉｜北青排版规范2.1][ref-1]，如有需要可以参考账号内已经排好的推送版面。（注：预设组件已附带了基础样式的调整，因此不需要在开始编辑前修改全局基础样式）
3. 小哥真的没有用秀米排过我们的推送orz，就不在此胡说八道了，所以没有第三点了嗯 ...


## 更新日志

- **v1.0.1** 上线版本。
- **v1.0.2** 添加 SM.MS 与 Elimage 图床支持。
- **v1.0.3** 修复了 Windows 环境下文件读写时编码错误的问题；添加了命令行界面，支持通过命令行选项来设置编码参数。
- **v1.0.4** 修复了部分图片与下方段落间未能正确空行的偶发问题。
- **v1.0.5** 修复了文前统计框内段落左外边距不正确导致的样式错误；修复了不能通过命令行选项指定是否需要渲染参考资料的错误。
- **v1.0.6** 修复了参考资料与尾注间多空一行的样式错误。
- **v1.0.7** 允许定义编者按和记者手记；允许定义 ignore 区域；修改了上传日志的输出的文件名；添加了限制图片最大宽度的 css 样式；添加了精简版的 template.docx 文档。
- **v1.0.8** 修复了在 \*.docx 文件中添加矢量形状导致插图识别错误的问题；修复了通过“样式”间接定义的加粗、居中等样式无法识别的错误；添加了不允许多张图片共存于同一段落内的限制；允许在 \*.docx 文档内定义编码参数；添加了以文件形式输出错误日志的功能。
- **v1.0.9** 修复了部分图片识别错误的问题；修复了连续图片间未能正确空行的错误；优化了以文章字数计算阅读时间的算法；将“参考资料”和“记者信息”单独定义为区域，并删除了与参考资料和记者信息相关的参数定义，现在将根据区域内容自动判断是否需要输出参考资料或记者信息；修改了多图同处于单行的判定方法，现在允许在单行内重复放置相同图片，但最终只输出一张图（这主要是为了兼容 \*.docx 文档的某些编码问题）；允许通过全角字符“＃”和“＠”申明注释段和参数定义段。
- **v1.1.0** 修改了正文部分标题的声明方式，现在不再需要在加粗的同时额外设置为居中对齐；修正了图注对齐方式为左对齐的样式错误。

## 证书

[MIT License](https://github.com/zhongxinghong/PKUyouthHTMLCoder/blob/master/LICENSE)

[ref-1]: https://mp.weixin.qq.com/s?__biz=MzA3NzAzMDEyNg==&mid=503340942&idx=1&sn=aa35da3aba5cb514212b2496e546978f&chksm=04acc80f33db41198d016a5ae58f727854a6e0e510009f793aa258dfea0248a650c2a0d9a47e#rd