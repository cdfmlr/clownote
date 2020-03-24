---
title: Leetcode P20 有效的括号
tags: School
---



# Leetcode [20. 有效的括号](https://leetcode-cn.com/problems/valid-parentheses/)

给定一个只包括 `'('`，`')'`，`'{'`，`'}'`，`'['`，`']'` 的字符串，判断字符串是否有效。

有效字符串需满足：

1. 左括号必须用相同类型的右括号闭合。
2. 左括号必须以正确的顺序闭合。

注意空字符串可被认为是有效字符串。

**示例 1:**

```
输入: "()"
输出: true
```

**示例 2:**

```
输入: "()[]{}"
输出: true
```

**示例 3:**

```
输入: "(]"
输出: false
```

**示例 4:**

```
输入: "([)]"
输出: false
```

**示例 5:**

```
输入: "{[]}"
输出: true
```

## 思路

括号不匹配的情况很多，但匹配的情况就3种：`()`，`[]`，`{}`。

以前刚学算法的时候看过一个大佬写的暴力解法，他把不匹配的情况的情况穷举出来了！他那个跑的飞快，但巨复杂。

我脑子没那么好，写不出他那个来。所以我选择老老实实用栈。我的思路很直接，遇到前括号就入栈，遇到后括号就出栈。如果每一步都匹配，且最后栈为空，就匹配成功。这个思路和人去判断是一致的。

## 实现

```python
class Solution:
    def isValid(self, s: str) -> bool:
        match = {')': '(', ']': '[', '}': '{'}
        stack = []
        for i in s:
            if i in match.values():
                stack.append(i)
            else:
                if len(stack) == 0:
                    return False
                front = stack.pop()
                if match.get(i) != front:
                    return False

        return (len(stack) == 0)
```



![image-20200324080539922](https://tva1.sinaimg.cn/large/00831rSTgy1gd4p1lylnsj31r90u0dk8.jpg)

其实这代码是我以前刚学的时候写的了，所以很慢。。。