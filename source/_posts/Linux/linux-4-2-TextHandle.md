---
title: linux-4.2-正文处理
date: 2017-01-03 12:55:26
tags: Linux
categories:
	- Linux
	- Beginning
---

# 正文.处理

## `unix2dos`, `dos2unix`：Unix 与 DOS 正文转化

UNIX 系统的正文（纯文字）格式中只用换行符`\n`作为行结束符；

DOS & Windows 系统的正文中是以回车符 `\r` 和换行符 `\n` 作为行结束符；

用 `cat -A filename` 可见二者区别。

将 DOS 格式的文件转换成 UNIX 格式的文件用 `dos2unix file_name`；

将 UNIX 格式的文件转换成 DOS 格式的文件用 `unix2dos file_name`；

## `diff`, `sdiff`：比较两个文件的差别

### `diff file_1 file_2`：只输出两者不同点

显示结果中：

- 字母c为 比较，比较某行二者不同点；
- 字母d是 不同，显示一文无一文有的；
- “<”表示第1个文件中的数据行。
- “>”表示第2个文件中的数据行。

```
$ diff letters.upper letters
2c2        # 第1个文件的第2行与第2个文件的第2行比较。
< B        # 第1个文件的第2行为B。
---
> b        # 第2个文件的第2行为b。
6c6        # 第1个文件的第6行与第2个文件的第6行比较。
< F        # 第1个文件的第6行为F。
---
> f        # 第2个文件的第6行为f。
8d7        # 第1个文件一共有8行，而第2个文件一共有7行。
< H        # 第1个文件的第8行（也是最后一行）为H。
```

### `sdiff file_1 file_2`：side-by-side 输出两者所有行，标示不同

显示结果中：

- “|”左侧表示第1个文件中的数据行。

- “|”右侧表示第2个文件中的数据行。

- “<”表示第1个文件中的数据行（当第1个文件中有数据，但第2个文件中没有时）。

- “>”表示第2个文件中的数据行（当第2个文件中有数据，但第1个文件中没有时）。

```
$ sdiff letters.upper letters
A                             A
B                            | b            # 第1个文件中为B，第2个文件中为b。
C                             C 
D                             D
E                             E
F                            | f            # 第1个文件中为F，第2个文件中为f。
G                             G
H                             <            # 第1个文件中为H，第2个文件中的这一行为空。
```

> `sdiff` 命令的显示结果更容易阅读。
> 但是如果比较的两个文件很大，而其中的差别又很少，使用 `diff` 命令可能更好些。

## `aspell`, `look`：检查单词的拼写

aspell，look 的字典是 `/usr/share/dict/words `

###  `aspell`

`aspell` 是Linux系统上的一个交互式的英语拼写检查程序，该程序通过一个简单的菜单驱动的界面来提供改正英文单词的建议。

```
$ aspell check file_name
        Enter后，
        光标停留在第1个有拼写错误的单词上，
        并在终端窗口下部给出一些可供选择的正确单词；
        输入某个单词前面的编号来选择这个单词，
        系统就会立即修改光标所在处的单词；
        之后光标将移到下一个有拼写错误的单词。
$ aspell list < file_name
            以非交互的方式在终端窗口中列出某个文件中的全部有拼法错误的英语单词
```

• `look  <sth>`：列出所有以sth开头的英语单词以供选择。

```
$ look progra
prograde
program
......
```

## `expand`, `fmt`, `pr`: 重新格式化正文

### `expand`：将Tab化为空格

```
$ expand [-t 1] data.tab > data.spaces
        -t n：表示将制表键转换成n个空格符。
```

### `fmt`: 格式化文本

```
$ fmt -u -w48 news > news.fmt
        fmt将它的输入格式化成一些段落，
        其中段落宽度是使用-wn选项来定义的（w为width，n为字符的数目，系统默认宽度为75个字符）。
        利用-u选项将文件中的空格统一化（每个单词之间使用一个空格分隔，每个句子之间使用两个空格分隔）。
            
        fmt命令将它的输入中的空行当作段落分隔符看待。
```

### `pr`：按照打印机的格式重新编排纯文本文件中的内容

```
$ pr file
        pr命令的默认输出为每页66行，其中56行为正文内容，并包括表头。
        若没有指定列表头（Header），系统默认使用文件名作为列表头，并在每页的页首部分显示。
        另外，每页的页首部分还有页码和时间(inode.M_time)。
$ pr -h"English Dictionary on Linux" -l18 -5 /usr/share/dict/words | more
        -h选项为列表头（Header），
        在h后面使用双引号括起来的就是要显示的表头信息，
        -l选项用来定义每页的行数，-l18表示每页都有18行，
                （-l选项后的数目不能太小，如果太小pr命令会忽略这一选项）
        -5表示每页打印5列。
        
---------------------------
        
# Output：

2006-10-08 02:00           English Dictionary on Linux            Page 1
&c             'prentice      'shun          'tis          'un
'd             're            'slid          'twas         've
......
2006-10-08 02:00           English Dictionary on Linux            Page 2
-acal          -acy          -age          -ana           -ar
-acea          -ad           -agogue       -ance          -arch
--More--
```
