---
date: 2020-04-21 17:34:34
tags: School
title: Leetcode 101. 对称二叉树
---

# Leetcode [101. 对称二叉树](https://leetcode-cn.com/problems/symmetric-tree/)

## 题目

给定一个二叉树，检查它是否是镜像对称的。 

例如，二叉树 `[1,2,2,3,4,4,3]` 是对称的。

```
    1
   / \
  2   2
 / \ / \
3  4 4  3
```

但是下面这个 `[1,2,2,null,3,null,3]` 则不是镜像对称的:

```
    1
   / \
  2   2
   \   \
   3    3
```

进阶：

你可以运用递归和迭代两种方法解决这个问题吗？

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/symmetric-tree
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

## 暴力法

把左子树以**先左后右**的顺序遍历，把 val 用线性结构存下来；把右子树以**先右后左**的顺序遍历，把 val 用线性结构存下来。然后，比较两个结果，相等则说明对称。大概就这个思路，你细品。

涉及到空值处理的代码我喜欢用 Swift 实现：

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
    func isSymmetric(_ root: TreeNode?) -> Bool {
        var leftSubTreeVals = [root?.val]
        leftFirstWalk(root?.left, &leftSubTreeVals)
        
        var rightSubTreeVals = [root?.val]
        rightFirstWalk(root?.right, &rightSubTreeVals)

        return leftSubTreeVals == rightSubTreeVals
    }

    func leftFirstWalk(_ root: TreeNode?,_ vals: inout [Int?]) {
        vals.append(root?.val)
        if root == nil {
            return
        }
        leftFirstWalk(root?.left, &vals)
        leftFirstWalk(root?.right, &vals)
    }
    
    func rightFirstWalk(_ root: TreeNode?,_ vals: inout [Int?]) {
        vals.append(root?.val)
        if root == nil {
            return
        }
        rightFirstWalk(root?.right, &vals)
        rightFirstWalk(root?.left, &vals)
    }
}
```

![屏幕快照 2020-04-21 16.11.00](https://tva1.sinaimg.cn/large/007S8ZIlgy1ge1gffgsjwj31c60u01kx.jpg)

（一开始rightFirstWalk是直接复制粘贴leftFirstWalk过来的，里面的 left 忘改成 right 了😂，所以报了个WA）

## 递归法

和往常一样，我们递归的设计从考虑一个最简单的情形开始。考虑两棵只有一个节点的树：

```
n1      n2
```

它们是对称的当且仅当 `n1 == n2`。

如果这两个节点有且只有一层孩子：

```
    n1          n2
   / \         / \
 l1   r1     l2   r2
```

这时，两棵数对称的充要条件变成了：`n1 == n2` 且 `l1 == r2` 且 `r1 == r2`。

注意到 `l1 == r2` 等价于两棵只有一个节点的树 `l1` 和 `r2` 对称。

这给了我们一个启示，如果这两个节点有子树：

```
    n1          n2
   / \         / \
 l1   r1     l2   r2
```

这时，两棵数对称的充要条件就是：`n1 == n2` 且 `l1 与 r2 对称` 且 `r1 与 r2 对称`。

 Swift 实现：

```swift
class Solution {
    func isSymmetric(_ root: TreeNode?) -> Bool {
        return symmetric(root?.left, root?.right)
    }

    func symmetric(_ left: TreeNode?, _ right: TreeNode?) -> Bool {
        if left == nil && right == nil {
            return true
        }
        if left?.val != right?.val {
            return false
        }
        return symmetric(left?.left, right?.right) && symmetric(left?.right, right?.left)
    }
}
```

![image-20200421165205677](https://tva1.sinaimg.cn/large/007S8ZIlgy1ge1hly9ljrj31c60u01kx.jpg)

##  迭代法

```swift
class Solution {
    func isSymmetric(_ root: TreeNode?) -> Bool {
        var s = [root, root]
        while !s.isEmpty {
            let t1 = s.popLast()
            let t2 = s.popLast()

            if t1??.val != t2??.val {
                return false
            }
            if t1??.val != nil || t2??.val != nil {
                s.insert(contentsOf: [t1??.left, t2??.right], at: 0)
                s.insert(contentsOf: [t1??.right, t2??.left], at: 0)
            }
        }
        return true
    }
}
```

![image-20200421173132163](https://tva1.sinaimg.cn/large/007S8ZIlgy1ge1iqz5yxhj31c60u01kx.jpg)

---

## （蒟蒻的抱怨）

啪！

嘣！

蒟蒻把键盘一砸，就夺门而出。

“蒟蒻出门了！”，不知谁喊了这么一嗓子，家家户户便都急着开窗，太太们顾不得整理饰物就伸出头来围观蒟蒻的蓬头垢面。

先生们、孩子们、没有抢到窗口宝地的年轻小姐们，开始推攘着、嬉笑着挤出门来，平时能够两个人并排走的门，这时看来狭窄得可笑。走在后面的、脾气暴躁的老人好不容易挪到街上，发昏的视线马上被前面一排排高举着孩子的小伙子们皱起的后衣遮住了，只看得他们满目怒火。

八尺宽的街道一瞬间变得水泄不通，低着头的蒟蒻如平时那般忽视着身周的邻居们——他所到之处，人群也不知是怎么消退的，自然就让出了一个刚够蒟蒻前进的身位。他一路骂骂咧咧：“这 Leetcode 有毒，写了三个差不多的算法，一个比一个慢！早知道随便写他一个就溜了，浪费这么多时间也不见个效果，我图个啥了。。。”

这时，一个孩子。。。

（啊，终于下课了，吃饭去了。。。不写了👋）

---

By [CDFMLR](https://clownote.github.io).

