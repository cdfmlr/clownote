---
date: 2020-03-19 14:16:13
tags: School
title: Leetcode P150 逆波兰表达式求值
---



# Leetcode P150 逆波兰表达式求值

## 题目

根据[逆波兰表示法](https://baike.baidu.com/item/逆波兰式/128437)，求表达式的值。

有效的运算符包括 `+`, `-`, `*`, `/` 。每个运算对象可以是整数，也可以是另一个逆波兰表达式。

**说明：**

- 整数除法只保留整数部分。
- 给定逆波兰表达式总是有效的。换句话说，表达式总会得出有效数值且不存在除数为 0 的情况。

**示例 1：**

```
输入: ["2", "1", "+", "3", "*"]
输出: 9
解释: ((2 + 1) * 3) = 9
```

**示例 2：**

```
输入: ["4", "13", "5", "/", "+"]
输出: 6
解释: (4 + (13 / 5)) = 6
```

**示例 3：**

```
输入: ["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]
输出: 22
解释: 
  ((10 * (6 / ((9 + 3) * -11))) + 17) + 5
= ((10 * (6 / (12 * -11))) + 17) + 5
= ((10 * (6 / -132)) + 17) + 5
= ((10 * 0) + 17) + 5
= (0 + 17) + 5
= 17 + 5
= 22
```

From [https://leetcode-cn.com/problems/evaluate-reverse-polish-notation/](https://leetcode-cn.com/problems/evaluate-reverse-polish-notation/)


## 原理

这个东西只要写过简单计算器的话，肯定不在话下。这个题目逆波兰表达式求值最简单的情况了，原理很简单：

>  读到数字就入栈；
>
> 读到符号就出栈两个元素运算，结果入栈。

## 实现

#### 标准栈实现

基本版本，实现一个标准的栈，进行操作：

```go
import (
	"strconv"
)

func evalRPN(tokens []string) int {
    if len(tokens) == 0 {
        return 0
    }
	s := newStack()
	for _, i := range tokens {
		switch i {
		case "+":
			a, b := s.pop(), s.pop()
			s.push(b + a)
		case "-":
			a, b := s.pop(), s.pop()
			s.push(b - a)
		case "*":
			a, b := s.pop(), s.pop()
			s.push(b * a)
		case "/":
			a, b := s.pop(), s.pop()
			s.push(b / a)
		default:
			n, _ := strconv.Atoi(i)
			s.push(n)
		}
	}
	return s.pop()
}

type stack struct {
	data []int
}

func newStack() *stack {
	return &stack{
		data: make([]int, 0),
	}
}

func (s *stack) push(data int) {
	s.data = append(s.data, data)
}

func (s *stack) pop() int {
	top := s.data[len(s.data)-1]
	s.data = s.data[0 : len(s.data)-1]
	return top
}

```

#### 成熟的栈应该学会自己完成计算

那一大堆 `a, b := s.pop(), s.pop()` 和 ` s.push(b * a)` 很烦，优化一下，把刚才的标准 stack 换成一个“子类” calcStack。我们的 calcStack 是个成熟的栈了，应该学会自己完成计算：

```go
import (
	"strconv"
)

func evalRPN(tokens []string) int {
	s := newCalcStack()
	for _, i := range tokens {
		switch i {
		case "+":
			s.calc(func (a, b int) int { return b + a})
		case "-":
			s.calc(func (a, b int) int { return b - a})
		case "*":
			s.calc(func (a, b int) int { return b * a})
		case "/":
			s.calc(func (a, b int) int { return b / a})
		default:
			n, _ := strconv.Atoi(i)
			s.push(n)
		}
	}
	return s.pop()
}

type calcStack struct {
	data []int
}

func newCalcStack() *calcStack {
	return &calcStack{
		data: make([]int, 0),
	}
}

func (s *calcStack) push(data int) {
	s.data = append(s.data, data)
}

func (s *calcStack) pop() int {
	top := s.data[len(s.data)-1]
	s.data = s.data[0 : len(s.data)-1]
	return top
}

func (s *calcStack) calc(opt func(int, int)int) {
	s.push(opt(s.pop(), s.pop()))
}

```

![屏幕快照 2020-03-19 11.09.01](https://tva1.sinaimg.cn/large/00831rSTgy1gcz29bech9j31460u04ps.jpg)

#### 多用指针

如果你喜欢用指针，还可以再优化，我们甚至可以不需要 pop 了：

```go
import (
	"strconv"
)

func evalRPN(tokens []string) int {
	s := newCalcStack()
	for _, i := range tokens {
		switch i {
		case "+":
			s.calc(func (a, b *int) { *b += *a })
		case "-":
			s.calc(func (a, b *int) { *b -= *a })
		case "*":
			s.calc(func (a, b *int) { *b *= *a })
		case "/":
			s.calc(func (a, b *int) { *b /= *a })
		default:
			n, _ := strconv.Atoi(i)
			s.push(n)
		}
	}
	// return s.pop()
	return s.data[0]
}

type calcStack struct {
	data []int
}

func newCalcStack() *calcStack {
	return &calcStack{
		data: make([]int, 0),
	}
}

func (s *calcStack) push(data int) {
	s.data = append(s.data, data)
}

// func (s *calcStack) pop() int {
// 	top := s.data[len(s.data)-1]
// 	s.data = s.data[0 : len(s.data)-1]
// 	return top
// }

func (s *calcStack) calc(opt func(*int, *int)) {
	// s.push(opt(s.pop(), s.pop()))
	opt(&s.data[len(s.data)-1], &s.data[len(s.data)-2])
	s.data = s.data[0 : len(s.data)-1]
}

```

