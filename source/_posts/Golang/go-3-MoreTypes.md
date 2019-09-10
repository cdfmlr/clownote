---
title: golang-更多类型：指针、struct、slice和映射
date: 2019-08-31 10:24:03
tags: Golang
categories:
	- Golang
	- Beginning
---

## 更多类型：指针、struct、slice 和映射

### § [指针](https://tour.golang.org/moretypes/1)

Go 拥有指针。指针保存了值的内存地址。

类型 `*T` 是指向 `T` 类型值的指针。其零值为 `nil`。

```go
var p *int
```

`&` 操作符会生成一个指向其操作数的指针。

```go
i := 42
p = &i
```

`*` 操作符表示指针指向的底层值。

```go
fmt.Println(*p) // 通过指针 p 读取 i
*p = 21         // 通过指针 p 设置 i
```

这也就是通常所说的“间接引用”或“重定向”。

与 C 不同，Go 没有指针运算。

```go
package main

import "fmt"

func main() {
	i, j := 42, 2701

	p := &i
	fmt.Println(p)
	fmt.Println(*p)
	*p = 21
	fmt.Println(*p)

	p = &j
	*p /= 37
	fmt.Println(j)
}
```

输出：

```
0xc00008e000
42
21
73
```

### § [结构体](https://tour.golang.org/moretypes/2)

一个结构体（`struct`）就是一组字段（field）。

```go
package main

import "fmt"

type Vertex struct {
	x int
	y int
}

func main() {
	fmt.Println(Vertex{1, 2})
}
```

输出：

```
{1 2}
```

#### [结构体字段](https://tour.golang.org/moretypes/3)

结构体字段使用点号来访问。

```go
package main

import "fmt"

type Vertex struct {
	X int
	Y int
}

func main() {
	v := Vertex{1, 2}
	v.X = 4
	fmt.Println(v.X)
}
```

输出：

```
4
```

#### [结构体指针](https://tour.golang.org/moretypes/4)

结构体字段可以通过结构体指针来访问。

如果我们有一个指向结构体的指针 p，那么可以通过 `(*p).X` 来访问其字段 X。不过这么写太啰嗦了，所以语言也允许我们使用隐式间接引用，直接写 `p.X` 就可以。

```go
package main

import "fmt"

type Vertex struct {
	X int
	Y int
}

func main() {
	v := Vertex{1, 2}
	p := &v
	p.X = 1e9
	fmt.Println(v)
}
```

输出：

```
{1000000000 2}
```

#### [结构体文法(Struct Literals)](https://tour.golang.org/moretypes/5)

结构体文法通过直接列出字段的值来新分配一个结构体。

使用 `Name:` 语法可以仅列出部分字段。（字段名的顺序无关。）

特殊的前缀 `&` 返回一个指向结构体的指针。

```go
package main

import "fmt"

type Vertex struct {
	X, Y int
}

var (
	v1 = Vertex{1, 2}
	v2 = Vertex{X: 1}
	v3 = Vertex{}
	p0 = &Vertex{Y: 1, X: 2}
)

func main() {
	fmt.Println(v1, v2, v3, *p0)
}
```

输出：

```
{1 2} {1 0} {0 0} {2 1}
```

### § [数组](https://tour.golang.org/moretypes/6)

类型 `[n]T` 表示拥有 n 个 T 类型的值的数组。

表达式

`var a [10]int`

会将变量 a 声明为拥有 10 个整数的数组。

```go
package main

import "fmt"

func main() {
	var a [2]string
	a[0] = "Hello"
	a[1] = "World"
	fmt.Println(a[0], a[1])
	fmt.Println(a)

	primes := [6]int{2, 3, 5, 7, 11, 13}
	fmt.Println(primes)
}
```

输出：

```
Hello World
[Hello World]
[2 3 5 7 11 13]
```

数组的长度是其类型的一部分，因此数组不能改变大小。这看起来是个限制，不过没关系，Go 提供了更加便利的方式来使用数组。

### § 切片

每个数组的大小都是固定的。而切片则为数组元素提供动态大小的、灵活的视角。在实践中，切片比数组更常用。

类型 `[]T` 表示一个元素类型为 T 的切片。（不写元素个数的数组）

切片通过两个下标来界定，即一个上界和一个下界，二者以冒号分隔：

`a[low : high]`

它会选择一个半开区间，包括第一个元素，但排除最后一个元素。

以下表达式创建了一个切片，它包含 a 中下标从 1 到 3 的元素：

`a[1:4]`

