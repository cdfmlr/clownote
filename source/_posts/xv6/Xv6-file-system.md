---
date: 2021-02-21 14:49:29.288440
tags: xv6
title: Xv6 文件系统接口
---

![Meaning Unknown's Head Image](https://api.ixiaowai.cn/api/api.php)


# Xv6 文件系统接口

## 文件系统调用

| System call                           | Description                                                  |
| ------------------------------------- | ------------------------------------------------------------ |
| int chdir(char *dir)                  | 改变当前目录                                                 |
| int mkdir(char *dir)                  | 创建新目录                                                   |
| int open(char *file, O_CREATE)        | 创建新文件                                                   |
| int mknod(char *file, int, int)       | 创建新的设备文件（后两个参数是*主设备号*、*次设备号*，这两个数在内核中唯一确定一个设备），对设备文件的 read、write 会转发给设备，而不操作文件系统。 |
| int link(char *file1, char *file2)    | 为 file1 创建新的链接（名字）file2                           |
| int unlink(char *file)                | 移除文件（nlink -= 1），当 nlink == 0 时且无文件描述符指向文件时，文件的磁盘空间被释放 |
| int fstat(int fd, struct stat *st)    | 把一个打开的文件（fd）的信息放到  st                         |
| int stat(char *file, struct stat *st) | 把指定文件名的文件（file）的信息写入  st                     |



## 调用实例

```c
// ufilesystem.c
// try to use system calls about the file system

#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"
#include "kernel/fcntl.h"

void print_stat(char *msg, struct stat *st);

int 
main() 
{
	int fd;
	struct stat st;

	mkdir("/dir");
	chdir("/dir");
	fd = open("file", O_CREATE|O_RDWR);
	
	stat("file", &st);
	print_stat("file", &st);

	link("/dir/file", "file_link");

	stat("file_link", &st);
	print_stat("fiel_link", &st);

	unlink("/dir/file");
	unlink("/dir/file_link");
	
	fstat(fd, &st);
	print_stat("fd", &st);

	close(fd);
	exit(0);
}

void 
print_stat(char *msg, struct stat *st) 
{
	printf("%s: dev=%d ino=%d type=%d nlink=%d size=%d\n", 
			msg, st->dev, st->ino, st->type, st->nlink, st->size);
}
```

编译运行：

```sh
$ ufilesystem
file: dev=1 ino=30 type=2 nlink=1 size=0   # type 2 就是 file
fiel_link: dev=1 ino=30 type=2 nlink=2 size=0
fd: dev=1 ino=30 type=2 nlink=0 size=0
$ ls dir
.              1 29 64
..             1 1 1024
```

在 unlink 文件达到 nlink==0，并且所有指向文件的文件描述符都被释放之后，文件才会被删除。利用这个特性，就有了如下关于临时文件的习惯实现：

## An idiomatic trick

创建一个临时文件，在关闭文件描述符或进程退出时删除：

```c
fd = open("/tmp/xyz", O_CREATE|O_RDWR);
unlink("/tmp/xyz");  // nlink == 0

...

// temp file will be removed when:
close(fd);
// or:
exit();
```

---

EOF

---

```sh
# By CDFMLR 2021-02-21
echo "See you. 🚰"
```

顶部图片来自于[小歪API](https://api.ixiaowai.cn)，系随机选取的图片，仅用于检测屏幕显示的机械、光电性能，与文章的任何内容及观点无关，也并不代表本人局部或全部同意、支持或者反对其中的任何内容及观点。如有侵权，联系删除。