---
date: 2020-04-28 14:38:21
tags: School
title: Leetcode 236. 二叉树的最近公共祖先
---



# leetcode [236. 二叉树的最近公共祖先](https://leetcode-cn.com/problems/lowest-common-ancestor-of-a-binary-tree/)

## 题目

给定一个二叉树, 找到该树中两个指定节点的最近公共祖先。

百度百科中最近公共祖先的定义为：“对于有根树 T 的两个结点 p、q，最近公共祖先表示为一个结点 x，满足 x 是 p、q 的祖先且 x 的深度尽可能大（一个节点也可以是它自己的祖先）。”

例如，给定如下二叉树:  root = [3,5,1,6,2,0,8,null,null,7,4]

![img](https://tva1.sinaimg.cn/large/007S8ZIlgy1ge9c56ruw6j305k05aa9z.jpg) 

示例 1:

```
输入: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
输出: 3
解释: 节点 5 和节点 1 的最近公共祖先是节点 3。
```


示例 2:

```
输入: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
输出: 5
解释: 节点 5 和节点 4 的最近公共祖先是节点 5。因为根据定义最近公共祖先节点可以为节点本身。
```


说明:

所有节点的值都是唯一的。
p、q 为不同节点且均存在于给定的二叉树中。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/lowest-common-ancestor-of-a-binary-tree
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

---

。。。这个题，以前肯定刷过，记不得是哪个 OJ 的了。最简洁的方法应该是递归回溯，但不想写了。直接拿暴力法 ac 了，再改成并发玩玩吧。。。

## 暴力法

首先，实现一个辅助函数 `rewalk(root, node *TreeNode) []*TreeNode` ：遍历树，找到从某节点到根节点到一条路径，即找到这个节点的所有祖先节点。

通过这个 rewalk 函数，获得 p、q 的所有祖先节点，然后从里面找距离 p、q 最近的公共祖先节点返回即可。

Golang 实现：

```go
/**
 * Definition for TreeNode.
 * type TreeNode struct {
 *     Val int
 *     Left *ListNode
 *     Right *ListNode
 * }
 */
func lowestCommonAncestor(root, p, q *TreeNode) *TreeNode {
    rp := rewalk(root, p)
    rq := rewalk(root, q)

    for _, pp := range rp {
        for _, qq := range rq {
            if pp == qq {
                return pp
            }
        }
    }
    return &TreeNode{}
}

func rewalk(root, node *TreeNode) []*TreeNode {
    if root == nil {
        return []*TreeNode{}
    }
    if root.Left == node || root.Right == node {
        return []*TreeNode{node, root}
    }
    if r := rewalk(root.Left, node); len(r) > 1 {
        return append(r, root)
    }
    if r := rewalk(root.Right, node); len(r) > 1 {
        return append(r, root)
    }
    return []*TreeNode{node}
}

```

![image-20200428102347236](https://tva1.sinaimg.cn/large/007S8ZIlgy1ge99q4zyelj31cn0u04qp.jpg)

Swift:

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
    func lowestCommonAncestor(_ root: TreeNode?, _ p: TreeNode?, _ q: TreeNode?) -> TreeNode? {
        for pp in rewalk(root, p) {
            for qq in rewalk(root, q) {
                if pp?.val == qq?.val {
                    return pp
                }
            }
        }
        return nil
    }

    func rewalk(_ root: TreeNode?, _ node: TreeNode?) -> [TreeNode?] {
        if root == nil {
            return [TreeNode?]()
        }
        if root?.left?.val == node?.val || root?.right?.val == node?.val {
            return [node, root]
        }
        var rl = rewalk(root?.left, node)
        if rl.count > 1 {
            rl.append(root)
            return rl
        }
        var rr = rewalk(root?.right, node)
        if rr.count > 1 {
            rr.append(root)
            return rr
        }
        
        return [node]
    }
}
```

![image-20200428104142149](https://tva1.sinaimg.cn/large/007S8ZIlgy1ge9a8pvmnnj31cn0u01kx.jpg)

## 并发

在前几天写的 [从「Leetcode 100. 相同的树」出发讨论为什么用「并发」](https://clownote.github.io/2020/04/21/School/Leetcode_P100_same-tree/) 一文里，我讨论过，有的时候用并发并不是为了跑的快，只是让解决问题的思路变得更清晰、操作更加“原子化”、避免时间不同步造成的额外储存使用。这里也是一样的，我们可以把刚才的暴力法改成用 goroutine 和 channel，Golang 实现：

```go
func lowestCommonAncestor(root, p, q *TreeNode) *TreeNode {
    cp := make(chan *TreeNode)
    cq := make(chan *TreeNode)
    
    go rewalk(root, p, cp)
    go rewalk(root, q, cq)

    ans := make(chan *TreeNode)

    go func() {
        ap := []*TreeNode{}
        aq := []*TreeNode{}
        for {
            select {
            case p := <- cp:
                for _, q := range aq {
                    if p == q {
                        ans <- p
                    }
                }
                ap = append(ap, p)
            case q := <- cq:
                for _, p := range ap {
                    if q == p {
                        ans <- q
                    }
                }
                aq = append(aq, q)
            }
        }
    }()

    return <-ans
}

func rewalk(root, node *TreeNode, ch chan *TreeNode) bool {
    if root == nil {
        return false
    }
    if root.Left == node || root.Right == node {
        ch <- node
        ch <- root
        return true
    }
    if r := rewalk(root.Left, node, ch); r {
        ch <- root
        return true
    }
    if r := rewalk(root.Right, node, ch); r {
        ch <- root
        return true
    }
    ch <- node
    return false
}
```

![image-20200428113206480](https://tva1.sinaimg.cn/large/007S8ZIlgy1ge9bp875ekj31cn0u01kx.jpg)

通过调整超时（就是在 select 里加一个 `case <- time.After(...*time.Microsecond)`），我去卡了 leetcode 的测试用例出来看，他的数据规模都比较小，给的树都不大，所以这个用并发优势体现不出来。但如果你的树炒鸡大，这个用并发的算法肯定是会有一定优势的。比如如果给的 p、q 距离树根都有 10,000,000 个祖先节点，暴力法要全部跑一边、存下来、再嵌套for  10,000,000 个  10,000,000 个的去遍历，而如果它们的最近公共祖先只距离 1000 个节点，那并发只要跑 1000 个就结束了、检查的遍历也是在 1000 * 1000 里的，这要快得多、省得多了。

