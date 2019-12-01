---
title: linux-2.0-用户管理
date: 2016-12-21 14:26:02
tags: Linux
categories:
	- Linux
	- Beginning
---

# 用户管理

- `su`：切换用户

```
$ su [-]用户名
    -   ：有则重启shell，重装$PATH（环境变量），pwd切换至用户名的$HOME（家目录）
         无则不变 环境变量（检索命令的目录），pwd不变
```

用户名 ：缺省为 root

```
[me@Example ~]$ su - root
密码：
[root@Example~]# whoami
root
[root@Example~]# exit
logout
[me@Example~]$ whoami
me
```

- `passwd`：修改密码

1⃣️ *普通用户：*

```
$ passwd            修改当前用户密码
```

多按几个回车可取消退出

对于root “too short”的密码重输也可以成功

2⃣️ *root：*

```
# passwd username    修改某用户密码
# passwd -S username    查看密码状态，【注意】S大写
```

- 新建，删除 用户

1. useradd：新建用户：`# useradd new_user_name`

```
[root@Example ~]# useradd newone
[root@Example ~]# passwd -S newone
newone LK [2016-12-18 0 99999 7 -1](tel:2016-12-18 0 99999 7 -1)(密码已被锁定。)       # 说明密码未设定
[root@Example ~]# passwd newone
更改用户 newone 的密码 。
新的 密码：             # 尝试键入一个弱口令
无效的密码:  过于简单化/系统化        # 提示口令过于简单，但不阻止
重新输入新的 密码:                   # 仍输入那个弱口令，可以成功，因为是root
passwd： 所有的身份验证令牌已经成功更新。
# 如果是普通用户，键入弱口令不可成。（不会叫“Retype“，而是“New“）
[root@Example ~]# passwd -S newone
newone PS [2016-12-18 0 99999 7 -1](tel:2016-12-18 0 99999 7 -1)(密码已设置，使用 SHA512 加密。
```

2. userdel：删除用户:  `userdel [-r] [-f] user_name`

​                `-r` ：同时删除用户的家目录

​                        无'-r'时，家目录不会被删除

​                `-f` ：强行删除，哪怕用户已登录，这个选项有些危险，会使系统进入不一致状态

```
[root@Example ~]# userdel -r newone
userdel: user newone is currently used by process 3848    # 用户正登录，删除失败
[root@Example ~]# userdel -fr newone                        #用 -f 强行删除
userdel: user newone is currently used by process 3848    # 说明用户正登录，但命令本身已经成功
# 这时虽然还被删user还是登入、活跃状态，但已经被删除，登出后不可再登入

--------------------

[newone@Example ~]$ exit                                    #退出用户
logout

--------------------

[root@Example ~]# userdel -r newone
userdel：用户“newone”不存在                            #再作尝试时，确定用户已被之前的 -f 删除
[root@Example ~]# ls /home
c  lost+found                                        #家目录被 -r 删除
```

参考：

https://www.linuxidc.com/Linux/2016-05/131755.htm
