---
title: Leetcode 104. 二叉树的最大深度
tags: School
---

# Leetcode [104. 二叉树的最大深度](https://leetcode-cn.com/problems/maximum-depth-of-binary-tree/)

## 题目

给定一个二叉树，找出其最大深度。

二叉树的深度为根节点到最远叶子节点的最长路径上的节点数。

说明: 叶子节点是指没有子节点的节点。

示例：
给定二叉树 `[3,9,20,null,null,15,7]`，

```
    3
   / \
  9  20
    /  \
   15   7
```

返回它的最大深度 3 。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/maximum-depth-of-binary-tree
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

## 递归

求深度，深度优先去跑一遍就出来了。Golang 实现:

```go
/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
func maxDepth(root *TreeNode) int {
    if root == nil {
        return 0
    }
    leftDepth := maxDepth(root.Left) + 1
    rightDepth := maxDepth(root.Right) + 1
    if leftDepth > rightDepth {
        return leftDepth
    }
    return rightDepth
}
```

![image-20200428084432376](https://tva1.sinaimg.cn/large/007S8ZIlgy1ge96uvbw9fj31co0u01kx.jpg)

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
    func maxDepth(_ root: TreeNode?) -> Int {
        if root == nil {
            return 0
        }
        return max(maxDepth(root?.left), maxDepth(root?.right)) + 1
    }
}
```

![image-20200428084300289](https://tva1.sinaimg.cn/large/007S8ZIlgy1ge96tea5w1j31ih0u0qss.jpg)

## 迭代

把递归改成栈，DFS也能出来，基本是一样的。Golang 实现:

```go
func maxDepth(root *TreeNode) int {
    if root == nil {
        return 0
    }
    depth := 1
    root.Val = 1
    stack := []*TreeNode{root}
    for len(stack) > 0 {
        node := stack[len(stack) - 1]
        stack = stack[: len(stack) - 1]
        if node.Val > depth {
            depth = node.Val
        }
        if node.Left != nil {
            node.Left.Val = node.Val + 1
            stack = append(stack, node.Left)
        }
        if node.Right != nil {
            node.Right.Val = node.Val + 1
            stack = append(stack, node.Right)
        }
    }
    return depth
}
```

![屏幕快照 2020-04-28 08.51.08](https://tva1.sinaimg.cn/large/007S8ZIlgy1ge972t6548j31co0u01kx.jpg)

虽然不地道，但代码基本不变，改几个符号就可以放到 Swift 里跑了:

```swift
class Solution {
    func maxDepth(_ root: TreeNode?) -> Int {
        if root == nil {
            return 0
        }
        var depth = 1
        root?.val = 1
        var stack: [TreeNode] = [root!, ]
        while !stack.isEmpty {
            let node = stack.popLast()!
            if node.val > depth {
                depth = node.val
            }
            if node.left != nil {
                node.left?.val = node.val + 1
                stack.append(node.left!)
            }
            if node.right != nil {
                node.right?.val = node.val + 1
                stack.append(node.right!)
            }
        }
        return depth
    }
}
```

![image-20200428092824475](https://tva1.sinaimg.cn/large/007S8ZIlgy1ge984g3z1qj31co0u01kx.jpg)

