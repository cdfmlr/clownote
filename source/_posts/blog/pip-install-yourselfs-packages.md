---
date: 2020-05-07 10:17:44
tags: Python
title: 如何用 pip 安装自己写的包
---



# 如何用 pip 安装自己写的包

昨天突发奇想，想让自己写的包也可以像我们常用的 numpy、flask、tensorflow 那样直接一个 `pip install XXX` 命令就安装上。

要实现这个，首先，我们需要了解 pip 和 Pypi。

（如果你懂一点点英语，请直接看这篇文档：[Packaging and distributing projects](https://packaging.python.org/guides/distributing-packages-using-setuptools/#packaging-and-distributing-projects)）

（如果你用 Windows，我不保证你可以顺利完成所有操作，自求多福 [告辞]）

## Pypi

![pypi](https://tva1.sinaimg.cn/large/007S8ZIlgy1gejog1c7xdj31e00u0kdb.jpg)

> The Python Package Index (PyPI) is a repository of software for the Python programming language.

这是 [Pypi](https://pypi.org) 的官网上对自己的描述，大概翻译一下：

> Python Package Index (PyPI) 是 Python 编程语言的软件库。

其实，我们平时使用 pip 时，就是在 Pypi 里拉取这些包的，例如：

- [numpy](https://pypi.org/project/numpy/): pip install numpy
- [tensorflow](https://pypi.org/project/tensorflow/): pip install tensorflow

如何用 pip 安装包可以参考：[文档 - Installing Packages](https://packaging.python.org/tutorials/installing-packages/)，这不是本文的重点。

我们接下来参考 [文档 - Packaging Python Projects](https://packaging.python.org/tutorials/packaging-projects/)，讨论如何打包、发布自己的项目，然后用 pip 安装自己写的包。

## 项目结构

大家都知道（不然这篇文章还不适合现在的你，不用看了），我们写一个 Python 项目时，最基本的目录结构如下：

```
packaging_tutorial/
  example_pkg/
    __init__.py
```

当我们要开源或者以其他形式发布一个项目时，比如放到 Github 之前，还会加一些测试、LICENSE、README，目录就变成了这样：

```
packaging_tutorial/
  example_pkg/
    __init__.py
  tests/
  LICENSE
  README.md
```

现在我们要打包发布这个项目，还需要再加一个 `setup.py`：

```
packaging_tutorial/
  example_pkg/
    __init__.py
  tests/
  setup.py
  LICENSE
  README.md
```



## setup.py

` setup.py` 描述了你的项目，告诉别人你项目的名称、版本、描述、依赖......类似于写 node.js 同学的 `package.json `。

说的官方一点就是：setup.py 是 setuptools 的构建脚本。它告诉 setuptools 关于你的软件包（如名称和版本）以及要包含哪些代码文件。

一个基本的 setup.py 长这样：

```python
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='packaging_tutorial',
    version='0.0.1',
    packages=setuptools.find_packages(),
    url='https://github.com/pypa/sampleproject',
    license='MIT',
    author='Example Author',
    author_email='author@example.com',
    description='A small example package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['numpy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

```

其实基本看名字就知道是些什么了，我们只说明几个特别的：

- `packages`，这里可以写一个list，比如 `packages=['example_pkg1', 'example_pkg2', ...]`，即你的目录里的 Python 包（带`__init__.py`的那种目录），也可以如官网建议的直接让 setuptools 给你去找。



- `long_description`，我们从 README.md 里直接读取的 markdown 文档，所以把`long_description_content_type` 对于设置了 markdown。



- `install_requires`，是你这个项目依赖的包，可以让 pip 安装你的包的时候检查依赖，如果依赖没有安装或版本不对，就把正确的依赖也一起装上。注意，这里的依赖必须是 pypi 里有的(即你可以用 pip install xxx 安装的)。要了解更多请看：[install_requires vs requirements files](https://packaging.python.org/discussions/install-requires-vs-requirements/#install-requires-vs-requirements-files)



- `classifiers`，就是给你的项目贴些标签，方便别人检索啦，可选的在这个目录里：https://pypi.org/classifiers/



setup.py 里还可以指定很多其他东西的，具体看文档：https://packaging.python.org/guides/distributing-packages-using-setuptools/#setup-args

---

写完 setup.py 其实我们就可以在自己的电脑上 pip 安装这个包了！

```shell
$ cd packaging_tutorial
$ pip3 install .
$ cd ~
$ python3
>>> import example_pkg    # 注意这里import的不是setup里的name，而是packages列表里的包名
```

如果本地安装没问题（我没遇到问题，不清楚有没有坑），接下来，我们把包就要上传到 Pypi 了。

## 注册 Pypi 账号

和 GitHub 一样哈，你得先注册一个号才能上传到 Pypi。

直接点这个链接注册：[https://pypi.org/account/register/](https://pypi.org/account/register/)。

注册好之后，生成一个 token：https://pypi.org/manage/account/#api-tokens。由于我们是要上传新项目，所以不要限制 scope 到特定的项目。

⚠️**注意：token 生成出来以后不要马上关掉页面，不然就没了！！！把 token 复制粘贴保存到个本地的文件里(你要手抄我不反对，一百多位，别抄错就行 [狗头])。**

然后，创建一个纯文本文件 `$HOME/.pypirc` （Windows 咋搞自行解决，我不用Windows），在里面写：

```
[pypi]
username = __token__
password = <换成你刚刚复制下来的 token, 包括 `pypi-` 前缀>
```

注意，**不要把username改成你的用户名**，就是写 `username = __token__`，固定der！因为我们是要用 token 嘛，所以用户是 `__token__`。`password = token` 把 token 换成你的 token，注意不要换行，也不要加其他乱七八糟的空白字符（如果你要Windows的记事本，请小心BOM）。

例如：

```
[pypi]
username = __token__
password = pypi-BCqRT66666666kLTI1NjQzZGUJXsgElwaS576OnvGVIshizhegedeshisabiJzaW9uIjogMXC05ZzcIWlOs2lyTZCOCCCCU1NwACvbnL9IsWyPMiOiAidXiJBBBcmcicN0AAAYgCB82jrAI9RDJl5BJfK2333333
```

## 打包、上传

打包很简单：

```sh
$ cd packaging_tutorial
$ python setup.py sdist
$ tree .
.
├── LICENSE
├── README.md
├── packaging_tutorial.egg-info
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   ├── dependency_links.txt
│   ├── requires.txt
│   └── top_level.txt
├── dist
│   └── packaging_tutorial-0.0.1.tar.gz
├── setup.py
└── example_pkg
    ├── __init__.py
    └── src.py
```

你会看见出来些 `packaging_tutorial.egg-info`、`dist` 啦。如果你没兴趣，就不用管它们，把他们看成“编译”出来的二进制文件就好。这些也不用加版本管理里，你随时可以生成的。

然后就是上传了，这一步需要我们先安装一个 twine：

```sh
$ pip install twine
```

好了之后，用 twine 就可以把包上传到 pypi 了：

```sh
$ twine upload dist/*
```

当然，你可以只上传某个特定版本： `twine upload dist/packaging_tutorial-0.0.1.tar.gz`。

如果失败，请检查你的网络，确保你可以上 [pypi官网](https://pypi.org) (搞这些最好科学上网，不然我不知道能不能成)；还有检查你的 `$HOME/.pypirc`，token 有没有写错。

上传完它就会输出一个 URL：`https://pypi.org/project/<sampleproject>`，打开就可以在 pypi 里看到你的项目了！

## 用 Pip 安装自己写的包

最后，换台计算机（我们自己的电脑上已经安装过了嘛，痛失贞洁了，不好玩了）。

在另一台机器上（安装了 python、pip的）：

```sh
$ pip install packaging_tutorial
```

你可以看到下载、依赖处理、安装的过程。好了之后你就可以用自己写的包了：

```sh
$ python
>>> import example_pkg
```

## 最后

这篇文章只是对整个流程简要的记录和介绍，官方的这篇文章写了更完整的介绍：[Packaging and distributing projects](https://packaging.python.org/guides/distributing-packages-using-setuptools/#packaging-and-distributing-projects)。





