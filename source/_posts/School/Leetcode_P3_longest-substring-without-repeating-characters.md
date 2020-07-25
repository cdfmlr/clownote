---
date: 2020-04-07 08:12:39
tags: School
title: Leetcode 3. 无重复字符的最长子串
---

# Leetcode [3. 无重复字符的最长子串](https://leetcode-cn.com/problems/longest-substring-without-repeating-characters/)

## 题目

给定一个字符串，请你找出其中不含有重复字符的 最长子串 的长度。

示例 1:

```
输入: "abcabcbb"
输出: 3 
解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。
```


示例 2:

```
输入: "bbbbb"
输出: 1
解释: 因为无重复字符的最长子串是 "b"，所以其长度为 1。
```


示例 3:

```
输入: "pwwkew"
输出: 3
解释: 因为无重复字符的最长子串是 "wke"，所以其长度为 3。
```


​     请注意，你的答案必须是 子串 的长度，"pwke" 是一个子序列，不是子串。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/longest-substring-without-repeating-characters
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

## 可能是滑窗的解法

（这道题我去年写的了，大概看了一下，还可以，就不重新写 了）

其实就是像人一样去找，这个算法还是很直接暴力的，C语言实现：

```c
int lengthOfLongestSubstring(char * s){
    char *pmhead = s;
    char *pmtail = s;
    int max = 0;
    
    char c = *s;
    int i = 0;
    char *pc;
    
    int j;
    
    while (c = s[i++], c != '\0') {
        j = pmtail - pmhead;
        pc = memchr(pmhead, c, j);
        if (pc != NULL) {
            if (j > max) {
                max = j;
            }
            pmhead = pc + 1;
        }
        pmtail++;
    }
    
    if (pmtail - pmhead > max) {
        max = pmtail - pmhead;
    }
    
    return max;
}

```

![image-20200407080959808](https://tva1.sinaimg.cn/large/00831rSTgy1gdkvuf8tzaj31l10u0dkk.jpg)

