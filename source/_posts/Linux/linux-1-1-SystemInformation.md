---
categories:
- Linux
- Beginning
date: 2016-12-19 14:14:14
tags: Linux
title: linux-1.1-系统信息
---

# 系统信息

* `uname` 命令:  获取系统信息
(其中'u'代表UNIX)

* `$ uname`       显示当前操作系统
        `-n`    显示主机名
        `-i`    硬件平台名
        `-r`    系统发布版本信息
        `-s`    系统名
        `-m`    机器硬件名
        `-p`    显示CPU信息
        `-a`    以上全部
用 `-n -r` == `-i -n` == `-ni` == `-in`；
(详见 `$ man uname`。)
* `$ date`       显示当前系统日期、时间
* `$ cal`		 显示日历：
	* `$ cal`         无参显示本月日历
	* `$ cal m y`    m y是月份 年份，显示y年m月的
	* `$ cal y`      y 是年份，     显示y全年

	(详见 `$ man cal`。)
