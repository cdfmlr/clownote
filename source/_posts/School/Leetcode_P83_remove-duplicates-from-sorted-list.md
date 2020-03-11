---
title: Leetcode P83 删除排序链表中的重复元素
tags: School
---

# Leetcode P83 删除排序链表中的重复元素

## 题目

给定一个排序链表，删除所有重复的元素，使得每个元素只出现一次。

示例 1:

```
输入: 1->1->2
输出: 1->2
```


示例 2:

```
输入: 1->1->2->3->3
输出: 1->2->3
```

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/remove-duplicates-from-sorted-list
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

## 双指针法

这道题还是很容易的，双指针法，和 [Leetcode P26 删除排序数组中的重复项](https://blog.csdn.net/u012419550/article/details/104402182) 一样的算法，只是把数组改成链表（甚至我还觉得更简单了？）

就搞两个指针 `current` 和 `toDel`，`current` 遍历链表，维护 `toDel` 前的节点值不重复。直接上代码吧，Golang：

```go
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func deleteDuplicates(head *ListNode) *ListNode {
    current := head
    toDel := head
    for current != nil {
        if current.Val != toDel.Val {
            toDel.Next = current
            toDel = current
        }
        current = current.Next
    }
    if toDel != nil && toDel.Next != nil && toDel.Next.Val == toDel.Val {
        toDel.Next = nil
    }
    return head
}
```

![屏幕快照 2020-03-11 16.36.36](https://tva1.sinaimg.cn/large/00831rSTgy1gcq2u4ysbpj31d60u0e7f.jpg)

## 优化：单指针

这个题还可以只用一个指针完成，因为链表是用指针指下一个的嘛，我们可以方便地把任意节点的下一节点改成其后的某一节点，来达到“删除”中间的一些节点的目的。比如`current.Next = current.Next.Next`，就相当于把 `current.Next` 删除了。

用这个思路就可以用一个指针把链表中的重复元素删除：

```go
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func deleteDuplicates(head *ListNode) *ListNode {
    current := head
    for (current != nil) && (current.Next != nil) {
        if current.Next.Val == current.Val {
            current.Next = current.Next.Next
        } else {
            current = current.Next
        }
    }
    return head
}
```

![image-20200311170330484](https://tva1.sinaimg.cn/large/00831rSTgy1gcq3j6dznqj31d60u04qp.jpg)

哈哈，一开始我没写 else 分句，`current = current.Next` 写在外面，这么做是错的，如果输入是 `[1,1,1,1]`，就会输出 `[1,1]`，少了尾部最后的处理。然后我改这个的时候顺手把 for 条件里的 `current != nil` 也删了，但他有 `[]` 的输入，又错了一次🤦‍♂️