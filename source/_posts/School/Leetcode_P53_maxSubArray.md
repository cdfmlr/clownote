---
date: 2020-02-25 16:29:02
tags: School
title: Leetcode P53 最大子序和
---

# Leetcode P53 最大子序和

## 题目

给定一个整数数组 nums ，找到一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。

示例:

输入: [-2,1,-3,4,-1,2,1,-5,4],
输出: 6
解释: 连续子数组 [4,-1,2,1] 的和最大，为 6。
进阶:

如果你已经实现复杂度为 O(n) 的解法，尝试使用更为精妙的分治法求解。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/maximum-subarray
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

## 贪心

emmm，一看又是动规题。但我不（bu）爱（hui）写动规，每次写动规都要爆炸好久。。。先试试能不能贪心贪出来吧。

我们来考虑这样的贪心策略：

> 从头到尾遍历数组，在每一个元素 `i` 处，贪最大和。

也就是在每次迭代里，一个部分最大和要么是*前面的某一部分和* + *当前元素值*，要么是当前元素一个就比前面辛苦积累起来的和大了，那部分最大和就变成当前元素一个人的值了；之后，如果我们新得到的这个部分和比之前的全局的最优解还大，那么全局最优解就变成现在的这个部分和了。

用代码来表示，即当前部分最大和 `part = Max(part + nums[i], nums[i])`，以及全局最大和 `max = Max(max, part)`，这样我们每一步都保证 `part`、`max` 都是最优的，完成遍历就得到了全局最优解。

Golang 实现，首先为了突出贪心策略，我们实现一个辅助的 `MaxI()` 来返回两个 `int` 的最大值：

```go
// V1 (记住这些代码版本的标号呀。本文代码版本比较多，而且有相互比较)
func MaxI(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func maxSubArray(nums []int) int {
	part, max := nums[0], nums[0]
	for i := 1; i < len(nums); i++ {
		part = MaxI(nums[i], part + nums[i])
		max = MaxI(part, max)
	}
	return max
}
```

