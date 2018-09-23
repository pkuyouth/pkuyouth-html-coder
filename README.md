# PKUyouthHTMLCoder

《北大青年》微信推送自动排版小工具 v1.0.6


## 环境配置

通过 [Python 官网](https://www.python.org/downloads/) 下载 Python3 安装包，并以默认方式安装即可。安装成功后，打开命令行，输入 `python3 --version` 可看到如下输出结果。
```console
debian-9:~# python3 --version
Python 3.6.6
```

pip3 应该已经默认安装了。打开命令行，输入 `pip3 --version` 可看到如下输出结果。
```console
debian-9:~# pip3 --version
pip 9.0.1 from /usr/lib/python3/dist-packages (python 3.6)
```
如果未找到 pip3 命令，Windows 用户可能需要检查一下 pip3 是否已被添加到系统环境变量中。如果是并未附带安装，请手动安装 pip3 ，例如通过 [pip 官网](https://pip.pypa.io/en/stable/reference/pip_install/) 或 [get-pip.py](https://bootstrap.pypa.io/get-pip.py)。安装过程比价简单就不赘述了，有问题可自行查阅网上教程，或者来问小哥。

你也可以选择性安装 git 来方便地下载和同步更新该项目。通过 [git 官网](https://git-scm.com/downloads) 下载，并以默认方式安装即可。安装成功后，打开命令行，输入 `git --version` 可看到如下输出结果。
```console
debian-9:~# git --version
git version 2.11.0
```

## 下载项目

你可以直接下载该项目的 [zip 文件包](https://github.com/zhongxinghong/PKUyouthHTMLCoder/archive/master.zip) 并解压。
```console
debian-9:~# wget https://github.com/zhongxinghong/PKUyouthHTMLCoder/archive/master.zip
debian-9:~# unzip master.zip
debian-9:~# mv PKUyouthHTMLCoder-master/ PKUyouthHTMLCoder/
debian-9:~# cd PKUyouthHTMLCoder/
debian-9:~/PKUyouthHTMLCoder# ls
LICENSE  README.md  cache  config  lib  project  requirements.txt  static
```

如果你已经安装了 git，也可以在命令行下载。以下命令将会在你的当前路径下新建文件夹 `PKUyouthHTMLCoder` 并将项目下载到其中。
```console
debian-9:~# git clone https://github.com/zhongxinghong/PKUyouthHTMLCoder.git
debian-9:~# cd PKUyouthHTMLCoder/
debian-9:~/PKUyouthHTMLCoder# ls
LICENSE  README.md  cache  config  lib  project  requirements.txt  static
```

git 可以方便地同步更新项目，如果该项目发生更新，你可以通过如下命令进行同步。
```console
debian-9:~/PKUyouthHTMLCoder# git pull origin master
From https://github.com/zhongxinghong/PKUyouthHTMLCoder
 * branch            master     -> FETCH_HEAD
Already up-to-date.
```

## 安装依赖包

接下来利用 pip3 安装该项目的依赖包。该项目依赖于 `requests` 和 `lxml`，你也可选择性安装 `simplejson` 。

以下命令将从 pip3 默认源下载和安装最新版本的 `requests` 和 `lxml` 。
```console
debian-9:~# pip3 install requests lxml
```

同理，运行以下命令可选择性安装 `simplejson` 。
```console
debian-9:~# pip3 install simplejson
```

你也可以手动指定 pip3 下载源来加快下载速度，这里以清华镜像源为例。
```console
debian-9:~# pip3 install requests lxml simplejson -i https://pypi.tuna.tsinghua.edu.cn/simple
```

你也可以通过项目根目录中的 `requirements.txt` 来安装指定版本的依赖包。首先进入项目根目录，然后运行以下命令即可。
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
├── lib                             # 程序包
│   ├── coder.py                        # 编码主程序
│   ├── elimage.py                      # elimage API
│   ├── error.py                        # 错误类型定义
│   ├── smms.py                         # SM.MS API
│   ├── tags.py                         # DOM 节点定义
│   ├── tietuku.py                      # 贴图库 API
│   └── util.py                         # 通用函数/类
├── project                         # 项目目录
│   ├── build                           # 排版结果的输出目录
│   │   └── images                          # 图片解压输出目录
│   ├── old                             # 存放旧工程
│   ├── run.py                          # 主程序
│   └── template                        # 排版模板和样例
│       ├── sample.docx
│       └── template.docx
├── requirements.txt
└── static
    ├── favicon.ico
    └── preview.template.html
```

## 使用方法

### 流程简介

1. 进入 `project` 目录，并将 `template` 目录下的 `template.docx` 模板文件复制到该目录下。
```console
debian-9:~/PKUyouthHTMLCoder/project# cp template/template.docx ./today_prj.docx
debian-9:~/PKUyouthHTMLCoder/project# ls -l
total 20
drwxr-xr-x 2 root root    24 Aug  5 10:21 build
drwxr-xr-x 2 root root    24 Aug  5 10:21 old
-rwxr-xr-x 1 root root  1633 Aug  5 10:21 run.py
drwxr-xr-x 2 root root    46 Aug  5 10:21 template
-rw-r--r-- 1 root root 13718 Aug  5 10:47 today_prj.docx
```

2. 按照模板内写好的规则（详细说明见下方 “模板规则”）将文章排版好，并 **直接保存**，不要另存为，或是新建一个 \*.docx 文件，然后将模板内容复制进去。

> 由于不同版本的 word 编码的 \*.docx 文件，内部使用的 xml 规则不统一，出于兼容性考虑，就请使用提供好的 \*.docx 文件来排版，确保使用的是 `Microsoft Word 2007-2013 XML (.docx)` 格式，避免出现兼容性问题。
>
> 但是这并不能保证完全兼容，如果你发现有排版异常，请将问题与小哥反馈。我可以根据你提供的 \*.docx 文件向项目中添加新的 xml 解析规则。

3. 运行 `run.py`，即可完成转码。
```console
debian-9:~/PKUyouthHTMLCoder/project# python3 run.py
[INFO] docxparser, 11:12:24, parse /root/PKUyouthHTMLCoder/project/today_prj.docx
[INFO] tietuku, 11:12:24, uploading image d148236d3022064bbf2d7386afbdfd44.jpeg
[INFO] tietuku, 11:12:25, uploading image da76f2cd35bbe4376caeda09ac7d8d99.jpeg
[INFO] tietuku, 11:12:25, get image da76f2cd35bbe4376caeda09ac7d8d99.jpeg from cache
[INFO] tietuku, 11:12:25, uploading image 174fa7651026cc44f4d4de202a5f833a.jpeg
[INFO] tietuku, 11:12:26, uploading image f9619493156f9e151bbbbd1b53afae50.jpeg
[INFO] tietuku, 11:12:26, uploading image c2a970e3d6d10acd26a4aaa3f42cac81.jpeg
[INFO] tietuku, 11:12:27, uploading image 8523fc7842ce8d521159ce89654f882d.jpeg
[INFO] tietuku, 11:12:27, uploading image 7b3c85bac56cf405a3ce0998a9fdfcbb.jpeg
[INFO] tietuku, 11:12:28, uploading image 0974da2802f35b1ce62992934e618e4e.jpeg
[INFO] htmlcoder, 11:12:29, build today_prj.html in /root/PKUyouthHTMLCoder/project/build
```

> 如果目录下放置了多个 \*.docx 文件，则程序会选择性转码该目录下 **修改日期最新** 的 \*.docx 文件，以防止排错文件。不过还是建议你将已经完成的工程整理到 `old` 文件夹中。

4. 完成转码后，将会在 `build` 文件夹中输出 `preview.html` 文件和与你当前项目同名的 `today_prj.html` 文件。
```console
debian-9:~/PKUyouthHTMLCoder/project# cd build/
debian-9:~/PKUyouthHTMLCoder/project/build# ls
preview.html  today_prj.html
```

5. 双击 `preview.html` 可以在浏览器中查看编码结果，你可以根据预览结果返回到 `project` 目录中，重新修改和转码 \*.docx 文件，在浏览器中按 `F5` 刷新，即可实时查看修改结果。

> 程序无法识别在 \*.docx 编辑过程中对图片的旋转处理，因此，需要将图片 **预先旋转** 好后再插入，否则在预览中会出现方向错误的图片。

6. 确保排版结果基本满意后，按 `Ctrl + A` 全选网页 iframe 框中已经排版好的推送预览并按 `Ctrl + C` 复制。登录微信公众号后台，新建一个图文素材，然后按 `Ctrl + V` 粘贴，并确保图片均上传成功。（注：安全起见，请使用宽度不小于 **480 px** 的图片，具体原因见下方的 “工作原理” 介绍）

> 请使用 **非IE浏览器** 进行复制操作（推荐使用 **Chrome浏览器** ）！实践证明 IE浏览器 在复制过程中可能存在字符编码错误的问题。
>
> 如果发现部分图片未能成功上传，并不需要全部重新上传。这种情况是由于微信服务器在粘贴的一瞬间并发请求和下载文档内图片素材速度过快导致对方静态服务器延时而造成的，只需要在随后尝试重新请求静态资源即可。因此，可以直接在公号的素材编辑器中删除上传失败的图片，然后从 iframe 预览结果中单独选中相应图片，一张张重新复制粘贴到响应位置，即可实现上传。如果实在不行，也可以从公号后台手动上传和添加图片。

7. 填写标题、作者、摘要、封面、原文链接等其他相关信息（注意：标题竖线用 **全角**；如果有两个及以上记者，则 ”作者“ 写 **北大青年**，如果只有一个记者，就填那个记者的名字），并 **声明原创**（”文章类别“ 填 **其他**）！然后查看 **预览**，确认无误后准备群发。

> 在编辑器中，可能会发现图片过大，右半截超出编辑器可视范围，这是正常情况，只要在预览中图片能够以 100% 宽度显示、不发生裁剪即可。


### 参数配置

出于多方考虑，小哥提供了两种修改编码参数的方法。首先，在 `config` 目录中保存了各模块的默认配置，你可以通过修改相应配置文件中的特定字段来实现参数变更。其次，你也可以通过添加命令行的运行选项来快捷地指定几个常用的编码参数。下面对这两种方法分别加以说明。

#### 方法一（不推荐）：
对 `config` 目录结构说明如下：
```console
debian-9:~/PKUyouthHTMLCoder# tree config/
config/
├── coder.ini           # 编码参数配置，主要需要关注的文件
├── elimage.ini         # elimage 图床配置
├── smms.ini            # SM.MS 图床配置
├── style.css           # 排版的 css 样式表（实际上是 style.ini 的正常 *.css 表示，编码时不使用该文件）
├── style.ini           # 排版的 css 样式配置
└── tietuku.ini         # 贴图库 图床配置

0 directories, 6 files
```
主要的编码参数配置位于 `coder.ini` 文件中，可以根据其内的注释说明做所需的更改。

#### 方法二：
在 `project` 目录下，运行 `run.py -h` 或 `run.py --help` 查看说明字段。
```console
debian-9:~/PKUyouthHTMLCoder/project# python3 run.py --help
Usage: run.py [options]

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

    --no-reporter       Whether this article has reporters information or not.
                        (Default: False)
    --has-reference     Whether this article has references or not. (Default:
                        False)
    --count-word        Output word's sum. (Default: True)
    --count-picture     Output picture's sum. (Default: False)

  Extended Options:
    These options may be helpful to you.

    -e, --extract-picture
                        Extract all pictures to 'project/build/images/' dir in
                        sequence.
```
参数意义与 `coder.ini` 文件夹中的参数意义相同。

#### 一个示例：
```console
debian-9:~/PKUyouthHTMLCoder/project# python3 run.py -s SM.MS --no-reporter --count-picture
```
这说明本次编码使用 SM.MS 图床，统计图片数，且不添加记者信息。

#### 一点说明：
程序在设计时规定不可同时统计字数和图片数，而此处 --count-word 默认为 True ，理论上添加 --count-picture 应当会导致冲突。因此这里做了一个小调整。如果指定了 --count-picture ，则自动设置 --count-word 为 False 。秉承特殊情况优先的原则，如果你不小心同时指定了 --count-word 和 --count-picture ，那么程序将采用 --count-pictrue ，也就是说如下命令将渲染出统计图片数的 \*.html 文件。由于 --count-word 字段默认为 True 且处于低优先级的位置，因此这个参数实际上没有任何用处，是否指定它并不会对输出结果造成影响。当然，如果你修改了 coder.ini 文件的默认配置，将该字段改为 False ，那么此处你就需要显式指定 --count-word 了。
```console
debian-9:~/PKUyouthHTMLCoder/project# python3 run.py --count-word --count-picture
```

#### 关于图床：
该项目目前提供了 `Tietuku`, `SM.MS`, `Elimage` 三款免费图床的 API 接口封装，默认使用 `Tietuku` ，因为其上传速度较快，且并发下载速度较快，复制过程中不容易掉图。后两款图床的服务器在境外，相较之下速度较慢。不过需要注意 Tietuku 存在较多限制，比如图片自动过期（7 天）和上传频率限制（<= 100 张/小时）等。本项目对其上传图片的默认缓存时间是 12 h 。（注：过期不代表推送中的图片过期，推送中的图片一经复制上传成功后将永久有效）

考虑到有可能需要手动上传图片，这里额外提供了自动提取图片的选项。在运行时添加 `-e` 或 `--extract-pictrue` 选项，可以在编码的同时将图片按顺序提取到 `build/images` 文件夹内，并以统一格式的编号命名文件，在图片复制上传频繁失败的情况下，方便对需要手动上传的图片进行快速、准确的定位。
```console
debian-9:~/PKUyouthHTMLCoder/project# python3 run.py -e
[INFO] docxparser, 10:14:24, parse /root/PKUyouthHTMLCoder/project/today_prj.docx
[INFO] docxparser, 10:14:24, extract image 180909_001.jpeg to /root/PKUyouthHTMLCoder/project/build/images
[INFO] tietuku, 10:14:24, get image d148236d3022064bbf2d7386afbdfd44.jpeg from cache
[INFO] docxparser, 10:14:24, extract image 180909_002.jpeg to /root/PKUyouthHTMLCoder/project/build/images
[INFO] tietuku, 10:14:24, get image da76f2cd35bbe4376caeda09ac7d8d99.jpeg from cache
[INFO] docxparser, 10:14:24, extract image 180909_003.jpeg to /root/PKUyouthHTMLCoder/project/build/images
[INFO] tietuku, 10:14:24, get image da76f2cd35bbe4376caeda09ac7d8d99.jpeg from cache
[INFO] docxparser, 10:14:24, extract image 180909_004.jpeg to /root/PKUyouthHTMLCoder/project/build/images
[INFO] tietuku, 10:14:24, get image 174fa7651026cc44f4d4de202a5f833a.jpeg from cache
[INFO] docxparser, 10:14:24, extract image 180909_005.jpeg to /root/PKUyouthHTMLCoder/project/build/images
[INFO] tietuku, 10:14:24, get image f9619493156f9e151bbbbd1b53afae50.jpeg from cache
[INFO] docxparser, 10:14:24, extract image 180909_006.jpeg to /root/PKUyouthHTMLCoder/project/build/images
[INFO] tietuku, 10:14:24, get image c2a970e3d6d10acd26a4aaa3f42cac81.jpeg from cache
[INFO] docxparser, 10:14:24, extract image 180909_007.jpeg to /root/PKUyouthHTMLCoder/project/build/images
[INFO] tietuku, 10:14:24, get image 8523fc7842ce8d521159ce89654f882d.jpeg from cache
[INFO] docxparser, 10:14:24, extract image 180909_008.jpeg to /root/PKUyouthHTMLCoder/project/build/images
[INFO] tietuku, 10:14:24, get image 7b3c85bac56cf405a3ce0998a9fdfcbb.jpeg from cache
[INFO] docxparser, 10:14:24, extract image 180909_009.jpeg to /root/PKUyouthHTMLCoder/project/build/images
[INFO] tietuku, 10:14:24, get image 0974da2802f35b1ce62992934e618e4e.jpeg from cache
[INFO] htmlcoder, 10:14:24, build today_prj.html in /root/PKUyouthHTMLCoder/project/build
debian-9:~/PKUyouthHTMLCoder/project# tree build/images/
build/images/
├── 180909_001.jpeg
├── 180909_002.jpeg
├── 180909_003.jpeg
├── 180909_004.jpeg
├── 180909_005.jpeg
├── 180909_006.jpeg
├── 180909_007.jpeg
├── 180909_008.jpeg
└── 180909_009.jpeg

0 directories, 9 files
```

事实上， \*.docx 文件是一个 \*.zip 文件，因此你也可以通过常规的解压缩手段对其内的图片素材进行提取。解压后的图片文件位于 `<docx_folder>/word/media` 目录内，已自动编好号。
```console
debian-9:~/PKUyouthHTMLCoder/project# unzip -d docx_unzip today_prj.docx
Archive:  today_prj.docx
  inflating: docx_unzip/_rels/.rels
  inflating: docx_unzip/word/theme/theme1.xml
  inflating: docx_unzip/word/styles.xml
  inflating: docx_unzip/word/_rels/document.xml.rels
  inflating: docx_unzip/word/settings.xml
  inflating: docx_unzip/word/media/image1.jpeg
  inflating: docx_unzip/word/fontTable.xml
  inflating: docx_unzip/customXml/_rels/item2.xml.rels
  inflating: docx_unzip/customXml/_rels/item1.xml.rels
  inflating: docx_unzip/customXml/itemProps1.xml
  inflating: docx_unzip/customXml/item2.xml
  inflating: docx_unzip/customXml/item1.xml
  inflating: docx_unzip/customXml/itemProps2.xml
  inflating: docx_unzip/docProps/custom.xml
  inflating: docx_unzip/docProps/app.xml
  inflating: docx_unzip/docProps/core.xml
  inflating: docx_unzip/[Content_Types].xml
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

### 模板规则

#### 符号说明
| Symbol | Meaning |
| :----- | :------ |
| #      | 注释符，该行内容全部忽略 |
| {% xxx %} | 区域标识符，划定区域范围，需要配对 |

#### 区域划分
| Zone | Range |
| :--- | :---- |
| head | 文前部分，包含 记者信息 |
| body | 正文部分，包含 正文、段落大标题、图片、图注 |
| tail | 尾注部分，包含 参考文献、尾注（左）、微信编辑、图片来源 |

#### \*.docx 文档排版样式规定
| Zone | Component | Style |
| :--- | :-------- | :---- |
| **head** | | |
| head | “记者信息”正文 | 任意对齐，不加粗（默认） |
| head | “记者信息”标题 | 任意对齐，加粗 |
| **body** | | |
| body | 正文 | 左对齐/两端对齐，不加粗（默认） |
| body | 正文（右） | 右对齐，不加粗 |
| body | 图片 | **单独成行**（否则同段落的文字将被忽略） |
| body | 图注 | 居中，不加粗 |
| body | 段落大标题 | 居中，加粗 |
| **tail** | | |
| tail | ”参考文献“标题 | 左对齐/两端对齐，加粗 |
| tail | ”参考文献“正文 | 左对齐/两端对齐，不加粗 |
| tail | 微信编辑｜图片来源 | 右对齐 |

#### 几点说明：
1. \*.docx 文档中的任何多余空行均不会影响实际输出（事实上空行只起到分段作用）。
2. 除以上必要样式外，其他任意样式均不影响实际输出（颜色、字体、字号、斜体、下划线等）。
3. 如果原文档存在修订，请选择`全部接受`。通过选项卡 `审阅 > 修订 > 所有标记/简单标记` ，选择 `接受 > 接受所有修订` 。如果需要保留校订，可以保留原文档，然后将其内容复制到新的 `template.docx` 内，复制过来的文本会默认接受所有修订。


## 工作原理

这个项目的工作原理很简单，核心工作在于：在 lxml 库对常规 HTML DOM 节点类定义的基础上，根据我们推送的样式，自定义各种组件类，封装相应样式。随后解析 \*.docx 文件，利用自定义的组件类，对其内各种 \*.xml 文件记录的格式信息加以重新描述，然后将其渲染成 \*.html ，从而完成转码的工作。

#### 具体流程：
1. 基于 lxml 库，根据我们推送的样式要求，封装定义各种组件类，详见 `tags.py` 。由于微信不允许复制上传含有 `div` 标签的 HTML 片段，因此该项目仿照秀米的手法，统一使用 `section` 标签替换 `div` 标签。
2. \*.docx 文件实际上是 \*.zip 文件和 \*.xml 文件的组合，因此利用 zipfile 库解压 \*.docx 文件，并对其内的目录结构加以解析，由此定义了 `DocxParser` 类。
3. 首先读取和上传所需的图片素材，由此利用 requests 库对三种图床的 API 接口做了封装。为图片提供外链是为了让微信服务器能够通过外网访问和下载到所需的静态资源。
4. \*.docx 文档中的 `word/document.xml` 文件描述了该文档的排版。但是其内的各种素材均使用预定义的 ID 来表示，通过观察可以发现，素材的映射关系定义于 `word/_rels/document.xml.rels` 文件中，因此首先解析该文件，找到素材 ID 与实际图片 target 的映射关系。
5. 文档在构建时已预先分成三段，此处利用 lxml 库，根据自定义的区域符对三部分的划分，分段解析 word/document.xml 文件，并用已定义好的各种组件类对其排版格式进行重新描述，注意在解析过程中把握好逻辑关系。由此定义 `HTMLCoder` 类。
6. 提供带有确定尺寸 iframe 元素（height: 640 px, weight: 768~1024 px）的 \*.html 预览渲染结果。

> 注： 这里的确定尺寸主要是为了确保宽度下限至少为 768 px ，这是因为 HTML 代码在复制上传的过程中，会丢失以百分数定义的所有尺寸信息，并以复制时网页显示的图片的绝对尺寸替代之，图片将不能自适应屏幕宽度。也就是说，假如在复制时屏幕宽度很小，比如只有 100 px ，那么上传到推送中的图片尺寸也将被设定为 100 px 宽，这有可能导致图片无法达到 100% 宽度的显示。为了防止这种情况的发生，这里使用 iframe 限制了最小宽度。同时，该项目并没有指定渲染出的 HTML 代码中 img 元素宽度为 100% ，因此不足 768 px 宽的图片在 iframe 中并不会自适应地放大，而是以小于 768 px 宽的原始宽度存在，那么，如果原始图片本身过小，也可能导致推送中的图片尺寸过小。综合考虑各款手机的屏幕宽度，安全起见，建议不要使用宽度小于 **480 px** 的图片。
>
> 补充说明： 微信的推送网页采用了响应式设计，当屏幕宽度超过 1024 px （以前好像是 768 px）时，会自动转换布局，并将推送文章页面限制在 720 px 宽的元素中。因此没有必要让图片宽度超过 1024 px 。


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
| “参考文献”标题 | **15 px**，两端对齐/左对齐，红色，加粗 |
| “参考文献”正文 | 12 px，两端对齐，灰色 |
| 尾注(左) | 12 px，两端对齐，灰色 |
| 微信编辑｜图片来源 | 12 px，右对齐，灰色，竖线用**全角** |
| 编者按｜勘误｜... | 见参考资料 [视觉｜北青排版规范2.1][ref-1] |
| 分割线 | 14 px，灰色，高度 1 px，上下边距 0.5 em |
| **空行** | **14 px** |


### 空行说明

1. 头图前不空行，底图后不空行。
2. 各种组件间如果存在空行，那么应该是 **一行** 。例如，段落与段落、头图与字数统计、字数统计与记者信息、正文与参考文献、正文与尾注、微信编辑与底图等组件之间的空行均为 **一行** 。需要注意空行的字号应当统一为 **14 px** ，否则会出现空行高度不一致的情况。


### 秀米排版详细流程

1. 利用我们的 **官方秀米账号** 登录，打开 **图文收藏**，里面保存有预设的排版组件，请仔细阅读其内的说明。
2. 务必 **充分利用** 预设的组件进行排版！并严格遵守 [视觉｜北青排版规范2.1][ref-1]，如有需要可以参考账号内已经排好的推送版面。（注：预设组件已附带了基础样式的调整，因此不需要在开始编辑前修改全局基础样式）
3. 小哥真的没有用秀米排过我们的推送orz，就不在此胡说八道了，所以没有第三点了嗯 ...


## 历史版本

- v1.0.1 上线版本。
- v1.0.2 添加 SM.MS 与 Elimage 图床支持。
- v1.0.3 修复了 Windows 环境下文件读写时编码错误的问题；添加了命令行界面，支持通过命令行选项来设置编码参数。
- v1.0.4 修复了部分图片与下方段落间未能正确空行的偶发问题。
- v1.0.5 修复了文前统计框内段落左外边距不正确导致的样式错误；修复了不能通过命令行选项指定是否需要渲染参考文献的错误。
- v1.0.6 修复了参考文献与尾注间多空一行的样式错误。

## 证书

[MIT License](https://github.com/zhongxinghong/PKUyouthHTMLCoder/blob/master/LICENSE)

[ref-1]: https://mp.weixin.qq.com/s?__biz=MzA3NzAzMDEyNg==&mid=503340942&idx=1&sn=aa35da3aba5cb514212b2496e546978f&chksm=04acc80f33db41198d016a5ae58f727854a6e0e510009f793aa258dfea0248a650c2a0d9a47e#rd