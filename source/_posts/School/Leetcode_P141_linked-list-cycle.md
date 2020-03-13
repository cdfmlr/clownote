---
title: Leetcode P141 环形链表
tags: School
---



# Leetcode P141 环形链表

## 题目

给定一个链表，判断链表中是否有环。

为了表示给定链表中的环，我们使用整数 pos 来表示链表尾连接到链表中的位置（索引从 0 开始）。 如果 pos 是 -1，则在该链表中没有环。 

示例 1：

```
输入：head = [3,2,0,-4], pos = 1
输出：true
解释：链表中有一个环，其尾部连接到第二个节点。
```


示例 2：

```
输入：head = [1,2], pos = 0
输出：true
解释：链表中有一个环，其尾部连接到第一个节点。
```


示例 3：

```
输入：head = [1], pos = -1
输出：false
解释：链表中没有环。
```


进阶：

你能用 O(1)（即，常量）内存解决此问题吗？

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/linked-list-cycle
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

## 哈希表法

首先，最简单直接的想法，用哈希表，遍历一个存一个，每次都检查当前节点是否已经存过，存过就说明有环：

```go
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func hasCycle(head *ListNode) bool {
    for nodes := map[*ListNode]bool{}; head != nil; head = head.Next {
        if (nodes[head] == true) {
            return true
        } else {
            nodes[head] = true
        }
    }
    return false
}
```

![屏幕快照 2020-03-12 15.33.08](https://tva1.sinaimg.cn/large/00831rSTgy1gcr749hdvdj31d60u01kx.jpg)

## 快慢指针法

还可以用快慢指针法。

想象这样的情景：两人比赛跑步，甲快，乙慢。如果赛道无环，相当于就一条直线，肯定是甲先到终点；如果赛道有环，在环上跑，速度不一样的甲乙必然在某一时刻相遇。

利用这个思路，赛道是链表，甲乙化身快慢指针，就得到了空间消耗 $O(1)$ 的解法：

```go
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func hasCycle(head *ListNode) bool {
    if (head == nil) || (head.Next == nil) {
        return false
    }

    slow, fast := head, head.Next

    for slow != fast {
        if fast == nil || fast.Next == nil {
            return false
        }
        fast, slow = fast.Next.Next, slow.Next
    }
    return true
}
```

![image-20200312155153189](https://tva1.sinaimg.cn/large/00831rSTgy1gcr730im9jj31d60u01kx.jpg)

---

## 题外话

总有人问我每天写代码快乐吗？图个啥呀？

今天看书的时候，看到一段很有感触的话，算是对这个问题的回答吧，收藏了：

> There is much joy in programming. There is joy in analyzing a problem, breaking it down into pieces, formulating a solution, mapping out a strategy, approaching it from different directions, and crafting the code. There is very much joy in seeing the program run for the first time, and then more joy in eagerly diving back into the code to make it better and faster.
>
> There is also often joy in hunting down bugs, in ensuring that the program runs smoothly and predictably. Few occasions are quite as joyful as finally identifying a particularly recalcitrant bug and defin- itively stamping it out.
>
> There is even joy in realizing that the original approach you took is not quite the best. Many developers discover that they’ve learned a lot while writing a program, including that there’s a better way to structure the code. Sometimes, a partial or even a total rewrite can result in a much better application, or simply one that is structurally more coherent and easier to maintain. The process is like standing on one’s own shoulders, and there is much joy in attaining that perspective and knowledge.
>
> ---
>
> ​	From *Creating Mobile Apps with Xamarin*
>
> ​			Chapter 1 *How does Xamarin.Forms fit in?*

哈哈，伟人站在巨人肩膀上随和微笑，蒟蒻站在自己肩膀上看着代码傻笑。

