---
date: 2020-10-15 23:54:34
tags: Bullshit
title: gcc编译时优化
---

# 胡言乱语之gcc优化

本文为业余蒟蒻尝试分析一段简单的 C 代码在 gcc `-O0`、`-O1`、`-O2` 下的优化情况。

```
______________
< 大佬驱散！！ >
 --------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

做数值分析的实验，写了点 C 代码，浮点数性质的实验，很无聊。所以来尝试用不同优化等级，生成汇编代码玩玩。

- `a1.c`

原始 C 代码，将 100个 a3 逐个加到 a1 上，返回 a1。

```c
float a1_add_100a3_way1(float a1, float a3) {
    for (int i = 0; i < 100; i++) {
        a1 += a3;
    }
    return a1;
}
```

- `gcc-9 -O0 -S a1.c`

用 0 级优化，编译成汇编，相当忠实地「直译」：


```asm
_a1_add_100a3_way1:
LFB2:
	pushq	%rbp
LCFI3:
	movq	%rsp, %rbp
LCFI4:
	movss	%xmm0, -20(%rbp)
	movss	%xmm1, -24(%rbp)
	movl	$0, -4(%rbp)
	jmp	L3
L4:
	movss	-20(%rbp), %xmm0
	addss	-24(%rbp), %xmm0
	movss	%xmm0, -20(%rbp) 
	addl	$1, -4(%rbp)
L3:
	cmpl	$99, -4(%rbp)
	jle	L4
	movss	-20(%rbp), %xmm0
	popq	%rbp
LCFI5:
	ret
```

- `gcc-9 -O1 -S a1.c`

用 1 级优化：

```asm
_a1_add_100a3_way1:
LFB2:
	movl	$100, %eax
L4:
	addss	%xmm1, %xmm0
	subl	$1, %eax
	jne	L4
	ret
```

这个程序简单嘛，O1 已经优化的相当出色了，各种临时遍历能砍的全砍了。手写汇编也就这水平了。值得一提的是，它把 i 从 0 加到 `< 100`（即 `== 99`）的判断改成了从 100 减到 0，直接使用减法设置的 ZF，避免了一次 cmpl，很刺激。

- `gcc-9 -O2 -S a1.c`

用 2 级优化，编译成汇编：

```asm
_a1_add_100a3_way1:
LFB2:
	movl	$100, %eax
	.p2align 4,,10
	.p2align 3
L4:
	subl	$1, %eax
	addss	%xmm1, %xmm0
	jne	L4
	ret
```

和 1 级优化比，感觉几乎没有提升。但我有个不确定的**猜想**：

O2 编译把 subl 提到 addss 前运算，这样到 jne「取指」时，subl 已经到了「执行」，用一个 bubble 就可以避免流水线冒险。 而 O1 的版本里，jne 紧随 subl，jne  达到「取指」时，subl 还在「译码」阶段，需要更多的 bubble 或者其他方式来处理这里的流水线冒险，代价稍微大了一点点🤏。（流水线学的并不好，我不保证这个分析正确、有意义）

# 免责声明

这是一篇在桌面上找到的意义不明的文章。我于过去的某天偶然写下了这些东西，看上去很厉害，所以分享一下（但不知道内容是否正确、有效）。

> 「胡言乱语」(Bullshit) 系列文章（包括但不限于相关的汉字、拼音、拉丁字母、日语假名、阿拉伯字母、单词、句子图片、影像、录音，以及前述之各种随意组合等等）均为本人随意敲击键盘所出。用于检测本人电脑键盘录入、屏幕显示的机械、光电性能，并不代表本人局部或全部同意、支持或者反对其中的任何内容及观点。
