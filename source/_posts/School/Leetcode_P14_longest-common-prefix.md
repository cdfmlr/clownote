---
date: 2020-03-31 09:37:05
tags: School
title: Leetcode 14. 最长公共前缀
---



# Leetcode [14. 最长公共前缀](https://leetcode-cn.com/problems/longest-common-prefix/)

## 题目

编写一个函数来查找字符串数组中的最长公共前缀。

如果不存在公共前缀，返回空字符串 ""。

示例 1:

```
输入: ["flower","flow","flight"]
输出: "fl"
```

示例 2:

```
输入: ["dog","racecar","car"]
输出: ""
解释: 输入不存在公共前缀。
```

说明:

所有输入只包含小写字母 a-z 。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/longest-common-prefix
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

## 暴力遍历法

这个方法的思路是这样：

例如，处理题例 `strs = ["flower","flow","flight"]`:

第一轮：

1. 从 `strs[0]` 即~~第0个~~第一个元素 `"flower"` 取出第一个字符 `"f"`
2. 遍历 `strs`，若有元素没有前缀 `"f"`，则最长公共前缀为 `""`

第二轮：

1. 从 `strs[0]` 即~~第0个~~第一个元素 `"flower"` 取出前两个字符 `"fl"`
2. 遍历 `strs`，若有元素没有前缀 `"fl"`，则最长公共前缀为 `"f"`

第三轮：

1. 从 `strs[0]` 即~~第0个~~第一个元素 `"flower"` 再取出前三个字符，得到 `"flo"`
2. 遍历 `strs`，若有元素没有前缀 `"flo"`，则最长公共前缀为 `"fl"`

......

Golang 实现：

```go
import (
    "strings"
)

func longestCommonPrefix(strs []string) string {
    if len(strs) == 0 {
        return ""
    }
    i := 0
    for ; i < len(strs[0]); i++ {
        for j := 1; j < len(strs); j++ {
            if !strings.HasPrefix(strs[j], strs[0][:i+1]) {
                return strs[0][:i]
            }
        }
    }
    return strs[0][:i]
}
```

![屏幕快照 2020-03-31 08.28.51](https://tva1.sinaimg.cn/large/00831rSTgy1gdct2u0iynj31930u04pt.jpg)

感觉还有好多种暴力遍历的方法，随便怎么都出得来，但好像效率都差不多？大概是 $O(\sum_{i=0}^{len(strs)}len(strs[i]))$？

## 分治法

我想用分治来写这个，感觉会比较有意思。

其实就是一个递归，用二分法“分”问题，分到最后基础情况就是只剩一个元素直接返回；然后“合”就是求二分左右递归各自返回来的两个串的最长公共前缀：

![image-20200331093206511](https://tva1.sinaimg.cn/large/00831rSTgy1gdcuvnmzffj31sz0u0gqr.jpg)

（我疯了，居然用 XMind 画这个。。。）

代码实现，Golang：

```go
import (
    "strings"
)

func longestCommonPrefix(strs []string) string {
    if len(strs) == 0 {
        return ""
    }
    return partLongestCommonPrefix(strs)
}

func partLongestCommonPrefix(strs []string) string {
    if len(strs) <= 1 {
        return strs[0]
    } else {
        m := len(strs) / 2
        l := partLongestCommonPrefix(strs[: m])
        r := partLongestCommonPrefix(strs[m :])
        return fuzzbuzz(l, r)
    }
}

/**
 * fuzzbuzz 是一个函数，用来返回两个字符串的最长公共前缀
 * 用这个函数来举反例，以此呼吁大家认真命名、取有意义的名字！
 */
func fuzzbuzz(foo, bar string) string {
    fuzz := len(foo)
    if len(bar) < fuzz {
        fuzz = len(bar)
    }
    buzz := 0
    for ; buzz < fuzz; buzz++ {
        if foo[buzz] != bar[buzz] {
            return foo[: buzz]
        }
    }
    return foo[: buzz]
}
```

其实这个时间复杂度和刚才那个暴力法差不多，而空间占用还更多了：

![image-20200331091205895](https://tva1.sinaimg.cn/large/00831rSTgy1gdcuauj2g2j31930u01kx.jpg)

