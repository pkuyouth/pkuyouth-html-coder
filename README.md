PKUyouthHTMLCoder
=================
《北大青年》微信推送自动排版小工具 v2.0.1


安装步骤
----------
1. 通过 [Python 官网](https://www.python.org/downloads/) 下载 Python3 安装包，并以默认方式安装即可。安装成功后，打开命令行，输入 `python3 --version` 或 `python --version` 可查看版本号。

2. pip3 应该已经默认安装了。打开命令行，输入 `pip3 --version` 或 `pip --version` 可查看版本号。

    - 如果未找到 pip3 命令，Windows 用户可能需要检查一下 pip3 是否已被添加到系统环境变量中。如果是并未附带安装，请手动安装 pip3 ，例如通过 [pip 官网](https://pip.pypa.io/en/stable/reference/pip_install/) 或 [get-pip.py](https://bootstrap.pypa.io/get-pip.py)，安装过程比价简单就不赘述了。

3. 直接下载该项目的 [zip 文件包](https://github.com/zhongxinghong/PKUyouthHTMLCoder/archive/master.zip) 并解压。

4. 该项目依赖于 `requests` 和 `lxml` ，可在命令行中通过 `pip3 install requests lxml -i https://pypi.tuna.tsinghua.edu.cn/simple` 命令进行安装。


使用方法
----------
1. 将 `template` 目录下的 `template.docx` 或 `template.concise.docx` 模板文件复制到 `input` 目录下，并重命名成你喜欢的标题（例如当天稿件的标题）。

    - `input` 文件夹内修改日期最新的 \*.docx 文件将会被程序读入，这可以用以区分多份稿件。但是更加建议只在 `input` 文件夹内放置当次稿件的 \*.docx 文件，而将已经排过的 \*.docx 文件保存到其他地方。

1. 按照模板内写好的规则（详见 [模板规则](#模板规则)）将文章排版好，并且 **直接保存**，不要 “另存为”，或是新建一个 \*.docx 文件，然后将模板内容复制进去。

    - 这是为了确保使用的是 `Microsoft Word 2007-2013 XML (.docx)` 格式，以避免出现兼容性问题。

3. 运行 `main.py`，即可完成转码，可通过双击 `main.py` 或在命令行（确保路径处于项目根目录）内输入 `python3 main.py` 或 `python main.py` 来实现。

    - 如果程序因错误而异常退出，将会在 `logs` 文件夹内记录相应的错误日志。

4. 完成渲染后，将会在 `output` 文件夹内输出一个与输入的 \*.docx 文件同名的 HTML 网页文件。

5. 双击 HTML 网页文件，即可在浏览器中查看编码结果，不断修改输入的 \*.docx ，并重新渲染，直到输出结果已经没有问题，注意核对输出网页上方的易错提示。

    - 请使用 **非 IE, Edge 浏览器** 打开，强烈建议使用 **Chrome浏览器** ，以避免乱码。
    -  程序无法识别在 \*.docx 编辑过程中对图片的旋转处理，因此，需要将图片 **预先旋转** 好后再插入，否则在预览中会出现方向错误的图片。

6. 按 `Ctrl + A` 全选网页 iframe 框中已经排版好的推送预览并按 `Ctrl + C` 复制。登录微信公众号后台，新建一个图文素材，然后按 `Ctrl + V` 粘贴，并确保图片均上传成功。（注：安全起见，请使用宽度不小于 **480 px** 的图片！）

    - 如果发现部分图片未能成功上传，并不需要全部重新上传。可以直接在公号编辑器中删除上传失败的图片，然后从预览结果中单独选中相应图片，重新复制粘贴到相应位置，即可实现上传。
    - 如果图片一直上传失败，通常是因为图片过大，这时候可以从公号后台的素材库手动上传。
    - 在公号编辑器中，可能会发现图片过大，右半截超出编辑器可视范围，这是正常情况，只要在预览中图片能够正常显示即可。

7. 填写标题、作者、摘要、封面、原文链接等其他相关信息（注意：标题竖线用 **全角**；如果有两个及以上记者，则 ”作者“ 写 **北大青年**，如果只有一个记者，就填那个记者的名字），并 **声明原创**（”文章类别“ 填 **其他**）！然后查看 **预览**，确认无误后即可准备群发。


模板规则
-----------

### 符号说明

| Symbol        | Meaning |
| :------------ | :------ |
| #             | 注释符，该行内容全部忽略 |
| @ key = value | 参数设置符 |
| {% xxx %}     | 区域定义符 -- 起始边界 |
| {% ENDxxx %}  | 区域定义符 -- 终止边界 |

### 区域划分

| Zone         | Range |
| :----------- | :---- |
| ignore       | 忽略该区域内的所有内容 |
| reporter     | 文前部分，包含 记者信息 |
| body         | 正文部分，包含 正文、段落大标题、图片、图注 |
| ending       | 尾注部分，包含 参考资料、尾注（左）、微信编辑、图片来源 |
| editornote   | 编者按 |
| reporternote | 记者手记 |
| reference    | 参考资料 |

### \*.docx 文档排版样式规定

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


几点说明
----------
- \*.docx 文档中的任何多余空行均不会影响实际输出（事实上空行只起到分段作用）。
- 除以上必要样式外，其他任意样式均不影响实际输出（颜色、字体、字号、斜体、下划线等）。
- 如果原文档存在修订，请选择`全部接受`。通过选项卡 `审阅 > 修订 > 所有标记/简单标记` ，选择 `接受 > 接受所有修订` 。


证书
---------
[MIT License](https://github.com/zhongxinghong/PKUyouthHTMLCoder/blob/master/LICENSE)
