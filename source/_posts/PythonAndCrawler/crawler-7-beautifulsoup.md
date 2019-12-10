---
title: Python之BeautifulSoup
date: 2019-02-16 22:49:55
tags: Crawler
categories:
	- Crawler
---

# Python爬虫解析库的使用之BeautifulSoup

> 本文主要介绍解析库 BeautifulSoup 的使用。



## BeautifulSoup

> BeautifulSoup 提供一些简单的、Python式的函数用来处理导航、搜索、修改分析树等功能。它通过解析文档为用户提供需要抓取的数据。利用它我们可以提高解析效率。

BeautifulSoup 拥有完善的官方中文文档，可以查看 [BeautifulSoup官方文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/)

⚠️【注意】需要安装好 BeautifulSoup 和 LXML。

BeautifulSoup 可以使用多种解析器，主要的几种如下：

| 解析器 | 使用方法 | 优势 | 劣势 |
| -- | -- | -- | -- |
| Python标准库 | BeautifulSoup(markup, "html.parser") | Python的内置标准库、执行速度适中 、文档容错能力强 | Python 2.7.3 or 3.2.2)前的版本中文容错能力差 |
| LXML HTML 解析器 | BeautifulSoup(markup, "lxml") | 速度快、文档容错能力强 | 需要安装C语言库 |
| LXML XML 解析器 | BeautifulSoup(markup, "xml") | 速度快、唯一支持XML的解析器 | 需要安装C语言库 |
| html5lib | BeautifulSoup(markup, "html5lib") | 最好的容错性、以浏览器的方式解析文档、生成 HTML5 格式的文档 | 速度慢、不依赖外部扩展 |

我们一般使用 LXML 解析器来进行解析，使用方法如下：

```python
from bs4 import BeautifulSoup
soup = BeautifulSoup('<p>Hello</p>', 'lxml')    
print(soup.p.string)
```

#### BeaufulSoup对象的初始化

使用如下代码就可以导入HTML，完成BeautifulSoup对象的初始化，并自动更正（如闭合未闭合的标签）。

```python
soup = BeautifulSoup(markup, "lxml")   # markup 是 HTML 的 str
```

初始化之后我们还可以对要解析的字符串以标准的缩进格式输出：

```python
print(soup.prettify())
```

#### 节点选择器

##### 选择标签

选择元素的时候直接通过调用节点的名称就可以选择节点元素，
调用 string 属性就可以得到节点内的文本。

```python
from bs4 import BeautifulSoup

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

soup = BeautifulSoup(html, 'lxml')

print(soup.title)           # <title>The Dormouse's story</title>
print(type(soup.title))     # <class 'bs4.element.Tag'>
print(soup.title.string)    # The Dormouse's story
print(soup.head)            # <head><title>The Dormouse's story</title></head>
print(soup.p)               # <p class="title" name="dromouse"><b>The Dormouse's story</b></p>
```

##### 嵌套选择

我们还可以进行 **嵌套选择**，即做类似 `父.子.孙` 的选择：

```python
print(soup.head.title.string)
```

##### 关联选择

有时候我们难以做到一步就可以选择到想要的节点元素，这时我们可以先选中某一个节点元素，然后以它为基准再选择它的子节点、父节点、兄弟节点等等

###### 获取**子孙节点**

选取到了一个节点元素之后，如果想要获取它的直接 **子节点** 可以调用 `contents` 属性，将返回一个依次列有所有子节点的list。

如p标签之类的节点中可能既包含文本，又包含节点，返回的结果会将他们以列表形式都统一返回。

```python
soup.p.contents     # 注意里面的文字被切成了几部分

'''(result)
[
    'Once upon a time ... were\n',
    <a class="sister" href="..." id="link1"><!-- Elsie --></a>,
    ',\n',
    <a class="sister" href="..." id="link2">Lacie</a>,
    ' and\n',
    <a class="sister" href="..." id="link3">Tillie</a>,
    ';\nand ... well.'
]
'''
```

同时，查询 **子节点**，我们还可以使用 `children` 属性，它将返回一个 list_iterator object，化为 list 之后，就和 contents 一样了：

```python
>>> s.p.children
<list_iterator object at 0x109d6a8d0>
>>> a = list(soup.p.children)
>>> b = soup.p.contents
>>> a == b
True
```

我们可以逐个编号输出子节点：

```python
for i, child in enumerate(soup.p.children):
    print(i, child)
```

要得到所有的 **子孙节点**（所有下属节点）的话可以调用 descendants 属性，descendants 会递归地查询所有子节点（深度优先），得到的是所有的子孙节点，返回结果是一个 `<generator object Tag.descendants at 0x109d297c8>`：

```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
print(soup.p.descendants)
for i, d in enumerate(soup.p.descendants):
    print(i, d)
```

###### 获取父节点和祖先节点

如果要获取某个节点元素的父节点，可以调用 `parent` 属性，返回一个节点:

```python
>>> soup.span.parent
# 结果是 <p>...</p>
```

如果我们要想获取所有的祖先节点(一层层向上找，直到整个html)，可以调用 `parents` 属性，返回一个generator：

```python
>>> soup.span.parents
<generator object PageElement.parents at 0x109d29ed0>
>>> list(soup.span.parents)
# 结果是 [<p>...</p>, <div>...</div>, <body>...</body>, <html>...</html>]
```

⚠️【注意】父是 parent，祖先是 parents

###### 获取兄弟节点

要获取同级的节点也就是兄弟节点，我们可以调用了四个不同的属性，它们的作用不尽相同：

