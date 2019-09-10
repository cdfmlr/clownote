---
title: golang-包、变量和函数
date: 2019-08-31 10:17:18
tags: Golang
categories:
	- Golang
	- Beginning
---

## 包、变量和函数

### § [包](https://tour.golang.org/basics/1)

每个 Go 程序都是由包构成的。

一般程序从 `main` 包的 `main` 函数开始运行，除非有 `init` 函数。

```go
package main

import (
	"fmt"
	"math/rand"
)

func main() {
	fmt.Println("This is a rand int:", rand.Intn(10))
}
```

输出：

```
This is a rand int: 1
```

本程序通过导入路径 `"fmt"` 和 `"math/rand"` 来使用这两个包。

按照约定，包名与导入路径的最后一个元素一致。例如，`"math/rand"` 包中的源码均以 `package rand` 语句开始。

*注意：* 若此程序的运行环境是固定的，`rand.Intn` 将总是会返回相同的数字。

（要得到不同的数字，需为生成器提供不同的种子数（使用 [`rand.Seed`](https://golang.org/pkg/math/rand/#Seed)）。 常用时间的值作为种子数。）

#### [导入](https://tour.golang.org/basics/2)

正如我们在之前的代码中看见的，我们使用 `import` 语句来导入包。

```go
package main

import (
	"fmt"
	"math"
)

func main() {
	fmt.Printf("8's sqrt is %g.\n", math.Sqrt(8))
}
```

输出：

```
This is a rand int: 1
```

此代码用圆括号组合了导入，这是“分组”形式的导入语句。

当然你也可以编写多个导入语句，例如：

`import "fmt"`
`import "math"`

不过使用分组导入语句是更好的形式。

#### [导出名](https://tour.golang.org/basics/3)

在 Go 中，如果一个名字以大写字母开头，那么它就是已导出的。例如，`Pizza` 就是个已导出名，`Pi` 也同样，它导出自 `math` 包。

pizza 和 pi 并未以大写字母开头，所以它们是未导出的。

在导入一个包时，你只能引用其中已导出的名字。任何“未导出”的名字在该包外均无法访问。

```go
package main

import (
	"fmt"
	"math"
)

func main() {
	fmt.Println(math.pi)
}
```

执行代码，可以观察到错误输出：

```
# command-line-arguments
./src.go:9:14: cannot refer to unexported name math.pi
./src.go:9:14: undefined: math.pi
```

然后将 `math.pi` 改名为 `math.Pi` 再试着执行一次，就可以得到预想的输出了：


输出：

```
3.141592653589793
```

### § [函数](https://tour.golang.org/basics/4)

```go
package main

import "fmt"

func add(x int, y int) int {
	return x + y
}

func main() {
	fmt.Println(add(12, 13))
}
```

输出：

```
25
```

函数可以没有参数或接受多个参数。

在本例中，`add` 接受两个 `int` 类型的参数。

注意类型在变量名**之后**。

（参考 [这篇关于 Go 语法声明的文章](http://blog.golang.org/gos-declaration-syntax) 了解这种类型声明形式出现的原因。）

#### [函数（续）](https://tour.golang.org/basics/5)

当连续两个或多个函数的已命名形参类型相同时，除最后一个类型以外，其它都可以省略。

```go
package main

import "fmt"

func add(x, y int) int {
	return x + y
}

func main() {
	fmt.Println(add(1, 2))
}
```

输出：

```
3
```

在本例中，

`x int, y int`

被缩写为

`x, y int`

#### [多值返回](https://tour.golang.org/basics/6)

函数可以返回**任意数量**的返回值。

```go
package main

import "fmt"

func swap(x, y string) (string, string) {
	return y, x
}

func main() {
	a, b := swap("Hello", "World")
	fmt.Println(a, b)
}
```

输出：

```
World Hello
```

swap 函数返回了两个字符串。

#### [命名返回值](https://tour.golang.org/basics/7)

Go 的返回值可被命名，它们会被视作定义在函数顶部的变量。

返回值的名称应当具有一定的意义，它可以作为文档使用。

没有参数的 `return` 语句返回已命名的返回值。也就是 直接 返回。

直接返回语句应当仅用在下面这样的短函数中。在长的函数中它们会影响代码的可读性。

```go
package main

import "fmt"

func split(sum int) (x, y int) {
	x = sum * 4 / 9
	y = sum - x
	return
}

func main() {
	fmt.Println(split(17))
}
```

输出：

```
7 10
```

### § [变量](https://tour.golang.org/basics/8)

`var` 语句用于声明一个变量列表，跟函数的参数列表一样，类型在最后。

```go
package main

import "fmt"

var i, j int

func main() {
	var y, n bool
	fmt.Println(i, j, y, n)
}
```

输出：

```
0 0 false false
```

就像在这个例子中看到的一样，`var` 语句可以出现在包或函数级别。

#### [变量的初始化](https://tour.golang.org/basics/9)

变量声明可以包含初始值，每个变量对应一个。

如果初始化值已存在，则可以省略类型；变量会从初始值中获得类型。

```go
package main

import "fmt"

var i, j int = 1, 2

func main() {
	var y, n, a, b = true, false, "Hello", 3.14
	fmt.Println(i, j, y, n, a, b)
}
```

输出：

```
1 2 true false Hello 3.14
```

#### [短变量声明](https://tour.golang.org/basics/10)

在函数中，简洁赋值语句 `:=` 可在类型明确的地方代替 `var` 声明。

函数外的每个语句都必须以关键字开始（var, func 等等），因此 `:=` 结构不能在函数外使用。

```go
package main

import "fmt"

func main() {
	i := 100
	fmt.Println(i)
}
```

输出：

```
100
```

#### [基本类型](https://tour.golang.org/basics/11)

Go 的基本类型有:

| 类型 | 描述 | 说明 | 衍生 |
| -- | -- | -- | -- |
| `bool` | 布尔型 | `true` or `false` |  |
| `string` | 字符串 | 一串固定长度的字符连接起来的字符序列，使用 UTF-8 编码标识 Unicode 文本。|  |
| `int` | 整型 | 32位机上为32位，64位机上是64位 | 指定大小的整型: int8  `int16`  `int32`  `int64` |
| `uint` | 无符号整型 |   | `uint8`、`uint16`、`uint32`、`uint64`、`uintptr` |
| `float32`、`float64` | 浮点型 |  |  |
| `complex64`、`complex128` | 复数 | 复数的字面值常量写作`1+2i` |  |
| `byte` |  | uint8 的别名 |  |
| `rune` | 表示一个 Unicode 码点 | int32 的别名 | |


下例展示了几种类型的变量。 同导入语句一样，变量声明也可以“分组”成一个语法块：

```go
package main

import (
	"fmt"
	"math/cmplx"
)

var (
	ToBe   bool       = false
	MaxInt uint64     = 1<<64 - 1
	z      complex128 = cmplx.Sqrt(-5 + 12i)
)

func main() {
	fmt.Printf("Type: %T\t\tValue: %v\n", ToBe, ToBe)
	fmt.Printf("Type: %T\t\tValue: %v\n", MaxInt, MaxInt)
	fmt.Printf("Type: %T\tValus: %v\n", z, z)
}
```

输出：

```
Type: bool		Value: false
Type: uint64		Value: 18446744073709551615
Type: complex128	Valus: (2+3i)
```

`int`, `uint` 和 `uintptr` 在 32 位系统上通常为 32 位宽，在 64 位系统上则为 64 位宽。 当你需要一个整数值时应使用 `int` 类型，除非你有特殊的理由使用固定大小或无符号的整数类型。

#### [零值](https://tour.golang.org/basics/12)

没有明确初始值的变量声明会被赋予它们的 *零值*。

零值是：

数值类型为 `0`，
布尔类型为 `false`，
字符串为 `""`（空字符串）。

```go
package main

import "fmt"

func main() {
	var i int
	var f float64
	var c complex128
	var b bool
	var s string

	fmt.Printf("%v %v %v %v %q\n", i, f, c, b, s)
}
```

输出：

```
0 0 (0+0i) false ""
```

#### [类型转换](https://tour.golang.org/basics/13)

表达式 `T(v)` 将值 `v` 转换为类型 `T`。

一些关于数值的转换：

```go
var i int = 42
var f float64 = float64(i)
var u uint = uint(f)
```

或者，更加简单的形式(在函数中)：

```go
i := 42
f := float64(i)
u := uint(f)
```

与 C 不同的是，Go 在不同类型的项之间赋值时需要显式转换，否则会报错。

```go
package main

import (
	"fmt"
	"math"
)

func main() {
	var x, y int = 3, 4
	var f float64 = math.Sqrt(float64(x*x + y*y))
	var z uint = uint(f)
	fmt.Println(x, y, z)
}
```

输出：

```
3 4 5 5
```

#### [类型推导](https://tour.golang.org/basics/14)

在声明一个变量而不指定其类型时（即使用不带类型的 `:=` 语法或 `var =` 表达式语法），变量的类型由右值推导得出。

```go
package main

import "fmt"

func main() {
	i := 1
	j := 1.1
	k := 1 + 2i
	fmt.Printf("%T\t%T\t%T\n%v\t%v\t%v\n", i, j, k, i, j, k)
}
```

输出：

```
int	float64	complex128
1	1.1	(1+2i)
```

当右值声明了类型时，新变量的类型与其相同：

```go
var i int
j := i // j 也是一个 int
```

不过当右边包含未指明类型的数值常量时，新变量的类型就可能是 `int`, `float64` 或 `complex128` 了，这取决于常量的精度：

```go
i := 42           // int
f := 3.142        // float64
g := 0.867 + 0.5i // complex128
```

#### [常量](https://tour.golang.org/basics/15)

常量的声明与变量类似，只不过是使用 **`const`** 关键字替换 `var`。

常量可以是字符、字符串、布尔值或数值。

常量不能用 `:=` 语法声明。

```go
package main

import "fmt"

const PI = 3.14

func main() {
	const NAME = "World"
	fmt.Println("Hello,", NAME)
	fmt.Println(PI)
}
```


输出：

```
Hello, World
3.14
```


#### [数值常量](https://tour.golang.org/basics/16)

数值常量是高精度的**值**。

一个未指定类型的常量由上下文来决定其类型。

```go
package main

import "fmt"

const (
	// 将 1 左移 100 位来创建一个非常大的数字
	// 即这个数的二进制是 1 后面跟着 100 个 0
	Big = 1 << 100
	// 再往右移 99 位，即 Small = 1 << 1，或者说 Small = 2
	Small = Big >> 99
)

func needInt(x int) int {
	return x*10 + 1
}

func needFloat(x float64) float64 {
	return x * 0.1
}

func main() {
	fmt.Println(needInt(Small))
	fmt.Println(needFloat(Small))
	fmt.Println(needFloat(Big))
	// fmt.Println(needInt(Big))
}
```

输出：

```
21
0.2
1.2676506002282295e+29
```

尝试一下输出 `needInt(Big)` 将会报错（溢出）。

（`int` 类型最大可以存储一个 64 位的整数，有时会更小。）
