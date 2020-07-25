---
date: 2020-03-10 20:33:52
tags: School
title: Leetcode P21 合并两个有序链表
---

# Leetcode P21 合并两个有序链表

## 题目

将两个有序链表合并为一个新的有序链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的。 

示例：

```
输入：1->2->4, 1->3->4
输出：1->1->2->3->4->4
```

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/merge-two-sorted-lists
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

## 直观解法

首先我们尝试用归并的方法，和我们做 [Leetcode P88](https://blog.csdn.net/u012419550/article/details/104527464) 的方法一样，只是把数组换成链表。

Golang 实现：

```go
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func mergeTwoLists(l1 *ListNode, l2 *ListNode) *ListNode {
    if l1 == nil && l2 == nil {
        return nil
    }
    merged := &ListNode{}
    head := merged
    for (l1 != nil) || (l2 != nil) {
        if l1 == nil {
            merged.Val = l2.Val
            l2 = l2.Next
            goto NEXT_MERGED
        }
        if l2 == nil {
            merged.Val = l1.Val
            l1 = l1.Next
            goto NEXT_MERGED
        }
        if l1.Val <= l2.Val {
            merged.Val = l1.Val
            l1 = l1.Next
        } else {
            merged.Val = l2.Val
            l2 = l2.Next
        }
NEXT_MERGED:
        if (l1 != nil) || (l2 != nil) {
            merged.Next = &ListNode{}
            merged = merged.Next
        }
    }
    return head
}
```

别介意我的 `goto`，都说不要用 goto，但我觉得用在这里就挺好！你写个正常的条件跳转，变成汇编的时候不还是个 goto 么......

![屏幕快照 2020-03-10 20.09.22](https://tva1.sinaimg.cn/large/00831rSTgy1gcp3ipsv29j31d60u0e7r.jpg)

## 优化

Woc，我刚才傻了，居然不停的 new 出 ` &ListNode{}` 来，直接用原来的节点不就好了么，难怪刚才那么高空间占用。。。

优化一下：

```go
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func mergeTwoLists(l1 *ListNode, l2 *ListNode) *ListNode {
    if l1 == nil && l2 == nil {
        return nil
    }
    merged := &ListNode{}
    head := merged
    for (l1 != nil) || (l2 != nil) {
        if l1 == nil {
            merged.Next = l2
            l2 = l2.Next
            goto NEXT_MERGED
        }
        if l2 == nil {
            merged.Next = l1
            l1 = l1.Next
            goto NEXT_MERGED
        }
        if l1.Val <= l2.Val {
            merged.Next = l1
            l1 = l1.Next
        } else {
            merged.Next = l2
            l2 = l2.Next
        }
NEXT_MERGED:
        if (l1 != nil) || (l2 != nil) {
            merged = merged.Next
        }
    }
    return head.Next
}
```

![image-20200310202641869](https://tva1.sinaimg.cn/large/00831rSTgy1gcp3saqmlbj31d60u01kx.jpg)

......

好吧，这 Leetcode 就这样，经常是你去优化一下代码还更慢了😂

## 再优化

其实，还可以再优化一点，如果一条链为空了，那直接把另一条链接到合并后的链上就好了，不用再迭代着一个一个节点地接。

```go
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func mergeTwoLists(l1 *ListNode, l2 *ListNode) *ListNode {
    if l1 == nil && l2 == nil {
        return nil
    }
    merged := &ListNode{}
    head := merged
    for (l1 != nil) && (l2 != nil) {
        if l1.Val <= l2.Val {
            merged.Next = l1
            l1 = l1.Next
        } else {
            merged.Next = l2
            l2 = l2.Next
        }
        merged = merged.Next
    }
    if l1 == nil {
        merged.Next = l2
    }
    if l2 == nil {
        merged.Next = l1
    }
    return head.Next
}
```

![image-20200310203129875](https://tva1.sinaimg.cn/large/00831rSTgy1gcp3xaldorj31d60u01kx.jpg)

差不多就这样了吧🤷‍♂️