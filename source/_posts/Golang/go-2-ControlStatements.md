---
title: golang-流程控制语句：for、if、else、switch 和 defer
date: 2019-08-31 10:21:42
tags: Golang
categories:
	- Golang
	- Beginning
---

## 流程控制语句：for、if、else、switch 和 defer

### § [for](https://tour.golang.org/flowcontrol/1)

Go 只有一种循环结构：`for` 循环。

基本的 `for` 循环由三部分组成，它们用分号隔开：

* 初始化语句：在第一次迭代前执行
* 条件表达式，则前后的`;`会被去掉，若有：在每次迭代前求值
* 后置语句：在每次迭代的结尾执行

初始化语句通常为一句短变量声明，该变量声明仅在 `for` 语句的作用域中可见。

一旦条件表达式的布尔值为 `false`，循环迭代就会终止。

注意：和 C、Java、JavaScript 之类的语言不同，Go 的 for 语句后面的三个构成部分外没有小括号 `( )`， 而大括号 `{ }` 则是必须的。

```go
package main

import "fmt"

func main() {
	sum := 0
	for i := 0; i < 10; i++ {
		sum += i
	}
	fmt.Println(sum)
}
```

输出：

```
45
```

初始化语句和后置语句是可选的，例如：

```go
package main

import "fmt"

func main() {
	i := 0
	j := 100
	c := 0
	for i != j {    // for ;i != j; { 自动格式化后的结果，go 中的"while"
		i++
		j--
		c += 1
	}
	fmt.Printf("i: %v, j: %v, c: %v\n", i, j, c)
}
```

输出：

```
i: 50, j: 50, c: 50
```


如果只有条件表达式，则前后的 `;` 会被 `go fmt` 去掉，成为 go 中的"while"。若有初始化语句、条件表达式、后置语句中的两个，则不会被省略。

#### [for 也是 go 的 “while”](https://tour.golang.org/flowcontrol/3)

可以去掉分号，在 `for`  与 `{` 只写条件语句。
C 的 while 在 Go 中也叫做 `for`。

```go
package main

import "fmt"

func main() {
	s := 1
	for s <= 1000 {
		s += s
	}
	fmt.Println(s)
}
```

输出：

```
1024
```

#### [无限循环](https://tour.golang.org/flowcontrol/4)

如果省略循环条件，`for` 与 `{` 间什么都不写，该循环就不会结束，因此无限循环可以写得很紧凑。
（没有条件的 for 同 for true 一样。）


```go
package main

import (
	"fmt"
	"time"
)

func main() {
	i := 0
	for {
		fmt.Println(i)
		i++
		time.Sleep(100 * time.Millisecond)  // 暂停100毫米
	}
}
```

输出：

```
0
1
2
...     // 省去部分输出
^Csignal: interrupt     // 键入了 control+C，以终止程序
```

### § [if](https://tour.golang.org/flowcontrol/5)

Go 的 if 语句与 for 循环类似，表达式外无需小括号 `( )` ，而大括号 `{ }` 则是必须的。

```go
package main

import (
	"fmt"
	"math"
)

func sqrt(x float64) string {
	if x < 0 {
		return sqrt(-x) + "i"
	}
	return fmt.Sprint(math.Sqrt(x))
}

func main() {
	fmt.Println(sqrt(2), sqrt(-4))
}
```

输出：

```
1.4142135623730951 2i
```

#### [if 的简短语句](https://tour.golang.org/flowcontrol/6)

同 `for` 一样， `if` 语句可以在条件表达式前执行一个简单的语句。

该语句声明的变量作用域仅在 `if` 之内。

（在最后的 `return` 语句处使用 `v` 看看。）

```go
package main

import (
	"fmt"
	"math"
)

func pow(x, n, lim float64) float64 {
	if v := math.Pow(x, n); v < lim {
		return v
	}
	return lim
}

func main() {
	fmt.Println(
		pow(3, 2, 10),
		pow(3, 3, 20),
	)
}
```

输出：

```
9 20
```

