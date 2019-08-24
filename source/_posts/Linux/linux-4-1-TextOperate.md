---
title: linux-4.1-正文文本操作
date: 2017-01-02 12:51:52
tags: Linux
categories:
	- Linux
	- Beginning
---

# 正文文本操作

### `tr`：字符转换

```
$ tr 'A-Z' 'a-z' < w.txt > u.txt        # 将w中的大写->小写，放入u中
$ tr -d "\r" < dept.data > dept.data.unix        # 将DOS格式的正文文件（以回车“\r”符和换行“\n”符结束一行）转换成Linux格式的文件（只用换行符“\n”来结束一行）
```

### `cut`：从文件中剪出一个字段(列)至1(stdout)

```
$ cut [options] [file]
        -f：说明(定义)字段(列)
        -c：要剪切的字符：
                「-c4-7」：剪下每行4～7的字符
        -d：说明(定义)字段的分隔符(默认为Tab)
                「-d,」：以“,”为分隔符
$ cut -f2 emp.data
        显示emp.data中的第二列至stdout
```

### `paste`：粘贴

```
$ paste  -d,  name.txt  score.txt  >  student.txt
        -d：说明(定义)字段的分隔符(默认为Tab)
                「-d,」：以“,”为分隔符
        > ：横向合并文件：
            |Mike|         |99|          |Mike,99|
            |Jake|    +    |98|    ->    |Jake,98|
            |Anny|         |97|          |Anny,97|

```

### `uniq`：去掉文件中相邻的重复行

```
$ uniq [opts] [file]
        -c：在显示的行前冠以该行出现的次数
        -d：只显示重复行
        -i：忽略字符的大小写
        -u：只显示唯一的行
```

### `sort`：排序

```
$ sort [opt] [file]
         -r：反向排序
         -f：忽略大小写
         -n：按数字顺序排序
          -u：去掉重复行
          -t c：以字符c为分割符
          -k N1,[N2]：按N1->N2字段排序
```

### `col`: Tab转空格：

```
$ col -x < e.tabs >e.spaces
        将e.tabs中的Tab字符(^I)化为空格存在e.spaces中
```
