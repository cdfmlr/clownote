---
categories:
- Rust
- Beginning
date: 2021-07-23 11:55:33.804773
tags: Rust
title: Hello, Rust!
---

Hello, Rust!
===

久违的学习笔记系列！！

天天复习考研，吐了。划一天水放松一下吧，学学 Rust。

> 本文是学习以下（主要）内容的笔记：
>
> - Rust 官网 get started： https://www.rust-lang.org/zh-CN/learn/get-started
>
> - Rust By Example (中文译本) 1. Hello World: http://rustwiki.org/zh-CN/rust-by-example/hello.html
>   - Rust 文档 `std::fmt`： https://doc.rust-lang.org/std/fmt/

# 安装

以 `*nix`系统为例，用 `rustup`：

```sh
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

安装检查：

```sh
cargo --version
```

（`cargo` 是构建、包管理的工具，Rust 的编译器是 `rustc`）

更新：

```sh
rustup update
```

# Hello World

可以只写一个文件，也可以做成一个项目。

## 单一源文件

新建一个 `hello.rs`：

```rust
fn main() {
    println!("Hello, world!");
}
```

编译、运行：

```sh
$ rustc hello.rs
$ ./hello
```

在我的电脑上（Intel macBook Pro 2017，macOS 11.4）编译出来的二进制文件（`./hello`）有 `408K`。同样功能的 C 程序只有 `48K`，Swift 为 `49K`，而 Go 程序要 `1.2M` 。

## Cargo 项目

新建项目：

```sh
cargo new hello-rust
```

生成一个项目目录 `./hello-rust/`，其内容如下：

```sh
hello-rust
|- Cargo.toml  # Rust 的清单文件: 包含项目的元数据和依赖库
|- src
  |- main.rs   # 写代码的地方
```

（它甚至给 `git init` 了，还写了 `.gitignore`）

`main.rs` 里面已经写好了一个 hello world：

```rust
fn main() {
    println!("Hello, world!");
}
```

运行：

```sh
cargo run
```

# 注释

```rust
// 单行注释

/* 注释块 */
```

文档注释：

```rust
/// 文档注释
fn hello() { ... }
```

用 `rustdoc hello.rs` 来编译文档，结果是个网站，放在 `./doc` 里。随便开个服务就可以看了：

```sh
python3 -m http.server -d doc
```

# 格式化输出

由 std 里的一堆宏实现格式化输出（这些 `!` 就说明是**宏**）：

- 格式化字符串：`format!`
- 标准输出：`print!`， `println!`
- 标准错误：`eprint!`，`eprintln!`

这些东西的语法和 C 的 `printf` 类似，都是 `format!("a string literal", ...)`，具体的用法见 https://doc.rust-lang.org/std/fmt/index.html。下面只简要介绍：

`format!` 是返回格式化后的字符串， 而四种 `print` 就是把 `format!` 的结果写到 `io::stdout` 或 `io::stderr`。

在格式字符串字面值常量中用 `{name_or_index:formatting}` 来指定替换内容。

替换也就要把一个特定类型的对象格式化（`toString`）。格式化一个对象的方式在 Rust 中叫做 *traits*。Rust 有好几个不同的 traits，所以同一个数据可以有好几种显示的方式，例如一个数字可以写成二进制、十进制、十六进制等等。每个 traits 对应有一种 `{:口}` （`口` 是某种字符）。

最常用的两种 traits 是 Display 和 Debug，二者在格式字符串中分别写作 `{}` （也就是`{:口}` 的 `口` 为空的情形） 和 `{:?}` 。二者分别和 Go 语言 fmt 包的 `%v` 和 `%#v` 类似。

```rust
// `{}` 是 `fmt::Display`，用来显示任意内容，优雅格式
println!("Hello, {}, {}, {}", 233, 1.2, "world");
// Hello, 233, 1.2, world

// `{:?}` 叫做 `fmt::Debug` 用来输出调试风格的文本
println!("Hello, {:?}, {:?}, {:?}", 233, 1.2, "world");
// Hello, 233, 1.2, "world"
```

