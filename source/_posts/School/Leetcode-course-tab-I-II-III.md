---
title: Leetcode 课程表 I、II、III
tags: School
---



# Leetcode 课程表 I、II、III

这篇文章介绍 Leetcode 的课程表 I、II、III 三道题目的解法。

[TOC]

本文由 CDFMLR 原创，收录于个人主页 https://clownote.github.io。

## [207. 课程表](https://leetcode-cn.com/problems/course-schedule/)

### 题目

你这个学期必须选修 numCourse 门课程，记为 0 到 numCourse-1 。

在选修某些课程之前需要一些先修课程。 例如，想要学习课程 0 ，你需要先完成课程 1 ，我们用一个匹配来表示他们：[0,1]

给定课程总量以及它们的先决条件，请你判断是否可能完成所有课程的学习？

示例 1:

```
输入: 2, [[1,0]] 
输出: true
解释: 总共有 2 门课程。学习课程 1 之前，你需要完成课程 0。所以这是可能的。
```


示例 2:

```
输入: 2, [[1,0],[0,1]]
输出: false
解释: 总共有 2 门课程。学习课程 1 之前，你需要先完成课程 0；并且学习课程 0 之前，你还应先完成课程 1。这是不可能的。
```


提示：

1. 输入的先决条件是由 **边缘列表** 表示的图形，而不是 邻接矩阵 。详情请参见[图的表示法](http://blog.csdn.net/woaidapaopao/article/details/51732947)。
2. 你可以假定输入的先决条件中没有重复的边。
3. `1 <= numCourses <= 10^5`

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/course-schedule
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

### DFS

这个东西要可以学就是要图里没有环。有环就“循环依赖”，没法学了。所以解法就是深度优先去搜索有没有环，有就不行，没有就行。

```go
func canFinish(numCourses int, prerequisites [][]int) bool {
    adj := make([][]int, numCourses)
    for _, p := range prerequisites {
        adj[p[1]] = append(adj[p[1]], p[0])
    }

    for i := 0; i < numCourses; i++ {
        if hasCycle(i, adj, make([]bool, numCourses)) {
            return false
        }
    }
    return true
}

func hasCycle(node int, adj [][]int, visited []bool) bool {
    visited[node] = true
    for _, a := range adj[node] {
        if visited[a] || hasCycle(a, adj, visited) {
            return true
        }
    }
    visited[node] = false
    return false
}

```

![执行通过的截图，图片上显示执行用时44ms在所有 Go 提交中击败了14.12%的用户，内存消耗6.7MB在所有 Go 提交中击败了100%的用户](https://tva1.sinaimg.cn/large/007S8ZIlgy1gepo6jel4dj30qe05ymxv.jpg)

## [210. 课程表 II](https://leetcode-cn.com/problems/course-schedule-ii/)

### 题目

现在你总共有 n 门课需要选，记为 0 到 n-1。

在选修某些课程之前需要一些先修课程。 例如，想要学习课程 0 ，你需要先完成课程 1 ，我们用一个匹配来表示他们: [0,1]

给定课程总量以及它们的先决条件，返回你为了学完所有课程所安排的学习顺序。

可能会有多个正确的顺序，你只要返回一种就可以了。如果不可能完成所有课程，返回一个空数组。

示例 1:

```
输入: 2, [[1,0]] 
输出: [0,1]
解释: 总共有 2 门课程。要学习课程 1，你需要先完成课程 0。因此，正确的课程顺序为 [0,1] 。
```


示例 2:

```
输入: 4, [[1,0],[2,0],[3,1],[3,2]]
输出: [0,1,2,3] or [0,2,1,3]
解释: 总共有 4 门课程。要学习课程 3，你应该先完成课程 1 和课程 2。并且课程 1 和课程 2 都应该排在课程 0 之后。
     因此，一个正确的课程顺序是 [0,1,2,3] 。另一个正确的排序是 [0,2,1,3] 。
```

**说明**:

输入的先决条件是由边缘列表表示的图形，而不是邻接矩阵。详情请参见图的表示法。
你可以假定输入的先决条件中没有重复的边。

**提示**:

1. 这个问题相当于查找一个循环是否存在于有向图中。如果存在循环，则不存在拓扑排序，因此不可能选取所有课程进行学习。
2. 通过 DFS 进行拓扑排序 - 一个关于Coursera的精彩视频教程（21分钟），介绍拓扑排序的基本概念。
3. 拓扑排序也可以通过 BFS 完成。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/course-schedule-ii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

### 拓扑排序

这个题就是做拓扑排序，但拓扑排序只能用于 DAG (有向无环图) ！所以我们直接把上面那个题目的 hasCycle 抄过来判断是否有环，有环就返回一个空序列就好了，没环就拿去拓扑排序。

```go
func findOrder(numCourses int, prerequisites [][]int) []int {
    adj := make([][]int, numCourses)
    for _, p := range prerequisites {
        adj[p[1]] = append(adj[p[1]], p[0])
    }

    visited :=  make([]bool, numCourses)
    ret := make([]int, 0)

    for i := 0; i < numCourses; i++ {
        if hasCycle(i, adj, make([]bool, numCourses)) {
            return []int{}
        }
        dfsForTopoSort(i, adj, visited, &ret)
    }
    if len(ret) < numCourses {
        return []int{}
    }
    reverse(ret)
    return ret
}

func hasCycle(node int, adj [][]int, visited []bool) bool {
    visited[node] = true
    for _, a := range adj[node] {
        if visited[a] || hasCycle(a, adj, visited) {
            return true
        }
    }
    visited[node] = false
    return false
}

func dfsForTopoSort(node int, adj [][]int, visited []bool, ret *[]int) {
    if !visited[node] {
        visited[node] = true

        for _, a := range adj[node] {
            if !visited[a] {
                dfsForTopoSort(a, adj, visited, ret)
            }
        }
        
        *ret = append(*ret, node)
    }
}

func reverse(a []int) {
    for left, right := 0, len(a)-1; left < right; left, right = left+1, right-1 {
        a[left], a[right] = a[right], a[left]
    }
}

```

这个很好理解，也可以通过，但判断环 + 拓扑排序跑了两遍嘛，最后还做了一个切片翻转，所以比较慢。

![Leetcode 执行结果截图，执行用时 40 ms, 在所有 Go 提交中击败了11.81%的用户; 内存消耗 6.8 MB, 在所有 Go 提交中击败了100.00%的用户](https://tva1.sinaimg.cn/large/007S8ZIlgy1geproy8i5cj30o805maar.jpg)



## [630. 课程表 III](https://leetcode-cn.com/problems/course-schedule-iii/)

### 题目

这里有 n 门不同的在线课程，他们按从 1 到 n 编号。每一门课程有一定的持续上课时间（课程时间）t 以及关闭时间第 d 天。一门课要持续学习 t 天直到第 d 天时要完成，你将会从第 1 天开始。

给出 n 个在线课程用 (t, d) 对表示。你的任务是找出最多可以修几门课。

示例：

```
输入: [[100, 200], [200, 1300], [1000, 1250], [2000, 3200]]
输出: 3
解释: 
这里一共有 4 门课程, 但是你最多可以修 3 门:
首先, 修第一门课时, 它要耗费 100 天，你会在第 100 天完成, 在第 101 天准备下门课。
第二, 修第三门课时, 它会耗费 1000 天，所以你将在第 1100 天的时候完成它, 以及在第 1101 天开始准备下门课程。
第三, 修第二门课时, 它会耗时 200 天，所以你将会在第 1300 天时完成它。
第四门课现在不能修，因为你将会在第 3300 天完成它，这已经超出了关闭日期。
```


提示:

1. 整数 1 <= d, t, n <= 10,000 。
2. 你不能同时修两门课程。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/course-schedule-iii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

### 贪心优先队列

哇，这个题的贪心策略还是很6⃣️的，思路写起来比较麻烦，[官方题解](https://leetcode-cn.com/problems/course-schedule-iii/solution/ke-cheng-biao-iii-by-leetcode/) 写的很好了，直接照着它那个，其实基本的代码很简单的：

```go
// 伪代码
func scheduleCourse(courses [][]int) int {
	sort(&courses)

	queue := PriorityQueue{}
	time := 0
	for _, c := range courses {
		if time + c[0] <= c[1] {
			queue.Push(c[0])
			time += c[0]
		} else if !queue.IsEmpty() && queue.Top() > c[0] {
			time += c[0] - queue.Poll()
			queue.Push(c[0])
		}
	}

	return queue.Size()
}
```

问题是，这里面需要 sort 和 PriorityQueue。Python、Java、甚至 C++ 写这个都还是比较方便的，直接用标准库里的实现。但 Golang，，，标准库的这两个东西有点诡异，用起来没那么方便。

所以，我们先试试自己实现**排序**和**优先队列**，练习一下，也当是追忆以前写 C 时那种啥都自己写的时光。

#### 快速排序

优先队列一般我们使用堆去实现，但这里为了方便，我们直接维护一个切片，每次插入元素的时候排个序也就“优先队列”了。

我们先写一个快速排序，让 courses 的排序和优先队列都基于这个快排。

由于 courses 是 `[][]int`，优先队列是 `[]int`，我们写一种通用的——对 `[]interface{}` 的快排，这个代码还是很传统的：

```go
func quick_sort(pA *([]interface{}), p int, r int, le func(a, b interface{}) bool) {
	if p >= r {
		return
	}
	q := partition(pA, p, r, le)
	quick_sort(pA, p, q-1, le)
	quick_sort(pA, q+1, r, le)
}

func partition(pA *([]interface{}), p int, r int, le func(a, b interface{}) bool) int {
	A := (*pA)

	q := p
	for u := p; u < r; u++ {
		if le(A[u], A[r]) {
			A[q], A[u] = A[u], A[q]
			q++
		}
	}
	A[q], A[r] = A[r], A[q]
	return q
}
```

然后把它封装一层，分别提供`[][]int`、`[]int` 的排序接口，其实这两个代码基本是一样的：

```go
func quick_sort_sint(pA *([]int), p int, r int, le func(a, b interface{}) bool) {
	var interfaceSlice []interface{} = make([]interface{}, len(*pA))
	for i, d := range *pA {
		interfaceSlice[i] = d
	}
	quick_sort(&interfaceSlice, p, r, le)
	for i, v := range interfaceSlice {
		(*pA)[i] = v.(int)
	}
}

func quick_sort_ssint(pA *([][]int), p int, r int, le func(a, b interface{}) bool) {
	var interfaceSlice []interface{} = make([]interface{}, len(*pA))
	for i, d := range *pA {
		interfaceSlice[i] = d
	}
	quick_sort(&interfaceSlice, p, r, le)
	for i, v := range interfaceSlice {
		(*pA)[i] = v.([]int)
	}
}
```

写好了排序，再看优先队列，实现基本的入、出、顶、大小、空判断就好：

```go
type PriorityQueue struct {
	data []int
}

func (q *PriorityQueue) top() int {
	return q.data[0]
}

func (q *PriorityQueue) push(element int) {
	q.data = append(q.data, element)
	quick_sort_sint(&q.data, 0, len(q.data)-1, func (a, b interface{}) bool {
		return b.(int) <= a.(int)
	})
}

func (q *PriorityQueue) poll() int {
	r := q.data[0]
	q.data = q.data[1:]
	return r
}

func (q *PriorityQueue) isEmpty() bool {
	return len(q.data) == 0
}

func (q *PriorityQueue) size() int {
	return len(q.data)
}
```

合到一起，就有解了：

```go
func scheduleCourse(courses [][]int) int {
	quick_sort_ssint(&courses, 0, len(courses)-1,
		func(a, b interface{}) bool {
			return a.([]int)[1] <= b.([]int)[1]
		},
	)

	queue := PriorityQueue{}
	time := 0
	for _, c := range courses {
		if time + c[0] <= c[1] {
			queue.push(c[0])
			time += c[0]
		} else if !queue.isEmpty() && queue.top() > c[0] {
			time += c[0] - queue.poll()
			queue.push(c[0])
		}
	}

	return queue.size()
}

/** 优先队列 **/

type PriorityQueue struct {
	data []int
}

func (q *PriorityQueue) top() int {
	return q.data[0]
}

func (q *PriorityQueue) push(element int) {
	q.data = append(q.data, element)
	quick_sort_sint(&q.data, 0, len(q.data)-1, func (a, b interface{}) bool {
		return b.(int) <= a.(int)
	})
}

func (q *PriorityQueue) poll() int {
	r := q.data[0]
	q.data = q.data[1:]
	return r
}

func (q *PriorityQueue) isEmpty() bool {
	return len(q.data) == 0
}

func (q *PriorityQueue) size() int {
	return len(q.data)
}

/** 把对 []int 的快排转化为对 []interface{} 的快排  **/

func quick_sort_sint(pA *([]int), p int, r int, le func(a, b interface{}) bool) {
	var interfaceSlice []interface{} = make([]interface{}, len(*pA))
	for i, d := range *pA {
		interfaceSlice[i] = d
	}
	quick_sort(&interfaceSlice, p, r, le)
	for i, v := range interfaceSlice {
		(*pA)[i] = v.(int)
	}
}

/** 把对 [][]int 的快排转化为对 []interface{} 的快排  **/

func quick_sort_ssint(pA *([][]int), p int, r int, le func(a, b interface{}) bool) {
	var interfaceSlice []interface{} = make([]interface{}, len(*pA))
	for i, d := range *pA {
		interfaceSlice[i] = d
	}
	quick_sort(&interfaceSlice, p, r, le)
	for i, v := range interfaceSlice {
		(*pA)[i] = v.([]int)
	}
}

/** 对 []interface{} 的快排  **/

func quick_sort(pA *([]interface{}), p int, r int, le func(a, b interface{}) bool) {
	if p >= r {
		return
	}
	q := partition(pA, p, r, le)
	quick_sort(pA, p, q-1, le)
	quick_sort(pA, q+1, r, le)
}

func partition(pA *([]interface{}), p int, r int, le func(a, b interface{}) bool) int {
	A := (*pA)

	q := p
	for u := p; u < r; u++ {
		if le(A[u], A[r]) {
			A[q], A[u] = A[u], A[q]
			q++
		}
	}
	A[q], A[r] = A[r], A[q]
	return q
}

```

这个版本算法是正确的，但提交运行会超时！

`clown0te（防{盗[文()爬]虫}的追踪标签，读者不必在意）`

#### 插入排序 + 归并排序

我们的程序里大量的排序，这个也是最主要的时间消耗，而刚才简单粗暴的全用了快排，这肯定不是最好的，考虑在这方面优化一下：

1. `PriorityQueue.Push` 数据基本有序，对基本有序的数据用快排肯定慢（所以我们有时候用快排要先把数据打乱），我们把这里改成对基本有序的数据最快的——插入排序。
2. `courses` 的排序，既然不需要重复使用快排我们就可以把之前的 `interface{}` 封装去掉，直接实现一个对 `[][]int` 的排序（我还把快排改成了归并排序，只是为了好玩）

先写最简单的插入排序：

```go
func insertSortReverse(pA *[]int) {
	A := *pA
	for i := 1; i < len(A); i++ {
		key := A[i]
		j := i - 1
		for j >= 0 && A[j] < key {
			A[j+1] = A[j]
			j -= 1
		}
		A[j+1] = key
	}
}
```

然后，归并排序，这个代码也不是很难：

```go
var INF = []int{99999999, 99999999}

func merge(pA *[][]int, p, q, r int, le func (a, b []int) bool) {
	// n1 := q - p + 1
	// n2 := r - q
	// b, c := make([][]int, n1+1), make([][]int, n2+1)
	A := *pA

	b := append(make([][]int, 0), A[p: q+1]...)
	c := append(make([][]int, 0), A[q+1: r+1]...)

	b = append(b, INF)
	c = append(c, INF)
	i, j := 0, 0
	for k := p; k <= r; k++ {
		if le(b[i], c[j]) {
			A[k] = b[i]
			i++
		} else {
			A[k] = c[j]
			j++
		}
	}
}

func mergeSort(pA *[][]int, p int, r int, le func (a, b []int) bool) {
	if p >= r {
		return
	}
	q := (p + r) / 2
	mergeSort(pA, p, q, le)
	mergeSort(pA, q+1, r, le)
	merge(pA, p, q, r, le)
}
```

这个代码写的时候要注意一点，b 和 c 这里，不能直接这样：

```go
b := append(A[p: q+1], INF)
c := append(A[q+1: r+1], INF)
```

原因是，**切片和底层数组**。你构建 b 的时候往里面 append 了一个 INF，实际上是底层数组的`A[q+1]` 位置变成了 INF，所以再构建 c 的时候，切片 `A[q+1: r+1]` 的值就成了 `[INF, ...]`，然后归并就爆炸了💥。

把代码合一下：

```go
func scheduleCourse(courses [][]int) int {
	mergeSort(&courses, 0, len(courses)-1, func (a, b []int) bool {
		return a[1] <= b[1]
	})

	queue := PriorityQueue{}
	time := 0
	for _, c := range courses {
		if time + c[0] <= c[1] {
			queue.Push(c[0])
			time += c[0]
		} else if !queue.IsEmpty() && queue.Top() > c[0] {
			time += c[0] - queue.Poll()
			queue.Push(c[0])
		}
	}

	return queue.Size()
}

/** 优先队列 **/

type PriorityQueue struct {
	data []int
}

func (q *PriorityQueue) Top() int {
	return q.data[0]
}

func (q *PriorityQueue) Push(element int) {
	q.data = append(q.data, element)
	insertSortReverse(&q.data)
}

func (q *PriorityQueue) Poll() int {
	r := q.data[0]
	q.data = q.data[1:]
	return r
}

func (q *PriorityQueue) IsEmpty() bool {
	return len(q.data) == 0
}

func (q *PriorityQueue) Size() int {
	return len(q.data)
}

/**  对 []int 的插入排序**/

func insertSortReverse(pA *[]int) {
	A := *pA
	for i := 1; i < len(A); i++ {
		key := A[i]
		j := i - 1
		for j >= 0 && A[j] < key {
			A[j+1] = A[j]
			j -= 1
		}
		A[j+1] = key
	}
}

/** 对 [][]int 的归并排序 **/

var INF = []int{99999999, 99999999}

func merge(pA *[][]int, p, q, r int, le func (a, b []int) bool) {
	// n1 := q - p + 1
	// n2 := r - q
	// b, c := make([][]int, n1+1), make([][]int, n2+1)
	A := *pA

	b := append(make([][]int, 0), A[p: q+1]...)
	c := append(make([][]int, 0), A[q+1: r+1]...)

	b = append(b, INF)
	c = append(c, INF)
	i, j := 0, 0
	for k := p; k <= r; k++ {
		if le(b[i], c[j]) {
			A[k] = b[i]
			i++
		} else {
			A[k] = c[j]
			j++
		}
	}
}

func mergeSort(pA *[][]int, p int, r int, le func (a, b []int) bool) {
	if p >= r {
		return
	}
	q := (p + r) / 2
	mergeSort(pA, p, q, le)
	mergeSort(pA, q+1, r, le)
	merge(pA, p, q, r, le)
}

```

这一个版本就可以通过了：

![Leetcode 执行结果截图，执行用时 580 ms, 在所有 Go 提交中击败了50.00%的用户;内存消耗 8.1 MB, 在所有 Go 提交中击败了100.00%的用户](https://tva1.sinaimg.cn/large/007S8ZIlgy1geq2tnkgy4j30p605yjs3.jpg)

#### 标准库 sort + heap

Go 的标准库还是很强大的，但是标准库的设计相当的 Golang，才从其他语言转过来用着真的很不习惯（比如 math 包里连 Max 都没有），不过多用用这些东西、多看看它们的源码（Go 标准库的好多源码写的挺有意思的），对理解 Go 的思想很有帮助。

我们用到的两个东西，排序和优先队列，Go 标准库里其实都有可用的：

- 排序：`sort` 包
- 优先队列：`container/heap` 包，Go 没有直接的优先队列，但我们可以用堆来快速实现一个。

首先看排序：

> **Package sort**
>
> Package sort provides primitives for sorting slices and user-defined collections.

`sort` 包里已经封装好了很多我们常用的排序情况，比如，对整数切片 `[]int` 的排序：

```go
package main

import (
	"fmt"
	"sort"
)

func main() {
	s := []int{5, 2, 6, 3, 1, 4} // unsorted
	sort.Ints(s)
	fmt.Println(s)	// [1 2 3 4 5 6]
}

```

这种用起来很方便，但我们现在要排一个 `[][]int` 这就不太常规了。对这种非常规东西的排序，go 提供的方式和其他语言有一些区别。

大多数语言，对这种非常规东西的排序，我们是把一个可迭代对象传进去，然后给他一个函数，告诉它比较的结果。例如，这是 C++ STL 的用法：

```cpp
bool myfunction (int i,int j) { return (i<j); }
int main () {
	int myints[] = {32,71,12,45,26,80,53,33};
  	std::vector<int> myvector (myints, myints+8);	// 32 71 12 45 26 80 53 33
    // using function as comp
	std::sort (myvector.begin()+4, myvector.end(), myfunction);	// 12 32 45 71(26 33 53 80)
}
```

Go 语言里也有这种用法，它提供了一个`sort.Slice` 对任意切片进行排序，比如这是一个文档里的例子：

```go
package main

import (
	"fmt"
	"sort"
)

func main() {
	people := []struct {
		Name string
		Age  int
	}{
		{"Gopher", 7},
		{"Alice", 55},
		{"Vera", 24},
		{"Bob", 75},
	}
	sort.Slice(people, func(i, j int) bool { return people[i].Name < people[j].Name })
	fmt.Println("By name:", people) // By name: [{Alice 55} {Bob 75} {Gopher 7} {Vera 24}]

	sort.Slice(people, func(i, j int) bool { return people[i].Age < people[j].Age })
	fmt.Println("By age:", people) // By age: [{Gopher 7} {Vera 24} {Alice 55} {Bob 75}]
}

```

到这里对 `[][]int` 排序的需求可以解决了，but we do need one more thing.

Go 还提供了一种更加 Go 风格的排序：`sort.Sort`。

> `func Sort(data Interface)`
>
> Sort sorts data. It makes one call to data.Len to determine n, and O(n*log(n)) calls to data.Less and data.Swap. The sort is not guaranteed to be stable.

这玩意儿是传一个 `sort.Interface` 的实现进来，这真的很 Golang！

```go
type Interface interface {
    // Len is the number of elements in the collection.
    Len() int
    // Less reports whether the element with
    // index i should sort before the element with index j.
    Less(i, j int) bool
    // Swap swaps the elements with indexes i and j.
    Swap(i, j int)
}

```

长度、大小、交换的方法都由你来定。其实一般用起来还是很简单的，Len、Swap基本就这样，一般要改的只有 Less（只改Less，其实也差不多就是 sort.Slice，但内部实现还是有所区别的）：

```go
package main

import (
	"fmt"
	"sort"
)

type Person struct {
	Name string
	Age  int
}

func (p Person) String() string {
	return fmt.Sprintf("%s: %d", p.Name, p.Age)
}

// ByAge implements sort.Interface for []Person based on
// the Age field.
type ByAge []Person

func (a ByAge) Len() int           { return len(a) }
func (a ByAge) Swap(i, j int)      { a[i], a[j] = a[j], a[i] }
func (a ByAge) Less(i, j int) bool { return a[i].Age < a[j].Age }

func main() {
	people := []Person{
		{"Bob", 31},
		{"John", 42},
		{"Michael", 17},
		{"Jenny", 26},
	}
	fmt.Println(people)

	sort.Sort(ByAge(people))
	fmt.Println(people)

}

```

排序的问题解决了，再看优先队列：

> Package container/heap
>
> Package heap provides heap operations for any type that implements heap.Interface. A heap is a tree with the property that each node is the minimum-valued node in its subtree.
>
> The minimum element in the tree is the root, at index 0.
>
> A heap is a common way to implement a priority queue. To build a priority queue, implement the Heap interface with the (negative) priority as the ordering for the Less method, so Push adds items while Pop removes the highest-priority item from the queue. The Examples include such an implementation; the file example_pq_test.go has the complete source.

优先队列可以用堆来实现，实现一个堆要实现 heap.Interface，你可以看到，这个接口是“继承”了 sort.Interface 的，这也是为什么我们刚才要介绍它的原因：

```go
type Interface interface {
    sort.Interface
    Push(x interface{}) // add x as element Len()
    Pop() interface{}   // remove and return element Len() - 1.
}

```

具体要怎么做，其实 Go 的文档里给出了些优先队列的例子了：

```go
// This example demonstrates a priority queue built using the heap interface.
package main

import (
	"container/heap"
	"fmt"
)

// An Item is something we manage in a priority queue.
type Item struct {
	value    string // The value of the item; arbitrary.
	priority int    // The priority of the item in the queue.
	// The index is needed by update and is maintained by the heap.Interface methods.
	index int // The index of the item in the heap.
}

// A PriorityQueue implements heap.Interface and holds Items.
type PriorityQueue []*Item

func (pq PriorityQueue) Len() int { return len(pq) }

func (pq PriorityQueue) Less(i, j int) bool {
	// We want Pop to give us the highest, not lowest, priority so we use greater than here.
	return pq[i].priority > pq[j].priority
}

func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
	pq[i].index = i
	pq[j].index = j
}

func (pq *PriorityQueue) Push(x interface{}) {
	n := len(*pq)
	item := x.(*Item)
	item.index = n
	*pq = append(*pq, item)
}

func (pq *PriorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	item := old[n-1]
	old[n-1] = nil  // avoid memory leak
	item.index = -1 // for safety
	*pq = old[0 : n-1]
	return item
}

// update modifies the priority and value of an Item in the queue.
func (pq *PriorityQueue) update(item *Item, value string, priority int) {
	item.value = value
	item.priority = priority
	heap.Fix(pq, item.index)
}

// This example creates a PriorityQueue with some items, adds and manipulates an item,
// and then removes the items in priority order.
func main() {
	// Some items and their priorities.
	items := map[string]int{
		"banana": 3, "apple": 2, "pear": 4,
	}

	// Create a priority queue, put the items in it, and
	// establish the priority queue (heap) invariants.
	pq := make(PriorityQueue, len(items))
	i := 0
	for value, priority := range items {
		pq[i] = &Item{
			value:    value,
			priority: priority,
			index:    i,
		}
		i++
	}
	heap.Init(&pq)

	// Insert a new item and then modify its priority.
	item := &Item{
		value:    "orange",
		priority: 1,
	}
	heap.Push(&pq, item)
	pq.update(item, item.value, 5)

	// Take the items out; they arrive in decreasing priority order.
	for pq.Len() > 0 {
		item := heap.Pop(&pq).(*Item)
		fmt.Printf("%.2d:%s ", item.priority, item.value)
	}
}

```

真正用起来没有这么难，它这个是比较一般的情况了。我们这里需要的只是一个简单的基于 `[]int` 的堆，可以简化很多的。

用库就比较简单，直接写全部的代码了：

```go
import (
	"sort"
	"container/heap"
)

func scheduleCourse(courses [][]int) int {
	sort.Slice(courses, func (i, j int) bool {return courses[i][1] < courses[j][1]})
	
	queue := &PriorityQueue{}
	time := 0
	for _, c := range courses {
		if time + c[0] <= c[1] {
			heap.Push(queue, c[0])
			time += c[0]
		} else if queue.Len() != 0 && queue.Top() > c[0] {
			time += c[0] - heap.Pop(queue).(int)
			heap.Push(queue, c[0])
		}
	}
	return queue.Len()
}

type PriorityQueue []int

func (q PriorityQueue) Len() int {
	return len(q)
}

func (q PriorityQueue) Swap(a, b int) {
	q[a], q[b] = q[b], q[a]
}

func (q PriorityQueue) Less(a, b int) bool {
	return q[a] > q[b]
}

func (q PriorityQueue) Top() int {
	return q[0]
}

func (q *PriorityQueue) Push(x interface{}) {
	*q = append(*q, x.(int))
}

func (q *PriorityQueue) Pop() interface{} {
	v := (*q)[q.Len()-1]
	*q = (*q)[: q.Len()-1]
	return v
}

```

在 scheduleCourse 里调用 PriorityQueue 时要注意，我们使用的必须是 `heap.Push` 和 `heap.Pop`，不能去调用自己写的那个 `queue.Push/Pop`，heap.Push、Pop 才能保证堆的正确性。

这个可以通过，执行用时 152 ms（击败87.5%），内存消耗：7.3 MB。还有人写的比这快？

我看了一下 sort.Slice 源码，它用了些反射（reflectlite）😂，所以比 sort.Sort 慢（sort.Sort没有反射），那些写的更快的人都是用  sort.Sort ：

```go
import (
	"sort"
	"container/heap"
)

func scheduleCourse(courses [][]int) int {
	var coursesSoted SS4Sort = courses
	sort.Sort(coursesSoted)
	
	queue := &PriorityQueue{}
	time := 0
	for _, c := range coursesSoted {
		if time + c[0] <= c[1] {
			heap.Push(queue, c[0])
			time += c[0]
		} else if queue.Len() != 0 && queue.Top() > c[0] {
			time += c[0] - heap.Pop(queue).(int)
			heap.Push(queue, c[0])
		}
	}
	return queue.Len()
}

/** 对 [][]int 排序的接口 **/

type SS4Sort [][]int

func (s SS4Sort) Len() int {
	return len(s)
}

func (s SS4Sort) Swap(a, b int) {
	s[a], s[b] = s[b], s[a]
}

func (s SS4Sort) Less(a, b int) bool {
	return s[a][1] < s[b][1]
}

/** 优先队列 **/

type PriorityQueue []int

func (q PriorityQueue) Len() int {
	return len(q)
}

func (q PriorityQueue) Swap(a, b int) {
	q[a], q[b] = q[b], q[a]
}

func (q PriorityQueue) Less(a, b int) bool {
	return q[a] > q[b]
}

func (q PriorityQueue) Top() int {
	return q[0]
}

func (q *PriorityQueue) Push(x interface{}) {
	*q = append(*q, x.(int))
}

func (q *PriorityQueue) Pop() interface{} {
	v := (*q)[q.Len()-1]
	*q = (*q)[: q.Len()-1]
	return v
}

```

![Leetcode 执行结果截图，执行用时 136 ms, 在所有 Go 提交中击败了100.00%的用户; 内存消耗 7.3 MB, 在所有 Go 提交中击败了100.00%的用户](https://tva1.sinaimg.cn/large/007S8ZIlgy1geqkex0ey2j30oa05oaar.jpg)

哎，，Go 还是写结构化比较强的东西好用。这种库里大量的接口需要自己写实现，在工程里倒是挺好用，但拿来解这种小问题写起来就各种不方便了。

