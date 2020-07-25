---
date: 2020-04-21 15:34:10
tags: School
title: 从「Leetcode 100. 相同的树」出发讨论为什么用「并发」
---

# 从「Leetcode [100. 相同的树](https://leetcode-cn.com/problems/same-tree/)」出发讨论为什么用「并发」

## 题目

给定两个二叉树，编写一个函数来检验它们是否相同。

如果两个树在结构上相同，并且节点具有相同的值，则认为它们是相同的。

示例 1:

```
输入:       1         1
          / \       / \
         2   3     2   3

        [1,2,3],   [1,2,3]

输出: true
```

示例 2:

```
输入:      1          1
          /           \
         2             2

        [1,2],     [1,null,2]

输出: false
```

示例 3:

```
输入:       1         1
          / \       / \
         2   1     1   2

        [1,2,1],   [1,1,2]

输出: false
```

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/same-tree
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

## 递归

树嘛，最方便的解决方案就是递归。

 同时 Walk 两棵树，对于某一步有这么几种情况：

- 两个节点都走到 nil 了，说明之前都相等，这里也相等，返回 true;
- 两个节点一个到了 nil，另一个不是，说明不相等，返回 false;
- 两个节点都不为 nil，但其 Val 不等，说明不相等，返回 false;
- 两个节点都不为 nil，且 Val 相等，分别下一层递归左右子树，若左右子树都相等则返回 true.

Golang 实现：

```go
/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
func isSameTree(p *TreeNode, q *TreeNode) bool {
    if p == nil && q == nil {
        return true
    } else if (p == nil || q == nil) {
        return false
    } else if p.Val != q.Val {
        return false
    } else {
        return isSameTree(p.Left, q.Left) && isSameTree(p.Right, q.Right)
    }
}
```

AC：

