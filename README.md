# PKUyouthHTMLCoder

《北大青年》微信推送自动排版小工具


## 环境配置

通过 [Python 官网](https://www.python.org/downloads/) 下载 Python3 安装包（推荐 3.6.6），并以默认方式安装即可。安装成功后，打开命令行，输入 `python3 --version` 可看到如下输出结果
```console
debian-9:~# python3 --version
Python 3.6.6
```

pip3 应该已经默认安装了。打开命令行，输入 `pip3 --version` 可看到如下输出结果
```console
debian-9:~# pip3 --version
pip 9.0.1 from /usr/lib/python3/dist-packages (python 3.6)
```
如果未找到 pip3 命令，Windows 用户可能需要检查一下 pip3 是否已被添加到系统环境变量中。如果是并未附带安装，请手动安装 pip3 ，例如通过 [pip 官网](https://pip.pypa.io/en/stable/reference/pip_install/) 。安装过程比价简单就不赘述了，有问题可自行查阅网上教程，或者来问小哥。

你也可以选择性安装 git 来方便地下载和同步更新该项目。通过 [git 官网](https://git-scm.com/downloads) 下载，并以默认方式安装即可。安装成功后，打开命令行，输入 `git --version` 可看到如下输出结果
```console
debian-9:~# git --version
git version 2.11.0
```

## 下载项目

你可以直接下载该项目的 [zip 文件包](https://github.com/zhongxinghong/PKUyouthHTMLCoder/archive/master.zip) 并解压
```console
debian-9:~# wget https://github.com/zhongxinghong/PKUyouthHTMLCoder/archive/master.zip
debian-9:~# unzip master.zip
debian-9:~# mv PKUyouthHTMLCoder-master/ PKUyouthHTMLCoder/
debian-9:~# cd PKUyouthHTMLCoder/
debian-9:~/PKUyouthHTMLCoder# ls
LICENSE  README.md  cache  config  lib  project  requirements.txt  static
```

如果你已经安装了 git，也可以在命令行下载。以下命令将会在你的当前路径下新建文件夹 `PKUyouthHTMLCoder` 并将项目下载到其中
```console
debian-9:~# git clone https://github.com/zhongxinghong/PKUyouthHTMLCoder.git
debian-9:~# cd PKUyouthHTMLCoder/
debian-9:~/PKUyouthHTMLCoder# ls
LICENSE  README.md  cache  config  lib  project  requirements.txt  static
```

git 可以方便地同步更新项目，如果该项目发生更新，你可以通过如下命令进行同步
```console
debian-9:~/PKUyouthHTMLCoder# git pull origin master
From https://github.com/zhongxinghong/PKUyouthHTMLCoder
 * branch            master     -> FETCH_HEAD
Already up-to-date.
```

## 安装依赖包

接下来利用 pip3 安装该项目的依赖包。该项目依赖于 `requests` 和 `lxml`，你也可选择性安装 `simplejson`。

以下命令将从 pip3 默认源下载和安装最新版本的 `requests` 和 `lxml`
```console
debian-9:~# pip3 install requests lxml
```

同理，运行以下命令可选择性安装 `simplejson`
```console
debian-9:~# pip3 install simplejson
```

你也可以手动指定 pip3 下载源来加快下载速度，这里以清华镜像源为例
```console
debian-9:~# pip3 install requests lxml simplejson -i https://pypi.tuna.tsinghua.edu.cn/simple
```

你也可以通过项目根目录中的 `requirements.txt` 来安装指定版本的依赖包。首先进入项目根目录，然后运行以下命令即可
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

### 标准流程

- 进入 `project` 目录，并将模板复制到该目录下
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

- 按照模板内写好的规则将文章排版好，并 **直接保存**，不要另存为，或是新建一个 \*.docx 文件，然后将模板内容复制进去。

> 由于不同版本的 word 编码的 \*.docx 文件，内部使用的 xml 规则不统一，出于兼容性考虑，就请使用提供好的 \*.docx 文件来排版，确保使用的是 `Microsoft Word 2007-2013 XML (.docx)` 格式，避免出现兼容性问题。
>
> 但是这并不能保证完全兼容，如果你发现有排版异常，请将问题与小哥反馈。我可以根据你提供的 \*.docx 文件向项目中添加新的 xml 解析规则。

- 运行 `run.py`，即可完成转码
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

> 如果目录下放置了多个 \*.docx 文件，则程序会选择性转码该目录下**修改日期最新**的 \*.docx 文件，以防止排错文件。不过还是建议你将已经完成的工程整理到 `old` 文件夹中。

- 完成转码后，将会在 `build` 文件夹中输出 `preview.html` 文件和与你当前项目同名的 `today_prj.html` 文件。
```console
debian-9:~/PKUyouthHTMLCoder/project# cd build/
debian-9:~/PKUyouthHTMLCoder/project/build# ls
preview.html  today_prj.html
```

- 双击 `preview.html` 可以在浏览器中查看编码结果，你可以根据预览结果返回到 `project` 目录中，重新修改和转码 \*.docx 文件，在浏览器中按 `F5` 刷新，即可实时查看修改结果。

- 确保排版结果基本满意后，按 `Ctrl + A` 全选网页 iframe 框中已经排版好的推送预览并按 `Ctrl + C` 复制。登录微信公众号后台，新建一个图文素材，然后按 `Ctrl + V` 粘贴，并确保图片均上传成功。如果发现图片未能上传，请尝试重新上传。如果一直未能上传成功，请手动添加素材。然后记得将该情况与小哥反馈。

> 请使用**非IE浏览器**进行复制操作（推荐使用**Chrome浏览器**）！实践证明IE浏览器在复制过程中可能存在字符编码错误的问题。

- 确认无误后即可群发！记得声明原创！


### 参数配置

出于多方考虑，小哥提供了两种修改编码参数的方法。首先，在 `config` 目录中保存了各模块的默认配置，你可以通过修改相应配置文件中的特定字段来实现参数变更。其次，你也可以通过添加命令行的运行参数来快捷地指定几个常用的编码参数。下面对这两种方法分别加以说明。

方法一： `config` 目录结构说明如下：
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

方法二： 在 `project` 目录下，运行 `run.py -h` 或 `run.py --help` 查看说明字段。
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
    --no-reference      Whether this article has references or not. (Default:
                        True)
    --count-word        Output word's sum. (Default: True)
    --count-picture     Output picture's sum. (Default: False)

  Extended Options:
    These options may be helpful to you.

    -e, --extract-picture
                        Extract all pictures to 'project/build/images/' dir in
                        sequence.
```
参数意义与 `coder.ini` 文件夹中的参数意义相同。

考虑到有可能需要手动上传图片，这里额外提供了自动提取图片的选项。在运行时添加 `-e` 或 `--extract-pictrue` 选项，可以在编码的同时将图片按顺序提取到 `build/images` 文件夹内，并对其做统一格式的编号，在图片复制上传频繁失败的情况下，方便你快速而清晰地定位需要手动上传的图片。
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

事实上， \*.docx 文件是一个 \*.zip 文件，因此你也可以通过常规的解压缩手段对其内的图片素材进行提取。解压后的图片文件已自动编好号。
```console

```

## 工作原理

待补充


## 北青推送排版规则

待补充。老规则可见 [这篇推送](https://mp.weixin.qq.com/s?__biz=MzA3NzAzMDEyNg==&tempkey=OTY4XzRVODRqRDkrQmFrTit1YmFEVmw4UmVqY1JwRnRoYUxKNm9PdVdlOTFZQ1gwWmlBOUt3dVRYRzhsREhhUnVfOEloYTlXeXdINDhWMHUxY3RwY0xTUFdXYkR5eG1NeGlmQkNSSlRMTEllcjFpQW82dDNsZTkzTTZnWDRmUUU1bjNjU2hjRC1jX1hCVlRxbkRNWmRGUy1Gc215U3BQZ2tSUkRZZDJReVF%2Bfg%3D%3D&chksm=04acc80f33db41198d016a5ae58f727854a6e0e510009f793aa258dfea0248a650c2a0d9a47e#rd) 和 [这篇推送](https://mp.weixin.qq.com/s?__biz=MzA3NzAzMDEyNg==&tempkey=OTY4X3czR1RoQWJGZDBiaUdOL3lEVmw4UmVqY1JwRnRoYUxKNm9PdVdlc2dpek41RWpBODV5Ujk3NlV4T3dPNUt5SXc1d1hlajdNRXpQdmI5aGM5WjNZVjVOdE92RmlEZXhuNWhXMWllNXN1NE11cWtSMTkwRVEyQ25PUzdTX0FTa0dKVmNYemNYMk1ST0MzMHVSeHZ0UndtVk40Y2VUZVM2bjJKUXFVbEF%2Bfg%3D%3D&chksm=16c4990821b3101e310754723ba3b143947e6cf673654eaa5e9d40f4310d9d0da20368d51b68#rd) →_→