![屏幕快照 2020-02-25 15.15.03](https://tva1.sinaimg.cn/large/0082zybpgy1gc8om3s4ngj319q0u0hc0.jpg)

Nice，过了，难得有这种懒得动规拿贪心这么简单就贪到的题目。

再整理一下代码，去掉 `MaxI`，减少函数调用的消耗：

```go
// V2
func maxSubArray(nums []int) int {
	part, max := nums[0], nums[0]
	for i := 1; i < len(nums); i++ {
        part += nums[i]
        if nums[i] > part {
            part = nums[i]
        }
        if part > max {
            max = part
        }
	}
	return max
}
```

![屏幕快照 2020-02-25 15.17.46](https://tva1.sinaimg.cn/large/0082zybpgy1gc8om9mpytj319q0u01kx.jpg)

Emmm，不但没有优化，还更差了，不管了，这个是运气问题。

分析一下这个算法，时间上只遍历了一次数组，$O(n)$；空间上都是常量空间，$O(1)$。应该说这个算法还是不错的。

## 动规

虽然不喜欢，但还是要练习嘛，动规肝起。

建一个备忘录 `memo` 来记录各个可能的部分和，最后返回 `memo` 中最大的就好了。

这里“各个可能的部分和”，我们采取和刚才贪心类似的思路，记录每一个元素处的最大值。具体来说，我们可以采用这样的方法：看看备忘录 `memo` 中前面一个元素处的最大值如果这个值是负的了，那当前元素加上它肯定更小了，所以当前最大和就是当前元素本身；如果记录中前面的值是正的，那加上就更大了，所以我们务必把它加上。

继续 Golang 实现：（Golang 写服务和写题都是很舒服的😌）

```go
// V3
import "sort"

func maxSubArray(nums []int) int {
	memo := make([]int, len(nums))
	memo[0] = nums[0]
	for i := 1; i < len(nums); i++ {
		if memo[i-1] < 0 {
			memo[i] = nums[i]
		} else {
			memo[i] = memo[i-1] + nums[i]
		}
	}
	sort.Ints(memo)
	return memo[len(memo)-1]
}
```

![屏幕快照 2020-02-25 16.06.33](https://tva1.sinaimg.cn/large/0082zybpgy1gc8prg5j7dj319q0u01kx.jpg)

。。。我们这里用了一个标准库里的 `sort.Ints`，它的代码实现是个 quick sort。这居然没有影响速度，空间的影响倒是看出来了。

（其实这个动规也不难）

分析一下这个算法，时间主要是一个迭代（$n$）还有一个快排（$n\log n$），合起来是 $O(n\log n)$；空间上，写了一个 $n$ 的备忘录，$O(n)$。

其实这一个版本的代码里有好几个地方可以优化，第一这个快排完全是可以避免的，用之前贪心时的策略，用一个 `max` 取记录每一步后的全局最优解:

```go
// V4
func maxSubArray(nums []int) int {
	memo := make([]int, len(nums))
	memo[0] = nums[0]
	max := nums[0]
	for i := 1; i < len(nums); i++ {
		if memo[i-1] < 0 {
			memo[i] = nums[i]
		} else {
			memo[i] = memo[i-1] + nums[i]
		}
		if memo[i] > max {
			max = memo[i]
		}
	}
	return max
}
```

先不忙跑这个版本，还可以继续优化，再观察代码，我们自始至终只使用了 `memo[i-1]` 这一个记录值来更新下一个记录值 `memo[i]`，之前的所有记录都不会用到。既然如此，何不直接用一个 `int` 变量把之前的数组取代掉，空间就从 $O(n)$ 降到 $O(1)$ 了：

```go
// V5
func maxSubArray(nums []int) int {
	memo := nums[0]
	max := nums[0]
	for i := 1; i < len(nums); i++ {
		if memo < 0 {
			memo = nums[i]
		} else {
			memo += nums[i]
		}
		if memo > max {
			max = memo
		}
	}
	return max
}
```

![屏幕快照 2020-02-25 16.30.49](https://tva1.sinaimg.cn/large/0082zybpgy1gc8qbpo8axj319q0u01kx.jpg)

这个结果比较好，时间上比之前的所有版本都要快。

接下来再研究一下能不能搞出分治。，，嗯？？！！等一下！发现一个有意思的东西！

我们再来观察一下 `V5` 和 `V2` 这两个版本的代码，一个是优化后的贪心，一个是优化后的动规。为了方便观察，我们稍微修改一下代码表述（算法、大体框架都不动），然后把它们肩并肩比较一下：

![屏幕快照 2020-02-25 16.42.05](https://tva1.sinaimg.cn/large/0082zybpgy1gc8qmkxcpvj31yi0tm7bl.jpg)

我们会发现，这两个版本的大体框架是一样的，区别在于迭代里的处理。而且，这不一样的代码都是用来这一步当前的最大部分和的！稍微思考一下这两个方法，V5 里如果前面的记录是正的我们才加，负的就不加了；V2 里我们是先加上去试试看，如果加上去变小了就不加了。而我们知道由 $a + b < a$ 可以推出 $b < 0$。也就是说，我们的这两种处理在本质上是一样的！

哈，一个是优化后的贪心，一个是优化后的动规，从不同的思想出发，居然殊途同归！还是很有意思的。



## 分治

~~【16:46】：分治好难的，平时用的也不多，好多东西我都忘了。。。~~

~~【16:49】: 唉，早知不能回学校就应该把《算法导论》（还有我的琴23333）带回来的，看扫描版的 PDF 好难受啊。😭~~

~~【17:26】：啊，天呐，我发现我完全忘了，只会归并排序了（归并可能都不能完全流畅手写了），不想做了。~~

~~【17:39】：我直接看了题解。。。试着自己复述一遍吧。~~

---

用类似于二分法的思想啊，最大和子串的所有元素可能在这三个位置：

- 全在数组中心左边
- 跨过数组中心
- 全在数组中心右边

我们“分治“就是”分“这几种情况了。其中比较特殊的是跨中心的，跨中心的需要从中心左侧和中心右侧分别用贪心，求得跨中心的最大和。

而非跨中心的情况就分左右去递归嘛，把问题看成只有左边一半、右边一半分别求解。

我们的递归需要有基础情况，那这个问题中的基础情况就是递归到子串只是单独的一个元素了，那这个元素自己就是这个子序的最大子序了，直接返回它本身。而非基础情况的时候，也就是子串长度>1时，就像刚才说的那样递归下去，继续用上面讨论的三种情况找子串啊。

递归到头后，返回来时有点像棵树，比较兄弟（左半、右半、跨中 三种情况分别取得的最大和）的值，找到最大的往上返回......这样返回到头问题就解决了。

（好乱啊，没写代码，边思考边来写思路好怪，其实我还没完全搞懂这个算法是在干什么，不管了，来试一下代码实现，代码出来思路就清晰了。）

```go
// V6
func maxSubArray(nums []int) int {
	return getMaxSubArray(nums, 0, len(nums)-1)
}

func getMaxSubArray(nums []int, left, right int) int {
	if left == right {
		return nums[right]
	}

	center := (left + right) / 2
    
	leftSum := getMaxSubArray(nums, left, center)
	crossSum := getCrossSum(nums, left, center, right)
	rightSum := getMaxSubArray(nums, center+1, right)
    
	return maxI(leftSum, crossSum, rightSum)
}

func getCrossSum(nums []int, left, center, right int) int {
	if left == right {
		return nums[right]
	}

	leftSubMaxSum := nums[center]
	memo := 0
	for i := center; i >= left; i-- {
		memo += nums[i]
		if memo >= leftSubMaxSum {
			leftSubMaxSum = memo
		}
	}
	rightSubMaxSum := nums[center+1]
	memo = 0
	for i := center + 1; i <= right; i++ {
		memo += nums[i]
		if memo >= rightSubMaxSum {
			rightSubMaxSum = memo
		}
	}

	return leftSubMaxSum + rightSubMaxSum
}

func maxI(a, b, c int) int {
	switch {
	case a >= b && a >= c:
		return a
	case b >= a && b >= c:
		return b
	default:
		return c
	}
}
```

![屏幕快照 2020-02-25 22.38.51](https://tva1.sinaimg.cn/large/0082zybpgy1gc9110gn6pj319q0u01kx.jpg)

这样，分治法就过了，其实分治没有之前的那些算法快，这个分治是个 $O(n\log n)$，递归调用也会比较耗时，还有空间消耗也会比较大，因为开递归栈要了 $O(\log n)$，但整个问题解决的比较精妙，代码很漂亮。

P.S. 我前面写的思路不太清楚，所以补一张图来说明这个算法是在干什么（我思考的时候随手画的，不一定正确，仅供参考）：

![image-20200225230422143](https://tva1.sinaimg.cn/large/0082zybpgy1gc91o1k64ij30u00yegro.jpg)

## 暴力

再补一个暴力解法吧，把这道题主要的几种方法都写全。

暴力法就是把所有的可能子序都搞出来，比较它们的和，返回最大的。

Golang 实现：

```go
// V7
func maxSubArray(nums []int) int {
	maxSubSum := nums[0]
	for l := 0; l < len(nums); l++ {
		part := 0
		for r := l; r < len(nums); r++ {
			part += nums[r]
			if part > maxSubSum {
				maxSubSum = part
			}
		}
	}
	return maxSubSum
}
```

![屏幕快照 2020-02-26 08.37.10](https://tva1.sinaimg.cn/large/0082zybpgy1gc9ibdwblmj319q0u04qg.jpg)

## 一行代码的解法

按照传统，我还是尽力想出一个使用最短代码行数的解法。

我们首先来看一个两行代码的 Python3 解法：（不算`import`）。

```python
# V8
from functools import reduce
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        nums[0] = (nums[0], nums[0])
        return reduce(lambda x, y: (max(x[0]+y, y), max(x[1], x[0]+y, y)), nums)[1]
```

其实这就是我们的贪心/动规解法嘛，只是利用了 reduce 来在一行代码里完成所有操作（另一行代码为这一行代码做了必要的准备），我挺喜欢这个解法的，还是很优雅的。

![屏幕快照 2020-02-26 09.21.26](https://tva1.sinaimg.cn/large/0082zybpgy1gc9jkwzn71j319q0u04pc.jpg)

再来把代码减少到一行：

```python
# V9
from functools import reduce
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        return reduce(lambda x, y: (max(x[0]+y[0], y[0]), max(x[1], x[0]+y[0], y[0])), [(i, i) for i in nums])[1]
```

为了完成一行代码的任务，我们用了一个生成器生成了好多无用的数据，造成了时间、空间的浪费，结果就不太好了：

![image-20200226094257065](https://tva1.sinaimg.cn/large/0082zybpgy1gc9k4h6ab8j31d90u01kx.jpg)

## 最后的废话

这一道题，我们写出来 9 个版本的代码，还是很有意思的，从贪心、动规到分治，最后居然还用一行代码解决了它！不同的思考角度出发，我们写出过几乎相同的代码；用相同的思想去实现，我们又写出了不同的程序......这或许就是编程的魅力吧。我不喜欢编程，但编程的这种魅力深深地吸引着我，为我指引着未来或许没有希望的方向。