---
title: linux-3.0.1-文件及其操作
date: 2016-12-26 16:06:36
tags: Linux
categories:
	- Linux
	- Beginning
---

# 文件及其操作

## Linux文件类型：

| 表示 | 名称           | 解释                                         |
| ---- | -------------- | -------------------------------------------- |
| -    | regular file   | 普通文件，或称正规文件                       |
| d    | directory      | 目录                                         |
| l    | symbolic link🏎 | 符号（软）连接                               |
| b    | block          | 块特殊文件：一般是指块设备，如硬盘。         |
| c    | character      | 字符特殊文件：一般是指字符设备，如键盘。     |
| p    | pipe           | 命名的管道文件：一般用于在进程之间传输数据。 |
| s    | socket🐶        | 套接字：通信（过程中）的一个终点。           |

🏎. 详见本系列文章的“<u>连接(link)</u>”

🐶.  socket 的比喻性解释：

**socket与电话十分相似：**

_当与某人通话时就要建立两个通信的终点：_

_（1）自己的电话_

_（2）对方的电话_

_只要双方进行通话，就必须有两个通话所必需的终点（电话）和一条在它们之间的通信线路存在。_

        socket就相当于一条通信线路的终点（电话），而在这些终点（sockets）之间存在着数据通信网络。

_当打电话给他人时，需要拨打对方的电话号码。_

        sockets使用网络地址取代了电话号码。通过访问远程（计算机）的socket地址，本机程序就可以用的本机socket与远程的终点（socket）之间建立起一条通信线路。


## 文件操作

- file：确定文件类型

```
$ file 文件名
```

- touch：刷新、新建文件

```
$ touch file(s)
        若file存在，更新时间戳
        若file不存在，新建空文件
```

- cp：复制

```
$ cp [-option(s)]  source(s)  target
    把source复制到target：
        -i：交互式：防止覆盖，覆盖前提示
        -f：强制式：有同名，强制覆盖，不提示
        -r：递归式：复制目录时包括子目录
        -p：维持式：保留属性（如时间戳）
        source是目录名或文件名
        target是目录名或 新文件名(复制并重命名)
```

- mv：移动及修改文件、目录名

```
$ mv file(s) target
    把source移动到target：
        source是目录名或文件名
        target是目录名或 新文件名(移动并重命名)
```

        重命名可用“**mv  path/old\_name  path/new\_nam**e”实现

- rm：删除

```
$ rm  [option(s)]  file(s)|directory(s)
    删除文件或 目录(加-r)：
        -i：交互式：删前提示
        -r：递归式：包括子目录、文件
        -f：强制性：不询问，直接删
```

- find：搜索文件和目录

```
$ find Pathname Expressions Actions
    •Pathname：遍历起始路径
    •Expressions：条件表达式：
        -name“指定文件名”
        -size[+|-]n
                文件大小大于小于或等于(n*512B)
        -atime[+|-]n
                访问天数
        -mtime[+|-]n：更改天数
        -user LoginID：属于某用户的所有文件
        -type：某一类型的文件：
                f：文件
                d：目录
                e t c
        -perm：查找具有某些特定访问许可位的文件
    •Actions：对找出的文件进行的操作：
        -exec命令{} \;
                在每一个所定位的文件上运行指定的命令。
                “{}“  表明文件名将传给前面的命令。
                “ \;” 表示命令的结束。
                （在大括号与反斜线之间必须有一个空格。）
        -ok命令{} \;
                -exec命令的交互方式
                （在find命令对每个定位的文件执行命令之前需要确认）
        -print
                指示find命令将当前的路径名打印在终端屏幕上
                （默认方式）
        -ls
                显示当前路径名和相关的统计信息
                如i节点（inode）数、以K字节为单位的大小（尺寸）、保护模式、硬连接和用户
```

    可用`find /etc -name passwd  2>finderrs.txt`重定向，把权限不足的错误不在屏幕显示。