```go
package main

import "fmt"

func main() {
	primes := [6]int{2, 3, 5, 7, 11, 13}

	var s []int = primes[1:4]
	fmt.Println(s)
}
```

输出：

```
[3 5 7]
```

#### [切片就像数组的引用](https://tour.golang.org/moretypes/8)

切片并不存储任何数据，它只是描述了底层数组中的一段。

更改切片的元素会修改其底层数组中对应的元素。

与它共享底层数组的切片都会观测到这些修改。

```go
package main

import "fmt"

func main() {
	names := [4]string{
		"A",
		"B",
		"C",
		"D",
	}
	fmt.Println(names)

	a := names[0:2]
	b := names[1:3]
	fmt.Println(a, b)

	b[0] = "XXX"
	fmt.Println(a, b)
	fmt.Println(names)
}
```

输出：

```
[A B C D]
[A B] [B C]
[A XXX] [XXX C]
[A XXX C D]
```

#### [切片文法(Slice literals)](https://tour.golang.org/moretypes/9)

切片文法类似于没有长度的数组文法。

这是一个数组文法：

`[3]bool{true, true, false}`

下面这样则会创建一个和上面相同的数组，然后构建一个引用了它的切片：

`[]bool{true, true, false}`

```go
package main

import "fmt"

func main() {
	q := []int{2, 3, 5, 7, 11, 13}
	fmt.Println(q)

	r := []bool{true, false, true, false}
	fmt.Println(r)

	s := []struct {
		i int
		b bool
	}{
		{2, true},
		{3, false},
		{5, true},
	}
	fmt.Println(s)
}
```

输出：

```
[2 3 5 7 11 13]
[true false true false]
[{2 true} {3 false} {5 true}]
```

#### [切片的默认行为](https://tour.golang.org/moretypes/10)

在进行切片时，你可以利用它的默认行为来忽略上下界。

切片下界的默认值为 0，上界则是该切片的长度。

对于数组

`var a [10]int`

来说，以下切片是等价的：

`a[0:10]`

`a[:10]`

`a[0:]`

`a[:]`

```go
package main

import "fmt"

func main() {
	s := []int{2, 3, 5, 7, 11, 13}

	s = s[1:4]
	fmt.Println(s)

	s = s[:2]
	fmt.Println(s)

	s = s[1:]
	fmt.Println(s)
}
```

输出：

```
[3 5 7]
[3 5]
[5]

```

#### [切片的长度与容量](https://tour.golang.org/moretypes/11)

切片拥有 **长度** 和 **容量**。

* 切片的 长度 就是它所包含的元素个数。

* 切片的 容量 是从它的第一个元素开始数，到其底层数组元素末尾的个数。

切片 `s` 的长度和容量可通过表达式 `len(s)` 和 `cap(s)` 来获取。

