---
categories:
- Linux
- Beginning
date: 2017-01-10 19:51:00
tags: Linux
title: linux-9.0-grep
---

# grep/egrep/fgrep

grep、egrep、fgrep：搜索文件中满足特定模式(pattern)或字符串的内容，将结果输出到1，不改变原文件。

（UNIX中的patterns被称为 _Regular Expressions_）

> grep="Global，Regular Expressions，Print"，即“在文件全局中用正则表达式搜索结果打印输出”

grep、egrep能在一个或多个文件等内容中搜索某一特定的Character Pattern（R.E.）。

### grep

grep命令支持以下几种正则表达式的元字符（regular expression metacharacters），即通配符：

- `c*` ：将匹配0个（即空白）或多个字符c（c为任一字符）。
- `.` ：将匹配任何一个字符而且只能是一个字符。
- `[xyz]` ：将匹配方括号中的任意一个字符。
- `[^xyz]`  ：将匹配不包括方括号中的字符的所有字符。
- `^` ：锁定行的开头。
- `$` ：锁定行的结尾。

在基本正则表达式中：

        如元字符`*`、`+`、`{`、`|`、`(` 和 `)` 已经失去了它们原来的含义，

        如果要恢复它们原本的含义要在之前冠以反斜线'\\'，如 `\*`、`\+`、`\{`、`\|`、`\(` 和 `\)`。

grep命令是用来在每一个文件中或标准输出上搜索特定的模式。

当使用grep命令时，包含一个指定字符模式的每一行都会被打印在屏幕上，

使用grep命令并不改变文件中的内容。

```
grep 选项 模式 文件名
        选项可以改变grep命令的搜寻方式：
            -c：仅列出包含模式的行的数量。
            -i：忽略模式中的字母大小写。
            -l：列出带有匹配行的文件名。
            -n：在每行的最前面列出行号。
            -v：列出没有匹配模式的行。
            -w：把表达式作为一个完整的单字来搜寻，忽略那些部分匹配的行。
[⚠️]除了-w选项之外，其他的每个选项都可以在egrep和fgrep命令中使用。
[⚠️]如果是搜索多个文件，grep命令的结果只显示在文件中发现匹配模式的文件名，而搜索的是单一的文件，grep命令的结果将显示每一个包含匹配模式的行。
```

_e.g._

```
$ grep CLERK emp.data        #显示包含了CLERK的行
7369    SMITH   CLERK   800     17-DEC-80
7876    ADAMS  CLERK   1100    23-MAY-87
$ grep -c CLERK emp.data        # 只显示用几个满足行
2
$ grep ^78 emp.data      # 列出在emp.data文件中所有以78开始的数据行
$ grep '1..0' emp.data    #'1..0'表示以1开始随后是两个任意字符最后是0的字符串。
$ grep '[12]..0'        # '[12]..0'表示以1或2开始随后是两个任意字符最后是0的字符串。
$ grep -l root group passwd hosts    # 在当前目录中的group、passwd和hosts 3个文件中搜索模式root并列出包含这一模式的文件名。
$ grep '/bash$' passwd    # 列出在passwd文件中所有以/bash结尾的行（Get所有默认使用bash的用户）。
$ ps -e | grep ftp    # 获取目前系统使用的ftp服务的进程名
$ ps -e | grep ora    # To know is Oracle Database runing
```

### egrep

<p align="left"><span style="color: rgb(253, 4, 4);">/* egrep 在RHEL等Linux上其实是「grep -E」的别名 \*/</span></p>
<p align="left">egrep的语法格式与grep命令相同，</p>
但egrep是用来在一个或多个文件的内容中利用**扩展的正则表达式**的元字符搜索特定的模式。

egrep所增加的元字符：

- +：匹配一个或多个前导字符。
- a|b：匹配a或b。
- (RE)：匹配括号中的正则表达式RE。

e.g.

```
$ egrep '[1-5]+000' emp.data        # 匹配1000，2000，3000，4000，5000
$ egrep 'S[A-Z]+MAN' emp.fmt        # 匹配“Sxx...xxMAN”
$ egrep 'E(S|R) ' emp.fmt           # 在每一行数据中搜寻字母E后面紧跟着S或R
```

### fgrep

<span style="color: rgb(253, 4, 4);">/* fgrep 在RHEL等Linux上其实是「grep -F」的别名 \*/</span>

fgrep也用来在一个或多个文件中搜索与指定字符串匹配的行。

搜索文件fgrep的速度要比grep快，

fgrep可以一次迅速地搜索多个模式。

与grep不同，fgrep命令不能搜索任何正则表达式，

即将**通配符当作普通字符**来处理（按该字符的字面意思来处理）。

搜索文件命令fgrep不能使用特殊字符，只能搜索确定的模式。

fgrep既可以在命令行上键入搜索的模式，

也可以使用-f选项从文件中读取要搜索的模式。

e.g.

```
$ cat emp.fmt | fgrep -f conditions
    # 等价于
$  fgrep -f conditions.txt emp.fmt
		# grep也可以如以上二者操作: 列出emp.fmt文件中所有与conditions.txt文件中内容相匹配的数据行。

```