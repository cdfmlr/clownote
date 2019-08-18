---
title: linux-0.2-系统开关
date: 2016-12-17 13:57:31
tags: Linux
---

# 系统开关

- 关闭系统：

```
# sync
# init 0    或    shutdown -n    或    halt
```

- 重启系统：

```
# sync
# init 6    或    shutdown -rn
```

- 退出当前用户登录：

```
$ exit
```

Linux的 `exit` 类似于 Windows 的注销；

- 查看当前使用的虚拟终端：

```
$ tty
/dev/tty2        #二号虚拟终端
```


- 切换终端：

```
{Ctr + Alt + Fn}
		#	其中 n = {1, 2, 3, ... ,7},代表 tty n
```

切换至图形终端（也是一个tty）：

```
{Ctr + Alt + F7}
```


- 清空屏幕：

```
$ clear
```

- 找到系统中所有shell：

```
$ cat /etc/shells
```

- 切换shell：

```
$ sh		# 切换至Bourn Shell
$ ksh		# 切换至Korn Shell
```

可以在命令行中输入一个不存在的命令（如`OK`），以确定用户当前的shell。
