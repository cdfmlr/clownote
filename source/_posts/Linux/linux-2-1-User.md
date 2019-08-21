---
title: linux-2.1-用户
date: 2016-12-22 15:25:29
tags: Linux
---

# 用户（User）

- 用户（Users）

- 系统中的每一个**用户**都有一个唯一的**用户标识符**（号码），即**uid**（user identifier）

（*uid 0* 为 `root` 用户的标识符。）

- 所有的用户名和_用户标识符_都被存放在 `/etc/passwd` 文件中。
  
- 在 _passwd_ 文件中还存放了每个用户的家目录，以及该用户登录后第一个执行的程序

（通常是 shell，在 Linux 系统中默认是 bash。）

- 如果没有相应的权限就不能**读、写或执行**其他用户的文件。

- passwd 文件：用户信息数据库

_<u>/etc/passwd</u>_ 储存用户信息

```
/etc/passwd 的内容：
e.g|  exp :  x  :     500    :       500     :Example_User:	/home/exp :   /bin/bash
说明| 用户名:密码否:uid（用户ID）:gid（所属群组ID）:   注释信息  :   家目录  :	启动后第一个执行程序

```

关于第二个字段：如果是**x**，表示这个用户登录Linux系统时必须使用密码，如果为**空**则该用户在登录系统时无须提供密码。

- shadow文件：用户密码数据库

\[⚠️\]普通用户无权访问_<u>/etc/shadow</u>_

_<u>/etc/shadow</u>_ 储存用户密码

```
/etc/shadow 的内容：
e.g|  exp :$1$wg...w4:14561:0:99999:7:::
说明| 用户名:   密码   :      :      :  :::

```

关于第二个字段：第2列是密码，这个密码是经过MD5加密算法加密过的密码。

* 如果该列以$1$开头，则表示这个用户已经设定了密码。
    （包括手动把passwd中的x去掉，不用密码即可登录的“空秘密”）
    
* 如果该列以!!开头，则表示这个用户还没有设定密码。
    （新建后**passwd -S**显示_Password locked_的状态，这种用户不可登录）