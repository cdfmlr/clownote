---
title: Python爬虫解析库的使用之PyQuery
date: 2019-02-17 22:49:55
tags: Crawler
categories:
	- Crawler
---

# Python爬虫解析库的使用之PyQuery

> 本文主要介绍解析库 PyQuery 的使用。



## PyQuery

> pyquery: a jquery-like library for python

PyQuery 的使用方法和jQuery基本相同。

⚠️【注意】需要安装好 PyQuery。

#### 初始化

PyQuery 初始化时可以传入多种形式的数据源，如内容是 HTML 的字符串、源的URL、本地的文件名等。

##### 字符串初始化

```python
from pyquery import PyQuery as pq

html = '''
<h1>Header</h1>
<p>Something</p>
<p>Other thing</p>
<div>
    <p>In div</p>
</div>
'''

doc = pq(html)      # 传入HTML字符串
print(doc('p'))     # 传入CSS选择器

'''(results)
<p>Something</p>
<p>Other thing</p>
<p>In div</p>

'''
```

##### URL初始化

```python
from pyquery import PyQuery as pq
doc = pq(url='http://www.baidu.com', encoding='utf-8')      # 这里不写encoding可能中文乱码
print(doc('title'))

'''(result)
<title>百度一下，你就知道</title>
'''
```

#### CSS选择器

详见 [CSS 选择器表](http://www.w3school.com.cn/cssref/css_selectors.asp)。

#### 查找节点

* 查找**子**节点用 `children('css-selector')` 方法，参数为空则为全部。
* 查找**子孙**节点用 `find('css-selector')` 方法，**参数不可为空！**
* 查找**父**节点用 `parent('css-selector')` 方法，参数为空则为全部。
* 查找**祖先**节点用 `parents('css-selector')` 方法，参数为空则为全部。
* 查找**兄弟**节点用 `siblings('css-selector')` 方法，参数为空则为全部。

```python
>>> p = doc('div')
>>> p
[<div#wrapper>, <div#head>, <div.head_wrapper>, <div.s_form>, <div.s_form_wrapper>, <div#lg>, <div#u1>, <div#ftCon>, <div#ftConw>]
>>> type(p)
<class 'pyquery.pyquery.PyQuery'>
>>> p.find('#head')
[<div#head>]
>>> print(p.find('#head'))
<div id="head"> ... </div> 
```

#### 遍历

用 PyQuery 选择到的结果可以遍历：

```python
>>> for i in  p.parent():
...     print(i, type(i))
... 
<Element a at 0x1055332c8> <class 'lxml.html.HtmlElement'>
<Element a at 0x105533368> <class 'lxml.html.HtmlElement'>
<Element a at 0x105533458> <class 'lxml.html.HtmlElement'>
```

注意是lxml的Element了，要用lxml的方法处理。

#### 获取信息

##### `attr()` 获取属性

```python
a = doc('a')
print(a.attr('href'))
```

attr() 必须传入要选择的属性名。
若对象包含多个节点，调用对象的attr()，只会返回第一个对象的对应结果。要返回每一个的需要遍历。

##### `text()` 获取文本

```python
a = doc('a')
a.text()
```

这个会输出所有包含节点的文本join的结果。

#### 节点操作

PyQuery 还可以操作节点，这个不是重点。

