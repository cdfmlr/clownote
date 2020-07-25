---
date: 2020-03-26 10:13:14
tags: School
title: Leetcode 641. 设计循环双端队列
---



# Leetcode [641. 设计循环双端队列](https://leetcode-cn.com/problems/design-circular-deque/)

## 题目

设计实现双端队列。
你的实现需要支持以下操作：

- MyCircularDeque(k)：构造函数,双端队列的大小为k。
- insertFront()：将一个元素添加到双端队列头部。 如果操作成功返回 true。
- insertLast()：将一个元素添加到双端队列尾部。如果操作成功返回 true。
- deleteFront()：从双端队列头部删除一个元素。 如果操作成功返回 true。
- deleteLast()：从双端队列尾部删除一个元素。如果操作成功返回 true。
- getFront()：从双端队列头部获得一个元素。如果双端队列为空，返回 -1。
- getRear()：获得双端队列的最后一个元素。 如果双端队列为空，返回 -1。
- isEmpty()：检查双端队列是否为空。
- isFull()：检查双端队列是否满了。

**示例：**

```
MyCircularDeque circularDeque = new MycircularDeque(3); // 设置容量大小为3
circularDeque.insertLast(1);			        // 返回 true
circularDeque.insertLast(2);			        // 返回 true
circularDeque.insertFront(3);			        // 返回 true
circularDeque.insertFront(4);			        // 已经满了，返回 false
circularDeque.getRear();  				// 返回 2
circularDeque.isFull();				        // 返回 true
circularDeque.deleteLast();			        // 返回 true
circularDeque.insertFront(4);			        // 返回 true
circularDeque.getFront();				// 返回 4
 
```

 

**提示：**

- 所有值的范围为 [1, 1000]
- 操作次数的范围为 [1, 1000]
- 请不要使用内置的双端队列库。

## 链表实现

经典的数据结构就不解释了，大家都懂，直接上代码，Golang 实现：

```go
type Node struct {
	Data int
	Next *Node
	Priv *Node
}

type MyCircularDeque struct {
	Front  *Node
	Last   *Node
	length int
	maxLen int
}

/** Initialize your data structure here. Set the size of the deque to be k. */
func Constructor(k int) MyCircularDeque {
	return MyCircularDeque{
		length: 0,
		maxLen: k,
		Front:  nil,
		Last:   nil,
	}
}

/** Adds an item at the front of Deque. Return true if the operation is successful. */
func (this *MyCircularDeque) InsertFront(value int) bool {
	if this.length == this.maxLen {
		return false
	}
	if this.length == 0 {
		this.Last = &Node{
			Data: value,
		}
		this.Front = this.Last
	} else {
		this.Front.Priv = &Node{
			Data: value,
			Next: this.Front,
		}
		this.Front = this.Front.Priv
	}
	this.length++
	return true
}

/** Adds an item at the Last of Deque. Return true if the operation is successful. */
func (this *MyCircularDeque) InsertLast(value int) bool {
	if this.length == this.maxLen {
		return false
	}
	if this.length == 0 {
		this.Front = &Node{
			Data: value,
		}
		this.Last = this.Front
	} else {
		this.Last.Next = &Node{
			Data: value,
			Priv: this.Last,
		}
		this.Last = this.Last.Next
	}
	this.length++
	return true
}

/** Deletes an item from the front of Deque. Return true if the operation is successful. */
func (this *MyCircularDeque) DeleteFront() bool {
	if this.length == 0 {
		return false
	}
	this.Front = this.Front.Next
	if this.Front != nil {
		this.Front.Priv = nil
	}
	this.length--
	return true
}

/** Deletes an item from the Last of Deque. Return true if the operation is successful. */
func (this *MyCircularDeque) DeleteLast() bool {
	if this.length == 0 {
		return false
	}
	this.Last = this.Last.Priv
	if this.Last != nil {
		this.Last.Next = nil
	}
	this.length--
	return true
}

/** Get the front item from the deque. */
func (this *MyCircularDeque) GetFront() int {
	if this.length == 0 {
		return -1
	}
	return this.Front.Data
}

/** Get the last item from the deque. */
func (this *MyCircularDeque) GetLast() int {
	if this.length == 0 {
		return -1
	}
	return this.Last.Data
}

// Alias of GetLast for the foolish leetcode
func (this *MyCircularDeque) GetRear() int {
	if this.length == 0 {
		return -1
	}
	return this.Last.Data
}

/** Checks whether the circular deque is empty or not. */
func (this *MyCircularDeque) IsEmpty() bool {
	return (this.length == 0)
}

/** Checks whether the circular deque is full or not. */
func (this *MyCircularDeque) IsFull() bool {
	return (this.length == this.maxLen)
}


/**
 * Your MyCircularDeque object will be instantiated and called as such:
 * obj := Constructor(k);
 * param_1 := obj.InsertFront(value);
 * param_2 := obj.InsertLast(value);
 * param_3 := obj.DeleteFront();
 * param_4 := obj.DeleteLast();
 * param_5 := obj.GetFront();
 * param_6 := obj.GetLast();
 * param_7 := obj.IsEmpty();
 * param_8 := obj.IsFull();
 */
```

