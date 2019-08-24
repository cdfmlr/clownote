---
title: linux-1.0-用户信息
date: 2016-12-18 14:06:52
tags: Linux
categories:
	- Linux
	- Beginning
---

# 用户信息

* `$ whoami`
输出当前用户名
* `$ users`
列出当前登录的所有用户名
* `$ who am i`
显示用户名，登录终端，当前时间，IP
* `$ who`
比“who am i”多出 其他用户的信息
* `$ w`
信息更多的“who”：
```
[Me@Example ~]$ w
 10:59:09 up 4 min,  1 user,  load average:  0.46 , 0.35 ,  0.15
 当前时间 up 启动时长, 登录用户数, 平均提交任务数: 1min内, 10min内, 15min内
USER     TTY      FROM              LOGIN@    IDLE       JCPU       	PCPU     	WHAT
用户名    登录终端   登录地            登录时间   空闲时长    一共使用CPU时长    当前程序用CPU时长    当前任务CPU时长
                                                        
Me        pts/0    MyComputer       10:58     0.00s      0.06s      0.02s     w
```

