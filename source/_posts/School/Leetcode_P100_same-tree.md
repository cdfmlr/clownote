---
title: Leetcode 100. 相同的树
tags: School
---

# Leetcode [100. 相同的树](https://leetcode-cn.com/problems/same-tree/)

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

