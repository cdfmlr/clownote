---
categories:
- Linux
- Beginning
date: 2016-12-24 15:38:20
tags: Linux
title: linux-2.3-文件的安全控制
---

# 文件的安全控制

- Linux系统的安全模型

- 用户**登录**系统时必须**提供用户名和密码**。

/*  用户是由root用户创建的，最初的密码也是root用户设定的 \*/

- 使用**用户**和**群组**来控制使用者**访问**文件和其他资源的**权限**。
  
- 系统上的每一个**文件**都一定**属于**一个**用户**（一般该用户就是文件的创建者）并**与**一个**群组相关**。
  
- 每一个**进程**都会**与**一个**用户和群组**相**关联**。可以通过在所有的文件和资源上设定权限来只允许该文件的**所有者**或者某个**群组**的成员访问它们。

- Linux 上文件有三种类型的权限：

- 所有者  ：（u）：文件的**<u>所有者</u>**的权限
  
- 同组用户：（g）：与所有者**<u>同一群组</u>**的其他用户的权限
  
- 其他用户：（o）：非所有者也**<u>不同群</u>**的用户的权限

/* root用户不受权限限制，可以访问Linux上的任何资源 \*/

- 权限的表示：

  | 字母表示     | 数字表示 | 含义    | 对文件的权限                  | 对目录的权限                        |
  | ------------ | -------- | ------- | ----------------------------- | ----------------------------------- |
  | r            | 4        | Read    | 可阅读文件                    | 使用ls列出目录内容                  |
  | w            | 2        | Write   | 可编辑文件                    | 编辑目录(在其中创建、删除等)        |
  | x            | 1        | eXecute | 可执行程序(可执行文件)        | 使用cd进入目录，用ls -l查看目录详情 |
  | - （连字符） | 0        | no      | 没用相应的权限(同位的r\|w\|x) | 没用相应的权限(同位的r\|w\|x)       |

- 查看文件的权限

用 **ls -l **命令：显示结果中的第1列（10个字符）表示文件的mode：

![IMG_1065](http://ww3.sinaimg.cn/large/006tNc79gy1g60eo9tu5zj306n02j74b.jpg)

<p align="left">其中第1个字符表示文件的类型：</p>
- 如果是d就表示是目录
  
- 如果是-就表示是文件。

紧接其后的9个字符是这个文件或命令的权限：

![IMG_1062](http://ww2.sinaimg.cn/large/006tNc79gy1g60ep4llfaj30ax02fglj.jpg)

- Linux 的安全检测流程

![IMG_1060](http://ww4.sinaimg.cn/large/006tNc79ly1g60epak066j30go072aak.jpg)

- 设定文件或目录上的权限要用chmod命令：

```
chmod [-R] mode 文件或目录名
        -R：递归的，设置同时应用于目录中的子目录和所有文件，只有root可用。
        mode: 详见👇
```

<span style="color: rgb(38, 180, 80);">_\*._</span>**_mode_**：

1. 用**表达式**表示：

_用“{who}  {operator}  {permission}”表示mode：_

![IMG_1061](http://ww1.sinaimg.cn/large/006tNc79ly1g60eps4gcej30go03nmxf.jpg)

权限状态可以分成3个部分：

- 第1部分，表示要设定**谁**的状态：

- u：<span style="background-color: rgb(255, 250, 165);">所有者</span>的权限。
  
- g：<span style="background-color: rgb(255, 250, 165);">群组</span>的权限。
  
- o：既不是owner也不与owner在同一个group的<span style="background-color: rgb(255, 250, 165);">其他用户</span>的权限。
  
- a：所以，以上3组，也就是<span style="background-color: rgb(255, 250, 165);"><u>所有用户</u></span>的权限。

- 第2部分，**运算符**（操作符）

- +：<span style="background-color: rgb(255, 250, 165);">加入</span>权限。
  
- - ：<span style="background-color: rgb(255, 250, 165);">去掉</span>权限。
  
- \=：<span style="background-color: rgb(255, 250, 165);">设定</span>权限。

- 第3部分，**权限**（permission）

- r  ：read权限。
  
- w：write权限。
  
- x ：execute权限。

e.g.

```
$ chmod ug+x tastingFile
        在tastingFile文件上添加上所有者和同组用户的可执行权限
```

2. 用**数字**表示：

_用  一组三位数  表示mode：_

（1）第1个数字  代表  所有者      (own user)    的权限   （u）

（2）第2个数字  代表  群组       （group）       的权限   （g）

（3）第3个数字  代表  其他用户（other）        的权限   （o）

这组3位数中的每一位数字都是由以下表示资源权限状态的数字（即4、2、1和0）相加而获得的总和：

        4：100(2)：表示具有    read       权限。

        2：010(2)：表示具有    write      权限。

        1：001(2)：表示具有  execute   权限。

        0：000(2)：表示  没有相应的权限。

即：

![IMG_1064](http://ww3.sinaimg.cn/large/006tNc79ly1g60eq5o2mej30go05i3z4.jpg)

e.g.

![](http://ww2.sinaimg.cn/large/006tNc79ly1g60eqx53n4j30e204jwep.jpg)

```
# chmod -R 754 /home/foo/bar

        对owner(foo)开放家目录的bar子目录和其中所有文件的一切权限，但是对同组用户开放读和执行权限而对其他用户只开放读权限
```

- **特殊权限**（第4组权限）

第4组权限包括suid、sgid和sticky 3种权限。

其中，

- suid  ：100：4：借用u的可执行权限位，并以 **s** 来表示；  
  
- sgid  ：  10：2：借用g的可执行权限位，并以 **s** 来表示；
  
- sticky ：    1：1：借用o的可执行权限位，并以 **t** 来表示；

当在一个文件上加入suid|sgid|sticky特殊权限时：

如果原来的文件的u|g|o具有x权限：

就使用小写的s|s|t来代替x；

如果原来没有x：

就用大写的S|S|T来代替；

<u>设置</u>特殊权限：

```
# 字符：
$ chmod [u|g|o][+,-,=][s|s|t] file
# 数字：（第四组表示特殊权限）
$ chmod [0-7][0-7][0-7][0-7] file
```

特殊权限<u>作用</u>：

将suid和sgid设定在*可执行文件*上：

- 运行有suid特殊权限的可执行文件时：是以可执行文件的**所有者权限来运行**这一可执行文件的，而不是以执行者的权限来运行该命令。
  
- sgid特殊权限与suid类似，是以命令的群组的权限来运行这一命令的。

将sgid和sticky设定在*目录*上：  

- 一个目录上设置了sticky权限，就只有文件的所有者和root用户才可以删除该目录中的文件，而Linux系统不会理会group或other的写权限。
  
- 一个目录上设置了sgid权限，只要是同一群组的成员，都可以在这个目录中创建文件。
  
- 通常会对目录同时设置sticky和sgid这两个特殊权限以方便项目的管理（将同一个项目的文件都放到这一个目录中以方便同一项目的成员之间共享信息）。

