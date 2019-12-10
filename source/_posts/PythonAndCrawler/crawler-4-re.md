---
title: Python之正则表达式
date: 2019-02-13 22:49:55
tags: Crawler
categories:
	- Crawler
---

# 爬虫基本库的使用之RE

> 本文主要介绍 **正则表达式** 及 **RE 库**。



## 正则表达式

正则表达式是一种处理字符串的强大的工具，它有自己特定的语法结构，可以高效地实现字符串的检索、替换、匹配验证等操作。

我们可以利用正则表达式来提取 HTML 中我们感兴趣的信息，正如我们在使用 requests 库爬取知乎发现中的问题时那样。

下表为 正则表达式 的常用匹配规则：

| 模式 | 描述 |
| -- | -- |
| `\w` | 匹配字母数字及下划线 |
| `\W` | 匹配非字母数字及下划线 |
| `\s` | 匹配任意空白字符，等价于 `[\t\n\r\f]` |
| `\S` | 匹配任意非空字符 |
| `\d` | 匹配任意数字，等价于 `[0-9]` |
| `\D` | 匹配任意非数字 |
| `\A` | 匹配字符串开始 |
| `\Z` | 匹配字符串结束，如果是存在换行，只匹配到换行前的结束字符串 |
| `\z` | 匹配字符串结束 |
| `\G` | 匹配最后匹配完成的位置 |
| `\n` | 匹配一个换行符 |
| `\t` | 匹配一个制表符 |
| `^` | 匹配字符串的开头 |
| `$` | 匹配字符串的末尾 |
| `.` | 匹配任意字符，除了换行符，当 re.DOTALL 标记被指定时，则可以匹配包括换行符的任意字符 |
| `[...]` | 用来表示一组字符，单独列出：`[amk]` 匹配 'a'，'m' 或 'k' |
| `[^...]` | 不在 [] 中的字符：`[^abc]` 匹配除了 a,b,c 之外的字符。 |
| `*` | 匹配 0 个或多个的表达式。 |
| `+` | 匹配 1 个或多个的表达式。 |
| `?` | 匹配 0 个或 1 个由前面的正则表达式定义的片段，非贪婪方式 |
| `{n}` | 精确匹配 n 个前面表达式。 |
| `{n, m}` | 匹配 n 到 m 次由前面的正则表达式定义的片段，贪婪方式 |
| `a|b` | 匹配 a 或 b |
| `( )` | 匹配括号内的表达式，也表示一个组 |

⚠️【注意】贪婪匹配下，`.*` 会匹配尽可能多的字符；非贪婪匹配则尽可能匹配少的字符。
⚠️【注意】转义：如果在正则中想表现表中有的那些符号，我们需要转义，即使用 ` \ `+ 符号。例如要表现括号`(`，我们需要写 `\(`

例如，之前我们抓取「知乎-发现」中的问题时，使用的是如下正则表达式：

```
explore-feed.*?question_link.*?>(.*?)</
```

它就可以匹配请求到的 html 中的：

```html
<div class="explore-feed feed-item" data-offset="1">
<h2><a class="question_link" href="/question/311635229/answer/..." target="_blank" data-id="..." data-za-element-name="Title">
......
</a></h2>
```

## RE 库

Python 内置的 `re` 库提供了对正则表达式的支持。

下面我们来了解 re 库的使用：

#### `match()`

match() 方法，需要我们传入*要匹配的字符串*以及*正则表达式*，来检测这个字符串是否符合该正则表达式。

match() 方法判断是否匹配，如果匹配成功，返回一个Match对象，否则返回None。

match() 会从一开始匹配，也就是说，如果第一个字符就匹配不上去，则就不匹配。

我们常可以这样用：

```python
test = '待测字符串'
if re.match(r'正则表达式', test):
    print('Match')
else:
    print('Failed')
```

提取分组：

```python
>>> text = 'abc 123'

>>> print(re.match(r'\s+\w\d', text))
None

>>> r = re.match(r'\w*? (\d{3})', text)
>>> r
<re.Match object; span=(0, 7), match='abc 123'>
>>> r.group()
'abc 123'
>>> r.group(0)
'abc 123'
>>> r.group(1)
'123'
```

* group()、group(0) 会输出完整的匹配结果。
* group(1)，以及此例中没有的group(2)，group(3)... 则会输出第一、二、三...个被 `()` 包围的匹配结果。


#### 修饰符

| 修饰符 | 描述 |
| -- | -- |
| `re.I` | 使匹配对大小写不敏感 |
| `re.L` | 做本地化识别（locale-aware）匹配 |
| `re.M` | 多行匹配，影响 `^` 和 `$` |
| `re.S` | 使 `.` 匹配包括换行在内的所有字符 |
| `re.U` | 根据Unicode字符集解析字符。这个标志影响 `\w`, `\W`, `\b`, `\B`. |
| `re.X` | 该标志通过给予你更灵活的格式以便你将正则表达式写得更易于理解。 |

这些修饰符可以作为 re.match 的第三个参数传入，产生上面描述中的效果。

```python
result = re.match('^He.*?(\d+).*?Demo$', content, re.S)
```

#### `search()`

与 match() 不同，search() 在匹配时会扫描整个字符串，然后返回第一个成功匹配的结果，如果一处都没有，则返回 None.

```python
>>> p = '\d+'
>>> c = 'asd123sss'
>>> r = re.search(p, c)
>>> r
<re.Match object; span=(3, 6), match='123'>
>>> r.group()
'123'
```

#### `findall()`

`findall()` 会搜索整个字符串然后返回匹配正则表达式的所有内容，返回的结果为一个list。

```python
>>> import re
>>> p = '\d+'
>>> c = 'asd123dfg456;;;789'
>>> re.findall(p, c)
['123', '456', '789']
```
