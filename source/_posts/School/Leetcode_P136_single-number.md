---
date: 2020-04-08 14:57:55
tags: School
title: Leetcode 136. 只出现一次的数字
---

# Leetcode [136. 只出现一次的数字](https://leetcode-cn.com/problems/single-number/)

## 题目

给定一个非空整数数组，除了某个元素只出现一次以外，其余每个元素均出现两次。找出那个只出现了一次的元素。

说明：

你的算法应该具有线性时间复杂度。 你可以不使用额外空间来实现吗？

示例 1:

```
输入: [2,2,1]
输出: 1
```


示例 2:

```
输入: [4,1,2,1,2]
输出: 4
```

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/single-number
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

## 哈希表

这道题最简单的方法，哈希表暴力存一下出现次数就好了。由于题目保证最多有出现两次，所以用个bool去存出现次数就行了，Golang 实现：

```go
func singleNumber(nums []int) int {
    memo := make(map[int]bool)
    for _, v := range nums {
        memo[v] = !memo[v]
    } 
    for k, v := range memo {
        if v {
            return k
        }
    }
    return 0
}
```

## 异或

按位异或（C风格写做 `^`）有很多有趣的性质，这道题可以用其中的一两个：

1. `x ^ x = 0`
2. `0 ^ x = x`

其实这两个性质还是很显然的：

```
  100110
^ 100110
--------
  000000
  
  
  000000
^ 100110
--------
  100110
```

这两个性质合在一起就有：

```
a ^ a ^ b ^ b ^ ... ^ z = z
// 省略的那里也是一对一对的，只有z是单独一个
```

这道题就解决了。

Golang 实现：

```go
func singleNumber(nums []int) int {
    x := 0
    for _, v := range nums {
        x ^= v
    }
    return x
}
```

![image-20200408150554908](https://tva1.sinaimg.cn/large/00831rSTgy1gdmdhgx8xwj317x0u04qd.jpg)