* next_sibling：获取节点**向下一个**兄弟节点，返回节点。
* previous_sibling：获取**向上一个**兄弟节点，返回节点。
* next_siblings：获取**向下所有**兄弟节点，返回一个generator。
* previous_siblings：获取**向上所有**兄弟节点，返回一个generator。

```python
>>> from bs4 import BeautifulSoup
>>> html = """
... <html>
...     <body>
...         <p class="story">
...             Once upon a time there were three little sisters; and their names were
...             <a href="http://example.com/elsie" class="sister" id="link1">
...                 <span>Elsie</span>
...             </a>
...             Hello
...             <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> 
...             and
...             <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>
...             and they lived at the bottom of a well.
...         </p>
... """
>>> soup = BeautifulSoup(html, 'lxml')
>>> soup.a
<a class="sister" href="http://example.com/elsie" id="link1">
<span>Elsie</span>
</a>
>>> soup.a.next_sibling
'\n            Hello\n            '
>>> soup.a.previous_sibling
'\n            Once upon a time there were three little sisters; and their names were\n            '
>>> soup.a.next_siblings
<generator object PageElement.next_siblings at 0x1110e57c8>
>>> soup.a.previous_siblings
<generator object PageElement.previous_siblings at 0x1110e5de0>
>>> for i in soup.a.previous_siblings:
...     print(i)
... 

            Once upon a time there were three little sisters; and their names were
            
>>> for i in soup.a.next_siblings:
...     print(i)
... 

            Hello
            
<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
 
            and
            
<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>

            and they lived at the bottom of a well.
        
>>> 

```

----

#### 方法选择器

有时难以利用节点选择器直接找到想要的节点时，我们可以利用 find_all()、find() 等方法，传入相应等参数就可以灵活地进行查询，得到想要的节点，然后通过关联选择就可以轻松获取需要的信息。

##### `find()`

find() 传入一些属性或文本来得到符合条件的元素，返回第一个匹配的元素。

```python
find(name , attrs , recursive , text , **kwargs)
```

使用实例如下：

```python
from bs4 import BeautifulSoup

html='''
<div class="panel">
    <div class="panel-heading">
        <h4>Hello</h4>
    </div>
    <div class="panel-body">
        <ul class="list" id="list-1">
            <li class="element">Foo</li>
            <li class="element">Bar</li>
            <li class="element">Jay</li>
        </ul>
        <ul class="list list-small" id="list-2">
            <li class="element">Foo</li>
            <li class="element">Bar</li>
        </ul>
    </div>
</div>
'''

soup = BeautifulSoup(html, 'lxml')
print(soup.find(name='ul')
print(soup.find(attrs={'class': 'element'}))
print(soup.find(text=re.compile('.*?o.*?', re.S)))      # 结果会返回匹配正则表达式的第一个节点的文本（结果不是节点）
```

##### `findall()`

find_all，类似于 find，但是 find_all 查询所有符合条件的元素，返回所有匹配的元素组成的列表。

##### 更多

还有诸如find_parents()、find_next_siblings()、find_previous_siblings()等的find，基本使用都差不多，只是搜索范围不同，详见 [文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/)。

---

#### CSS选择器

BeautifulSoup 还提供了 CSS 选择器。
使用 CSS 选择器，只需要调用 select() 方法，传入相应的 CSS 选择器即可，返回的结果是符合 CSS 选择器的节点组成的列表：

```python
from bs4 import BeautifulSoup

html='''
<div class="panel">
    <div class="panel-heading">
        <h4>Hello</h4>
    </div>
    <div class="panel-body">
        <ul class="list" id="list-1">
            <li class="element">Foo</li>
            <li class="element">Bar</li>
            <li class="element">Jay</li>
        </ul>
        <ul class="list list-small" id="list-2">
            <li class="element">Foo</li>
            <li class="element">Bar</li>
        </ul>
    </div>
</div>
'''

soup = BeautifulSoup(html, 'lxml')
print(soup.select('.panel .panel-heading'))
print(soup.select('ul li'))
print(soup.select('#list-2 .element'))
print(type(soup.select('ul')[0]))
```

---

#### 提取信息

##### 获取完整标签

要获取一个标签的完整html代码，只需要写它的节点选择器即可： 

`soup.title`

##### 获取标签类型

利用 name 属性来获取节点的类型（p、a、title、pre 等）：

`print(soup.title.name)`

##### 获取标签内容

正如我们之前所说，调用 string 属性就可以得到节点内的文本：

`soup.title.string`

⚠️【注意】如果标签下包含其他标签，`.string` 是不起作用的，它会返回一个 None：

```python
>>> from bs4 import BeautifulSoup
>>> html = '<p>Foo<a href="#None">Bar</a></p>'
>>> soup = BeautifulSoup(html, 'lxml')
>>> print(soup.p.string)
None
```

获取内容，还可以使用节点的 get_text() 方法：

`soup.p.get_text()`

利用get_text，可以获取标签下所有文本，包括其子节点中的：

```python
>>> from bs4 import BeautifulSoup
>>> html = '<p>Foo<a href="#None">Bar</a></p>'
>>> soup = BeautifulSoup(html, 'lxml')
>>> print(soup.p.string)
None
>>> print(soup.p.get_text())
FooBar
```

##### 获取属性

每个节点可能有多个属性，比如 id，class，我们可以调用 attrs 获取所有属性，进而可以通过字典的取值方法(中括号加属性名称，或调用其`get()`方法)获取特定属性：

```python
print(soup.p.attrs)
print(soup.p.attrs['name'])

'''(results)
{'class': ['title'], 'name': 'dromouse'}
dromouse
'''
```

也可以直接使用中括号和属性名：

```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
for ul in soup.select('ul'):
    print(ul['id'])
    print(ul.attrs['id'])
    # 循环体的两行代码等效
```