`{:}` 的冒号前面可以给替换字符串命名，或者指定位置：

```rust
println!("Hello, {name} with number {a}!", name="foo", a="666");
// Hello, foo with number 666!

println!("Hello, {0} with number {1} + {1}!", "foo", a="666");
// Hello, foo with number 666 + 666!
```

`{:}` 的冒号后面是格式：

```rust
println!("dec: {0}, bin: {0:b}, hex: {0:X}", 66);
// dec: 66, bin: 1000010, hex: 42
```

具体格式的写法参考 https://doc.rust-lang.org/std/fmt/ 。大概的写法为 `FA+#?0W.PT`：

- `F` 是填充用的字符
- `A` 是 `<` 或 `^` 或 `>`，对齐的方向（不满用 F 填充）
- `+`：正数显示加号
- `#?` ：pretty-print 的 Debug
  - `#b`，`#o`，`#x`：显示二、八、十六进制的前缀
- `0` 数字前面补零至宽度
- `W` 宽度
- `.P` 小数位数
  - `.N$`：用参数 N 做精度（就是 `format!("{}", ...)` 的 `...`，从 0 开始）
    - 如果是整数，`{:N$}` ，就是那参数 N 作宽度。
  - `.*`：读两个二个参数，后一个参数是要格式化的小数，以前一个参数为精度，`format!("{:.*}", 5, 0.01)`  结果为 `0.01000`
