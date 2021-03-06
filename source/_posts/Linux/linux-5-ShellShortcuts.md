---
categories:
- Linux
- Beginning
date: 2017-01-04 10:10:35
tags: Linux
title: linux-5-快捷操作
---

# 快捷操作

## 快速命令

- 认识默认bash提示符：

```
[`whoami` @ `uname -n`   `pwd`]
```

- 用`{Tab}`补全命令。

若有多个可选方案，按一次不显示，按两次显示全部。

- Linux 通配符

| 通配符 | 作用                     |
| ------ | ------------------------ |
| *      | 匹配0或多个字符          |
| ?      | 匹配一个字符             |
| [xyz]  | 匹配括号中的任意一个字符 |
| [x-y]  | 匹配x～y范围内所有字符   |
| [^a-z] | 除a～z的字符             |
| [^xyz] | 除括号中的任意字符       |

- 使用`{}`

```
$ touch {a,b}
        分别touch文件a和b
$ touch a.{b,c}
        分别touch文件a.b和a.c
$ touch {a,b}.{c,d}
        分别touch文件a.c和a.d和b.c和b.d
```

- `history`命令：列出用户最近输入过的命令

  ​	左边是命令的编号

  ​	用`$ !<n>`：重新运行编号为`<n>`的命令

- `^x^y`：将上一命令中的x改为y后重新执行

- `{上下箭头}`：在以前使用过的命令中移动

- `{ctrl+r}`在命令的历史中查找:

  - 出现`(reverse-i-search)':`
  - 输入关键字
  - 出现命令，回车执行

- 先按`{Esc}`再按`{.}` 或 同时按`{Alt+.}`：提取上一命令的最后一个参数


## 终端快捷键

- `ctrl+A`: 光标移到命令行**开头**处
- `ctrl+E`: 光标移到命令行**结尾**处
- `ctrl+U`: 向前**删除内容**至提示符
- `ctrl+K`: 向后**删除内容**至结尾
- `ctrl+左|右`: 向左右**移动**一个字


## Gnome终端快捷键

- `ctrl+shift+T`: 开启新选项卡
- `ctrl+PgUp/PgDn`: 切换到上/下个选项卡
- `alt+N`: 切换到第N个选项卡
- `ctrl+shift+C/V`: 复制，粘贴
- `ctrl+shift+W`: 关闭一个选项卡