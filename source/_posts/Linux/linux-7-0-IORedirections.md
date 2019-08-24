---
title: linux-7.0-文件描述符与重定向
date: 2017-01-06 19:31:16
tags: Linux
categories:
	- Linux
	- Beginning
---

# 文件描述符与重定向

## 文件描述：决定从哪里读输入，向哪里写 输出 与 错误

**文件描述符：**

 由 `$ ls -l /dev/std*` 可见:

- `0` ：stdin
- `1` ：stdout
- `2` ：stderr

## 输出重定向：

- `cmd [1|2]> file` ：覆盖源文件，无则建
- `cmd [1|2\]>> file` ：追加，无则建

> 1. 不会自动递归补全路径
> 2. `[1|2]`，文件描述符（stdin|stderr），缺省为 `1`，与 `>` 之间无空格

- `$ ls > outfile 2>&1` ->    将stdout、stderr一同重定向到 `outfile`

> `1` 省略，`2` 重定向到 `1` 指向的文件

- `cmd &> file` ：把0，1，2都重定向至file。（`&` 代表 `0&1&2`）

> 用`&>`可能会在文文件中产生一些无用的信息

## 输入重定向（`<`）：

```
$ tr 'A-Z' 'a-z' < w.txt > u.txt        # 将w中的大写->小写，放入u中
                # 0 -> w.txt
```