---
date: 2021-08-07 09:22:32.141708
title: 不一样的“人工智能语言”Prolog
---
刚发布的八月份的 TIOBE 排行榜前 20，赫然出现了上古人工智能语言 Prolog！

TIOBE 说到：“And, even more astonishing, we see Prolog re-entering the top 20 after 15 years... making an unexpected comeback.”

![TIOBE Index for August 2021](https://tva1.sinaimg.cn/large/008i3skNgy1gt9psjnjf7j31gm0emgml.jpg)

（图片来自 TIOBE Index for August 2021）

时隔十余年，这个独特的语言居然又出现在了大家眼前，排名仅次于 Go！还不快学起来！

如果你学不动了，就请跟上我的脚步，今天，我们从一个清新脱俗的例子出发，领略这门不一样的“人工智能语言”。

另外，我们还做了一个和本文配套的 Prolog 入门视频，欢迎大家观看。如果视频对你有所帮助，别忘了一键三连哦：）

- [https://www.bilibili.com/video/BV14A411P7Vq/](https://www.bilibili.com/video/BV14A411P7Vq/)

（从脚本到音乐到剪辑全是自己做的，大家支持一下吧：）

# Prolog

```
like(mercury, kathy).        % mercury 喜欢 kathy。
like(kathy, mercury).        % kathy 喜欢 mercury。

lover(X, Y) :- like(X, Y), like(Y, X).        % 如果X喜欢Y，且Y也喜欢X，则X与Y是恋人。


询问mercury和谁是恋人：lover(mercury, Who).
电脑告诉我 Who = kathy，

这就是Prolog！
```

（这段文字取自一个如今犹在的上古网站 [Prolog 人工智能语言中文论坛](https://prolog.longluntan.com) 首页的一个醒目位置）

这是一首发人深思的好诗！但你可能很难想象这居然是一种「编程语言」。

回顾编程语言的发展，有可以分为几个时期。

- 第一代编程语言：机器语言，用 0 和 1 写代码（焊武帝同学为我们展现的失传已久的神技）。
- 第二代编程语言：汇编语言
- 第三代编程语言：高级语言，代表作 C，Java，C++，C#
  - 3.5 GL：晚期的第三代，如 Python、Lisp[^1]，抽象程度更高，已经有了第四代的影子。
- 第四代编程语言：抽象程度更高，更不用处理和硬件相关的细节，专注描述问题、解决问题，如 SQL，MATLAB

可能小伙伴们对编程语言的了解就止步这里了。但其实我们在几十年前就已经有了——

- **第五代编程语言**：人工智能语言，这一代编程语言期望计算机能自动求解问题，基于问题所给定的某些限制，交由程序来处理而不需以程序员再投入人力开发程序。

今天说「人工智能」你肯定想到 Python，但 Python 并不是第五代的人工智能语言。而 Prolog 就是这种没落十余年的第五代编程语言之一。

今天我们的重点不是谈为什么第五代编程语言集体没落，而是来学习这种上古语言 Prolog。

[^1]: Lisp：也有的资料说 Lisp 是第五代编程语言，但以我自己学习到的 Lisp 来看，Lisp 并不呼和第五代的定义，而是第五代语言可以用 Lisp 来实现。

## Prolog

Prolog 这个词来自 PROgramming of LOGic，也就是逻辑编程的意思。Prolog 不需要你编写程序运行过程，你只要给出事实和规则，它会自动分析其中的逻辑关系。然后你就可以通过查询，让 Prolog 完成复杂的逻辑运算。

## SWI-Prolog

Prolog 有非常多的实现，维基百科甚至专门有个词条比较不同的 Prolog 实现：

- [Wikipedia: Comparison of Prolog implementations](https://en.wikipedia.org/wiki/Comparison_of_Prolog_implementations)

这里我们采用 [SWI-Prolog](https://www.swi-prolog.org)——一个十分完善、仍在开发、维护的开源实现。在 macOS 中，可以用 `brew` 安装 SWI Prolog：

```sh
$ brew install swi-prolog
```

Debian 系 Linux 也可以用 `apt-get` 来轻松完成安装。其他系统可以去 [官网下载页](https://www.swi-prolog.org/download/stable) 寻找对应的二进制文件或者从源码构建。

如果你不想或难以完成安装，SWI-Prolog 还为你准备了 [在线版本](https://swish.swi-prolog.org)。

安装完成之后，通过 `swipl` 命令进入一个和 Python 类似的 SWI-Prolog REPL 环境（SWI-Prolog 的提示符是 `?-`）：

```sh
$ swipl
?- 
```

国际惯例，先写 Hello World：

```c
?- write('Hello, World!').
Hello, World!    % write 打印的结果
true.            % 返回值
```

注意 Prolog 的语句最后以 `.` 结尾。

要退出 SWI-Prolog，可以摁 `Control-D` 或输入 `halt.`。（你可以通过键入 `apropos(quit).` 来找到关于“退出”的主题 halt，然后用 `help(halt).` 查看如何退出）

## Prolog 基础语法

与我们平时接触的其他基于变量的编程语言不同，Prolog 的基础是

- Facts：事实
- Rules：规则
- Queries：查询

这几个概念就是字面意思，如

- 事实：`11 不能被 2 整除。`
- 规则：`不能被 2 整除的数是奇数。`
- 查询：`11 是奇数吗？`
  - 结果（答案）：`11 是奇数。`

在 Prolog 中**事实**和**规则**和在一起组成了知识库（Knowledge base），我们把这两者写在后缀名为 `.pl` 的文件里。

**查询**写在 REPL 中，基于已知知识库，对某个问题进行逻辑推理，给出答案。

### 事实

例如，假定我们知道一些事实（字面意思）是：

- Yomogi 和 Yume 相互喜欢；
- Kaneishi 也喜欢 Yomogi。

在 Prolog 中，这些个事实表示为：

```c
like(yomogi, yume).
like(yume, yomogi).
like(kaneishi, yomogi).
```

我们可以把这个写到一个 `./ssss.pl` 文件中，但不能写在 REPL 里。

在 Prolog 中，**小写**字母开头的单词是**常量**，表示一个对象，如 `like` 、`mercury`、`kathy` 都不需要预先定义，不需要赋值，直接写即可。

注意，喜欢这种事情是单向的。A 喜欢 B 不代表 B 喜欢 A（如 kaneishi 与 yomogi），所以这里为了表示 yomogi 与 yume 相互喜欢，必须写两句。

我们把 `like` 称为一种*关系*，即代表两个或多个对象之间某种相互联系，我们还可一定义只与一个对象有关的事实，这种事实称为*属性*：

```c
male(yomogi).
female(yume).
female(kaneishi).
```

### 规则

现在我们制订一个规则：

- 如果 X 喜欢 Y，且 Y 也喜欢 X，则 X 与 Y 就是恋人。

规则在 Prolog 表示为 `head :- goals`，即 goals 成立时，head 也就成立。

```c
lover(X, Y) :- like(X, Y), like(Y, X).
```

（这行代码也写到 `./ssss.pl` 中）

这行代码表示，如果 `like(X, Y)` 和 `like(Y, X)` 都成立，则有 `lover(X, Y)` 成立。用 Python 语言表示就是：

```python
def lover(X, Y):
    return like(X, Y) and like(Y, X)
```

在 Prolog 中的或与非：

- `A, B` 表示「A **与** B」
- `A; B` 表示「A **或** B」
- `\+ A` 表示「**非** A」

### 查询

前面的事实和规则都是定义，就是我们告诉 Prolog 一些已知信息。查询才是重头戏，就是让 Prolog 帮我们做逻辑题目。

使用 `swipl` 命令进入 Prolog 环境，然后使用 `consult("path/to/xxx.pl")` 加载写在 `.pl` 文件中的代码，来读取已知条件：

```c
$ swipl
Welcome to SWI-Prolog (threaded, 64 bits, version 8.2.4)
?- consult('ssss.pl').
true.
```

或者，也可以用 `[xxx].`  这个语法来加载 `xxx.pl`。

然后，如果我们想知道 yomogi 是否喜欢 yume，就可以问 Prolog：

```c
like(yomogi, yume).
true.
```

结果 `true` 表示 `like(yomogi, yume)` 即  yomogi 喜欢 yume 成立。而：

```c
?- like(yomogi, kaneishi).
false.

?- like(yomogi, gauma).
false.
```

`false` 就说明 yomogi 不喜欢 kaneishi，当然纯情的 yomogi 更不可能喜欢我们没定义过的陌生人 gauma。

前面这几次查询都是询问某个关系是否成立，也就是看看某个「事实」是否存在。而结合已定义 `lover` 的规则，Prolog 还可以：

```c
?- lover(yomogi, yume).
true.

?- lover(yume, yomogi).
true.

?- lover(yomogi, kaneishi).
false.

?- lover(kaneishi, yume).
false.
```

通过已知的 like 关系（事实），结合我们给的 lover 定义（规则），Prolog 可以推理：

- yomogi 和 yume 是恋人。当然，反过来说“yume 和 yomogi 是恋人”同样成立。
- 因为 yomogi 不喜欢 kaneishi，所以 yomogi 和 kaneishi 不是恋人！
- yume 和 kaneishi 之间没有任何一方喜欢的关系，所以两人也不是恋人。

如果只是这样，只会判断个对错，那 Prolog 就太弱了。在 Prolog 查询中还可以使用**变量**。

例如，我们想要知道~~蓬~~ yomogi 喜欢谁（Who）？就可以问 Prolog：

```c
?- like(yomogi, Who).
Who = yume.
```

这里 `Who` 是一个变量，Prolog 会求解查询中的变量，这里得到的结果是 `Who = yume`，也就是说 yomogi 喜欢 yume。

这里 Prolog 所做的操作其实就是解个方程，得到使查询结果为真的变量值：`like(yomogi, Who) = true` 得到 `Who=?`。

Prolog 中**大写**字母开头的单词是变量。（注意，Prolog 中变量大写、常量小写，和我们通常的 C 语言编程习惯是反的。）如果写错了大小写，意思就不对了，尝试查询：

```c
?- like(yomogi, who).
false.    % yomogi 不喜欢 who 这个人，咱也不知道 who 是谁
```

如果我们要查询 「yume 是否喜欢 yomogi」，而把 yume 写成了大写的 Yume，就变成了查询「喜欢 yomogi 的人是谁」：

```c
?- like(Yume, yomogi).    % Yume 是个变量，不是 yume 这个人
Yume = yume ;             % 摁 tab 键或摁 ; 键显示下一个结果
Yume = kaneishi.
```

这里 Yume 等于 Who，只是个变量，表示喜欢 yomogi 的人，而不是~~南同学~~前面定义中的 yume 这个人。根据我们一开始定义的事实，yume 和 kaneishi 都喜欢 yomogi，所以这里 Yume （Who）就可以是 yume 或 kaneishi。

对于这种有多个结果的查询。SWI-Prolog 默认每次只显示一个结果，然后等待，我们需要摁下 `;` （表示「或」，还记得吗）然后再显示下一个结果。（这里也可以摁 `tab` 键）

这里还想补充一点，Prolog 中有一个很有用的谓词 `listing`，可以列出某种关系的全部事实，或查看规则的定义：

```c
?- listing(like).
like(yomogi, yume).
like(yume, yomogi).
like(kaneishi, yomogi).
    
?- listing(lover).
lover(X, Y) :-
    like(X, Y),
    like(Y, X).
```

### 例：苏格拉底会不会死？

利用前面这些知识，就可以解决很多逻辑问题了，例如，已知：

- 苏格拉底是人
- 人都会死

所以可以退出结论：苏格拉底会死。

用 Prolog 来解决这个问题：

```c
person(socrates).       % 事实
mortal(X) :- person(X). % 规则

---
% 查询

?- mortal(socrates).    % 苏格拉底会死吗
true.
    
?- mortal(X).           % 谁会死
X = socrates
```

如果你觉得一个完整的程序不能只包括逻辑运算部分，还必须拥有输入输出，那么，结合 hello world 中的 write，我们可以实现：

```c
person(socrates).
person(plato).
person(aristotle).

mortal(X) :- person(X).

mortal_report :- 
    write('Known mortals are:'), nl, mortal(X), write(X), nl.  % nl 是换行
```

然后再解释器中调用：

```c
?- mortal_report.
socrates
plato
aristotle
```

这就得到了一些生命有限的凡人。

利用这种「逻辑编程」你还可以写成更多有趣的例子。如果你觉得这个例子已经理解不能了，那我推荐你重新学习一下基础的《数理逻辑》（很多《离散数学》书的第一章）。

---

到这里，我们其实只是看到了 Prolog 的最简单的用法，但完全没有接触到 Prolog 中真正强大的地方，例如递归，这些就写另一篇更深入的文章来进一步学习了，——不过我们现在这篇文章到此就结束了。


# 参考

[1] Blackburn, Patrick and Bos, Johan and Striegnitz, Kristina. [Learn Prolog Now!](http://lpn.swi-prolog.org/index.php). College Publications. 2006

[2] 阮一峰. [Prolog 语言入门教程](https://www.ruanyifeng.com/blog/2019/01/prolog.html). 阮一峰的网络日志. 2019

[3] SWI Prolog. [Getting Started](https://www.swi-prolog.org/GetStarted.html).

[4] Draveness. [Prolog 基础 <1>](https://draveness.me/prolog-ji-chu-1/). draveness.me, 2015

[5] 作者未知. Prolog 入门教程. 垂钓听竹轩. 2004

（最后这篇是我近10年前学习 Prolog 时看的文章，写的非常易懂。但如今网络上只有这篇的多手转载，以及其翻译的英文原文了，很难找到这份珍贵的中文译本，目前我只是找到了它最早可能是来自一个叫垂钓听竹轩的网站，但这个网站关了， archive.org 里的备份全是 3xx 错误，，有空我再考古一下了）
