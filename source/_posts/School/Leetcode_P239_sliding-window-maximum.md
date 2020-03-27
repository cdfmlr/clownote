---
title: Leetcode 239. 滑动窗口最大值
tags: School
---



# Leetcode [239. 滑动窗口最大值](https://leetcode-cn.com/problems/sliding-window-maximum/)

## 题目

给定一个数组 *nums*，有一个大小为 *k* 的滑动窗口从数组的最左侧移动到数组的最右侧。你只可以看到在滑动窗口内的 *k* 个数字。滑动窗口每次只向右移动一位。

返回滑动窗口中的最大值。

**进阶：**

你能在线性时间复杂度内解决此题吗？

**示例:**

```
输入: nums = [1,3,-1,-3,5,3,6,7], 和 k = 3
输出: [3,3,5,5,6,7] 
解释: 

  滑动窗口的位置                最大值
---------------               -----
[1  3  -1] -3  5  3  6  7       3
 1 [3  -1  -3] 5  3  6  7       3
 1  3 [-1  -3  5] 3  6  7       5
 1  3  -1 [-3  5  3] 6  7       5
 1  3  -1  -3 [5  3  6] 7       6
 1  3  -1  -3  5 [3  6  7]      7
```

**提示：**

- `1 <= nums.length <= 10^5`
- `-10^4 <= nums[i] <= 10^4`
- `1 <= k <= nums.length`



## 双向队列法

我们可以维护一个一个**双向队列**，在里面维护存在于**当前窗口中的**逐步最大值索引 ，每一步右端压入当前索引、清除比当前小的值的索引。从 k 处开始，每次取左端值即当前滑窗的最大值。

```go
func maxSlidingWindow(nums []int, k int) []int {
    if len(nums) < k || k <= 1 {
        return nums
    }

    memo := make([]int, 0)
    var e int

    swMax := make([]int, 1)
    swMax[0] = nums[0]

    for i := 0; i < k; i++ {
        for e = len(memo); e > 0 && nums[i] > nums[memo[e-1]]; e-- {
            continue
        }
        memo = memo[:e]
        memo = append(memo, i)
        if nums[i] > swMax[0] {
            swMax[0] = nums[i]
        }
    }
    // fmt.Println(memo)

    for i := k; i < len(nums); i++ {
        // leaving
        if len(memo) != 0 && memo[0] == i - k {
            memo = memo[1:]
        }
        // entering
        for e = len(memo); e > 0 && nums[i] > nums[memo[e-1]]; e-- {
            continue
        }
        memo = memo[:e]
        memo = append(memo, i)
        // ans
        swMax = append(swMax, nums[memo[0]])
    }
    return swMax
}

```

