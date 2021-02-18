---
date: 2021-02-18 17:37:17.516212
tags: xv6
title: Xv6 I/O 与文件描述符
---

![Meaning Unknown's Head Image](https://api.ixiaowai.cn/api/api.php)

# Xv6 I/O 与文件描述符

> 参考: [xv6-riscv-book](https://github.com/mit-pdos/xv6-riscv-book) 1.2 I/O and File descriptors

## Xv6 I/O 系统调用

本文会使用到如下 Xv6 的 I/O 系统调用：

| 系统调用                            | 说明                                                         |
| ----------------------------------- | ------------------------------------------------------------ |
| int open(char *file, int flags)     | 打开一个文件，flags 用来指示读or写，返回一个文件描述符       |
| int write(int fd, char *buf, int n) | 从 buf 写 n 个字节到文件描述符 fd，返回写入的字节数          |
| int read(int fd, char *buf, int n)  | 从文件描述符 fd 读 n 个字节到 buf，返回读取的字节数或 `0` 表示 EOF（文件结束） |
| int close(int fd)                   | 释放打开的文件描述符 fd                                      |
| int dup(int fd)                     | 返回一个新的文件描述符，指向与 fd 相同的文件                 |



open 的 flags 由 [ kernel/fcntl.h:1-5](https://github.com/mit-pdos/xv6-riscv/blob/riscv//kernel/fcntl.h#L1-L5) 提供：

| flag     | 说明                |
| -------- | ------------------- |
| O_RDONLY | 只读                |
| O_WRONLY | 只写                |
| O_RDWR   | 读和写              |
| O_CREATE | 不存在时新建        |
| O_TRUNC  | 把文件截断到 0 长度 |

这些都是用 bit 描述的，可以做或运算：

```c
fd = open("/dir/file", O_CREATE|O_WRONLY);
```

## Xv6 文件描述符

文件描述符就是一个整数，用来代表一个打开的 IO 对象（如文件），通过文件描述符就可以对 IO 对象进行读写操作。程序一开始就会被分配给如下惯例文件描述符：

| 文件描述符 | 说明            |
| ---------- | --------------- |
| 0          | stdin  标准输入 |
| 1          | stdout 标准输出 |
| 2          | stderr 标准错误 |

## read & write

```c
// useio.c
// Copies data from its standard input to its standard output.

#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"

int main() {
	char buf[512];
	int n;

	for(;;) {
		n = read(0, buf, sizeof buf);  // 0: stdin

		if (n == 0) {
			break;  // EOF
		}
		if (n < 0) {
			fprintf(2, "read error\n");  // 2: stderr
			exit(1);
		}
		if (write(1, buf, n) != n) {  // 1: stdout
			fprintf(2, "write error\n");
			exit(1);
		}
	}

	exit(0);
}
```

这个程序从标准输入读，写到标准输出，相当于一个简化的 cat：

```sh
$ useio > fff
123456  # 这是输入的
$ useio < fff
123456  # 这是输出的
```

## 重定向的实现

在通过如 open 的系统调用打开一个文件时，被分配给的文件描述符总是当前可用的描述符中**最小的**。

用这个特性就可以实现输入输出的重定向。Xv6 的 Shell ([user/sh.c:82](https://github.com/mit-pdos/xv6-riscv/blob/riscv//user/sh.c#L82)) 里就是这么实现的。

下面的程序实现一个 `cat < input.txt` 的效果：

```c
// uredirection.c
// A simplified version of the code a shell runs for the command `cat < input.txt`

#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"
#include "kernel/fcntl.h"  // define O_RDONLY

int main() {
	char *argv[2];
	argv[0] = "cat";
	argv[1] = 0;

	if (fork() == 0) {  // subprocess
		close(0);  // close stdin
		// A newly allocated file descriptor is always the lowest-numbered unused descriptor of the current process.
		open("input.txt", O_RDONLY);  // 0 => input.txt
		// exec replaces the calling process’s memory but preserves its file table.
		exec("cat", argv);
	}

	exit(0);
}
```

编译运行：

```
$ cat > input.txt
<Input something here>
$ uredirection
<what is inputted above>
```

fork 和 exec 分离的一个好处就是 shell 可以在 fork 和 exec 之间优雅实现重定向，如上面的程序。如果把二者合并，提供一个 `forkexec`  系统调用，重定向的实现就很烦了：需要多传参数；或者在调用 forkexec 前设置 shell 进程自己的描述符，然后又改回去；或者让每个程序自己去支持重定向。

##  共享偏移

fork 的时候会拷贝文件描述符表，但每个文件的偏移量（读/写到哪）会在父子进程间共享。

```c
// usharedoffset.c
// Although fork copies the file descriptor table, each underlying file offset is shared between parent and child. 

#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"
#include "kernel/fcntl.h"

int main() {
	if (fork() == 0) {
		write(1, "hello ", 6);
		exit(0);
	} else {
		wait(0);
		write(1, "world\n", 6);
	}
	exit(0);
}
```

运行效果：

```sh
$ echo "" > output.txt
$ usharedoffset > output.txt
$ cat output.txt
hello world
```

## dup

dup “复制”一个现有的文件描述符，返回的新描述符指向和原来一样的 I/O 物体（比如文件）。类似于 fork，新旧文件描述符共享 offset。

```c
// udup.c 
//
// The dup system call duplicates an existing file descriptor, 
// returning a new one that refers to the same underlying I/O object. 
// Both file descriptors share an offset, just as the file descriptors 
// duplicated by fork do. 

#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"
#include "kernel/fcntl.h"


int main() {
	int fd = dup(1);
	write(1, "hello ", 6);
	write(fd, "world\n", 6);

	exit(0);
}
```

运行效果：

```sh
$ udup > output.txt
$ cat output.txt
hello world
```

利用 dup，shell 就可以实现 `ls existing-file non-existing-file > tmp1 2>&1` 了。 `2>&1` 就是 `2 = dup(1)`，让标准错误和标准输出指向同一个文件，并且共享偏移（一直往后写）。

---

EOF

---

```sh
# By CDFMLR 2021-02-18
echo "See you.🧑‍💻"
```

顶部图片来自于[小歪API](https://api.ixiaowai.cn)，系随机选取的图片，仅用于检测屏幕显示的机械、光电性能，与文章的任何内容及观点无关，也并不代表本人局部或全部同意、支持或者反对其中的任何内容及观点。如有侵权，联系删除。

