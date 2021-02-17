---
date: 2021-02-17 12:39:25.798705
tags: xv6
title: Xv6 编译运行
---

![Meaning Unknown's Head Image](https://api.ixiaowai.cn/api/api.php)

# Xv6 编译运行

本文介绍在 macOS 下搭建环境、编译运行 6.S081 课程的 [mit-pdos/xv6-riscv](https://github.com/mit-pdos/xv6-riscv) 系统。

[TOC]

> 参考 https://pdos.csail.mit.edu/6.S081/2020/tools.html
>
> 本文仅介绍 macOS 的方法，用 Linux、Windows 的铜屑请看上面的链接👆

## 工具安装

以 macOS 为例，利用  [Homebrew](https://brew.sh/)，首先安装  [RISC-V 编译工具链](https://github.com/riscv/homebrew-riscv)：

```sh
$ brew tap riscv/riscv
$ brew install riscv-tools
```

如果 brew 没有正确链接（`riscv<TAB><TAB>` 看一下，出来一大堆就对了，否则就没有正确链接），可以手动加一下 PATH：

```sh
export PATH=$PATH:/usr/local/opt/riscv-gnu-toolchain/bin
```

安装 QEMU：

```sh
$ brew install qemu
```

## 测试安装

试一下，如果安装对了，是下面的效果：

```sh
$ riscv64-unknown-elf-gcc --version
riscv64-unknown-elf-gcc (GCC) 10.2.0
...
```

```sh
$ qemu-system-riscv64 --version
QEMU emulator version 5.2.0
...
```

## 编译运行

进入你 clone 的 xv6-riscv 仓库，编译运行：

```sh
$ cd /path/to/xv6-riscv
$ make qemu
```

P.S. 如果你还没有 clone the  xv6-riscv repo，请：`git clone git://github.com/mit-pdos/xv6-riscv.git`。如果你甚至没有 `git`，~~STFW~~ 请用您最喜欢的搜索引擎搜索 `git`。如果你现在依然不知所措，很抱歉，恕我直言，您学习 Xv6 的时候未到。

会输出一大堆编译信息，最后：

```sh
...
xv6 kernel is booting
...
init: starting sh
$ 
```

这就进入了运行在 QEMU 虚拟机里的 xv6 系统了， `ls` 看看你可以用 Xv6 做哪些事 ：

```sh
$ ls
.              1 1 1024
..             1 1 1024
README         2 2 2059
cat            2 3 24248
echo           2 4 23064
...
ls             2 10 26440
...
wc             2 17 25336
```

## 退出系统

要退出虚拟机时，按 `c-A X`（先按下 control 键不放开，接着按 A 键，送开两个键，然后按 X 键）。

---

```sh
# By CDFMLR 2021-02-17
echo "See you."
```

顶部图片来自于[小歪API](https://api.ixiaowai.cn)，系随机选取的图片，仅用于检测屏幕显示的机械、光电性能，与文章的任何内容及观点无关，也并不代表本人局部或全部同意、支持或者反对其中的任何内容及观点。如有侵权，联系删除。

