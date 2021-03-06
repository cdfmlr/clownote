---
categories:
- Linux
- Beginning
date: 2017-01-01 12:46:55
tags: Linux
title: linux-4.0-正文浏览
---

# 正文浏览

> 正文，即字符串 / 纯文本文件的内容。

### `cat`：浏览正文文件内容

```
$ cat [options] [files]
    -A：显示内容，包括不可见的特殊字符
    -s：将两个及以上的空行省略为一个空行
    -b：加入行号
$ cat > filename
    创建新文本文件，写入内容
    空行{Ctr+d}，保存退出        # {Ctr+c}:强行终止
            [注意]：用cat打开二进制文件会造成终端停止工作，可开启一个新的终端以解决。
```

           ⚠️ \[注意\]：用 cat 打开二进制文件可能会造成终端停止工作，可开启一个新的终端以解决。

### `head`：浏览文件头几行

```
$ head [-n x] file
    浏览文件头x行
    若省去[-n x]则显示头10行
```

### `tail`：浏览文件后几行

```
$ tail file
    浏览文件后10行
$ tail -[n]x  file
    显示从末尾算起的x行
    有无n都一样
$ tail +[n]x  file
    显示从文件第x行之后的内容
    有无n都一样
$tail -f file
    “-f“ == ”--follow“
    当一个正文文件内容发生变化时，把变化显示出来
    {ctrl+c}退出
# tail -f /var/log/messages
    监视日志
```

### `wc`：(word count)字数统计

```
$ wc [-options] file
    显示文件 行、单词、字符 数
        无选项依次显示l，w，c
        -l：行数
        -w：单词数
        -c：字符数
```

### `more [file]`：可翻页地浏览文件

在more中键入：

- `{空格}`：下一页
  
- `{Enter}`：移动一行
  
- `{b}`：上一页
  
- `{h}`：帮助
  
- `{/str}`：向前搜索str

- `{n}`：发现这个字符串的下一次出现

- `{q}`：退出 more
  
- `{v}`：在当前行启动 vi
