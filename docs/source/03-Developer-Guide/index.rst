Developer Guide
==============================================================================


How was findref designed
------------------------------------------------------------------------------
findref 的代码架构如下:

1. **底层用于动态渲染 Terminal App 的模块**. 使用的是我自己开发的 `afwf_shell <https://github.com/MacHu-GWU/afwf_shell-project>`_ Python 库. ``afwf_shell`` 是一个界面和操作逻辑类似于 `Alfred Workflow <https://www.alfredapp.com/workflows/>`_ 的命令行工具, 特点是 **跨平台**, Alfred Workflow 只支持 Mac, 而 afwf_shell 支持 Windows, MacOS, Linux; **安装简单**, 用 Python pip install 即可; 和 **免费**, Alfred Workflow 需要付费约 $50.
2. **中层用于下载数据集, 建立索引, 以及搜索的模块**. 使用的是我自己开发的 `sayt <https://github.com/MacHu-GWU/sayt-project>`_ Python 库. 它封装了一个类似于 ElasticSearch 的本地, 无服务器的搜索引擎, 并且了集成了查询缓存, 自动刷新数据等功能.
3. **顶层是 findref 将核心功能封装为命令行供用户使用的胶水代码**.

从用户的角度看, 安装了 findref 之后就自动会出现几个命令行命令, 这个命令行命令的名字就跟 Dataset 的名字一样, 不过所有的 underscore 都被替换成了 hyphen, 以跟 Linux 哲学一致, 防止下划线被 terminal 的主题吞掉使得看起来跟空格类似.

这些命令行命令在第一次被使用时候就会检查 ``${HOME}/.findref/${dataset_name}/`` 目录下寻找索引文件, 如果不存在则自动执行 ``downloader`` 函数下载数据, 构建索引. 对于大多数 dataset, 这个数据有效期是 30 天, 之后会自动重新下载数据刷新.

findref UI Interaction Logic
------------------------------------------------------------------------------
