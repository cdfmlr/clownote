---
date: 2020-03-18 21:24:10
tags: School
title: Leetcode P155 最小栈
---



# Leetcode P155 最小栈

## 题目

设计一个支持 push，pop，top 操作，并能在常数时间内检索到最小元素的栈。

- `push(x)` -- 将元素 x 推入栈中。
- `pop()` -- 删除栈顶的元素。
- `top()` -- 获取栈顶元素。
- `getMin()` -- 检索栈中的最小元素。

**示例:**

```
MinStack minStack = new MinStack();
minStack.push(-2);
minStack.push(0);
minStack.push(-3);
minStack.getMin();   --> 返回 -3.
minStack.pop();
minStack.top();      --> 返回 0.
minStack.getMin();   --> 返回 -2.
```

----

From [https://leetcode-cn.com/problems/min-stack/](https://leetcode-cn.com/problems/min-stack/)

## 额外最小栈

其实这个问题，直接用两个栈，一个存用户放入的数据，一个存对应另一个栈每一个位置的最小值就可以了，两个栈同时操作，同时 push、同时 pop：

```go
type MinStack struct {
    data []int
    min []int
    top int
}

/** initialize your data structure here. */
func Constructor() MinStack {
    return MinStack{
        data: make([]int, 0),
        min: make([]int, 0),
        top: 0,
    }
}

func (this *MinStack) Push(x int)  {
    this.data = append(this.data, x)
    if (this.top == 0 || x < this.min[this.top-1]) {
        this.min = append(this.min, x)
    } else {
        this.min = append(this.min, this.min[this.top-1])
    }
    this.top++
}

func (this *MinStack) Pop()  {
    this.data = this.data[0: this.top-1]
    this.min = this.min[0: this.top-1]
    this.top--
}

func (this *MinStack) Top() int {
    return this.data[this.top-1]
}

func (this *MinStack) GetMin() int {
    return this.min[this.top-1]
}

/**
 * Your MinStack object will be instantiated and called as such:
 * obj := Constructor();
 * obj.Push(x);
 * obj.Pop();
 * param_3 := obj.Top();
 * param_4 := obj.GetMin();
 */

```

![屏幕快照 2020-03-18 20.43.23](https://tva1.sinaimg.cn/large/00831rSTgy1gcyd9w7yf9j31460u0kir.jpg)

## 优化

在 min 的这个存最小值的栈里会有大量的重复的元素，所以我们干脆不要一对一的存最小值，而是最小值变更时再去操作最小值栈：

```go
type MinStack struct {
    data []int
    min []int
    top int
    minTop int
}

func Constructor() MinStack {
    return MinStack{
        data: make([]int, 0),
        min: make([]int, 0),
        top: 0,
        minTop: 0,
    }
}

func (this *MinStack) Push(x int)  {
    this.data = append(this.data, x)
    if (this.top == 0 || x <= this.min[this.minTop-1]) {
        this.min = append(this.min, x)
        this.minTop++
    }
    this.top++
}

func (this *MinStack) Pop()  {
    // 下面这个语句写优雅一点就是，但刷题嘛，尽量减少函数调用快一点：if t := this.Top(); t == this.Min() {}
    if t := this.data[this.top-1]; t == this.min[this.minTop-1] {
        this.min = this.min[0: this.minTop-1]
        this.minTop--
    }
    this.data = this.data[0: this.top-1]
    this.top--
}

func (this *MinStack) Top() int {
    return this.data[this.top-1]
}

func (this *MinStack) GetMin() int {
    return this.min[this.minTop-1]
}

```

![屏幕快照 2020-03-18 20.50.07](https://tva1.sinaimg.cn/large/00831rSTgy1gcydgmblqvj31460u01kx.jpg)

当然，把 top 属性去掉也是可以的，但调用 `len` 函数的话，消耗会大一点点：

```go
type MinStack struct {
    data []int
    min  []int
}

func Constructor() MinStack {
    return MinStack{
        data: make([]int, 0),
        min:  make([]int, 0),
    }
}

func (this *MinStack) Push(x int)  {
    this.data = append(this.data, x)
    if (len(this.min) == 0 || x <= this.min[len(this.min)-1]) {
        this.min = append(this.min, x)
    }
}

func (this *MinStack) Pop()  {
    if t := this.data[len(this.data)-1]; t == this.min[len(this.min)-1] {
        this.min = this.min[0: len(this.min)-1]
    }
    this.data = this.data[0: len(this.data)-1]
}

func (this *MinStack) Top() int {
    return this.data[len(this.data)-1]
}

func (this *MinStack) GetMin() int {
    return this.min[len(this.min)-1]
}

```

## In Python Way

对于这种问题，我还是喜欢用 Python 的内置工具去解决：

```python
class MinStack:

    def __init__(self):
        self.data = []

    def push(self, x: int) -> None:
        self.data.append(x)

    def pop(self) -> None:
        self.data.pop()

    def top(self) -> int:
        return self.data[-1]

    def getMin(self) -> int:
        return min(self.data)

```

![image-20200318210602995](https://tva1.sinaimg.cn/large/00831rSTgy1gcydvphv7pj31460u01kx.jpg)

这个 `min` 消耗太大了，我们把策略改成和刚才第一个版本的 Golang 一样：

```python
class MinStack:

    def __init__(self):
        self.data = []
        self.min = []

    def push(self, x: int) -> None:
        self.data.append(x)
        self.min.append(min(x, self.min[-1] if len(self.min) else 2147483648))

    def pop(self) -> None:
        self.data.pop()
        self.min.pop()

    def top(self) -> int:
        return self.data[-1]

    def getMin(self) -> int:
        return self.min[-1]

```

![image-20200318211544338](https://tva1.sinaimg.cn/large/00831rSTgy1gcye5sgkw7j31460u01kx.jpg)

还可以继续优化，但懒得写了。