吐槽一下Leetcode，给你的模版里是个 `GetLast`，你写好了，运行的时候就会爆出个错说你的 MyCircularDeque 里方法 `GetRear` 缺失，要把 GetLast 的代码抄一遍写个 GetRear 才行！

![image-20200326094017120](https://tva1.sinaimg.cn/large/00831rSTgy1gd730nmy30j31930u01kx.jpg)

用链表做算法题肯定时间空间结果都不好，但有意思嘛，写个切片去套快是快了、空间用的也小。

## 循环数组

参考 [JoshuaTsui《LeetCode 设计循环双端队列》](https://blog.csdn.net/JoshuaTsui/article/details/105102674)，Golang 实现：

```go
type MyCircularDeque struct {
	data   []int
	pFront int
	pAfterLast  int
	maxLen int
}

/** Initialize your data structure here. Set the size of the deque to be k. */
func Constructor(k int) MyCircularDeque {
	return MyCircularDeque{
		maxLen: k+1,
		pFront: 0,
		pAfterLast: 0,
		data: make([]int, k+1),
	}
}

/** Adds an item at the front of Deque. Return true if the operation is successful. */
func (this *MyCircularDeque) InsertFront(value int) bool {
	if this.IsFull() {
		return false
	}
	this.pFront = (this.pFront - 1 + this.maxLen) % this.maxLen	// notice to promise >= 0
	this.data[this.pFront] = value
	return true
}

/** Adds an item at the Last of Deque. Return true if the operation is successful. */
func (this *MyCircularDeque) InsertLast(value int) bool {
	if this.IsFull() {
		return false
	}
	this.data[this.pAfterLast] = value
    this.pAfterLast = (this.pAfterLast + 1) % this.maxLen
	return true
}

/** Deletes an item from the front of Deque. Return true if the operation is successful. */
func (this *MyCircularDeque) DeleteFront() bool {
	if this.IsEmpty() {
		return false
	}
	this.pFront = (this.pFront + 1) % this.maxLen
	return true
}

/** Deletes an item from the Last of Deque. Return true if the operation is successful. */
func (this *MyCircularDeque) DeleteLast() bool {
	if this.IsEmpty() {
		return false
	}
	this.pAfterLast = (this.pAfterLast - 1 + this.maxLen) % this.maxLen
	return true
}

/** Get the front item from the deque. */
func (this *MyCircularDeque) GetFront() int {
	if this.IsEmpty() {
		return -1
	}
	return this.data[this.pFront]
}

/** Get the last item from the deque. */
func (this *MyCircularDeque) GetLast() int {
	if this.IsEmpty() {
		return -1
	}
	return this.data[(this.pAfterLast - 1 + this.maxLen) % this.maxLen]
}

// Alias of GetLast for the foolish leetcode
func (this *MyCircularDeque) GetRear() int {
	if this.IsEmpty() {
		return -1
	}
	return this.data[(this.pAfterLast - 1 + this.maxLen) % this.maxLen]
}

/** Checks whether the circular deque is empty or not. */
func (this *MyCircularDeque) IsEmpty() bool {
	return (this.pFront == this.pAfterLast)
}

/** Checks whether the circular deque is full or not. */
func (this *MyCircularDeque) IsFull() bool {
	return (this.pAfterLast + 1) % this.maxLen == this.pFront
}
```

![image-20200326113533190](https://tva1.sinaimg.cn/large/00831rSTgy1gd76ckm54wj31930u01kx.jpg)