#### [if-else](https://tour.golang.org/flowcontrol/7)

```go
package main

import (
	"fmt"
	"math"
)

func pow(x, n, lim float64) float64 {
	if v := math.Pow(x, n); v < lim {
		return v
	} else {
		fmt.Printf("%g >= %g\n", v, lim)
	}
	// 这里开始就不能使用 v 了
	return lim
}

func main() {
	fmt.Println(
		pow(3, 2, 10),
		pow(3, 3, 20),
	)
}
```

输出：

```
27 >= 20
9 20
```

在 `if` 的简短语句中声明的变量同样可以在任何对应的 `else` 块中使用。

（在 `main` 的 `fmt.Println` 调用开始前，两次对 `pow` 的调用均已执行并返回其各自的结果。）

### § [switch](https://tour.golang.org/flowcontrol/9)

`switch` 是编写一连串 `if - else` 语句的简便方法。它运行第一个值等于条件表达式的 case 语句。

Go 的 `switch` 语句类似于 C、C++、Java、JavaScript 和 PHP 中的，不过 Go 只运行选定的 `case`，而非之后所有的 `case`。 实际上，Go 自动提供了在这些语言中每个 `case` 后面所需的 `break` 语句。 除非以 `fallthrough` 语句结束，否则分支会自动终止。 Go 的另一点重要的不同在于 `switch` 的 `case` 无需为常量，且取值不必为整数。

```go
package main

import (
	"fmt"
	"runtime"
)

func main() {
	fmt.Print("Go runs on ")
	switch os := runtime.GOOS; os {
	case "darwin":
		fmt.Println("OS X.")
	case "linux":
		fmt.Println("Linux.")
	default:
		// freebsd, openbsd,
		// plan9, windows...
		fmt.Printf("%s.\n", os)
	}
}
```

输出：

```
Go runs on OS X.
```

#### [switch 的求值顺序](https://tour.golang.org/flowcontrol/10)

`switch` 的 `case` 语句从上到下顺次执行，直到匹配成功时停止。

（例如，

```go
switch i {
case 0:
case f():
}
```

在 i==0 时 f 不会被调用。）

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	fmt.Println("When's Saturday?")
	today := time.Now().Weekday()
	switch time.Saturday {
	case today + 0:
		fmt.Println("Today.")
	case today + 1:
		fmt.Println("Tomorrow.")
	case today + 2:
		fmt.Println("In two days.")
	default:
		fmt.Println("Too far away.")
	}
}
```

输出：

```
When's Saturday?
Tomorrow.
```

#### [没有条件的 switch](https://tour.golang.org/flowcontrol/11)

没有条件的 `switch` 同 `switch true` 一样。

这种形式能将一长串 `if-then-else` 写得更加清晰。

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	t := time.Now()
	switch {
	case t.Hour() < 12:
		fmt.Println("Good morning!")
	case t.Hour() < 17:
		fmt.Println("Good afternoon.")
	default:
		fmt.Println("Good evening.")
	}
}
```

输出：

```
Good evening.
```

### § [defer](https://tour.golang.org/flowcontrol/12)

`defer` 语句会将函数推迟到外层函数返回之后执行。

推迟调用的函数其参数会立即求值（闭包?🤔️），但直到外层函数返回前该函数都不会被调用。

```go
package main

import "fmt"

func main() {
	defer fmt.Println("world")

	fmt.Println("hello")
}
```

输出：

```
hello
world
```

#### [defer 栈](https://tour.golang.org/flowcontrol/13)

推迟的函数调用会被压入一个栈中。当外层函数返回时，被推迟的函数会按照**后进先出**的顺序调用。

更多关于 `defer` 语句的信息，[参考阅读此文](https://blog.golang.org/defer-panic-and-recover)。

```go
package main

import "fmt"

func main() {
	fmt.Println("counting...")

	for i := 0; i < 10; i++ {
		defer fmt.Println(i)
	}

	fmt.Println("done.")
}
```

输出：

```
counting...
done.
9
8
7
6
5
4
3
2
1
0
```
