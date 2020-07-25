---
categories:
- Linux
- Beginning
date: 2016-12-23 15:32:56
tags: Linux
title: linux-2.2-群组
---

# 群组（Group）

- Linux群组的**特性**：

- Linux系统中，每一个**用户**都一定**隶属于**至少一个**群组**，而每一个群组都有一个group标识符（号码），即gid。
  
- 所有的群组和对应的gids都存放在_<u>/etc/group</u>_文件中。
  
- Linux系统在**创建用户时**为每一个用户**创建**一个**同名的群组**并且把这个用户加入到该群组中，也就是说每个用户至少会加入一个与他同名的群组中，并且也可以加入到其他的群组中。加入到其他群组的目的是为了获取适当的权限来访问（存取）特定的资源。
  
- 如果有一个文件属于某个群组，那么这个群组中所有的用户都可以存取这个文件。

- <span style="color: #fd0404;"><span style="color: rgb(253, 4, 4);">**group**</span></span>文件

**_/etc/group_** 保存着群组信息。

```
/etc/group的内容：

 e.g.| foobar **:   **x   **: **503 **: **foo**,**bar

means| 群组名  **: **密码否 **: **gid **: **群组成员
```

        # 第二字段为x表示这个群组在登录Linux时必须使用密码。

- <span style="color: rgb(253, 4, 4);">**gshadow**</span>文件

**_/etc/gshadow _**保存着群组信息。

\[⚠️\]普通用户无权访问_<u>/etc/gshadow</u>_

```
# more /etc/gshadow

root:::root            # 在gshadow中，每个群组占一行记录

bin:::root,bin,daemon ......

foo:!::

bar:!::

群组名:加密后的密码::
```
