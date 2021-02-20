---
date: 2021-02-20 14:13:57.605051
tags: xv6
title: Xv6 管道
---

![Meaning Unknown's Head Image](https://api.ixiaowai.cn/api/api.php)

# Xv6 管道

> 参考: [xv6-riscv-book](https://github.com/mit-pdos/xv6-riscv-book) 1.3 Pipes

[TOC]


## pipe

Xv6 系统调用 `pipe()` 来创建管道。管道类似于 Go 语言中的 chan。在 Shell 里我们用 `|` 表示管道，对于命令： `echo "hello world" | wc`，可以用如下代码实现：

```c
// upipe.c
//
// Runs the program wc with standard input connected to the read end of a pipe.

#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"

int main() {
	int p[2];  // file descriptors for the pipe
	
	char *argv[2];
	argv[0] = "wc";
	argv[1] = 0;  // NULL

	pipe(p);  // creates a new pipe: records the read and write file descriptors in the array p

	if (fork() == 0) {
		// redirection
		close(0);
		dup(p[0]);  // stdin = <- pipe

		close(p[0]);
		close(p[1]);

		exec("wc", argv);
	} else {
		close(p[0]);

		write(p[1], "hello world\n", 12);  // pipe <- str

		close(p[1]);
	}

	exit(0);
}
```

编译运行：

```sh
$ upipe
1 2 12
```

Xv6 sh 里的管道处理实现其实就和这段代码类似：fork 两个进程，分别重定向标准输出 or 输入、运行管道左右两边的命令。详见 [user/sh.c:100](https://github.com/mit-pdos/xv6-riscv/blob/riscv//user/sh.c#L100)。

## 管道 V.S. 临时文件

用管道与用临时文件，使用上似乎区别不大：

```sh
# 管道
echo "hello world" | wc
```

```sh
# 临时文件
echo hello world >/tmp/xyz; wc </tmp/xyz
```

但管道更好：

- 管道会自动清理（临时文件要手动删除）
- 管道可以放任意长度的数据流（临时文件需要有足够的磁盘空间）
- 管道可以并行运行（临时文件只能一个运行完，第二个再开始）
- 在处理进程间通信问题时，管道的阻塞式读写比用非阻塞的临时文件方便。

---

EOF

---

```sh
# By CDFMLR 2021-02-20
echo "See you. 🪐"
```

顶部图片来自于[小歪API](https://api.ixiaowai.cn)，系随机选取的图片，仅用于检测屏幕显示的机械、光电性能，与文章的任何内容及观点无关，也并不代表本人局部或全部同意、支持或者反对其中的任何内容及观点。如有侵权，联系删除。