- `T` 是显示的方式，即 traits（可以让自定义类型自己定制各种显示效果）：
  - *nothing* ⇒ [`Display`](https://doc.rust-lang.org/std/fmt/trait.Display.html)
  - `?` ⇒ [`Debug`](https://doc.rust-lang.org/std/fmt/trait.Debug.html)
    - `x?` ⇒ [`Debug`](https://doc.rust-lang.org/std/fmt/trait.Debug.html) with lower-case hexadecimal integers （对应 `X?` 是大写的十六进制）
  - `o` ⇒ [`Octal`](https://doc.rust-lang.org/std/fmt/trait.Octal.html)
  - `x` ⇒ [`LowerHex`](https://doc.rust-lang.org/std/fmt/trait.LowerHex.html)
  - `X` ⇒ [`UpperHex`](https://doc.rust-lang.org/std/fmt/trait.UpperHex.html)
  - `p` ⇒ [`Pointer`](https://doc.rust-lang.org/std/fmt/trait.Pointer.html)
  - `b` ⇒ [`Binary`](https://doc.rust-lang.org/std/fmt/trait.Binary.html)
  - `e` ⇒ [`LowerExp`](https://doc.rust-lang.org/std/fmt/trait.LowerExp.html)
  - `E` ⇒ [`UpperExp`](https://doc.rust-lang.org/std/fmt/trait.UpperExp.html)

```rust
println!("{:_<9} {:09} {:`^9} {:9.6} {:09.6} {:)>9} {:#?}", "left", 123, "center", 3.14, 3.14, "right", 2.17e5);

// left_____ 000000123 `center``  3.140000 03.140000 ))))right 217000.0
```

所有的类型，若想用 `std::fmt` 的格式化打印，都要求实现至少一个可打印的 `traits`。 自动的实现只为一些类型提供，比如 `std` 库中的类型。所有其他类型 都**必须**手动实现。下面介绍如何输出自定义类型：

## Debug

`fmt::Debug` ，就是 `{:?}`， 比较容易实现，一般直接用推导（`derive`）来自动创建：

```rust
// 一个自定义的结构体
#[derive(Debug)]  // 加了这个才能打印
struct Point2D {
    x: f64,
    y: f64,
}

fn main() {
    let p = Point2D { x:66.0, y:77.0 };

    println!("{:?}", peter);
    // Point2D { x: 66.0, y: 77.0 }

    println!("{:#?}", peter);  // 更好看一点
    // Point2D {
    //     x: 66.0,
    //     y: 77.0,
    // }
}
```

## Display

`fmt::Display` ，就是 `{}`， 须手动实现。

```rust
use std::fmt;

#[derive(Debug)]
struct Complex {
    real: f64,
    imag: f64,
}

impl fmt::Display for Complex {
    // `f` 是个 buffer，此方法必须将格式化后的字符串写入其中
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        // `write!` 和 `format!` 类似，但是将格式化后的字符串写入 buffer
        write!(f, "{} + {}i", self.real, self.imag)
    }
}

fn main() {
    println!("Display: {0}\nDebug: {0:?}", Complex{ real: 3.3, imag: 7.2});
    // Display: 3.3 + 7.2i
    // Debug: Complex { real: 3.3, imag: 7.2 }
}
```

注意上面这个例子中 `write!(...)` 后面不加 `;`。这个语法是 `return write!(...);` 的简写，以最后的表达式作为函数返回值。如果不写 `return` 又加了 `;` 就变成返回空 `()` 了。

用类似的方法，还可以实现其他的 traits，比如：[`Octal`](https://doc.rust-lang.org/std/fmt/trait.Octal.html)，[`LowerHex`](https://doc.rust-lang.org/std/fmt/trait.LowerHex.html)， [`UpperHex`](https://doc.rust-lang.org/std/fmt/trait.UpperHex.html)， [`Pointer`](https://doc.rust-lang.org/std/fmt/trait.Pointer.html)，[`Binary`](https://doc.rust-lang.org/std/fmt/trait.Binary.html)，[`LowerExp`](https://doc.rust-lang.org/std/fmt/trait.LowerExp.html)， [`UpperExp`](https://doc.rust-lang.org/std/fmt/trait.UpperExp.html)。

## 错误处理

对于一个集合，要 fmt 输出的话，需要迭代写每个值：

```rust
use std::fmt; // 导入 `fmt` 模块。

// 定义一个包含单个 `Vec` 的结构体 `List`。
struct List(Vec<i32>);

impl fmt::Display for List {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        // 使用元组的下标获取值，并创建一个 `vec` 的引用。
        let vec = &self.0;

        write!(f, "[")?;

        // 使用 `v` 对 `vec` 进行迭代，并用 `count` 记录迭代次数。
        for (count, v) in vec.iter().enumerate() {
            // 对每个元素（第一个元素除外）加上逗号。
            // 使用 `?` 或 `try!` 来返回错误。
            if count != 0 { write!(f, ", ")?; }
            write!(f, "{}", v)?;
        }

        // 加上配对中括号，并返回一个 fmt::Result 值。
        write!(f, "]")
    }
}

fn main() {
    let v = List(vec![1, 2, 3]);
    println!("{}", v);
}
```

这里就需要多次调用 `write!`，`write!` 是可能返回错误的哦。一旦错误了就不该继续写了，所以在调用末尾用了 `?` 语法：

```rust
write!(f, "{}", value)?;
// 等同于：
try!(write!(f, "{}", value));
```

这个语法是尝试 `write!` ，若发生错误，则直接返回相应的错误，结束函数；否则继续执行后面的语句。也就是类似于 Go 中的：

```go
_, err := DoSomething()
if err != nil {
    return err
}
```

如果不加这个 `?` 默认会编译时 warning，提醒你可能没处理错误。

## 格式化

再看一个例子：

```rust
use std::fmt::{self, Formatter, Display};

#[derive(Debug)]
struct Color {
    red: u8,
    green: u8,
    blue: u8,
}

impl Display for Color {
    fn fmt(&self, f: &mut Formatter) -> fmt::Result {
        write!(f, "RGB({R}, {G}, {B}) {R:#02X}{G:02X}{B:02X}", 
            R=self.red, G=self.green, B=self.blue)
    }
}

fn main() {
    for color in [
        Color { red: 128, green: 255, blue: 90 },
        Color { red: 0, green: 3, blue: 254 },
        Color { red: 0, green: 0, blue: 0 },
    ].iter() {
        println!("{}", *color)
    }
}
```

输出：

```rust
RGB(128, 255, 90) 0x80FF5A
RGB(0, 3, 254) 0x003FE
RGB(0, 0, 0) 0x00000
```

