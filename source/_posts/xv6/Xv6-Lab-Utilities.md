---
date: 2021-02-24 15:03:34.892093
tags: xv6
title: Xv6 Lab Utilities
---

![Meaning Unknown's Head Image](https://api.ixiaowai.cn/api/api.php)

# Xv6 Lab Utilities

6.S081 Lab 1: Xv6 and Unix utilities

> 参考: [Lab: Xv6 and Unix utilities](https://pdos.csail.mit.edu/6.S081/2020/labs/util.html)

## sleep

Implement the UNIX program `sleep` for xv6; your `sleep` should pause for a user-specified number of ticks. A tick is a notion of time defined by the xv6 kernel, namely the time between two interrupts from the timer chip. Your solution should be in the file `user/sleep.c`.

Some hints:

- Before you start coding, read Chapter 1 of the [xv6 book](https://pdos.csail.mit.edu/6.S081/2020/xv6/book-riscv-rev1.pdf).
- Look at some of the other programs in `user/` (e.g., `user/echo.c`, `user/grep.c`, and `user/rm.c`) to see how you can obtain the command-line arguments passed to a program.
- If the user forgets to pass an argument, sleep should print an error message.
- The command-line argument is passed as a string; you can convert it to an integer using `atoi` (see user/ulib.c).
- Use the system call `sleep`.
- See `kernel/sysproc.c` for the xv6 kernel code that implements the `sleep` system call (look for `sys_sleep`), `user/user.h` for the C definition of `sleep` callable from a user program, and `user/usys.S` for the assembler code that jumps from user code into the kernel for `sleep`.
- Make sure `main` calls `exit()` in order to exit your program.
- Add your `sleep` program to `UPROGS` in Makefile; once you've done that, `make qemu` will compile your program and you'll be able to run it from the xv6 shell.
- Look at Kernighan and Ritchie's book *The C programming language (second edition)* (K&R) to learn about C.

```c
#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"

int
main(int argc, char *argv[])
{
  int ticks;  // time to sleep

  if(argc <= 1){
    fprintf(2, "usage: sleep ticks\n");
    exit(1);
  }
  ticks = atoi(argv[1]);

  sleep(ticks);

  exit(0);
}
```

build & run:

```sh
$ make qemu
...
init: starting sh
$ sleep 10
(nothing happens for a little while)
$
```

## pingpong

Write a program that uses UNIX system calls to ''ping-pong'' a byte between two processes over a pair of pipes, one for each direction. The parent should send a byte to the child; the child should print "`<pid>: received ping`", where `<pid>` is its process ID, write the byte on the pipe to the parent, and exit; the parent should read the byte from the child, print "`<pid>: received pong`", and exit. Your solution should be in the file `user/pingpong.c`.

Some hints:

- Use `pipe` to create a pipe.
- Use `fork` to create a child.
- Use `read` to read from the pipe, and `write` to write to the pipe.
- Use `getpid` to find the process ID of the calling process.
- Add the program to `UPROGS` in Makefile.
- User programs on xv6 have a limited set of library functions available to them. You can see the list in `user/user.h`; the source (other than for system calls) is in `user/ulib.c`, `user/printf.c`, and `user/umalloc.c`.

```c
#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"

int
main(int argc, char *argv[])
{
	int p[2];  // file descriptors for pipe
	char recv_buf[128];

	pipe(p);

	if (fork() == 0) {  // child
		read(p[0], recv_buf, 4);
		close(p[0]);

		printf("%d: received %s\n", getpid(), recv_buf);

		write(p[1], "pong", 4);
		close(p[1]);

		exit(0);
	} else {  // parent
		write(p[1], "ping", 4);
		close(p[1]);

		read(p[0], recv_buf, 4);
		close(p[0]);

		printf("%d: received %s\n", getpid(), recv_buf);

		exit(0);
	}
}
```

Result:

```sh
$ make qemu
...
init: starting sh
$ pingpong
4: received ping
3: received pong
```

## primes

Write a concurrent version of prime sieve using pipes. This idea is due to Doug McIlroy, inventor of Unix pipes. The picture halfway down [this page](http://swtch.com/~rsc/thread/) and the surrounding text explain how to do it. Your solution should be in the file `user/primes.c`.

Your goal is to use `pipe` and `fork` to set up the pipeline. The first process feeds the numbers 2 through 35 into the pipeline. For each prime number, you will arrange to create one process that reads from its left neighbor over a pipe and writes to its right neighbor over another pipe. Since xv6 has limited number of file descriptors and processes, the first process can stop at 35.

Some hints:

- Be careful to close file descriptors that a process doesn't need, because otherwise your program will run xv6 out of resources before the first process reaches 35.
- Once the first process reaches 35, it should wait until the entire pipeline terminates, including all children, grandchildren, &c. Thus the main primes process should only exit after all the output has been printed, and after all the other primes processes have exited.
- Hint: `read` returns zero when the write-side of a pipe is closed.
- It's simplest to directly write 32-bit (4-byte) `int`s to the pipes, rather than using formatted ASCII I/O.
- You should create the processes in the pipeline only as they are needed.
- Add the program to `UPROGS` in Makefile.

```c
#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"

#define MAX 36
#define FIRST_PRIME 2

int generate_natural();  // -> out_fd
int prime_filter(int in_fd, int prime);  // -> out_fd

int
main(int argc, char *argv[])
{
	int prime; 
	
	int in = generate_natural();
	while (read(in, &prime, sizeof(int))) {
		// printf("prime %d: in_fd: %d\n", prime, in);  // debug
		printf("prime %d\n", prime); 
		in = prime_filter(in, prime);
	}

	exit(0);
}

// 生成自然数: 2, 3, 4, ..< MAX
int
generate_natural() {
	int out_pipe[2];
	
	pipe(out_pipe);

	if (!fork()) {
		for (int i = FIRST_PRIME; i < MAX; i++) {
			write(out_pipe[1], &i, sizeof(int));
		}
		close(out_pipe[1]);

		exit(0);
	}

	close(out_pipe[1]);

	return out_pipe[0];
}

// 素数筛
int 
prime_filter(int in_fd, int prime) 
{
	int num;
	int out_pipe[2];

	pipe(out_pipe);

	if (!fork()) {
		while (read(in_fd, &num, sizeof(int))) {
			if (num % prime) {
				write(out_pipe[1], &num, sizeof(int));
			}
		}
		close(in_fd);
		close(out_pipe[1]);
		
		exit(0);
	}

	close(in_fd);
	close(out_pipe[1]);

	return out_pipe[0];
}
```

这个程序是参考 《[Go语言高级编程](https://chai2010.cn/advanced-go-programming-book/)》[1.6 常见的并发模式](https://chai2010.cn/advanced-go-programming-book/ch1-basic/ch1-06-goroutine.html) 中的那个 Golang 版本写的。Golang 的并发模型和 UNIX Pipe 本身就很像（refer: [Effective Go: Share by communicating](https://golang.google.cn/doc/effective_go#sharing)），这里只需把 chan 换成 pipe，Goroutine 换成 fork 的进程。但是，一定要、一定要、一定要注意那些在子进程中使用的文件描述符，父进程不用就要关了，不然就凉了。

运行·结果：

```sh
$ primes
prime 2
prime 3
prime 5
prime 7
prime 11
prime 13
prime 17
prime 19
prime 23
prime 29
prime 31
```

## find

Write a simple version of the UNIX find program: find all the files in a directory tree with a specific name. Your solution should be in the file `user/find.c`.

Some hints:

- Look at user/ls.c to see how to read directories.
- Use recursion to allow find to descend into sub-directories.
- Don't recurse into "." and "..".
- Changes to the file system persist across runs of qemu; to get a clean file system run make clean and then make qemu.
- You'll need to use C strings. Have a look at K&R (the C book), for example Section 5.5.
- Note that == does not compare strings like in Python. Use strcmp() instead.
- Add the program to `UPROGS` in Makefile.

```c
#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"
#include "kernel/fs.h"
#include "kernel/fcntl.h"

char*
fmtname(char *path)
{
	char *p;

	// Find first character after last slash.
	for(p=path+strlen(path); p >= path && *p != '/'; p--)
		;
	p++;

	return p;
}

void
find(char *path, char *targetname) 
{
	char buf[512], *p;
	int fd;
	struct dirent de;
	struct stat st;

	if (!strcmp(fmtname(path), targetname)) {
		printf("%s\n", path);
	}

	if ((fd = open(path, O_RDONLY)) < 0) {
		fprintf(2, "find: cannot open [%s], fd=%d\n", path, fd);
		return;
	}

	if (fstat(fd, &st) < 0) {
		fprintf(2, "find: cannot stat %s\n", path);
		close(fd);
		return;
	}

	if (st.type != T_DIR) {
		close(fd);
		return;
	}

	// st.type == T_DIR
	
	if (strlen(path) + 1 + DIRSIZ + 1 > sizeof buf) {
		printf("find: path too long\n");
		close(fd);
		return;
	}
	strcpy(buf, path);
	p = buf+strlen(buf);
	*p++ = '/';
	while (read(fd, &de, sizeof(de)) == sizeof(de)) {
		if (de.inum == 0)
			continue;
		memmove(p, de.name, DIRSIZ);
		p[DIRSIZ] = 0;
		
		if (!strcmp(de.name, ".") || !strcmp(de.name, ".."))
			continue;

		find(buf, targetname);
	}
	close(fd);
}

int
main(int argc, char *argv[])
{
	if(argc < 3){
		fprintf(2, "usage: find path filename\n");
		exit(1);
	}

	find(argv[1], argv[2]);

	exit(0);
}
```

主要就是抄 `user/ls.c`。这个指针玩的，，太骚了[捂脸]。C 还是有意思啊。

结果：

```sh
$ echo > b
$ mkdir a
$ echo > a/b
$ find . b
./b
./a/b
```

## xargs

Write a simple version of the UNIX xargs program: read lines from the standard input and run a command for each line, supplying the line as arguments to the command. Your solution should be in the file `user/xargs.c`.

The following example illustrates xarg's behavior:

```sh
$ echo hello too | xargs echo bye
bye hello too
$
```

Note that the command here is "echo bye" and the additional arguments are "hello too", making the command "echo bye hello too", which outputs "bye hello too".

Please note that xargs on UNIX makes an optimization where it will feed more than argument to the command at a time. We don't expect you to make this optimization. To make xargs on UNIX behave the way we want it to for this lab, please run it with the -n option set to 1. For instance

```sh
$ echo "1\n2" | xargs -n 1 echo line
line 1
line 2
$
```

Some hints:

- Use `fork` and `exec` to invoke the command on each line of input. Use `wait` in the parent to wait for the child to complete the command.
- To read individual lines of input, read a character at a time until a newline ('\n') appears.
- kernel/param.h declares MAXARG, which may be useful if you need to declare an argv array.
- Add the program to `UPROGS` in Makefile.
- Changes to the file system persist across runs of qemu; to get a clean file system run make clean and then make qemu.

xargs, find, and grep combine well:

```sh
$ find . b | xargs grep hello
```

will run "grep hello" on each file named b in the directories below ".".

```c
#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"
#include "kernel/param.h"  // MAXARG

#define is_blank(chr) (chr == ' ' || chr == '\t') 

int
main(int argc, char *argv[])
{
	char buf[2048], ch;
	char *p = buf;
	char *v[MAXARG];
	int c;
	int blanks = 0;
	int offset = 0;

	if(argc <= 1){
		fprintf(2, "usage: xargs <command> [argv...]\n");
		exit(1);
	}

	for (c = 1; c < argc; c++) {
		v[c-1] = argv[c];
	}
	--c;

	while (read(0, &ch, 1) > 0) {
		if (is_blank(ch)) {
			blanks++;
			continue;
		}

		if (blanks) {  // 之前有过空格
			buf[offset++] = 0;

			v[c++] = p;
			p = buf + offset;

			blanks = 0;
		}

		if (ch != '\n') {
			buf[offset++] = ch;
		} else {
			v[c++] = p;
			p = buf + offset;

			if (!fork()) {
				exit(exec(v[0], v));
			}
			wait(0);
			
			c = argc - 1;
		}
	}

	exit(0);
}
```

主要是字符串操作麻烦。。

运行：

```sh
$ echo hello too | xargs echo bye
bye hello too
$ find . b
./b
./a/b
$ find . b | xargs echo hello
hello ./b
hello ./a/b
```

## 参考

1. MIT. Lab guidance. https://pdos.csail.mit.edu/6.S081/2020/labs/guidance.html
2. MIT. Lab: Xv6 and Unix utilities. https://pdos.csail.mit.edu/6.S081/2020/labs/util.html
3. KatyuMarisa. MIT 6.S081 xv6调试不完全指北. https://www.cnblogs.com/KatyuMarisaBlog/p/13727565.html
4. EASTON MAN. xv6操作系统实验 – 质数筛. https://blog.eastonman.com/blog/2020/11/xv6-primes/
5. ABCDLSJ. MIT 6.828 Lab 1: Xv6 and Unix utilities. https://abcdlsj.github.io/post/mit-6.828-lab1xv6-and-unix-utilities/

---

Woc，这个 Lab 做了好久。前天写到 primes，被忘记 close 的 bug 卡了一下，然后就沉迷娱乐，补了半部番，看了两本轻小说。昨天停电，练了一早上琴，下午又看了两本轻小说🤦‍♂️，就今天才写完。

By CDFMLR 2020-02-24

顶部图片来自于[小歪API](https://api.ixiaowai.cn)，系随机选取的图片，仅用于检测屏幕显示的机械、光电性能，与文章的任何内容及观点无关，也并不代表本人局部或全部同意、支持或者反对其中的任何内容及观点。如有侵权，联系删除。