![image-20200421104735760](https://tva1.sinaimg.cn/large/007S8ZIlgy1ge172qhlqij31c60u01kx.jpg)

Golang 在处理这种涉及 nil 值判断的问题的时候都显得稍微繁琐了一点，用 Swift 可以写出更简洁的代码：

```swift
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     public var val: Int
 *     public var left: TreeNode?
 *     public var right: TreeNode?
 *     public init(_ val: Int) {
 *         self.val = val
 *         self.left = nil
 *         self.right = nil
 *     }
 * }
 */
class Solution {
    func isSameTree(_ p: TreeNode?, _ q: TreeNode?) -> Bool {
        if p == nil && q == nil {
            return true
        } else if p?.val != q?.val {
            return false
        }
        return isSameTree(p?.left, q?.left) && isSameTree(p?.right, q?.right)
    }
}
```

![屏幕快照 2020-04-21 11.48.10](https://tva1.sinaimg.cn/large/007S8ZIlgy1ge18xo0znij31c60u01kx.jpg)

## 迭代

把递归改成用一个 ~~栈~~ 队列就可以在迭代里完成这个功能了，Golang 实现：

```go
func isSameTree(p *TreeNode, q *TreeNode) bool {
    s := [][2]*TreeNode{[2]*TreeNode{p, q}}
    for len(s) > 0 {
        if p, q, s = s[0][0], s[0][1], s[1:]; !func (pn, qn *TreeNode) bool {
            switch {
            case p == nil && q == nil:
                return true
            case p == nil || q == nil:
                return false
            case p.Val != q.Val:
                return false
            default:
                return true
            }
        }(p, q) {
            return false
        } else if p != nil {
            s = append(s, [2]*TreeNode{p.Left, q.Left}, [2]*TreeNode{p.Right, q.Right})
        }
    }
    return true
}
```

我不喜欢这个算法，所以我故意把代码写的很恶心，但它可以运行通过，而且不慢：

![image-20200421145136574](https://tva1.sinaimg.cn/large/007S8ZIlgy1ge1e4ks0hqj31c60u01kx.jpg)

利用 Swift 的 **Optionals** 和 **Closures**，可以在很大程度上简化刚才的 golang 代码，这个代码就看得懂了：

```swift
class Solution {
    func isSameTree(_ p: TreeNode?, _ q: TreeNode?) -> Bool {
        var s = [[p, q], ]
        while !s.isEmpty {
            let pn = s[0][0]
            let qn = s[0][1]
            s.remove(at: 0)
            if !{ $0?.val == $1?.val }(pn, qn) {
                return false
            }
            if pn != nil {
                s.append([pn?.left, qn?.left])
                s.append([pn?.right, qn?.right])
            }
        }
        return true
    }
}
```

![image-20200421152621048](https://tva1.sinaimg.cn/large/007S8ZIlgy1ge1f4q9thqj31c60u01kx.jpg)

## 进一步探究：相同的二叉查找树

在 *A Tour of Go* 的「并发」章节里有这么一个叫 [Exercise: Equivalent Binary Trees](https://tour.golang.org/concurrency/7) 的练习题，和我们的「 Leetcode 100. 相同的树」都是判断树是否相同的，但题目有所区别。

*A Tour of Go* 里的题目大概如下：

> 不同二叉树的叶节点上可以保存相同的值序列。例如，以下两个二叉树都保存了序列 `1，1，2，3，5，8，13`。
>
> ![img](https://tva1.sinaimg.cn/large/007S8ZIlgy1ge2umnsl25j30dn0513yh.jpg)
>
> 在大多数语言中，检查两个二叉树是否保存了相同序列的函数都相当复杂。 我们将使用 Go 的并发和信道来编写一个简单的解法。

这个题是让判断两个**二叉查找树**（不仅是二叉树！）里保存的序列是否相同。

我先贴一下这道题的二叉搜索树实现（为了测试，我把树大小调的比较大）：

```go
// Copyright 2011 The Go Authors.  All rights reserved.
// Use of this source code is governed by a BSD-style
// license that can be found in the LICENSE file.

package tree // import "golang.org/x/tour/tree"

import (
	"fmt"
	"math/rand"
)

// A Tree is a binary tree with integer values.
type Tree struct {
	Left  *Tree
	Value int
	Right *Tree
}

// New returns a new, random binary tree holding the values k, 2k, ..., 10k.
func New(k int) *Tree {
	var t *Tree
	for _, v := range rand.Perm(10000000) {
		t = insert(t, (1+v)*k)
	}
	return t
}

func insert(t *Tree, v int) *Tree {
	if t == nil {
		return &Tree{nil, v, nil}
	}
	if v < t.Value {
		t.Left = insert(t.Left, v)
	} else {
		t.Right = insert(t.Right, v)
	}
	return t
}

func (t *Tree) String() string {
	if t == nil {
		return "()"
	}
	s := ""
	if t.Left != nil {
		s += t.Left.String() + " "
	}
	s += fmt.Sprint(t.Value)
	if t.Right != nil {
		s += " " + t.Right.String()
	}
	return "(" + s + ")"
}

```

要解决这个问题，我们可以跑个中序遍历，把值存下来，即把二叉搜索树里的数据放到排好序的顺序结构中，再比较两个顺序结构是否等价。比如对于题目中这两棵树，我们分别把他们化为顺序结构，刚好两个结果都是 `[1，1，2，3，5，8，13]`，所以，两棵树是等价的。代码实现：

```go
// noConcurrency.go

package main

import (
	"./tree"
	"fmt"
)

const TreeHeight int = 10000000

// Walk 步进 tree t 将所有的值从 tree 发送到 channel ch。
func Walk(t *tree.Tree, ch *[]int) {
	if t != nil {
		Walk(t.Left, ch)
		*ch = append(*ch, t.Value)
		Walk(t.Right, ch)
	}
}

// Same 检测树 t1 和 t2 是否含有相同的值。
func Same(t1, t2 *tree.Tree) bool {
	c1 := make([]int, 0)
	c2 := make([]int, 0)
	Walk(t1, &c1)
	Walk(t2, &c2)
	for i := 0; i < TreeHeight; i++ {
		if c1[i] != c2[i] {
			return false
		}
	}
	return true
}

func main() {
	testSame()
}

func testSame() {
	fmt.Println(Same(tree.New(1), tree.New(1)))
	fmt.Println(Same(tree.New(1), tree.New(2)))
}
```

这个实现依赖额外的数据储存，内存消耗很大：

![屏幕快照 2020-04-22 21.33.05](https://tva1.sinaimg.cn/large/007S8ZIlgy1ge2vh6wvlvj311a0padom.jpg)

所以，还有更好的实现吗？是的！我一开始介绍了，这个题目是出现在「并发」章节里的！乍一看，你可能觉得这个题用并发，好像就是可以把两个化为顺序结构的递归放两个线程里，单独跑，可以快一些吗？这好像也快不了多少。。

其实，之所以用并发，不是为了快，是为了省内存！利用 Go 程与信道，我们可以相当方便的实现一个**不用额外顺序结构**的实现。

这个实现的思路是，开两个 goroutine 里分别跑 Walk，中序那里不是 append 切片，而是把值传到信道里。再开另一个 goroutine 阻塞，等两个 Walk goroutine 的信道都有值了，就判断这两个值是否相等，不等就直接返回了；相等的话继续阻塞，判断下一组传过来的值，直到遍历完树。如果遍历完了，每一组值都相等，就说明两棵树是相等的：

```go
// concurrency.go

package main

import (
	"./tree"
	"fmt"
)

const TreeHeight int = 10000000

// Walk 步进 tree t 将所有的值从 tree 发送到 channel ch。
func Walk(t *tree.Tree, ch chan int) {
	if t != nil {
		Walk(t.Left, ch)
		ch <- t.Value
		Walk(t.Right, ch)
	}
}

// Same 检测树 t1 和 t2 是否含有相同的值。
func Same(t1, t2 *tree.Tree) bool {
	c1 := make(chan int)
	c2 := make(chan int)

	ans := make(chan bool)

	go Walk(t1, c1)
	go Walk(t2, c2)

	go func() {
		for i := 0; i < TreeHeight; i++ {
			if <-c1 != <-c2 {
				ans <- false
			}
		}
		ans <- true
	}()

	return <-ans
}

func main() {
	testSame()
}

func testSame() {
	fmt.Println(Same(tree.New(1), tree.New(1)))
	fmt.Println(Same(tree.New(1), tree.New(2)))
}

```

虽然时间上区别不大（所以我没贴出来），但这个版本的代码里，我们把 `noConcurrency.go` 里的两个空间复杂度 $O(n)$ 切片改成了 $O(1)$ 的信道！所以内存消耗相当显著得下降了：

![屏幕快照 2020-04-22 21.35.47](https://tva1.sinaimg.cn/large/007S8ZIlgy1ge2vi16zg2j311a0pa7cz.jpg)

## 启示：关于并发的思考

在过去还没有学习并发技术的很长的一段时间里，我都认为并发这些东西就是为了快！直到我学 Python 的时候学了一点点并发，才了解到并发在我们的通信、服务这方面有多重要。不过这个时候，我依然认为本源是并发可以跑得快！它跑得快所以单位时间内能处理的服务增多了。。。

学习了 Go 之后，回头想想这些想法，就感觉有点片面了。

诚然，在如今的多核/超线程处理器下，并发、并行的确能带来性能的提升。但这些手段在单核单线程的处理器上跑得并不快，还不如单线程呢。甚至有的时候，即使是在多线程处理器下并发跑得也不快，就比如我刚才写的两个版本判断相同的二叉查找树的代码，它们耗时几乎是一样的。即便如此，我们还是在用并发——不是为了效率，而是把问题拆分成小的模块，单独去处理一个一个的小模块。模块与模块之间相对独立，只在必要的时机传递必要的、最小化的信息（而且最好是单向点对点的传递，一个发，一个收）。

模块间的通信是这种系统的精髓。

我们一开始写的 `noConcurrency.go` 里两个 Walk 模块独自运行（虽然这里两个模块不是并发的，但不影响讨论，你可以看作是并发，给Walk调用前面加个go就好了），它们之间没有任何通讯把它们联系起来。这导致了两个模块必须各自把整颗树跑完，返两个超大的切片回来，再逐位判断两个切片里的值是否相等。要注意，这两个超大的切片里每一个值我们都只有了一次啊，但是用之前它在那里占用内存，用之后它还在那里消耗资源。一大堆($O(n)$)这样的「当前没有正在被使用的值」导致了大量的浪费。

我们不希望这样的浪费，即希望尽量减少这种「当前没有正在被使用的值」。那要怎么办？尽量减少就减到零嘛，那这任务就完成不了了。零个不行，就考虑 $O(1)$ 个。我们很自然就想到了两个 Walk 分别把自己遍历到的值放到变量 `c1`、`c2` 里，然后及时地比较 `c1`、`c2` ，比较完就扔，然后两个 Walk 又可以往里面放值了，然后再次比较。这种想法即可以完成任务，又把消耗降到了 $O(1)$。

我们来试着这种想法，用传统的代码，需要同时遍历两颗树：

```go
func DuplicateWalk(t1 *tree.Tree, t2 *tree.Tree) {
	if t1 != nil && t2 != nil {
		Walk(t1.Left, t2.Left)
        if t1.Value != t2.Value {
            // not Equivalent
        }
		Walk(t1.Right, t2.Right)
	}
}
```

你会发现这很不优雅！明明是两棵不同的树的遍历，现在都连到一起了！在这个问题里因为遍历二叉树这种任务很简单，所以这种写法勉强可以接受，但如果你面对的不是树的遍历而是一个超复杂的工作、也不止是两个同时，而是上千个任务，这种写法就会复杂的不可接受，乃至无法实现了。

既要同时发生（`Walk(t1, t2)`），又要同时停止进行比较（`if t1.Value != t2.Value {...}`），还要不恶心地把两棵树的遍历写在一起，这就是「并发」可以干的事了：

```go
go Walk(t1, c1)
go Walk(t2, c2)

go func() {
    for i := 0; i < TreeHeight; i++ {
        if <-c1 != <-c2 {
            ans <- false
        }
    }
    ans <- true
}()
```

树的递归还是一颗树一颗树分开的（这很好，一个模块就只应该做一个事），而且这次它们同时运行。同时运行就可以进行通信！它们分别靠两个信道把遍历到的值传出来，然后另一个 goroutine （模块）就等着这两个信道都有值的时候把值取出来比较一波。这样在并发下靠信道来通信，单向，点对点，一个发、一个收，在优雅地完成任务的同时，又把消耗降到了最低。所以说模块间的通信是并发系统的精髓。

当然，并发还有另一种好处：在这种模块化的系统中，只有模块设计的适当小，分离得足够充分，模块间的通信控制得足够准确，如果其中一个模块出了问题，除了与之通信的有限个模块随之挂起外，其他的模块都还是好的。这种小规模的局部问题是可以处理的，不容易造成全盘连锁崩溃。这在服务端程序里尤为重要。

（我困了写不下去了，就这样吧，有机会再改改、再补充）

---

By CDFMLR.

