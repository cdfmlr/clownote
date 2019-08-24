---
title: linux-6-计算与逃逸
date: 2017-01-05 09:33:44
tags: Linux
categories:
	- Linux
	- Beginning
---

# 计算与逃逸

1. 用Linux命令进行数字运算

```
$ $a1=1;a2=2;        # 定义变量，一行可多个
$ echo $a1           # 输出a1的值
$ echo $[$a1+$a2]    # 输出a1+a2的值
# 可用运算有：
     + - * / % **    # 同Python，对整数用／要去尾
```

2. `\`——逃逸符号

```
$ echo "$6830"        # 未定义的空变量$6
830        # output
$ echo "\$6830"       # 用“\”逃逸符号还原“$”
$6830      # output
```

'\\'还可以放在命令最后表续行（在下一行继续输入该命令）

3. `'str'`、`"str"`：文字 -> 字符串
   * `'abc'`   ：禁止所有命令行拓展功能
   * `"abc"`  ：允许以下拓展：
   
   ```
   $
   `
   \
   !
   ```


4. 利用拓展：

将一个命令的输出作为另一个的参数：

```
$ echo "Today is `date`"
等价于
$ echo "Today is $(date)"
即：
    用“ `cmd` ”或“ $(cmd) ”实现：
        print('Today is %s' % cmd())
```