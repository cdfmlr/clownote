---
categories:
- Linux
- Beginning
date: 2016-12-30 22:46:15
tags: Linux
title: linux-3.1.3-文件归档与压缩
---

# 文件归档与压缩

## 归档

归档（archiving）就是将许多文件（或目录）打包成一个文件。

归档的目的就是方便备份、还原及文件的传输操作。

Linux操作系统的标准归档命令是tar（tape archive）。

tar命令的功能是将多个文件（也可有目录）放在一起存放到一个磁带或磁盘归档文件中，

并且将来可以根据需要只还原归档文件中的某些指定的文件。

tar命令默认并不进行文件的压缩。

```
tar [选项]... [归档文件名]...
    必须至少使用如下选项中的一个：
        c：创建一个新的tar文件。
        t：列出tar文件中内容的目录。
        x：从tar文件中抽取文件。
        f：指定归档文件或磁带（也可能是软盘）设备（一般都要选）
            （在RHEL 4之前的版本中规定在f选项之后必须紧跟着文件名而不能再加其他参数，
                但是从RHEL 4开始已经取消了这一限制。）
以下为可选的选项：
        v：显示所打包的文件的详细信息（v是verbose）
                (执行过程中会显示所有打包的文件和目录)
        z：使用gzip压缩算法来压缩打包后的文件。
                「$ tar cvfz arch.tar.gz dir2arch」
        j：使用bzip2压缩算法来压缩打包后的文件。
                「$ tar cvfj arch.tar.bz2 dirarch」
【注意】在tar命令中，所有的选项之前都不能使用前导的“-”。
```

创建新的归档文件：`c\[v\]f`

```
$ tar  cvf  arch.tar  dir2arch    # File to be archived should be a RELATIVE path
dir2arch/
dir2arch/learning.txt
dir2arch/name.txt
……
```

查看归档文件内容：`t\[v\]f`

```
$ tar tf arch.tar
dir2arch/
dir2arch/learning.txt
dir2arch/name.txt 
……
# 可以在tar命令中再加入v命令来显示文件更加详细的信息(like 「ls -l」):
$ tar tvf arch.tar
drwxrwxr-x User/User           0 2010-02-04 05:09:43 dir2arch/
-rw-r--r--   User/User        4720 2010-02-04 05:07:22 dir2arch/learning.txt
-rw-rw-r--   User/User          84 2010-02-04 05:07:22 dir2arch/name.txt 
……

```

解开打包好的文件：`x\[v\]f`

\[⚠️\]<span style="color: #fd0404;">解开前要将工作目录切换到打包时所在的目录，才能保证抽取的文件放回到原来的位置。</span>

```
$ tar xvf arch.tar
dir2arch/
dir2arch/learning.txt
dir2arch/name.txt
dir2arch/flowers.JPG
dir2arch/dog.JPG  ……
```

## 压缩

进行文件压缩的主要目的是缩小文件的大小。

一般对正文文件进行压缩之后，文件的大小可以被压缩大约75%。

但是二进制的文件，如图像文件通常不会被压缩多少。

Linux系统中两组常用的压缩工具：

  1. `gzip \ gunzip -> [*.gz]`

\[⚠️\]<span style="color: #fcb100;">用gzip不能压缩**目录**</span>

用gzip来压缩文件，就必须使用gunzip来解压缩。

它们是Linux系统上标准的压缩和解压缩工具，

*gzip对正文文件的压缩比一般超过75%*

```
gzip [选项] [压缩文件名…]
        若不用-c则会压缩源文件（把原来多foo.txt变成一个foo.txt.gz）
        -v：在屏幕上显示出文件的压缩比（v是verbose的第1个字母）。
        -c：保留原来的文件，而新创建一个压缩文件(要重定向出来)，其中压缩文件名以.gz结尾。
                （gzip -vc bar.txt > foobar.gz）
解压缩时，输入gunzip空格后跟要解压缩的文件，如命令gunzip arch.gz。
```
  2. `bzip2 \ bunzip2 ->[*.bz2]`

用bzip2压缩，必须用bunzip2解压。

它们是Linux系统上比较新的压缩和解压缩工具，

通常bzip2对归档文件的压缩比要优于gzip工具。

比较新的Linux版本才支持bzip2和bunzip2命令。
