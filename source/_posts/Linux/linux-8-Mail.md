---
categories:
- Linux
- Beginning
date: 2017-01-09 19:43:44
tags: Linux
title: linux-8-邮件系统
---

# 邮件系统

## 使用 `mail` 命令发送邮件：

```
$ mail -s "主题" 目标 [< 内容]
        目标：可以是本机上的用户名；
            也可以是一般的邮件地址；
        若使用重定向输入内容，Enter后直接发送，不回显；
        若不重定向，键入命令后从stdin读邮件正文（类似于“cat > file”）。
    
        要结束邮件内容，在一个空白行输入一个点('.')，然后Enter；
        之后会出现“Cc: ”（Carbon copy，副本）填写抄送目标，Enter；
        之后，mail发送邮件并退出。
```

e.g.    **foo** 用户发送邮件给 **bar** 用户：

```
[foo@Example ~]$ mail -s "A Testing Mail" bar        # To bar
Hi Bar,
Its a testing mail.        # 正文
From foo
.                          # 结束
Cc:                        # Enter，发送，退出
[foo@Example ~]
```

## 阅读电子邮件

- 收件箱：

```
$ ls -l /var/spool/mail
        Linux为每个用户准备了一个邮箱（file）
        以存放用户的邮件（including all mails）
$ cat /var/spool/mail/USER_NAME
        查看某用户的所有邮件（收件箱）
```

- 显示收件箱中的邮件列表：

```
[User@Example ~]$ mail        # to get a mail list.
Heirloom Mail version 12.4 7/29/08.  Type ? for help.
"/var/spool/mail/User": 2 messages 2 new
>N  1 Mail Delivery System  Thu Aug 23 12:46  80/2695  "Undelivered Mail Retu"
 N  2 Mail Delivery System  Thu Aug 23 12:52  94/3407  "Undelivered Mail Retu"
& 2        # Enter the number after 'N' to see the E-mail which you want.
Head
......        # Details.
End
& x    # Enter {x} to keep that mail in Mail-Box,
       # while {q} to move it to Trush-Box(mbox,a file to keep removed mail in $HOME).
```