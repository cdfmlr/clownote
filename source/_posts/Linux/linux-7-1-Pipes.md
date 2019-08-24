---
title: linux-7.1-管道(|)操作
date: 2017-01-07 19:38:35
tags: Linux
categories:
	- Linux
	- Beginning
---

# 管道(|)操作

## `|`：管道：

“<span style="color: rgb(9, 175, 255);">$ </span><span style="color: rgb(9, 175, 255);">cmd1 | cmd2</span>” ：将cmd1的**输出**  <u>重定向</u> 为cmd2的**输入。**

![ink-image](https://tva1.sinaimg.cn/large/006y8mN6ly1g6b05sda96j31kw0km75u.jpg)

使用管道符号将两个命令组合起来就相当于使用水管接头将水龙头与高压水枪接在一起，还可以先将水龙头来的水送到热水炉加温后再送到高压水枪，使用水管接头将3个现有的正常工作器系统组合成一个新的功能更强的系统。

![IMG_1047](https://tva1.sinaimg.cn/large/006y8mN6ly1g6b05sl6pxj30go01i0so.jpg)

```
$ who | wc -l
        显示工作用户数
$ cat /etc/passwd | wc -l
        显示注册用户数
$ ls -lF /bin | more
        用more显示ls的大量信息（可翻页）
```

## `| xargs`”：将管道导入的数据转换成后面命令的输入参数

```
$ cat bd.txt
a.txt
b.txt
c.txt
$ cat bd.txt | xargs rm -f        # 删除a.txt，b.txt，c.txt
```

## `|tee`：命令分流输出：（T型管道）

将前一个命令的输出结果直接输入给后一个命令，同时还要将前面命令的结果存入一个文件。

> tee命令的功能就是将标准输入复制给每一个指定的文件和标准输出。

![ink-image](https://tva1.sinaimg.cn/large/006y8mN6ly1g6b10dk5pcj31kw0km40s.jpg)

 T型管道的概念来自生活中的自来水管的T型接头。在一个公厕的水管阀门上接了一个T型接头将“免费”的水进行了分流，同时接入了洗车的高压水枪和抽水马桶。

![IMG_1048](https://tva1.sinaimg.cn/large/006y8mN6ly1g6b10nyojhj30bu043weo.jpg)

e.g.

```
$ cut -f1 -d: /etc/passwd | tee passwd.cut | sort -r | tee passwd.sort | more
        从/etc/passwd中剪出注册用户名列表，通过在sort -r命令之前和之后加入管道符和tee命令的方式将排序之前和之后的数据分别存入passwd.cut和passwd.sort文件。
        tee passwd.cut命令将由管道送过来的数据存入passwd.cut文件，同时还通过管道将这些数据送给下一个命令进行处理（sort -r命令进行反向排序）。tee passwd.sort命令将由管道送过来的数据（反向排序后的用户名）存入passwd.sort文件，同时还通过管道将这些数据送给下一个命令进行处理（more命令进行分页显示）。
```