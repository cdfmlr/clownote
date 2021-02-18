---
date: 2021-02-18 11:39:54.923026
tags: xv6
title: Xv6 多进程编程
---

![Meaning Unknown's Head Image](https://api.ixiaowai.cn/api/api.php)


# Xv6 多进程编程

> 参考: [xv6-riscv-book](https://github.com/mit-pdos/xv6-riscv-book) 1.1 Processes and memory
> 

本文参考 xv6-riscv-book，介绍如何使用 Xv6 系统调用，实现多进程编程。（其实就是把书上的代码完整化，并附上真实系统中的实现方式）

| 系统调用                             | 描述                                                         |
| ------------------------------------ | ------------------------------------------------------------ |
| `int fork()`                         | 创建一个进程（通过复制当前进程）返回子进程 PID               |
| `int exit(int status)`               | 终止当前进程，status 会被报告给 wait()，无返回值             |
| `int wait(int *status)`              | 等待一个子进程退出，把退出的状态(exit de status) 写到 status，返回退出的子进程 PID |
| `int exec(char *file, char *argv[])` | 载入一个文件，并以指定参数执行之。错误才返回                 |

## fork & wait

fork 系统调用通过复制当前进程，创建一个进程，返回子进程 PID。

wait 会等待当前进程的某个子进程退出（调用 exit）。

### Xv6

书上有关使用 `fork` 的代码的完整实现（在 Xv6 下运行。Help: [Xv6 编写用户程序](https://blog.csdn.net/u012419550/article/details/113836258)）：

```c
// usefork.c for xv6

#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"

int main() {
	int pid = fork();
	if(pid > 0) {
		printf("parent: child=%d\n", pid);
		pid = wait((int *) 0);
		printf("child %d is done\n", pid);
	} else if (pid == 0) {
		printf("child: exiting\n");
		exit(0);
	} else {
		printf("fork error\n");
	}

	exit(0);
}
```

注意，在 Xv6 里提供的 printf 线程不安全，运行程序打印出的字符可能随机混合在一起：

```sh
$ usefork   # 这个还稍好
parent: child=c5
hild: exiting
child 5 is done
$ usefork  # 这个就非常乱了
cphairledn:t :e xcihtiilndg=
7
child 7 is done
```

### Real Unix

在真实的 `*nix` 系统上（这里以 macOS 11，GCC 10 为例），这段代码的写法是：

```c
// usefork.c for macOS GCC

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
	int pid = fork();
	if(pid > 0) {
		printf("parent: child=%d\n", pid);
		pid = wait((int *) 0);
		printf("child %d is done\n", pid);
	} else if (pid == 0) {
		printf("child: exiting\n");
		// sleep(2);
		exit(0);
	} else {
		printf("fork error\n");
	}

	return 0;
}
```

真实系统中运行的效果会好一些，一般没有字符混合的情况：

```sh
$ gcc-10 usefork.c ; ./a.out 
parent: child=3598
child: exiting
child 3598 is done
```

## exec

exec 系统调用载入一个可执行文件，用其替换自身程序，以指定参数执行之。

### Xv6

```c
// useexec.c for Xv6

#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"

int main() {
	char *argv[3];

	argv[0] = "echo";
	argv[1] = "hello";
	argv[2] = 0;

	exec("echo", argv);
	// exec 成功了会替换程序，下面的就执行不到了:
	printf("exec error\n");

	exit(0);
}
```

编译运行：

```sh
$ useexec
hello
```

### Real Unix

```c
// useexec.c for macOS

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
	char *argv[3];

	argv[0] = "echo";
	argv[1] = "hello";
	argv[2] = 0;

	execv("/bin/echo", argv);
	// execv("/bin/echooooo", argv);  // an error one
	// exec 成功了会替换程序，下面的就执行不到了:
	printf("exec error\n");
}

```

编译运行：

```sh
$ gcc-10 useexec.c ; ./a.out 
hello
```

---

正文结束。

```sh
# By CDFMLR 2021-02-18
echo "See you.🥷"
```

顶部图片来自于[小歪API](https://api.ixiaowai.cn)，系随机选取的图片，仅用于检测屏幕显示的机械、光电性能，与文章的任何内容及观点无关，也并不代表本人局部或全部同意、支持或者反对其中的任何内容及观点。如有侵权，联系删除。


