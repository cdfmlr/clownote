---
date: 2020-02-27 08:56:29
tags: School
title: Leetcode P121 买卖股票的最佳时机
---

# Leetcode P121 买卖股票的最佳时机

TODO: 按照给定要领完成文中 TODO。

## 题目

给定一个数组，它的第 i 个元素是一支给定股票第 i 天的价格。

如果你最多只允许完成一笔交易（即买入和卖出一支股票），设计一个算法来计算你所能获取的最大利润。

注意你不能在买入股票前卖出股票。

示例 1:

输入: [7,1,5,3,6,4]
输出: 5
解释: 在第 2 天（股票价格 = 1）的时候买入，在第 5 天（股票价格 = 6）的时候卖出，最大利润 = 6-1 = 5 。
     注意利润不能是 7-1 = 6, 因为卖出价格需要大于买入价格。
示例 2:

输入: [7,6,4,3,1]
输出: 0
解释: 在这种情况下, 没有交易完成, 所以最大利润为 0。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

## 某种不知名的野生解法（也许是贪心？）

TODO：bullshit here。要领：总而言之就是遍历中更新最大值、最小值、极大值、极小值，最后输出最大值减最小值。

```go
func maxProfit(prices []int) int {
    if len(prices) <=1 {
        return 0
    }
    lowest := 0
    highest := 0
    l := prices[0]
    h := prices[0]
    for _, current := range prices {
        if current < l {
            l = current
            h = current
        }
        if current > h {
            h = current
            if h - l > highest - lowest {
                highest, lowest = h, l
            }
        }
    }
    return highest - lowest
}
```

![屏幕快照 2020-02-27 08.38.49](https://tva1.sinaimg.cn/large/0082zybpgy1gcanzsukqqj319s0u01kx.jpg)

这个算法只遍历一次数组，所以时间复杂度是 $O(n)$，空间消耗是常数，$O(1)$。

## 优化后的不知名的野生算法

TODO: bullshit +1。要领：pure bullshit。

这么做效率上区别不大，但代码简洁一些。

```go
func maxProfit(prices []int) int {
    if len(prices) <=1 {
        return 0
    }
    lowest := prices[0]
    bestProfit := 0
    for _, current := range prices {
        if current < lowest {
            lowest = current
        } else if current - lowest > bestProfit {
            bestProfit = current - lowest
        }
    }
    return bestProfit
}
```

![屏幕快照 2020-02-27 08.47.47](https://tva1.sinaimg.cn/large/0082zybpgy1gcao6m00isj319s0u01kx.jpg)

## 两行代码解法

因为它这个题有点恶心，会给个 `[]` 的测试数据，要判断是否为空，所以一行代码对这种特殊情况不好处理，要写两行。

```python
from functools import reduce
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        r = reduce(lambda x, y: (min(x[0], y[0]), max(y[0]-x[0],x[1])), [(i, 0) for i in prices])[1] if prices else 0
        return r
```

![image-20200227091010143](https://tva1.sinaimg.cn/large/0082zybpgy1gcaosnz1uyj319s0u01kx.jpg)

TODO: Final bullshit。要领：自己意会。