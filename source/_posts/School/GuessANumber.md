---
title: 猜测随机数
tags: School
---

# 猜测随机数

## 题目

![2271583200846_.pic_hd](https://tva1.sinaimg.cn/large/00831rSTgy1gcgr2q1foqj31qc0u0wps.jpg)

今天这个题目很别致啊。。。

## 昔日旧解

大一的时候写过这个题，翻一下那个时候的源码：

```cpp
#include <iostream>
#include <stdlib.h>
#include <time.h>

int main()
{
	unsigned randNum, usersNum;
	int cnt = 0;
//	char *tip;				// GCC warning: ISO C++ forbids converting a string constant to 'char*'
	std::string tip;		// 使用C++ 11的string类

	srand(time(NULL));			// 用当前时间作随机数种子
	randNum = rand() << 2 + rand() << 4;	// rand()提供的值在0～RAND_MAX == 32767之间, 通过运算防止每次结果太接近

	while(randNum > 100)			// 保证randNum的值在0～100
		randNum /= 10;
		
	std::cout << "Please enter a int to guess:" << std::endl;
	do {
		cnt++;
		std::cin >> usersNum;
		if (usersNum == randNum){
			tip = "You are RIGHT!";
			break;
		}
		else
			usersNum > randNum ? tip = "Yours is bigger!" : tip = "Yours is too small!";
		std::cout << "Try " << cnt << ": "<< tip << std::endl;
	} while(cnt < 10);
	if (cnt <= 10)				//当猜中终止循环时，补充break跳过的输出
		std::cout << "Try " << cnt << ": "<< tip << std::endl;
	std::cout << "Gussing over!" << std::endl;

	return 0;
}
```

这代码好怪，又慢又不安全，还有bug，，不管了，直接编译吧：

```shell
$ g++ guess.cc
```

结果一大堆报错：

![屏幕快照 2020-03-03 15.07.02](https://tva1.sinaimg.cn/large/00831rSTgy1gcgr7yimr3j31ey0u07wi.jpg)

吓得我满头~~大汉~~大汗，定睛一看主要是我写的是 `C++11`，编译器好像不认识`C++11`代码......先看一下gcc版本，

```bash
[c@My-MacBook:] guess !549 $ g++ --version
Configured with: --prefix=/Applications/Xcode.app/Contents/Developer/usr --with-gxx-include-dir=/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/c++/4.2.1
Apple clang version 11.0.0 (clang-1100.0.33.12)
Target: x86_64-apple-darwin18.7.0
Thread model: posix
InstalledDir: /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin
```

4.2.1的 gcc，还是 Xcode 的 clang！编译不了 `C++11` 也就不奇怪了。那我以前是怎么搞的？？？

我肯定不是用这个呀，翻了好久才翻到了正宗的 `GNU GCC` ，他原本的 `gcc` 链接都被 xcode 覆盖了，要 `gcc-9` 才是他😂

```sh
[c@My-MacBook:] guess !551 $ g++-9 --version
g++-9 (Homebrew GCC 9.2.0) 9.2.0
Copyright (C) 2019 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

这个就肯定没问题了，编译运行：

![image-20200303151634979](https://tva1.sinaimg.cn/large/00831rSTgy1gcgrhgp86dj31di0u0h8x.jpg)

## 正常解决方案

刚才那个代码有点怪，而且没做异常处理，再好好写一个。

这段时间都在用 Golang，所以今天写一个大家喜闻乐见的 Python3 版本:

```python
import random

if __name__ == "__main__":
    num = random.randint(0, 100)
    cnt = 0
    print("猜测一个0到100之间的整数.")
    while cnt < 100:
        cnt += 1
        try:
            inp = int(input(f"第 {cnt} 次猜，请输入一个整形数字: "))
            if inp == num:
                print("恭喜你猜对了，这个数是 %d。" % num)
                exit(0)
            print("太大" if inp > num else "太小")
        except ValueError:
            print("输入无效，这次不算。")
            cnt -= 1
    print("你怕不是个傻子！")
```

顺便提一下，这里我写了平时基本见不到大家写的 `f-String`。`f-String` 是 Python 3.6 引入的，更优雅的字符串插值方案，想要了解更多我推荐 [这篇文章](https://realpython.com/python-f-strings/)（这个网站挺不错的），当然你也可以直接读 [PEP 498](https://www.python.org/dev/peps/pep-0498/) 这是 f-String 的来源。

## 一行代码解法

这个要一行代码解决就麻烦了，但还是值得一试。

为了方便阅读，先拆成几个部分来写：

```python
import random
from functools import reduce

def d(x, y):
    return [x[0], print("猜中了") if x[3]==x[0] else None, exit(0) if x[3]==x[0] else None, int(input(("太大" if x[3] > x[0] else "太小") + "\n再试一次: "))]

reduce(d, [[random.randint(0,100), None, None, -1] if x == 0 else [0, None, None, -1] for x in range(100)])

print("你傻了")
```

只是这么做有个小 bug，一开始会输出一个“太小”，这当然也是可以解决的，但会让代码更恶心一点，我们在把代码压缩到一行的同时解决一下它：

```python
import random
from functools import reduce

print("你傻了吧" if reduce(lambda x, y: [x[0], print("猜中了") if x[3]==x[0] else None, exit(0) if x[3]==x[0] else None, int(input(("太大" if x[3] > x[0] else ("太小" if x[3]>=0 else "猜测一个0到100之间的整数.")) + "\n你的猜测: "))], [[random.randint(0,100), None, None, -1] if x == 0 else [0, None, None, -1] for x in range(10)])[-1] < 50 else "你傻了呀")
```

这就完成了一行代码解法，但是这么做就不能判断用户输入是否异常了。还是不推荐写这种代码，看起来看不懂、用起来也有隐患，只是娱乐一下了。

