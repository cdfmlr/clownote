---
date: 2021-02-17 17:50:30.473346
tags: xv6
title: Xv6 编写用户程序
---

![Meaning Unknown's Head Image](https://api.ixiaowai.cn/api/api.php)


# Xv6 编写用户程序

如何在 Xv6（[xv6-riscv](https://github.com/mit-pdos/xv6-riscv)）中添加自己编写的用户程序，比如实现一个 `helloworld`？

## 1. 编写代码

在 `xv6-riscv/user/` 里新建一个 `helloworld.c`，写一个 hello world：

```c
#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"

int main() {
	printf("Hello World!\n");
	exit(0);
}
```

这个和平时我们在真实系统中写的代码有少许区别：

1. 导库：`kernel/types.h`, `kernel/stat.h`, `user/user.h`。你可以看到  `xv6-riscv/user/*.c` 头三行基本都是这么写的，咱们有样学样就可。（这三行大概就是 include `<stdio.h>`，`<stdlib.h>`，`<unistd.h>` ）
2. 不要 `return 0;`，要 `exit(0);`（否则你会得到一个运行时的 ` unexpected scause 0x000000000000000f`）。这一点同样可以参考其他系统随附的程序得出。

## 2. 修改 Makefile

`Xv6` 系统中没有编译器的实现，所以我们需要把程序在编译系统时一并编译。修改 `xv6-riscv/Makefile`：

```sh
$ vim Makefile
```

找到 `UPROGS` (大概118行)，保持格式，在后面添加注册新程序：

```makefile
UPROGS=\
	$U/_cat\
	$U/_echo\
	...
	$U/_helloworld\
```

编写的代码 `user/xxx.c`，对应这里写 `$U/_xxx\`。

## 3. 编译运行 Xv6

编译运行 Xv6：

```sh
$ make qemu
```

在 Xv6 中 `ls`，可以看到我们的 helloworld 程序：

```sh
$ ls
...
helloworld   2 20 22352
```

运行程序：

```sh
$ helloworld
Hello World!
```

That's it!

---

```sh
# By CDFMLR 2021-02-17
echo "See you."
```

顶部图片来自于[小歪API](https://api.ixiaowai.cn)，系随机选取的图片，仅用于检测屏幕显示的机械、光电性能，与文章的任何内容及观点无关，也并不代表本人局部或全部同意、支持或者反对其中的任何内容及观点。如有侵权，联系删除。
