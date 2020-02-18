---
title: Leetcode P1 两数之和
tags: School
---

# 两数之和

Emmmm，写一篇学校作业。

> 给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那 两个 整数，并返回他们的数组下标。
>
> 你可以假设每种输入只会对应一个答案。但是，你不能重复利用这个数组中同样的元素。
>
> 示例:
>
> ```
> 给定 nums = [2, 7, 11, 15], target = 9
> 
> 因为 nums[0] + nums[1] = 2 + 7 = 9
> 所以返回 [0, 1]
> ```
>
> 来源：力扣（LeetCode）
> 链接：https://leetcode-cn.com/problems/two-sum
> 著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

## 暴力求解

这是 Leetcode 的第一题，最简单的题，其实没什么好写的，最简单的方法，暴力求解直接上，遍历两次数组，找到就返回。

曾经写的 C++ 代码（我刚开始刷题的时候写的）：

```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        for (int i = 0; i < nums.size(); i++) {
            for (int j = i+1; j < nums.size(); j++) {
                if (nums[i] + nums[j] == target) {
                    vector<int> result({i, j});
                    return result;
                }
            }
        }
        return vector<int>();
    }
};
```

时间 $O(n^2)$，空间 $O(1)$。通过用了 200ms，9.2MB。时间上只战胜了29.63%。。。

Emmmm，毕竟是很长时间之前写的了，不能责备过去的自己，但是这个成绩实在看不下去了，重新写一个吧。

## 哈希表

稍微考虑一下上面的暴力解法，我们做了这样的一件事：遍历数组，找有没有和当前元素对应的补，找到就返回当前元素和他的补的索引，没找到就继续。

内部的那个循环就是用来找 `nums` 中有没有一个 `nums[i]` 的补，即等于 `target - nums[i]` 的元素。

既然是要从一堆东西里快速找一个明确的，那就上哈希表嘛。空间复杂度加个 $n$，换来时间上减个 $n$，就这个问题来说还行吧。

Golang 实现：

```go
func twoSum(nums []int, target int) []int {
    numsMap := make(map[int]int)
    for i := 0; i < len(nums); i++ {
        cmpl := target - nums[i]
        if v, ok := numsMap[cmpl]; ok {
            return []int{v, i}
        }
        numsMap[nums[i]] = i
    }
    return []int{-1, -1}
}
```

这个就勉强看得过去了，时间 $O(n)$，空间 $O(n)$。通过用了 4ms、3.8MB。时间上战胜了 96.76%、空间是 44.82%，，，还行。

## 后话

哈，看了一眼官方题解，我这刚好是第一个方法和最后一个方法。

其实我写哈希表的时候差点写成了官方题解的*方法二*，先构建一张完整的表再找符合的两数，后来发现它这个题目说：

> 每种输入只会对应一个答案。但是，你不能重复利用这个数组中同样的元素。

先构建一张表出来我跑了一下执行会有重复😂，key已经有了的时候，会更新值嘛，碰到输入 `[1, 1, 1], target=2`，这种就会返回 `[2, 2]`，炸了。

要避免这个问题，可以像题解里方法二那种。但还可以更好，就有点类似与动规那种感觉嘛，放一个 for 里迭代，有了返回，没有再更新表就好了——实现就是上面写的第二版本代码。

