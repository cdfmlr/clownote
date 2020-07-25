---
categories:
- Linux
- Beginning
date: 2017-01-11 19:52:41
tags: Linux
title: linux-9.1-sed
---

# sed

利用被称为管道操作符的|，多个命令由管道符连成了管道线。

在UNIX或Linux系统中，流过管道线的信息（数据）就叫做流（stream）;

为了编辑或修改一条管道中的信息，就使用流编辑器（stream editor）;

这是sed这个命令的名字的由来。

sed编辑文件，将结果输出到1，不改变原文件。

```
sed [选项] '以引号括起来的命令表达式' [输入文件]
    -e <expression>：e是expression, 以选项中指定的script来处理输入的文本文件，后接表达式
    -f <file>：以选项中指定的script文件来处理输入的文本文件。
    -i：直接在文件中替换，不在终端输出
            -i常和 备份原本文件的-l 配合使用。
    在sed命令中使用多个命令表达式，这命令表达式中间要使用分号（;）分隔开
```

<span style="color: rgb(51, 51, 51);">在一个文件中指定数据行的范围内抽取某一字符串并用新的模式替代它：</span>

```
sed -e 's/旧模式/新模式/标志' file
        s是substitute，
        两个最有用的标志分别是g和n。
            g是globally，表示要替代每一行中所出现的全部模式。（无g只换每行的头一个）
            n告诉sed只替代前n行中所出现的模式。
```

    e.g.

```
grep CLERK emp.fmt | sed -e 's/ /;/g;s/CLERK/ASSISTANT MANAGER/g'
    1. grep将所有带CLERK的行找出；
    2. sed 将所有的空格（分隔符）都转换成分号（;）；
    3. sed 将所有的CLERK字符串都替换成ASSISTANT MANAGER；
```

删除某行：

```
$ sed 'nd' file
    在显示结果中删除第n行
$ sed 'm,nd' file
    在显示结果中删除第m到n行
$ sed '/str/d' file
    删除所有带str的行
$ sed '/^$/d' file
    删除所有空行        # re("^$") means a line without any word.(只有开始符^和结尾符$的行)
$ sed '1,/str/d' file
    删除从第1行开始直到包含有str的数据行（包括有str的那行）
```

e.g.

```
（1）电子邮件和一些应用程序显示的每一行信息都是以>开始的，使用下面的一条sed命令来做到这一点：
$ sed '/^$/d;s/^/> /g' source >result
    第1个命令表达式/^$/d表示要删除所有的空行，
    第2个命令表达式s/^/>/表示将开始符号替换成大于符号和空格符，
    最后的>result表示将sed命令的结果存入result文件。
------------------------------------------------------------------------------------------
（2）在删除所有空行的同时，删除所有包含了“cal“的行，并将所有的字符串“tie“变成“fox“,将结果保存：
$ sed '/^$/d;/cal/d;s/tie/fox/g' source >result
```