---
date: 2020-11-24 12:32:38.584971
tags: Python
title: Python删除字符串后缀问题
---
# Python删除字符串后缀问题

[TOC]

## 问题发现

我的 GitHub Pages 博客 [clownote](https://clownote.github.io) 是通过 Hexo + 一些自己写的本地脚本 + Github Action 来自动发布的（参考鄙人拙作《[还在手动发博客？GitHub Actions自动化真香](https://blog.csdn.net/u012419550/article/details/107594751)》）。

文章修改的 GitHub 提交信息是通过一个脚本自动生成的，它会列出修改的文章名对于具体的文章（都是 markdown），会忽略后缀 `.md`，这样好看一些，而其他文件（工具脚本）则保留完整文件名：

![截屏2020-11-24 11.39.24](https://tva1.sinaimg.cn/large/0081Kckwly1gl041kzke7j30n50ai0u3.jpg)

前几天写了篇名叫 `Intro_sham.md` 的文章，即《[我这人不懂什么操作系统，于是用Go语言模拟出了一个](https://blog.csdn.net/u012419550/article/details/109731346)》，它的提交信息是：

![截屏2020-11-24 11.41.14](https://tva1.sinaimg.cn/large/0081Kckwly1gl043el96rj30k303c3yq.jpg)

`changed files: Intro_sha` 莫名缺了一个 `m`。。。

## 问题定位

打开工具脚本，找到写 Git 提交 message 的代码在这里：

```python
def push(**kwargs):
    ...
    names = map(lambda f: os.path.basename(f).rstrip('.md'), changed)
    commit_msg = 'changed files: ' + ', '.join(names)
    ...
```

`changed files` 的名字是通过一个作用于所有改变了的文件的 map 方法得到的。这个 map 做的工作是把文件的路径和 `.md` 后缀去掉（只是为了好看）。

问题呼之欲出 —— `rstrip` 的错误使用。

## 问题复现

```python
>>> s = "emmm.md"
>>> s.rstrip('.md')
'e'
```

## RTFM

看一看 rstrip 的文档：https://docs.python.org/3.7/library/stdtypes.html#str.rstrip

```python
str.rstrip([chars])
```

里面写了：

> Return a copy of the string with trailing characters removed. 
> The chars argument is a string specifying the set of charactersto be removed. 
> The chars argument is not a suffix; rather, all combinations of its values are stripped.

是结尾处有你给的 chars 参数里字符的任意组合都会被删。

## 解决方案

这个问题其实是个长期以来的痛点，StackOverflow 相关问题阅读量破万，问题活跃时长超过 7 年。以前我就碰到过，当时写这里的时候就有点感觉，似乎用 rstrip 好像不太妥当，但随便测试了几个例子没问题也就这么用了。

### 正则

解决这种问题的一个方法是用正则：

```python
import re
re.sub('^' + re.escape(prefix), '', s)  # 删前缀
re.sub(re.escape(suffix) + '$', '', s)  # 删后缀
```

要导个包，麻烦。代码可读性也低，效率....估计也不怎么样。

### 切片

另一种方法是用切片解决，代码可以封装地好看一点：

```python
# Reference https://www.python.org/dev/peps/pep-0616/
def removeprefix(self: str, prefix: str, /) -> str:
    if self.startswith(prefix):
        return self[len(prefix):]
    else:
        return self[:]

def removesuffix(self: str, suffix: str, /) -> str:
    # suffix='' should not call self[:-0].
    if suffix and self.endswith(suffix):
        return self[:-len(suffix)]
    else:
        return self[:]
```

### 官方

实际上，为了解决这种问题，[PEP 616 -- String methods to remove prefixes and suffixes](https://www.python.org/dev/peps/pep-0616/) 提出了专门用来删前缀/后缀的方法，这是 Python 3.9 的新特性：

```python
s.removeprefix('prefix')
s.removesuffix('suffix')
```

P.S. 官方的 C 实现还是很有意思的，可以去看看：[cpython/pull/18939](https://github.com/python/cpython/pull/18939/files) 。

但这里我的环境是 Python 3.7，所以只能用前两种方法手撸一个啦。

## TL;DR 太长不看

用 `str.rstrip` 来删除字符串后缀是错误的，这个方法会删除参数中各字符的任意组合。

```python
>>> s = "emmm.md"
>>> s.rstrip('.md')
'e'
```

解决方法：

1. 用 Python 3.9：`s.removesuffix('suffix')`
2. 正则表达式：`re.sub(re.escape(suffix) + '$', '', s)`
3. endswith + 切片：

```python
def removesuffix(s: str, suffix: str) -> str:
    if suffix and self.endswith(suffix):
        return self[:-len(suffix)]
    else:
        return self[:]
```

---

好了，这节课我们不往下讲了，剩下的时间来做个小练习，看看今天的知识大家学废了吗。。。（**'蠢'.capitalize()**）

```python
# See you!
'CDFMLR 2020-11-24 11:22'.rstrip(':2333')
```

