---
categories:
- Python
- 基础手册
date: 2020-03-28 22:46:39
tag: Python
title: Python基础手册P2 基本数据类型基本类型
---

# Python 基本数据类型

。。。

今天没有想要写在开头的废话，，，好烦，要不破例直接开始吧。

## 变量与常量

### 变量

Python 是一门**动态语言**，这意味着 Python 变量本身的类型是不固定的。
在 Python 中使用变量前**不用声明**（不用写类似 `int a;` 的语句），**在首次使用前为其赋初始值**就行（直接用 `a = 0`）。

### 常量

实际上，在 Python 语法中并**没有定义常量**。

但是 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 定义了常量的命名规范为**大写字母和下划线**组成。在实际应用中，这种“常量”首次赋值后，**无法阻止其他代码对其进行修改或删除**。

要使用真正的常量，可以自己实现一个，例如：[constants-in-python](https://code.activestate.com/recipes/65207-constants-in-python/)。


## 空值

Python 中使用 `None` 来代表空值。
`None` 在交互式命令行中不会显示，但可以用 `print()` 打印出来：

```python
>>> None
>>> a = None
>>> a
>>> print(a)
None
```

## 布尔值

Python 中有布尔值 `True` 和 `False`。

### 真值问题

代表 ‘假’ 的值有：`False`，`None`，`0`，`''`，`[]`，`{}`，...；
其余值为真。

### 布尔值的相关的运算

| 逻辑运算符 | 相当于C中的 |
| ----- | --- |
| `and` | `&&` |
| `or` | `||` |
| `not` | `!` |

⚠️【注意 `and` 的优先级高于 `or`。

| 比较运算符 |
| --- |
| `<`, `>`, `==`, `!=` |

使用比较运算符得到的结果是布尔值（`True` 或 `False`）。

**使用逻辑运算符得到的结果未必是布尔值**：

具体的运算情况可以参考下面这段程序生成的表：

```python
# **注意，是第一列的值 and|or 第一行的值！**
li = ['and', 'or']
ls = [True, False, None, 0, 1, 2, '"abc"']

for opt in li:
    # head
    print('<%s>' % opt, end='\t')
    for j in ls:
        print(j, end='\t')
    print('\n')

    for i in ls:
        # col
        print(i, end='\t')
        for j in ls:
            # row
            print(
                    eval('%s %s %s' % (i, opt, j)),
                    end='\t'
                    )
        print('\n')
    # end
    print('\n-------\n')
```


从中可以看到，
`and` 的规则是：

> 前后两者 **皆为真** ，返回 **后** 者；
> 前后两者 **有一假** ，返回 **假** 者；
> 前后两者 **皆为假** ，返回 **前** 者；

`or` 的规则是：

> 前后两者 **皆为真** ，返回 **前** 者；
> 前后两者 **有一真** ，返回 **真** 者；
> 前后两者 **皆为假** ，返回 **后** 者；

此外，
`not` 的规则是：
> 若对象为 **真** ，返回 `False`
> 若对象为 **假** ，返回 `True`


## 数字

### int, float

Python 中内置有 [int](https://docs.python.org/3/library/functions.html#int) 和 [float](https://docs.python.org/3/library/functions.html#float) 两类数字。

| 数字 | 含义 | 表示范围 | 精度 |
| -- | -- | -- | -- |
| int | 整数 | 大小没有限制 | 始终是准确的 |
| float | （基于二进制的）浮点数 | 有一定大小限制，超出后表示为inf | 和C一样，不准确 |

### 复数

Python 还内置了对 [复数](https://zh.wikipedia.org/wiki/复数_(数学)) 的支持，使用后缀 `j` 或 `J` 表示虚数部分（例如，`3+5j`）。

```python
>>> a = 3 + 1j
>>> b = 3 - 1j
>>> a * b
(10+0j)
>>> 
```

关于这部分详见[官方文档](https://docs.python.org/3/library/stdtypes.html#typesnumeric)。

### 其他数字类型

在标准库中，python 还有对 [精确小数 Decimal（基于十进制的浮点数）](https://docs.python.org/3/library/decimal.html#decimal.Decimal)和 [分数  Fraction](https://docs.python.org/3/library/fractions.html#fractions.Fraction) 等其他数字类型的支持。

#### Decimal （小数）

在 Python 的标准库中，`decimal` 库提供了 *基于十进制的浮点数* **Decimal** 类型，这种数字类型修复了 float 的不准确问题，可以用 **Decimal** 实现更加精准的数学计算(但也不是绝对的准确，仍存在误差)。

```python
>>> from decimal import *
>>> 0.1 + 0.1 + 0.1 - 0.3   # float
5.551115123125783e-17       # 这个结果是不精确的
>>> Decimal(0.1) + Decimal(0.1) + Decimal(0.1) - Decimal(0.3)   # decimal
Decimal('2.775557561565156540423631668E-17')    # 较为精确
>>> getcontext().prec = 12    # 限制 Decimal 的小数位数
>>> Decimal(0.1) + Decimal(0.1) + Decimal(0.1) - Decimal(0.3)
Decimal('1.11022302463E-17')
```

正如上例，要使用 `Decimal` 类型，
* 首先要 `import decimal`；
* 然后用 `decimal.Decimal(Num)`来获取一个 Decimal 实例，这里的 Num 可以是如下几种：
```python
>>> Decimal('3.14')     # 内容是 float 的字符串
Decimal('3.14')
>>> Decimal((0, (3, 1, 4), -2))  # tuple (sign, digit_tuple, exponent)，得到的值是 (-1) * sign * digit_tuple 代表数字 * 10 ^ exponent
Decimal('3.14')
>>> Decimal(314)        # int，float 都可以
Decimal('314')
>>> Decimal(Decimal(314))  # 另一个 decimal 实例
Decimal('314')
>>> Decimal('  3.14  \\n')    # 前后可以有空白字符
Decimal('3.14')
```

* decimal.getcontext().prec 代表有效位数，
    * 通过 `print(decimal.getcontext().prec)` 来查看当前值，默认是28位
    * 通过 `decimal.getcontext().prec = Places` 来设置有效位数，这个精度的取值是 `[1, MAX_PREC]` ，MAX_PREC取值在64位机器上是 `999999999999999999`，32位为 `425000000`（这是因为这个值要可以转化为C的整型，详见[Python版的源码](https://github.com/python/cpython/blob/3.7/Lib/_pydecimal.py)）！

* 加减乘除运算入常

#### Fraction （分数）

在 `fractions` 库中，定义了 `Fraction` 类型，用以表达分数，加减乘除运算入常。

使用方法如下：

```python
>>> from fractions import *
>>> Fraction(1.5)    # 传入 float，会自动算出分数表示
Fraction(3, 2)
>>> Fraction(1, 3)   # 传入 分子，分母
Fraction(1, 3)
>>> Fraction(2, 6)   # 默认会有理化
Fraction(1, 3)
>>> Fraction(2, 6, _normalize=False)    # 指定不有理化
Fraction(2, 6)
>>> Fraction(Fraction(1/11))    # 另一个 Fraction 实例，Decimal 实例也可以
Fraction(3275345183542179, 36028797018963968)
>>> Fraction(' 22/7 ')    # 使用代表分数的字符串，注意 numerator/denominator，中间不可有空格，前后可有空白字符
Fraction(22, 7)
```

## 字符串

### 字符串的表示

Python 中，字符串可以用单引号 (`'...'`) 或双引号 (`"..."`) 标识单行内的字符串，
还可以使用连续三个单/双引号(`'''...'''` 或 `"""..."""`)表示与格式化的多行字符。

Python没有单独的字符类型；一个字符就是一个简单的长度为1的字符串。

```python
>>> st = '1\
... 2\
... 3\
... a'
>>> st
'123a'
>>> st = '''1
... 2
... 3
... a
... '''
>>> st
'1\n2\n3\na\n'
>>> 
```

⚠️【注意】单引号可以包含双引号，`'asd"123"fgh'` 是允许的，同样 `'''` 中也可以包含 `"""`。

### 字符编码

首先，附上几种字符编码的比较：
| 编码 | 长度 | 'A' | '中' |
| -- | -- | -- | -- |
| ASCII | 1 Byte | **01000001** | (无此字符) |
| Unicode | 通常是2 Byte | *00000000* **01000001** (ASCII前补零) | 01001110 00101101 |
| UTF-8 | 可变（1~6 Byte）| **01000001** （UTF-8包含着ASCII）| 11100100 10111000 10101101 |

Python3.x 默认用 Unicode 编码字符串。

编码 <=> 字符 的函数：
* `ord()`：获取字符的整数表示；
* `chr()`：把编码转换成对应的字符；

例如：

```python
>>> ord('A')
65
>>> ord('中')
20013
>>> chr(66)
'B'
>>> chr(20014)
'丮'
```

---

Python 的字符串类型是 `str`。

> `str` 在内存中以 Unicode 表示，一个字符对应若干字节。

在写入二级缓存（本地->硬盘 | 远程->网络）时，`str`将变为`bytes`。

> `bytes` 以字节为单位。

Python 用带 `b` 前缀的单/双引号表示 `bytes`。

| str | bytes |
| -- | -- |
| `'ABC'` | `b'ABC'` |

---

str <=> bytes:

* encode(): str --> bytes

```python
>>> 'abc'.encode('ascii')
b'abc'
>>> '中文'.encode('utf-8')
b'\xe4\xb8\xad\xe6\x96\x87'
>>> '中文'.encode('ascii')    # 超出范围了，报错
'''
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)
'''

```

* decode(): bytes --> str

```python
>>> b'abc'.decode('ascii')
'abc'
>>> b'\xe4\xb8\xad\xe6\x96\x87'.decode('utf-8')
'中文'
>>> b'\xe4\xb8\xad\xe6\x96\x87'.decode('ascii')    # 超出范围了，报错
'''
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeDecodeError: 'ascii' codec can't decode byte 0xe4 in position 0: ordinal not in range(128)
'''
>>> # 若 bytes 中包含无法解码的字节，decode() 会报错；
>>> # 可以在调用 decode() 时传入 `errors='ignore'` ，以忽略错误字节。
>>> b'\xe4\xb8\xad\xe6\x96\x87asd'.decode('ascii', errors='ignore')
'asd'
```

⚠️【注意】为避免乱码问题，**应始终使用 `utf-8` 编码对 `str` 和 `bytes` 进行转换。**

### 转义字符

Python 字符串中可以使用转义字符，可以参考下表：

| 转义字符 | 描述 |
| -- | -- |
| ` \ `(在行尾时) | 续行符 |
| `\\` | 反斜杠符号 |
| `\'` | 单引号 |
| `\"` | 双引号 |
| `\a` | 响铃 |
| `\b` | 退格(Backspace) |
| `\e` | 转义 |
| `\000` | 空 |
| `\n` | 换行 |
| `\v` | 纵向制表符 |
| `\t` | 横向制表符 |
| `\r` | 回车 |
| `\f` | 换页 |
| `\xxx` | 八进制数，例如：`'\100'` 代表 `'@'` |
| `\oyy` | 八进制数，yy代表的字符，例如：`'\o12'` 代表换行 |
| `\xyy` | 十六进制数，yy代表的字符，例如：`'\x0a'` 代表换行 |
| `\uxxxx` | 十六进制数，xxxx代表的字符，例如：`'\u4e2d\u6587'` 代表 `'中文'` |
| `\other` | 其它的字符以普通格式输出，例如：`'\sds'` 代表 `'\\sds'` |

若要取消转义，可以给字符串 `r` 前缀：

```python
>>> print('C:\some\name')  # here \n means newline!
C:\some
ame
>>> print(r'C:\some\name')  # note the r before the quote
C:\some\name
```

### 基本字符串操作

#### 获取字符串长度

Python 内置的 `len()` 函数可以获取多种类型的对象长度，包括字符串。

```python
>>> len(word)
6
>>> # 这个方法等效于：
>>> word.__len__()
6
```

#### 字符串连接

* 相邻的两个字符串文本自动连接在一起。

```python
>>> 'Py' 'thon'
'Python'
>>> # 这个功能可以用来写长字符串：
>>> text = ('Put several strings within parentheses '
            'to have them joined together.')
>>> text
'Put several strings within parentheses to have them joined together.'
```

* 字符串的 `+` 与 `*`

字符串可以由 + 操作符连接(粘到一起)，可以由 * 表示重复。

```python
>>> # 3 times 'un', followed by 'ium'
>>> 3 * 'un' + 'ium'
'unununium'
```

#### 字符串插值

字符串的插值主要有 4 种方式：

1. 字符串连接

```python
>>> a = 123
>>> "a is " + str(a) + ":)" 
'a is 123:)'
```

2. `%` 元组插值

```python
>>> a = 123
>>> b = 66.77
>>> c = 'hello'
>>> 'a = %s, b = %s, c = %s' % (a, b, c)
'a = 123, b = 66.77, c = hello'
```

3. 字符串的 `format` 方法

```python
>>> 'a = {arg_a}, b = {arg_b}, c = {arg_c}'.format(arg_a="东方", arg_b=123, arg_c=333.44+8j)
'a = 东方, b = 123, c = (333.44+8j)'
```

或者也可以匿名：

```python
>>> 'Another way: {0}, {2}, {1}, {3}'.format("zero", 2, 1.0, 3)
'Another way: zero, 1.0, 2, 3'
```

4. `f-string`

Python 3.6 引入了 `f-string`，让插值更加优雅：

```python
>>> a = 123
>>> b = 456.789
>>> f'{a} + {b} = {a+b}'
'123 + 456.789 = 579.789'
```

更多关于 `f-string` 的说明，可以参考 [realpython的这篇文章](https://realpython.com/python-f-strings/)，或者查看 `f-string` 的来源：[PEP 498 -- Literal String Interpolation](https://www.python.org/dev/peps/pep-0498/)。

#### 字符串切分

用字符串的 split 方法可以以指定字符串为分割切分字符串：

```python
>>> 'a b   c'.split(' ')
['a', 'b', '', '', 'c']
>>> 'he-*-ll-*-o--'.split('-*-')
['he', 'll', 'o--']
```

#### 字符串替换

用字符串的 replace 方法可以替换字符串的一部分：

```python
>>> 'he-*-ll-*-o--'.replace('-*-', '...')
'he...ll...o--'
```

#### 字符串索引及切片

* **索引**

| 字符 | P | y | t | h | o | n |
| -- | --| -- | -- | -- | -- | -- |
| 正向索引 | 0（-0） | 1 | 2 | 3 | 4 | 5 | 6 |
| 反向索引 | -6 | -5 | -4 | -3 | -2 | -1 |

```python
>>> word = 'Python'
>>> word[0]  # character in position 0
'P'
>>> word[-2]  # second-last character
'o'
```

* **切片**

索引用于获得单个字符，切片 让你获得一个子字符串。

切片的规则是：`str[起始:末尾:间隔]`
	* 起始：开始的索引（取），缺省为0
	* 末尾：结束的索引(不取)，缺省时，取到字符串最后一个字符（取得到）
	* 间隔：每取一个之后间隔几个（>0），缺省为1，为负值时倒着取

```python
>>> word[0:2]  # characters from position 0 (included) to 2 (excluded)
'Py'
>>> # 几个常用模式：
>>> word[1:-1]    # 去掉首位字符（可以用来去括号、引号）
'ytho'
>>> word[::-1]    # 字符串反向
'nohtyP'
```

⚠️【注意】切片包含起始的字符，不包含末尾的字符。
`s[:i] + s[i:] == s`
⚠️【注意】字符串**索引、切片**都是**只读**的，不可以给字符串索引、切片赋值！

### 正则表达式

字符串的使用肯定绕不过正则表达式，python 内置了正则表达式模块—— `re` 。

我不在这里介绍正则表达式的写法，只是展示怎么用 Python 完成常见的正则表达式操作。正则本身有问题，请到 https://regexr.com。

**匹配**：

```python
import re
pattern = r'abc(.*?)def'	# 正则里有大量'\',用r字符串取消转义
test = 'abc123def'
if re.match(pattern, test):
    print('ok')
else:
    print('failed')
```

**提取**：

```python
import re
pattern = r'abc(.*?)def(\d+)'
test = 'abc123def456'
m = re.match(pattern, test)
if m:
    print(m.groups())
else:
    print('failed')
```

用 m.groups() 即可获取提取到的组：`('123', '456')`。

**切分**：

```python
# 切分
re.split(r'[\s\,\;]+', 'a,b;; c  d')
```

## 集合类型

其实，在我心中，字符串也是种集合类型（你学过C语言就会有同感了，字符串不过是字符组成的 list 而已）。所以，刚才介绍字符串的很多操作，在接下来的 list 中也一样适用。

### list

list：列表，写在 `[]` 中。

```python
>>> l0 = []
>>> l1 = [1, 2, 3]
>>> l2 = list("hello")
>>> print(f'{l0}\n{l1}\n{l2}')
[]
[1, 2, 3]
['h', 'e', 'l', 'l', 'o']
```

**索引&切片**：

- get：`lst[索引 || 切片]`
- set：`lst[索引 || 切片] = 值`

```
>>> l[0] = 3.14
>>> l[0]
3.14
```

索引&切片 和字符串中介绍的相同，不了解可以这回去看。

我们来看 list 的基本操作：

**尾部添加**：`lst.append(值)`, `lst.extend(iterable)`

```python
>>> l = []
>>> l.append(12)
>>> l.append("abc")
>>> l.append(999)
>>> l.append([3, 4])
>>> l.extend(['你', '好'])
>>> l.extend({'再': 1, '见': 2})
>>> l
[12, 'abc', 999, [3, 4], '你', '好', '再', '见']
```

append 和 extend 一个是添加单个元素，一个是添加一系列元素。

利用切片，append 方法就等效于 `lst[len(lst):] = [值]`, 而 extend 即 `lst[len(lst):] = iterable`。

**插入**：`lst.insert(索引, 值)`

```python
>>> l = []
>>> l.insert(0, 100)
>>> l.insert(len(l), 200)       # 等效于 l.append(200)
>>> l.insert(1, 300)
>>> l.insert(1, 400)
>>> l
[100, 400, 300, 200]
```

**删**：`lst.remove(值)`, `lst.pop(索引)`, `clear()`

remove 是删除 list 中存在的一个值，若不存在，会报 ValueError。

pop 是删除 list 中给定索引处的值，若索引越界，会报 IndexError。

clear 就是清空（删除）所有元素；也可以用 `del a[:]` 完成类似的操作。

```python
>>> l
[100, 400, 300, 200]
>>> l.remove(400)
>>> l
[100, 300, 200]
>>> l.pop()		# pop 缺省参数则出最后一个，等效于 pop(-1) 或 pop(len(l)-1)
200
>>> l.pop(0)
100
>>> l
[300]
>>> l.remove('fool')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: list.remove(x): x not in list
>>> l.pop(999)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: pop index out of range
>>> l.clear()
>>> l
[]
```

**其他操作**：

- `list.index(x[, start[, end]])`: 你给值，它返索引
- `list.count(x)`: 你给值，它告诉你有几个
- `list.sort(key=None, reverse=False)`: 一种比较快的原址排序
- `list.reverse()`: 列表反转，调个个（这个词好怪a，我的问题嘛？）
- `list.copy()`: 返一个自己的*浅拷贝*。

关于 list ，可以写的东西实在太多了，都可以单独再写一篇，专门研究了。。。（以后再说吧，可能我会写吧，用了复习数据结构课。）

### tuple

tuple：元组，和 list 类似，只是常写在 `()` 中。

tuple 可以 get，**不能set**。也就是说，不能 append、不能 pop、不能索引赋值。

```python
>>> t = (1,2,3)
>>> t[1] = "sdfdsf"
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'tuple' object does not support item assignment
>>> t
(1, 2, 3)
>>> t.append(12)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'tuple' object has no attribute 'append'
>>> t.pop()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'tuple' object has no attribute 'pop'
>>> t[1:]
(2, 3)
```

注意，刚才我写了一句“tuple常写在`()`中”，何来此“常”，tuple 不就是写在圆括号里的嘛？如果你有此疑问，一定是没有好好读过文档。

给你个改过自新的机会：[https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences](https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences)：

![RTFM](https://tva1.sinaimg.cn/large/00831rSTgy1gdeo2dghg1j304j03mdfs.jpg)

文档里写了：

>  A tuple consists of a number of values separated by commas.

意思是说：“元组(tuple)是一系列用逗号分开的值！”，可没提用圆括号扩起来的呀，再看看这个例子:

```python
>>> t = 12345, 54321, 'hello!'
>>> t[0]
12345
>>> t
(12345, 54321, 'hello!')
>>> # Tuples 可以嵌套:
... u = t, (1, 2, 3, 4, 5)
>>> u
((12345, 54321, 'hello!'), (1, 2, 3, 4, 5))
>>> # Tuples 不可变:
... t[0] = 88888
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'tuple' object does not support item assignment
>>> # 但可以包含可变的元素:
... v = ([1, 2, 3], [3, 2, 1])
>>> v
([1, 2, 3], [3, 2, 1])
```

可见，tuple 对 Python 中例如函数参数的一系列元素的打包传递相当有用！

### set

`set` 是保证**元素唯一**的**无序**集合。

我们一般也就用它来消除重复，保证唯一。当然，你应该知道，`set` 就大概对应于数学里的「集合」，所以 `set` 可以算 ~~病娇茶部~~ 并、交、差、~~补~~（你可以想象，数学那种补是不能算的，但可以算「[对称差](https://en.wikipedia.org/wiki/Symmetric_difference)」）。

创建一个 set 有两种写法：`set()` 函数和使用花括号 `{ele1, ele2, ...}`。但如果你要建空 set，只能用 `set()`，而不能用 `{}`！因为你应该知道，`{}` 建的是空字典。

```python
>>> s = {}
>>> type(s)
<class 'dict'>
>>> s = set()
>>> type(s)
<class 'set'>
>>> s1 = set([1, 2, 3])
>>> s1
{1, 2, 3}
>>> s2 = {3, 4, 5, 5, 5}
>>> s2
{3, 4, 5}
>>> type(s2)
<class 'set'>
```

```python
>>> a
{1, 2, 3}
>>> b
{3, 4, 5}
>>> a | b    # 并，类似于「逻辑或」：在a或在b或都在
{1, 2, 3, 4, 5}
>>> a & b    # 交，类似于「逻辑与」：在a且在b
{3}
>>> a - b    # 差，类似于「逻辑差」：在a不在b
{1, 2}
>>> a ^ b    # 对称差，类似于「逻辑异或」：在a或在b，但不都在
{1, 2, 4, 5}
```

### dict

dict：字典，键值对，底层实现是哈希表。字面值写作 `{key1: value1, key2: value2, ...}`。

既然 dict 都写成和 set 一样的 `{}` 了，那你看可以想象，dict 也可以保证唯一性 —— dict保证 key 的唯一。

key 可以是任何「不可变」的值，也就是说，数字、字符串、不包含可变元素的元组都可以作为 key。

```python
>>> d = {1: 'abc', '2': 2.0001}
>>> d[1]
'abc'
>>> d['2']
2.0001
```

```python
>>> tel = {'jack': 4098, 'sape': 4139}
>>> tel['guido'] = 4127
>>> tel
{'jack': 4098, 'sape': 4139, 'guido': 4127}
>>> tel['jack']
4098
>>> del tel['sape']		# 删除元素
>>> tel['irv'] = 4127
>>> tel
{'jack': 4098, 'guido': 4127, 'irv': 4127}
>>> list(tel)			# 取键
['jack', 'guido', 'irv']
>>> sorted(tel)
['guido', 'irv', 'jack']
>>> 'guido' in tel		# 键在不在字典里
True
>>> 'jack' not in tel
False
```

用 `dict()` 函数可以有更多初始化字典的技巧，我随便从文档抄两个，你细品：

```python
>>> dict([('sape', 4139), ('guido', 4127), ('jack', 4098)])
{'sape': 4139, 'guido': 4127, 'jack': 4098}
>>> dict(sape=4139, guido=4127, jack=4098)
{'sape': 4139, 'guido': 4127, 'jack': 4098}
```

### 推导式

推导式（comprehensions）是用来创建集合类型实例的。

比如，你想建一个“1到10的平方组成的list”，你如何来写代码？

当然，数据量不大，我们肯定可以这样：

```python
a = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

但如果是1～100，1～100000呢？你想用循环对吧：

```python
>>> a = []
>>> for i in range(1, 101):
...     a.append(i**2)
... 
```

但这样不够简洁！

“1到10的平方组成的list”，说起来就一句话，代码也应该简简单单一行就完成！「推导式」就是干这个的：

```python
>>> [x**2 for x in range(1, 11)]
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

推导式的一般形式是：

```python
[表达式 任意个for或if句]
```

这个例子可以给你个比较好的印象：

```python
>>> [(x, y, x*y) for x in [1,2,3] for y in [3,1,4] if x != y]
[(1, 3, 3), (1, 4, 4), (2, 3, 6), (2, 1, 2), (2, 4, 8), (3, 1, 3), (3, 4, 12)]
>>> # 相当于：
>>> combs = []
>>> for x in [1,2,3]:
...     for y in [3,1,4]:
...         if x != y:
...             combs.append((x, y, x*y))
...
>>> combs
[(1, 3, 3), (1, 4, 4), (2, 3, 6), (2, 1, 2), (2, 4, 8), (3, 1, 3), (3, 4, 12)]
```

其实准确的说，我们刚才写的这些都是「列表推导式」。我们还有「set推导式」甚至是「dict推导式」。

```python
>>> {x for x in 'abracadabra' if x not in 'abc'}
{'r', 'd'}
>>> {x: x**2 for x in (2, 4, 6)}
{2: 4, 4: 16, 6: 36}
```

你可能还想写这个：

```python
>>> (x**2 for x in range(1, 11))
<generator object <genexpr> at 0x107988bd0>
```

哈哈，有点不一样了，这次它给你返了个 generator——生成器，这就不是推导式了，这里不做介绍，后面我们再讨论这东西。

最后，再看两个很有意思的例子：

```python
>>> [[(j, i, j*i) for j in range(1, i+1)] for i in range(1, 10)]
或
>>> [(j, i, j*i) for i in range(1, 10) for j in range(1, i+1)]
[[(1, 1, 1)], [(1, 2, 2), (2, 2, 4)], [(1, 3, 3), (2, 3, 6), (3, 3, 9)], [(1, 4, 4), (2, 4, 8), (3, 4, 12), (4, 4, 16)], [(1, 5, 5), (2, 5, 10), (3, 5, 15), (4, 5, 20), (5, 5, 25)], [(1, 6, 6), (2, 6, 12), (3, 6, 18), (4, 6, 24), (5, 6, 30), (6, 6, 36)], [(1, 7, 7), (2, 7, 14), (3, 7, 21), (4, 7, 28), (5, 7, 35), (6, 7, 42), (7, 7, 49)], [(1, 8, 8), (2, 8, 16), (3, 8, 24), (4, 8, 32), (5, 8, 40), (6, 8, 48), (7, 8, 56), (8, 8, 64)], [(1, 9, 9), (2, 9, 18), (3, 9, 27), (4, 9, 36), (5, 9, 45), (6, 9, 54), (7, 9, 63), (8, 9, 72), (9, 9, 81)]]
```

乘法表，这两种写法效果是一样的。

```python
>>> matrix = [
...     [1, 2, 3, 4],
...     [5, 6, 7, 8],
...     [9, 10, 11, 12],
... ]
>>> [[row[i] for row in matrix] for i in range(4)]
[[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]]
```

没错！矩阵转置，利用推导式中只用一行代码就可以实现。

---

未完待续...

（最近这两天都在补作业呀、补作业呀、补作业呀...不补作业的时候还要打游戏...忙得很。而且最近练习双拼，中文打字速度直线下降，所以这篇写了好久。现在作业大概补完了，双拼也已有了小成（大概？），以后应该会快一些了。）

Next: 【Python流程控制】