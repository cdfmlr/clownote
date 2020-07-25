---
date: 2020-02-20 11:58:00
tags: School
title: Leetcode P27 移除元素
---

# Leetcode P27 移除元素

还是作业题，leetcode 简单题+1。

## 题目

给定一个数组 nums 和一个值 val，你需要原地移除所有数值等于 val 的元素，返回移除后数组的新长度。

不要使用额外的数组空间，你必须在原地修改输入数组并在使用 O(1) 额外空间的条件下完成。

元素的顺序可以改变。你不需要考虑数组中超出新长度后面的元素。

示例 1:

```
给定 nums = [3,2,2,3], val = 3,

函数应该返回新的长度 2, 并且 nums 中的前两个元素均为 2。

你不需要考虑数组中超出新长度后面的元素。
```

示例 2:

```
给定 nums = [0,1,2,2,3,0,4,2], val = 2,

函数应该返回新的长度 5, 并且 nums 中的前五个元素为 0, 1, 3, 0, 4。

注意这五个元素可为任意顺序。

你不需要考虑数组中超出新长度后面的元素。
```

说明:

为什么返回数值是整数，但输出的答案是数组呢?

请注意，输入数组是以“引用”方式传递的，这意味着在函数里修改输入数组对于调用者是可见的。

你可以想象内部操作如下:


```c
// nums 是以“引用”方式传递的。也就是说，不对实参作任何拷贝
int len = removeElement(nums, val);

// 在函数里修改输入数组对于调用者是可见的。
// 根据你的函数返回的长度, 它会打印出数组中该长度范围内的所有元素。
for (int i = 0; i < len; i++) {
    print(nums[i]);
}
```

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/remove-element
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

## 双指针法

emmmm，这个题基本和昨天做的 [leetcode P26 删除排序数组中的重复项](https://leetcode-cn.com/problems/remove-duplicates-from-sorted-array/) 一模一样，直接套用那个题的方法就好了，具体算法见昨上一篇文章。

双指针法，Golang 实现：

```go
func removeElement(nums []int, val int) int {
    if len(nums) == 0 {
        return 0
    }
    t := -1
    for i := 0; i < len(nums); i++ {
        if nums[i] != val {
            t++
            nums[t] = nums[i]
        }
    }
    return t + 1
}
```

![屏幕快照 2020-02-20 10.57.43](https://tva1.sinaimg.cn/large/0082zybpgy1gc2olfvu1uj30mc05kmxz.jpg)

好的，0ms、2.1MB，击败 100%、99.78%，已经是最优了。

但看了一下题解，还有其他方法，学习了：

## 双指针 —— 动态数组长度

这个优化的思路是这样啊，因为从数组里移除特定的元素，这个元素一般比较少嘛，但我们需要为此完整遍历整个数组，不太划算。

既然题目不要求排序，所以我们考虑不把待删除的用下一个不相等的覆盖，而是用数组末尾元素覆盖，这样就不用遍历到原来最后一个哪里了，相当于把元素后面的不确定是否要删的提到前面来、把明确要删的扔到后面。这样就相当于干掉了一个长度，减少了一次迭代嘛。

Golang 实现：

```go
func removeElement(nums []int, val int) int {
    l := len(nums)
    if l == 0 {
        return 0
    }
    for i := 0; i < l; {
        if nums[i] == val {
            nums[i] = nums[l - 1]
            l--
        } else {
            i++
        }
    }
    return l
}
```

这个的结果和我们的上一个版本也差不多，~~内存排名还下去了一些~~。

![image-20200220111518525](https://tva1.sinaimg.cn/large/0082zybpgy1gc2p2ppnccj30lk05ct9i.jpg)

## 一行代码解法

既然优化不了了，就试点好玩的嘛，这个问题也有只用一行代码的解法。

方法是利用函数式编程的 `filter` 来把等于要删除的那个值的元素直接全部过滤掉。

Python3 实现：

```python
class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        nums[:] = filter(lambda x: x != val, nums)
```

![image-20200220115019134](https://tva1.sinaimg.cn/large/0082zybpgy1gc2q35ak4nj30ni056aaw.jpg)

当然，在 Python 中，还有另一种写法，用列表生成器完成过滤：

```python
class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        nums[:] = [x for x in nums if x != val]
```

![image-20200220144948410](https://tva1.sinaimg.cn/large/0082zybpgy1gc2v9wfloqj30nq05egmh.jpg)

