---
categories:
- Rust
- Beginning
date: 2021-07-29 21:11:32.722286
tags: Rust
title: Rust 原生类型
---
Rust 原生类型
===

> 学习 [Rust By Example 2. 原生类型](http://rustwiki.org/zh-CN/rust-by-example/primitives.html)
>
> - Rust std 文档中关于 Primitive Types 的部分：https://doc.rust-lang.org/std/index.html#primitives
> - Rust 程序设计语言 Data types 部分： https://doc.rust-lang.org/book/ch03-02-data-types.html

# Rust 原生类型

Rust 的原生类型（primitive）分两种：标量类型（scalar type）和**复合类型**（compound type）

## 标量类型

| 分类                  | 类型               | 特殊/说明                                              | 字面量 |
| --------------------- | ------------------ | ------------------------------------------------------ | ------ |
| 有符号整型            | i8、i16、i32、i64  | `isize`（指针宽度）                                    | `-16`  |
| 无符号整型            | u8、u16、u32、u64  | `usize`（指针宽度）                                    | `123`  |
| 浮点型                | f32、f64           |                                                        | `3.14` |
| 字符                  | char               | Unicode，一个 char 占4 字节                            | `'A'`  |
| 布尔型                | true、false        |                                                        | `true` |
| 单元类型（unit type） | 一个空的元组：`()` | 单元类型的值是个元组，但不包含多个值，所以不是复合类型 | `()`   |

## 复合类型

| 类型          | 字面量           | 说明                     |
| ------------- | ---------------- | ------------------------ |
| 数组（array） | `[1, 2, 3]`      | 编译时确定固定类型、大小 |
| 元组（tuple） | `(1, 0.2, true)` | 有限、可异类型的序列     |
| 切片（slice） |                  | 动态大小的序列视图       |
| 字符串（str） | `"abc"`          | 字符串切片               |

## 变量定义

用 `let 名 = 值;` 来声明变量，可以在变量名后加 `:类型` 来指定类型：

```rust
let floatval: f64 = 1.0;
```

不写类型说明就自动推断：

```rust
let autoint = 12;
```

字面值可以通过后缀指定类型：

```rust
let intval = 5i32;
```

Rust 还可以通过下文来推断：

```rust
let mut autoi64 = 12; // 根据下一行的赋值推断为 i64 类型
autoi64 = 4294967296i64; 
```

用 `let mut` 来声明**可变**变量，mut 的变量值可在后面改变，但类型不能变。

注：变量可以被遮蔽（shadow）掉，遮蔽就可以变类型了：

```rust
let mut mutable = 12;
let mutable = true; // shadow
```

（这章重点是类型，不是变量，关于变量后面还会详细学习）

# 字面量与运算符

**整数**的字面量还可以加前缀来写二、八、十六进制：`0b1010`，`0o34`，`0x12AB`。

还可以加下划线方便阅读：`1_000_000 == 1000000 `，`0.000_001 == 0.000001`。

Rust 的运算符和 C 类似。包括：

- 短路求值的逻辑运算：与 `&&`、或 `||`、非 `!`。
- 位运算：位与 `&`，位或 `|`，异或 `^`，左移 `<<`，右移 `>>`。

## 元组

元组 `(A, B)` 是一些值的集合，其中的元素类型可以不同。

```rust
let empty = ();
let single = (1, );
let more = (true, 3.14, "different types");
let nested = (1, (2, false), ("tuple"));
```

用 `{:?}` 可以输出元组，但注意这个不支持太长的，超过 12 个值的元组就不能打印了：

```rust
println!("{:?}\n{:?}\n{:?}\n{:?}", empty, single, more, nested);

-----output-----

()
(1,)
(true, 3.14, "different types")
(1, (2, false), "tuple")
```



元组可以用做参数和返回值：

```rust
fn reverse(pair: (i32, bool)) -> (bool, i32) {
    println!("pair: {}, {}", pair.0, pair.1); // 下标访问
    let (integer, boolean) = pair; // 解构 deconstruct：多个值赋给变量
    (boolean, integer)
}
```

也可以用来定义匿名字段的简单结构体：

```rust
#[derive(Debug)]
struct Matrix2x2 (f32, f32, f32, f32);

impl Display for Matrix2x2 {
    fn fmt(&self, f: &mut Formatter) -> fmt::Result {
        write!(f, "\n2x2 matrix: {}, {}\n            {}, {}", self.0, self.1, self.2, self.3)
    }
}

fn transpose(m: Matrix2x2) -> Matrix2x2 {
    // let (a, b, c, d) = m; ❌
    let (a, b, c, d) = (m.0, m.1, m.2, m.3);
    return Matrix2x2(a, c, b, d);
}
```



不含任何值的元组 `()` 是一种单独的特殊类型，被称为单元类型，这种类型只有一个实例值，还是写作  `()`，这个值被称为单元值（unit value），没写 return 的函数就会返回这个值。

## 数组和切片

数组 `[T; length]` 是另一种集合，和元组不同，一个数组中的元素都具有相同类型 `T`，这些元素对象在栈中连续储存。数组的大小 `length` 在编译时确定。

```rust
let xs: [i32; 5] = [1, 2, 3, 4, 5];
let ys = [2.72, 3.14];  // 自动推断
let zs: [i32; 100] = [42; 100];  // 100 个 42 重复

println!("第一个元素下标为 0: {}, {}, {}", xs[0], ys[0], zs[0]);
println!("数组长度: {}", xs.len());
println!("最后一个元素: {}", ys[ys.len() - 1]);

-----output-----

第一个元素下标为 0: 1, 2.72, 42
数组长度: 5
最后一个元素: 3.14
```

数字访问越界，会在运行时 panic 退出：

```
thread 'main' panicked at 'index out of bounds: the len is 2 but the index is 4'
```

切片 `&[T]` 表示数组的一部分，一个切片对象由两个字组成：
- 指向底层数组的指针
- 切片的长度

```rust
fn analyze_slice(s: &[i32]) {
    println!("slice: first element = {}, length = {}", s[0], s.len());
}

fn main() {
    analyze_slice(&xs);  // 整个数组作为 slice
    analyze_slice(&zs[10 .. 30]);  // 取出一部分
}

-----output-----

slice: first element = 1, length = 5
slice: first element = 42, length = 20
```

