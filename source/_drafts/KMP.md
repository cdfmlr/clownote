---
date: 2021-07-15 00:16:30.071187
title: KMP
---
# KMP

## 部分匹配表

参考 [Wikipedia](https://en.wikipedia.org/wiki/Knuth–Morris–Pratt_algorithm) 的算法（看英文页，中文页没写全，有些段落缺失）。

**手算**：

```go
func GetNext(substr: string) []int {  // substr: [0…M-1]
    M := len(substr)
    next := make([]int, M)

    next[0] = -1
    for j := 1; j <= M; j++ {
        next[j] = len(
            最长公共前后缀(substr[0:j])  // 就是 j 那个字符之前的
        )
    }

    return next
}
```

**编程**快速计算：

```go
func GetNext(substr string) []int {
	next := make([]int, len(substr))
	next[0] = -1

	i, j := 0, -1
	for i < len(substr)-1 {
		if j == -1 || substr[i] == substr[j] {
			i++
			j++
			next[i] = j
		} else {
			j = next[j]
		}
	}
	return next
}
```

## 匹配

KMP：

```go
func KMP(s string, substr string) int {
	next := GetNext(substr)

	i, j := 0, 0
	for i < len(s) && j < len(substr) {
		if j == -1 || s[i] == substr[j] {
			i++
			j++
		} else { // miss matching
			j = next[j]
		}
	}

	if j >= len(substr) { // matched
		return i - len(substr)
	}
	return -1 // not matched
}
```

这个程序是真的可以运行的：

```go
package main

// ...

func main() {
	s := "BBC ABCDAB ABCDABCDABDE"
	sub := "ABCDABD"

	res := KMP(s, sub)
	println(res)
}
```

## next 数组

补充一点：部分匹配表，还有几种不同的版本，比如《算法导论》上的，再比如我们的考研书（天勤王道）上的。

（考研书上把部分匹配表亲切地称为 “**next 数组**”。。。）

这几种的区别看下面这个例子：

| index     | 0    | 1    | 2    | 3    | 4    | 5    | 6    |                             |
| --------- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | --------------------------- |
| char      | a    | b    | a    | b    | a    | c    | a    |                             |
| CLRS      | 0    | 0    | 1    | 2    | 3    | 0    | 1    |                             |
| Wikipedia | -1   | 0    | 0    | 1    | 2    | 3    | 0    | = CLRS 右移一个，左边补`-1` |
| 天勤王道  | 0    | 1    | 1    | 2    | 3    | 4    | 1    | = Wikipedia + 1             |

若在原串（大的）索引 `i` 处、模式（子串）索引 `j` 处失配：

- CLRS 移动到 `T[j-1]` 上（特殊情况：`j=0` 则 `i+=1`）
- Wikipedia 移到 `T[j]` 上（特殊情况：`j=-1` 则 `j+=1`）。

## 更好理解的代码

说实话，我看不懂上面给的代码。主要是这段 `if (j==-1 || s[i] == substr[j]) {...}` WTF？？

研究了好久才看懂明明就是两种不同的情况，只是凑巧处理方式一样就合并在一起，，搁这儿写汇编呢。。吐了。

参考 [如何更好地理解和掌握 KMP 算法? - 阮行止的回答 - 知乎](https://www.zhihu.com/question/21923021/answer/1032665486) 把这两种情况分开写就容易理解多了：

```go
func GetNext(substr string) []int {
	next := make([]int, len(substr))
	next[0] = -1

	i, j := 0, -1
	for i < len(substr)-1 {
        if j == -1 { // 特殊: 到头了: 最小了，无可再缩
			i++
			j = 0
			next[i] = j
		} else if substr[i] == substr[j] { // 配上了：扩大一位
			i++
			j++
			next[i] = j
		} else { // 失配：缩小，重新匹配
			j = next[j]
		}
	}
	return next
}

func KMP(s string, substr string) int {
	next := GetNext(substr)

	i, j := 0, 0 // i 是 s 的，j 是 substr 的
	for i < len(s) && j < len(substr) {
        if j == -1 { // 特殊: 回到头了: i 移一个，j 从头比较
			i++
			j = 0
		} else if s[i] == substr[j] { // 配上了: 下一个字符
			i++
			j++
		} else { // 失配: j 移到下一个可能匹配的位置
			j = next[j]
		}
	}

	if j >= len(substr) { // matched
		return i - len(substr)
	}
	return -1 // not matched
}
```



# 改进 KMP

改进个🔨，睡了。
