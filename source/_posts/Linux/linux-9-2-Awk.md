---
categories:
- Linux
- Beginning
date: 2017-01-12 20:04:37
tags: Linux
title: linux-9.2-awk
---

# awk

## awk命令的通用语法格式

```
awk '{commands}'
    commands为一个或多个命令
    常用选项：
        -f，表明awk命令将从该标志之后的文件中读取指令而不是从命令行读取；
        -Fc，这个标志表明字段之间的分隔符是c而不是默认的空白字符（如制表键、一个或多个空格符）。
```

常用点：

- **print**：将一行接一行地打印出文件中的所有数据行。

可用 `print str1 str2 int1,int2...`

也可`print(A,B,C,...)`

```
$ who | awk '{ print }'
        ==直接使用「who」
```

awk 中也可以用 c 风格的 printf()：

```
printf("Total: %s\n",totalsize)
    用printf注意'\n'
```

## `$n`：字段变量

在文件和Linux命令的结果显示中:

        每行信息被指定的分隔符分隔成若干个字段，
    
        每个字段都被赋予一个唯一的标识符。
    
        如，字段1的标识符是 `$1`，字段2的标识符是 `$2` 等。
    
        特殊地，有变量 `$0` 表示整行 「`$0=re('^\*$')`」

```
$ who | awk '{ print $1 }'
    列出who命令显示结果中每行的第1个字段，即目前登录Linux系统的用户名
$ who | awk '{ print "User  " $1 " is on terminal line " $2}'
    再上一个命令的基础上加入一些解释性的话
$ awk '{ print "Employee  " $2 " has salary " $4}' emp.data
    emp.data文件中的第2个字段为员工姓，第4个字段为工资，
    在员工姓前加上Employee，
    在员工的姓和工资之间加上has salary字符串
$ egrep 'foo|bar' /etc/passwd | awk -F: '{ print $1" has " $7 " as loggin shell." }'
        # 在/etc/passwd中所有的字段都是以:分隔的。
  获取某些用户登录时使用的shell：
    egrep命令从/etc/passwd文件中抽取包含foo或bar的数据行；
    awk命令把冒号看成字段的分隔符并将列出第1个（用户名）和第7个字段（登录时的shell），
    同时还将在显示结果中加入一些描述信息以帮助阅读和理解；
$ awk -F: '{ print $7 }' /etc/passwd | sort | uniq -c
    获取系统上各个shell分别被几个用户默认使用
$ grep /bin/ /etc/passwd | awk -F: '{ print $1" " $7 }' | sed '/sync/d' | sort
    获取哪些用户在登录时使用的shell是存放在/bin目录中以及这个shell的名字；
    并且有个用/bin/sync的sync用户，不让它出现在显示的结果；
    最后进行排序。
$ who | awk '{ print $6": "$0}'
     在每个用户记录的最前面显示这个用户登录Linux系统所使用的计算机
     # who显示结果中的最后一个字段是用户登录Linux系统所使用的计算机的IP地址，如果为空表示是本机登录
```

## `NF`、`NR`变量

- `NF`

若 在命令表达式中使用没有 `$` 符号的NF变量：

         `NF` 将显示一行记录中**有多少个字段**。

若 在命令表达式中使用带有`$`符号的NF变量，

         `$NF` 将显示一行记录中**最后一个字段**(即，第NF个字段 -> 最后一个字段)

- `NR`

变量 `NR` 用来追踪所显示的数据行的数目，即**显示数据行的编号**。

```
$ who | awk '{ print NF }'
    列出who命令显示结果中每一行的字段数（列数）
$ who | awk '{ print $NF }'
    列出who命令显示结果中每一行的最后一个字段
$ egrep 'bin|sbin' /etc/passwd | awk -F: '{ print $NF }' | sort | uniq -c | sort -n
    egrep    ：从/etc/passwd文件中抽取包含bin或sbin的数据行
    awk      ：把冒号看成字段的分隔符，列出每一行的最后一个字段
    sort     ：将那些字段进行排序
    uniq -c  ：合并相同行，并在每行前面冠以该行出现次数
    sort -n  ：按次数的大小进行排序。
$ ls -l ~/wolf | awk '{ print NR": "$0}'        # 用N给每行一个编号
1: total 16
2: drwxrwxr-x  2 dog dog 4096 Jan 25  2009 boywolf
3: -rw-rw-r--  1 dog dog   84 Dec 22 19:07 delete_disable\
......
```

- awk的command中print可打印 `\n`, `\t` 等

```
$ ls -lF /boot | awk '{ print $5 "\t" $9}' | sort -rn | head -3
    列出/boot目录中每一个文件的文件名和大小，文件的大小在前，而文件名随后，文件大小和文件名由制表键隔开。
    按大小反序排列（从大到小）
    把其中最大的3个文件
```

## awk中计算

变量使用前不用声明

使用c语言的运算符

```
$ ls -lF /boot | awk '{ totalsize += $5; print totalsize }'
    获取/boot目录中所有文件大小的总和
    （将得到累加过程中每一步的totalsize值）
为得到最终结果，不输出中间值：
$ ls -lF /boot | awk '{ totalsize += $5; print totalsize }' | tail -1
    除了使用tail命令之外，一种更好的方法是在awk命令中使用END关键字：
$ ls -lF /boot | awk '{ totalsize += $5} END { print totalsize }'
```

## `END` 关键字：

在最后一步执行END后的{statements}，如上例最后一个命令。

## 将 `commands`表达式放入文件

- 用cat

框中为要输入的（注意末尾新行键入EOF后回车（<<EOF）可以自动退出）

（直接用cat > script2写完后ctrl+D也可以）

用此法会有写完后文件中“$5”字样缺失的问题。

- 用vi直接写完保存更好（不用写EOF，也没有$n缺失的问题）

保存入文件后可以：

```
$ ls -lF /boot | awk -f script1
```

- 将awk写入shell脚本

将一些经常使用的命令放入一个正文文件，这个文件就是所谓的shell脚本文件。

```
写入：（注意用""把命令括起来，否则将把"$(ls ...)"写入）
$ echo "ls -lF /boot | awk -f script1" > boot_size
调用：
$ bash boot_size
$ sh boot_size
$ ksh boot_size
...
```

## awk中使用if条件、for循环与 C 语言相似

```
$ awk  '{ if (length($4) == 3  ) print $0 }' emp.data | wc -l
```

![IMG_1074](https://tva1.sinaimg.cn/large/006y8mN6ly1g6b0tm7hpgj30go04qjrv.jpg)

`count[length($1)]++`：将第1个字段的长度作为数组元素的下标，并将这个数组元素的个数加1再重新存回到原来的数组元素中。（似动态语言）