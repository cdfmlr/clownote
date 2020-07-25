---
date: 2020-02-26 17:35:37
tags: School
title: Leetcode P88 合并两个有序数组
---

# Leetcode P88 合并两个有序数组

## 题目

给定两个有序整数数组 nums1 和 nums2，将 nums2 合并到 nums1 中，使得 num1 成为一个有序数组。

说明:

初始化 nums1 和 nums2 的元素数量分别为 m 和 n。
你可以假设 nums1 有足够的空间（空间大小大于或等于 m + n）来保存 nums2 中的元素。
示例:

输入:
nums1 = [1,2,3,0,0,0], m = 3
nums2 = [2,5,6],       n = 3

输出: [1,2,2,3,5,6]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/merge-sorted-array
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

## 一行代码解法

这道题好简单的啊，如果是在现实中遇到，我肯定直接一行代码上了：

Python3 实现：

```python
class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        nums1[:] = sorted(nums1[0:m] + nums2[0:n])
```

![屏幕快照 2020-02-26 16.32.16](https://tva1.sinaimg.cn/large/0082zybpgy1gc9w4t8dazj31d90u0hch.jpg)

直接搞了个排序居然还击败了 96% 😂 问题是 python 的 sorted 实现是什么？好像没研究过噢👀

我去搜了一下，python 的 document 里面好像没写，懒得查源码了，大佬们说那个是 Timsort，是个结合了合并排序（merge sort）和插入排序（insertion sort）而得出的排序算法。。。

好吧，这就超出咱的认知范围了，有时间再研究了。我们还是接着写这道题的正经解法吧。

## 归并

刚才的那个 merge sort 给了我们足够完成这道题的启示啊，这道题要干的就是归并排序里做的那种归并！

算法的思路大概是这样：由于两个数组都已经排好序了，那么要合成一个数组，就是不断比较两个数组的头部，看哪个头部元素比较小就把它拿到目标数组里的下一个位置。

e.g. 

```
step1: t=[],            n1=[1,2,3],  n2=[2,5,6] # 1比2小，把1移到t里
step2: t=[1],           n1=[2,3],    n2=[2,5,6] # 2和2一样大啊，随便放一个
step3: t=[1,2],         n1=[3],      n2=[2,5,6] # 2比3小，放2
step4: t=[1,2,2],       n1=[3],      n2=[5,6]   # 3比5小，放3
step5: t=[1,2,2,3],     n1=[],       n2=[5,6]   # n1空了，放n2的
step6: t=[1,2,2,3,5],   n1=[],       n2=[6]     # n1空了，放n2的
step6: t=[1,2,2,3,5,6], n1=[],       n2=[]      # 完成
```

这里怎么判断空，有很多种方法，我比较喜欢的一种方法是：在两个数组的末尾都放上一个超级大的元素，要保证它们比所有数据元素都大，这样的话，随便和谁比较，小的都不可能是它们，所以只要规定好目标数组的长度，它们就不会被加到最后的目标数组里。而且这么做还避免了写判断语句，判断在每一次迭代里都要执行，时间消耗很可能大于我们添加大数所用的常数时间。

Golang 实现：

```go
func merge(nums1 []int, m int, nums2 []int, n int)  {
    nums1Copy := make([]int, m+1)
    copy(nums1Copy, nums1)
    nums1Copy[m] = math.MaxInt32
    nums2 = append(nums2, math.MaxInt32)
    i, j := 0, 0
    for k := 0; k < m + n; k++ {
        if nums1Copy[i] <= nums2[j] {
            nums1[k] = nums1Copy[i]
            i++
        } else {
            nums1[k] = nums2[j]
            j++
        }
    }
}
```

![屏幕快照 2020-02-26 17.15.34](https://tva1.sinaimg.cn/large/0082zybpgy1gc9x8pno43j31ag0u07w5.jpg)

分析一下这个算法：时间复杂度 : $O(n+m)$，空间复杂度 : $O(m)$。

## 逆序归并

在刚才的归并解法中，我们可以观察到，在一开始（迭代之前），需要拷贝 `nums1` 的有效数据部分，这一步会消耗时间、空间；而 `nums1` 后面却有着大量的空白空间没有很好的利用起来。

我们来考虑是否可以把后面的空间利用起来，同时避免数据的拷贝。

事实上，如果我们**从大到小**逆序去完成归并，就可以达成这两个目的。

在逆序的归并中，我们依次把两个有序数组中的**较大者**，**从尾到头**放入目标数组。这样，`nums1` 后面的空白空间就利用起来了，同时，我们还不用拷贝 `nums1` 的数据部分了（因为题目保证了 `nums1` 的尾部可以放下整个 `nums2`，也就不可能出现数据被覆盖的情况了）。

Golang 实现：

```go
func merge(nums1 []int, m int, nums2 []int, n int)  {
    i, j := m-1, n-1
    for k := m+n-1; k >= 0; k-- {
        if i < 0 {
            nums1[k] = nums2[j]
            j--
            continue
        }
        if j < 0 {
            nums1[k] = nums1[i]
            i--
            continue
        }
        if nums1[i] >= nums2[j] {
            nums1[k] = nums1[i]
            i--
        } else {
            nums1[k] = nums2[j]
            j--
        }
    }
}
```

这里用到了另外一种判断数组是否已经到空的方法。

来看看运行结果：

![屏幕快照 2020-02-26 21.43.46](https://tva1.sinaimg.cn/large/0082zybpgy1gca528ctr9j31ag0u01kx.jpg)

在空间上明显有了很大的进步，时间上看不出来区别。事实上，这个算法时间复杂度依然是 $O(n+m)$。空间复杂度降到了 $O(1)$。

---

其实，我感觉还可以写的更好一点，但我做了大量的尝试（都是自己感觉可以了，然后提交上去就 runtime error😂）最后发现根本没有提升，最后通过的这个版本的代码巨丑就不放到这里污染环境了。。。

![image-20200226225852251](https://tva1.sinaimg.cn/large/0082zybpgy1gca74mcylkj30ru0gmjtn.jpg)