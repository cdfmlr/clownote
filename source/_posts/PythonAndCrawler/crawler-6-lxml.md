---
categories:
- Crawler
date: 2019-02-15 22:49:55
tags: Crawler
title: Python之LXML
---

# Python爬虫解析库的使用之LXML

> 本文主要介绍 XPath 和解析库 LXML 的使用。



## XPath & LXML

XPath (XML Path Language) 是设计来在XML文档中查找信息的语言，它同样适用于HTML。

我们在爬虫时，可以使用 XPath 来做相应的信息抽取。

⚠️【注意】需要安装好 LXML。

#### XPath常用规则

| 表达式 | 描述 |
| -- | -- |
| `nodename` | 选取此节点的所有子节点 |
| `/` | 从当前节点选取直接子节点 |
| `//` | 从当前节点选取子孙节点 |
| `.` | 选取当前节点 |
| `..` | 选取当前节点的父节点 |
| `@` | 选取属性 |

我们常用 `//` 开头的 XPath 规则来选取所有符合要求的节点。

另外，常用运算符见 [XPath 运算符](http://www.w3school.com.cn/xpath/xpath_operators.asp)。

#### 导入 HTML

##### 从字符串导入 HTML

导入了 LXML 库的 etree 模块，然后声明了一段 HTML 文本，调用 HTML 类进行初始化，这样我们就成功构造了一个 XPath 解析对象。

⚠️【注意】etree 模块可以对 HTML 文本进行修正。

调用 tostring() 方法即可输出修正后的 HTML 代码，结果是 bytes 类型（可以利用 decode() 方法转成 str 类型）

```python
from lxml import etree
text = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a>
     </ul>
 </div>
'''
html = etree.HTML(text)
result = etree.tostring(html)
print(result.decode('utf-8'))
```

##### 从文件导入 HTML

```python
from lxml import etree

html = etree.parse('./test.html', etree.HTMLParser())
result = etree.tostring(html)
print(result.decode('utf-8'))
```

#### 获取节点

##### 获取所有节点

获取一个 HTML 中的所有节点，使用规则 `//*`：

```python
from lxml import etree
html = etree.parse('./test.html', etree.HTMLParser())

result = html.xpath('//*')

print(result)
```

我们得到了一个 由 Element 类型组成的列表。

##### 获取所有指定标签

如果我们想获取所有 li 标签，我们可以把上例中的html.xpath() 中的规则改为 `'//li'`：

```python
from lxml import etree
html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//li')
print(result)
```

如果无法获取任何匹配结果，html.xpath 将会返回 `[]`

##### 获取子节点

选择 li 节点所有直接 a 子节点，使用规则 `'//li/a'`：

```python
from lxml import etree

html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//li/a')
print(result)
```

要获取其下所有子孙a节点可以这样：`//li//a`

##### 获取特定属性的节点

用 @ 符号进行属性过滤。
smt[...] 是有 ... 限制的smt。

选中 href 是 link4.html 的 a 节点，规则是 `'//a[@href="link4.html"]`:

```python
from lxml import etree

html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//a[@href="link4.html"]')
print(result)
```

##### 获取父节点

如果我们想获取上例的父节点, 然后再获取其 class 属性：

```python
from lxml import etree

html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//a[@href="link4.html"]/../@class')
# 也可以用“节点轴” '//a[@href="link4.html"]/parent::*/@class'

print(result)
```

关于节点轴的使用，详见 [XPath Axes](http://www.w3school.com.cn/xpath/xpath_axes.asp)

##### 获取节点中的的文本

XPath 中的 text() 方法可以获取节点中的直接文本（不包括其子节点中的文本）。

```python
from lxml import etree

html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//li[@class="item-0"]/text()')
print(result)
```

##### 获取属性

```python
from lxml import etree

html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//li/a/@href')
print(result)
```

用上面这种方法只能获取只有一个值的属性，
对于下面这种：

`<li class="li li-first"><a href="link.html">first item</a></li>`

 li 节点的 class 属性有两个值，上面这个方法会失效，我们可以使用 contains() 函数：

```python
from lxml import etree
text = '''
<li class="li li-first"><a href="link.html">first item</a></li>
'''
html = e#tree.HTML(text)
result = html.xpath('//li[contains(@class, "li")]/a/text()')
print(result)
```

这里还可以使用运算符 and 来连接：

```python
from lxml import etree
text = '''
<li class="li li-first" name="item"><a href="link.html">first item</a></li>
'''
html = etree.HTML(text)
result = html.xpath('//li[contains(@class, "li") and @name="item"]/a/text()')
print(result)
```

#### 补充

点击链接查看详细的 [XPath 教程](http://www.w3school.com.cn/xpath/index.asp) 、 [lxml 库](https://lxml.de)。