你可以通过重新切片来改变一个切片的长度(You can extend a slice's length by re-slicing it, provided it has sufficient capacity. )。

如果长度开得超出了容量(to extend it beyond its capacity)，会有 runtime error。

```go
package main

import "fmt"

func main() {
	s := []int{2, 3, 5, 7, 11, 13}
	printSlice(s)

	// 截取切片使其长度为 0
	s = s[:0]
	printSlice(s)

	// 拓展其长度
	s = s[:4]
	printSlice(s)

	// 舍弃前两个值
	s = s[2:]
	printSlice(s)

	// 向外扩展它的容量
	s = s[2:10]
	printSlice(s)
}

func printSlice(s []int) {
	fmt.Printf("len=%d\tcap=%d\t %v\n", len(s), cap(s), s)
}
```

输出：

```
len=6	cap=6	 [2 3 5 7 11 13]
len=0	cap=6	 []
len=4	cap=6	 [2 3 5 7]
len=2	cap=4	 [5 7]
panic: runtime error: slice bounds out of range

goroutine 1 [running]:
main.main()
	/Users/example/go/tour/slice-len-cap/src.go:22 +0x483
exit status 2
```

#### [nil 切片](https://tour.golang.org/moretypes/12)

切片的零值是 `nil`。

`nil` 切片的长度和容量为 `0` 且没有底层数组。

```go
package main

import "fmt"

func main() {
	var s []int
	fmt.Println(s, len(s), cap(s))
	if s == nil {
		fmt.Println("nil!")
	}
}
```

输出：

```
[] 0 0
nil!
```

#### [用 make 创建切片](https://tour.golang.org/moretypes/13)

切片可以用内建函数 `make` 来创建，这也是创建动态数组的方式。

`make` 函数会分配一个元素为零值的数组并返回一个引用了它的切片：

`a := make([]int, 5)  // len(a)=5`

要指定它的容量(cap)，需向 make 传入第三个参数：

```go
b := make([]int, 0, 5) // len(b)=0, cap(b)=5

b = b[:cap(b)] // len(b)=5, cap(b)=5
b = b[1:]      // len(b)=4, cap(b)=4
```

```go
package main

import "fmt"

func main() {
	a := make([]int, 5)
	printSlice("a", a)

	b := make([]int, 0, 5)
	printSlice("b", b)

	c := b[:2]
	printSlice("c", c)

	d := c[2:5]
	printSlice("d", d)
}

func printSlice(s string, x []int) {
	fmt.Printf("%s: len=%d cap=%d %v\n", s, len(x), cap(x), x)
}
```

输出：

```
a: len=5 cap=5 [0 0 0 0 0]
b: len=0 cap=5 []
c: len=2 cap=5 [0 0]
d: len=3 cap=3 [0 0 0]
```

#### [切片的切片](https://tour.golang.org/moretypes/14)

切片可包含任何类型，甚至包括其它的切片。

```go
package main

import (
	"fmt"
	"strings"
)

func main() {
	// 创建一个井字板（井字棋游戏）
	board := [][]string{
		[]string{"_", "_", "_"},
		[]string{"_", "_", "_"},
		[]string{"_", "_", "_"},
	}

	// 两个玩家轮流打上 X 和 O
	board[0][0] = "X"
	board[2][2] = "O"
	board[1][2] = "X"
	board[1][0] = "O"
	board[0][2] = "X"

	for i := 0; i < len(board); i++ {
		fmt.Printf("%s\n", strings.Join(board[i], "  "))
	}
}
```

输出：

```
X  _  X
O  _  X
_  _  O
```

#### [向切片追加元素](https://tour.golang.org/moretypes/15)

为切片追加新的元素是种常用的操作，为此 Go 提供了内建的 append 函数。内建函数的[文档](https://golang.org/pkg/builtin/#append)对此函数有详细的介绍。

`func append(s []T, vs ...T) []T`

`append` 的第一个参数 `s` 是一个元素类型为 `T` 的切片，其余类型为 `T` 的值将会追加到该切片的末尾。

`append` 的结果是一个包含原切片所有元素加上新添加元素的切片。

当 `s` 的底层数组太小，不足以容纳所有给定的值时，它就会分配一个更大的数组。返回的切片会指向这个新分配的数组。

```go
package main

import "fmt"

func main() {
	var s []int
	printSlice(s)

	// 将元素添加到一个空切片
	s = append(s, 0)
	printSlice(s)

	// 这个切片会按需增长
	s = append(s, 1)
	printSlice(s)

	// 可以一次添加多个元素
	s = append(s, 2, 3, 4)
	printSlice(s)
}

func printSlice(s []int) {
	fmt.Printf("len=%d cap=%d %v\n", len(s), cap(s), s)
}
```

输出：

```
len=0 cap=0 []
len=1 cap=1 [0]
len=2 cap=2 [0 1]
len=5 cap=6 [0 1 2 3 4]
```

（要了解关于切片的更多内容，请阅读文章 [Go 切片：用法和本质](https://blog.golang.org/go-slices-usage-and-internals)。）

### [Range](https://tour.golang.org/moretypes/16)

`for` 循环的 `range` 形式可遍历切片或映射。

当使用 `for` 循环遍历切片时，每次迭代都会返回两个值。第一个值为当前元素的下标，第二个值为该下标所对应元素的一份副本。

```go
package main

import "fmt"

var pow = []int{1, 2, 4, 8, 16, 32, 64, 128}

func main() {
	for i, v := range pow {
		fmt.Printf("2**%d = %d\n", i, v)
	}
}
```

输出：

```
2**0 = 1
2**1 = 2
2**2 = 4
2**3 = 8
2**4 = 16
2**5 = 32
2**6 = 64
2**7 = 128
```

#### [range（续）](https://tour.golang.org/moretypes/17)

可以将 下标 或 值 赋予 _ 来忽略它。

`for i, _ := range pow`
`for _, value := range pow`

若你只需要索引，忽略第二个变量即可:

`for i := range pow`

```go
package main

import "fmt"

func main() {
	pow := make([]int, 10)
	for i := range pow {
		pow[i] = 1 << uint(i) // == 2 ** i
	}
	for _, value := range pow {
		fmt.Printf("%d\n", value)
	}
}
```

输出：

```
1
2
4
8
16
32
64
128
256
512
```

### [Maps(映射)](https://tour.golang.org/moretypes/19)

映射将键映射到值。

映射的零值为 `nil` 。

`nil` 映射既没有键，也不能添加键。

`make` 函数会返回给定类型的映射，并将其初始化备用。

```go
package main

import "fmt"

type Vertex struct {
	Lat, Long float64
}

var m map[string]Vertex

func main() {
	fmt.Println(m)
	// m["A"] = Vertex{1.2, 3.4}    // 不可这样用

	m = make(map[string]Vertex)
	m["B"] = Vertex{
		40.05, -71.0,
	}
	fmt.Println(m["B"])
}
```

输出：

```
map[]
{40.05 -71}
```

#### [映射的文法](https://tour.golang.org/moretypes/20)

映射的文法与结构体相似，不过必须有键名。

```go
package main

import "fmt"

type Vertex struct {
	Lat, Long float64
}

var m = map[string]Vertex{
	"B" : Vertex{1, 2},
	"C" : Vertex{3, 4},
}

func main() {
	fmt.Println(m)
}
```

输出：

```
map[B:{1 2} C:{3 4}]
```

#### [映射的文法（续）](https://tour.golang.org/moretypes/21)

若顶级类型只是一个类型名，你可以在文法的元素中省略它:

```go
package main

import "fmt"

type Vertex struct {
	Lat, Long float64
}

var m = map[string]Vertex{
	"B": {1, 2},
	"C": {3, 4},
}

func main() {
	fmt.Println(m)
}
```

输出：

```
map[B:{1 2} C:{3 4}]
```

#### [修改映射](https://tour.golang.org/moretypes/22)

在映射 `m` 中插入或修改元素：

`m[key] = elem`

获取元素：

`elem = m[key]`

删除元素：

`delete(m, key)`

通过双赋值检测某个键是否存在：

`elem, ok = m[key]`

若 `key` 在 `m` 中，`ok` 为 `true` ；否则，`ok` 为 `false`。

若 `key` 不在映射中，那么 `elem` 是该映射元素类型的零值。

同样的，当从映射中读取某个不存在的键时，结果是映射的元素类型的零值。

**注** ：若 `elem` 或 `ok` 还未声明，可以使用短变量声明：

`elem, ok := m[key]`

```go
package main

import "fmt"

func main() {
	m := make(map[string]int)

	m["Answer"] = 42
	fmt.Println("The value:", m["Answer"])

	m["Answer"] = 48
	fmt.Println("The value:", m["Answer"])

	delete(m, "Answer")
	fmt.Println("The value:", m["Answer"])

	v, ok := m["Answer"]
	fmt.Println("The value:", v, "Present?", ok)
}
```

输出：

```
The value: 42
The value: 48
The value: 0
The value: 0 Present? false
```

### [函数值](https://tour.golang.org/moretypes/24)

函数也是值。它们可以像其它值一样传递。

函数值可以用作函数的参数或返回值。

```go
package main

import (
	"fmt"
	"math"
)

func compute(fn func(float64, float64) float64) float64 {
	return fn(3, 4)
}

func main() {
	hypot := func(x, y float64) float64 {
		return math.Sqrt(x*x + y*y)
	}
	fmt.Println(hypot(5, 12))

	fmt.Println(compute(hypot))
	fmt.Println(compute(math.Pow))
}
```

输出：

```
13
5
81
```

### [函数的闭包](https://tour.golang.org/moretypes/25)

Go 函数可以是一个闭包。闭包是一个函数值，它引用了其函数体之外的变量。该函数可以访问并赋予其引用的变量的值，换句话说，该函数被这些变量“绑定”在一起。

```go
package main

import "fmt"

func adder() func(int) int {
	sum := 0
	return func(x int) int {
		sum += x
		return sum
	}
}

func main() {
	pos, neg := adder(), adder()
	for i := 0; i < 10; i++ {
		fmt.Println(
			pos(i),
			neg(-2*i),
		)
	}
}
```

输出：

```
0 0
1 -2
3 -6
6 -12
10 -20
15 -30
21 -42
28 -56
36 -72
45 -90
```


👆函数 `adder` 返回一个闭包。每个闭包都被绑定在其各自的 `sum` 变量上。

实例：[*斐波纳契闭包*](https://tour.golang.org/moretypes/26)

```go
package main

import "fmt"

// fibonacci is a function that returns
// a function that returns an int.

func fibonacci() func() int {
	i, j := 0, 1
	return func() int {
		i, j = j, i + j
		return i
	}
}

func main() {
	f := fibonacci()
	for i := 0; i < 10; i++ {
		fmt.Println(f())
	}
}
```

输出：

```
1
1
2
3
5
...
```

---

