---
title: linux-1.2-帮助信息
date: 2016-12-20 14:18:40
tags: Linux
---

# 帮助信息

```
$ whatis *命令名*
```

​                说明*命令*是什么，了解命令的功能；

​                “whatis  *cmd*”命令 == “**man -f** *cmd*”

```
$ type [-options] 命令名
```

​    无选：显示命令类型

​    `-t`：显示文件的类型：

​        `file`：外部命令

​        `alias`：别名

​        `builtin`：shell内置命令

​    `-a`：列出所有包含指定命令名的命令，包括别名

​    `-p`：显示完整的文件名（外部命令）或内部命令


```
$ which 命令名
```

​    列出命令的类型相关的信息


```
$ *命令名* --help
```

​                显示*命令*的**简要说明**和**选项列表**


```
$ man *命令名*
```

​                浏览*命令*的 **Man Page** 1⃣️


```
$ man -k **keyword**
```

​                欲使用一个命令，又无法确定它的名字是用 -k选项+*关键字*搜寻它；

​                “man -k  *kw*”命令 == “**apropos** *kw*”命令；


```
$ info *cmd*
```

​                “info2⃣️”与“man”类似，但info更加简洁详尽(开发者认为的)；



1⃣️、2⃣️.  浏览 **Man page** *或*  **Info Page** ：

- - 使用man \ info命令进入Man \ Info Page

  - 键盘 < , > , ^, v , PgUp, PgDn, 空格：翻页

  - Home键：移到第一页

  - End键： 最后一页

  - 在屏幕底部`: `处输入`?string`：向前搜索string

  - - 按 n 键继续下一个搜索
    - 按 N 键进行反向搜索

  - 按 q 键退出Page

在 **Info Page** 中还有：

- - 按Tab：跳到下一个“*******”（超链接）
  - {Tab}*3：Index
