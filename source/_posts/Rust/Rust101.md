---
date: 2022-10-03 15:15:55.262666
title: Rust101
---
# Rust 101

Rust 入门，笔记，集合：vol 1

---

## Hello World

```rust
// hello.rs
fn main() {
    println!("Hello, world!");
}
```

```sh
$ rustc hello.rs
$ ./hello
Hello, world!
```

---

`cargo`：包管理、项目组织构建

```sh
$ cargo new hello_cargo  # 新建项目

$ cd hello_cargo
$ vim src/main.rs

$ cargo run    # 运行代码
$ cargo build  # 编译：debug
$ cargo build --release  # 编译：release
```

---

## Rust 量

- 常量：`const` 始终不可变
- 变量：
  - `let`：默认不可变
  - `let mut`：只可变，类型不可变

---

**遮蔽**（shadow）：作用域内重新声明同名变量。

- 名不变
- 值/**类型**可变

```rust
{
    let foo = 1;         # i64: 1
    let foo = 2.0;       # f64: 2.0
    {
        let foo = "3";   # &str: "3"
    }
                         # f64: 2.0
}
```

---

## Rust 静态类型

> 静态类型：编译时确定所有变量的类型。

---

### Rust 标量

| 类型   | 类型                            | 说明                                                         |
| ------ | ------------------------------- | ------------------------------------------------------------ |
| 整型   | `i/u + size`：`i16`，`u32`，... | * `isize`: 由机器架构决定(64 位机：`isize=i64`)<br />* `usize`: 用作索引值 |
| 浮点型 | `f32`，`f64`                    | 默认 `f64`，IEEE 754 格式                                    |
| 布尔型 | `bool`：`true | false`          | 实际内存中用 1 个 byte 存储<br />冷知识：C 语言中的 bool 也要一字节 (1 byte)，不是一位 (1 bit) |
| 字符   | `char`                          | 4 byte：unicode                                              |

---

#### 算术

`+`，`-`，`*`，`/`，`%`，...

> 整数 `/`：向下取整

---

#### 整型：字面量

| 进制       | 字面量    |
| ---------- | --------- |
| 二         | `0b1011`  |
| 八         | `0o76`    |
| 十         | `114_514` |
| 十六       | `0xfe`    |
| 字节（u8） | `b'A'`    |

---

#### 整型：溢出

- debug：panic
- release：二进制补（正常溢出）or 其他可选行为

---

### Rust 复合类型

**元组** `()`

```rust
let tup: (i32, f64, u8) = (500, 6.4, 1);`
```

- 多种类型 多个值 放一起，长度固定
- 解构：`let (x, y, z) = tup;`
- 索引：`let x = tup.0;`
- 单元类型：`()`，单元值：`()` 
  - 表达式不返回 => `return ();`

---

**数组** `[]`

```rust
let a: [ i32 ;  5 ] = [1, 2, 3, 4, 5];
         类型   长度
```

- 相同类型，长度固定
- Repeat：`let a = [3; 5];` => 5 个 3
- 访问：`let first = a[0];`
  - 越界：runtime panic

---

**Tips**：用 `dbg!` 宏答应表达式的值到 stderr

```rust
let foo = dbg!(表达式);
           └──> 打印并返回值
```

---

## Rust 函数

```rust
fn 名(参, 数) 〔-> 返回类型〕 {
    语句
    ...
    〔返回值表达式〕  // 可选，无则 return ()
}
```

注：六角括号 `〔〕` 表示内容可选

---

### 语句 vs 表达式

- 语句：操作，不返回值
- 表达式：计算，产生返回值
  - 函数、宏调用，代码块 `{ ... }` 都是表达式

> 语句 = 表达式 + `;`

```rust
let y = {
    let x = 3;
    x + 1         // 整个代码块值为 4 所以 y = 4
}
```

---

## Rust 控制流

### if 条件

```rust
if 表达式 {           // 表达式必须返回 bool 值，不会隐式转换
    ...
} else if ... {
    ...
} else {
    ...
}
```

`if ` 是表达式，有返回结果：

```rust
let num = if cond { 5 } else { 6 };
```

---

### 循环

- `loop`：无限循环（可以 break 出来）
- `while`：`while 条件 { ... }`
- `for`：`for element in array { ... }`

---

`break`：退出并从循环返回值

```rust
let result = loop {
    counter += 1;
    if counter == 10 {
        break counter * 2;
    }
}
```

---

Range:

```rust
for n in (1..4).rev() {  // .rev() 把 Range 反转
    ...
}
```

---

## Rust 所有权

> 管理权（ownership）主要是管理堆数据

Rust 值的存放：

- stack：编译时已知固定大小的数据
- heap：编译时大小未知或不定的数据

---

**所有权规则**：

1. 每个值在任一时刻都有且只有一个所有者（owner）变量
2. owner 离开作用域，值被丢弃（调用 drop 函数进行销毁）

---

### 移动 vs 克隆

栈值克隆：

```rust
let x = 5;
let y = 5;

// 栈中压入两个独立的 5 值
// 自动复制：一定是深拷贝
```

堆值移动：

```rust
let s1 = String::from("hello");
let s2 = s1;    // 值从 s1 移动到了 s2

// s1 不再可用：避免 double free
// Rust 没有浅拷贝：只移动，不拷贝
```

---

**自动复制**一定是运行时对性能影响小的**深拷贝**。

要克隆堆值，必须使用显式的深拷贝：

```rust
let s1 = String::from("hi");
let s2 = s1.clone();
```

---

#### trait: Copy & Drop

实际上，起决定作用的并不是“栈值”、“堆值”，而是看类型实现了那种 trait（二选一）：

- `Copy`：可克隆

  ```rust
  let new = old;
  // 之后 old 仍可用
  ```

- `Drop`：要移动

  离开作用域时，值被 drop


> 标量（整浮布字）都 impl 了 Copy；
>
> 元组所有元素 Copy，则元组 Copy；

---

### 所有权 & 函数

值传给函数：同赋值：

- Copy 的复制
- Drop 的移动：值移动到了 fn 里：外面（调用后面）不能用了

```rust
let i = 42;
let s = String::from("hi");

function(i, s);

println!("{}", i);  // ✅
println!("{}", s);  // ❌
```

---

#### 引用、借用

**引用**：类似于 C 的指针

- 引用：`&`
- 解引用：`*`

```rust
let s = String::from("hi");
let l = len(&s);

fn len(s: &String) -> usize {
    s.len()  // == (*s).len()
}
```

**借用**：传 `&s` 不让函数拥有 s 的所有权

- 函数 end，离开作用域 => 不 drop 值

---

#### 可变引用

- `&s` 只读引用
- `&mut s` 可用于修改 s 的值

```rust
let mut s = String::from("hello ");
change(&mut s);    // 形实都要加 mut

fn change(s: &mut String) {
    s.push_str("world");
}
```

---

同一时间，一个数据只能有**多个只读引用**或**一个可变引用**。

| 变 + 变 | 不变 + 变 | 不变 + 不变 |
| ------- | --------- | ----------- |
| ❌       | ❌         | ✅           |

=> （在编译时）避免（并发时） data race 

```rust
let mut s = String::from("hi");

{ let r0 = &mut s; }  // r0 离域，不再存在
let r1 = &mut s;      // ✅ r1 一个 &mut
let r2 = &mut s;      // ❌ r1、r2 两个 &mut
```

---

**非词法作用域生命周期**（Non-Lexical Lifetime，NLL）

> 引用的作用域是「声明 -> 最后一次使用」。

∴ 可以：

```rust
let ir = &s;
println!("{}", &ir);  // ir 不再使用：声明周期结束
let mr = &mut s;      // ✅
println!("{}", &mr);
```

---

### 悬垂引用

悬垂（dangling）引用：指向已释放的内存的引用。

=> Rust 直接编译时 Error

```rust
fn d() -> &String {
    let s = &String::from("hi");
    &s    // ❌ s 离开作用域即被 drop，&s 悬垂
}
```

---

### slice

**切片**（slice）：**引用**集合中的一段连续的元素。

```rust
let s = String::from("hello world");
let hello= &s[0..5];  // [0, 5)
// hello: &str => String 的 slice 是 &str
s.clear()  // ❌ 这个方法借 &mut s,
           //    但 hello 是借了个 immut
           //    immut + mut -> error
```

切片是一个不可变引用，结合“不能变+不变”的引用规则

=> 保证 slice 始终可用、未变。

---

字符串常量：

- 类型： `&str`
- 指向二进制程序中的某位置

> 一般处理字符串的函数都用 `fn f(s: &str)`
>
> 这样传参 `String` 对象和 `&str` （包括字面量）都可。

---

## Rust struct

### 一般结构体

定义：

```rust
struct User {
    email: String
    age:   u8
}
```

实例化：

```rust
let mut foo = User {
    email: String::from("foo@bar.com"),
    age:   8,
};

println!("{}", foo.email);
foo.email = String::from("changed@bar.com");
```

---

语法糖：变量名与字段同名 => 简写

 `{foo: foo, } => {foo, }`

```rust
fn build_user(email: String, age: u8) -> User {
    User {
        email,
        age,
    }
}
```

---

**结构体更新语法**

```rust
let user2 = User {
    email: String::from("user2@bar.com"),
    ..user1,    // 除了显式写的 email 字段，其余用 user1 的值
}
```

- 若 `user1` 中的 Drop 值被 `user2` 使用，则等于移动到了 `user2`，`user1` 不再可用；
- 若 `..user1` 只用了 `user1` 中的 Copy 值，则之后 `user1` 仍然可用：
  - User 中全是 Copy
  - 或 Drop 值全被显式给出

---

### 元组结构体

元组结构体：无字段名，匿名结构体。

```rust
struct Color(i32, i32, i32);

let red = Color(255, 0, 0);
```

访字段（同元组）：

- 解构：`let (r, g, b) = red;`
- 索引：`let r = red.0;`

---

**类单元结构体**（unit-like struct）

```rust
struct Foo;

let s = Foo;
```

---

### 方法

```rust
struct Foo {
    ...
}

impl Foo {
    fn bar(&self, ...) -> ... {
        ...
    }
}

fn main() {
    let foo = Foo{ ... };
    foo.bar();
}
```

---

**方法可以和字段重名**：

区别 -> 调用时：

- `foo.bar` 是字段
- `foo.bar()` 是方法

用于做 getter。

---

**自动（解）引用**

```rust
foo.bar()
```

会自动加上：

```rust
(&foo).bar()
(&mut foo).bar()
(*foo).bar()
```

使之匹配方法的 self 参数签名。

---

### 关联函数

- `impl` 中定义
- 首参非 `self`
- 调用通过 `::`

常用来做构造函数：

```rust
imple Foo {
    fn new() -> Foo {
        ...
    }
}

let foo = Foo::new();
```

---

## Rust 枚举

成员可带有值：

```rust
enum IpAddr {
    V4(u8, u8, u8, u8),
    V6(String),
}

let loopback = IpAddr::V6(String::from("::1"));
```

---

枚举可作为参数：

```rust
fn route(ip: IpAddr) {
    ...
}

let loopback = IpAddr::V6(String::from("::1"));
route(loopback)
```

---

枚举可实现方法：

```rust
impl IpAddr {
    fn call(&self) {
        ...
    }
}

ip.call();
```

---

### Option

- Rust 没有空值
- 用 `Option<T>` 表示可能为空的东西

```rust
enum Option<T> {
    Some(T),
    None,
}
```

该类型会 prelude，不用导入：可以忽略前缀(`Option::`)直接用 `Some`、`None`。

```rust
let some_number = Some(5);
let absent: Option<i32> = None;
```

---

### match

> match: switch-case in Rust.

```rust
match ip {
    IpAddr::V4(a, b, c, d) => {
        println!("{}", a);
        d
    },
    IpAddr::V6(addr) => addr.len(),
    _ => 0,    // default 分支
}
```

- match 是表达式：有返回值
- match 需要穷举：用 `_ => ...` 加默认分支

（没有返回值默认分支可以返回单元值：`_ => ()`）

---

用 match 处理 Option：

```rust
fn plus_one(x: Option<i32>) -> Option<i32> {
    match x {
        None => None,
        Some(i) => Some(i + 1),
    }
}
```

---

### if let

`if let` 只匹配一个模式，忽略其他。

```rust
let some_val = Some(10);

match some_val {
    Some(3) => println!("3"),
    _ => (), // 繁冗
}
```

改为：

```rust
if let Some(3) = some_val {
    println!("3");
}
```

后面还可以加 `else { ... }`

---

## Rust 项目：模块系统

一个 package 包含一或多个 crate：

```rust
         ╭
         │ Cargo.toml
         │
package ╶┤ bin crate  *  ╮
         │               ├╴ +
         │ lib crate  ?  ╯
         ╰
```

> | `*`        | `?`      | `+`      |
> | ---------- | -------- | -------- |
> | 一个或以上 | 零或一个 | 一个以上 |

---

### crate

bin crate：

- `src/main.rs`：一个与 package 同名的二进制可执行
- `src/bin/*`：多个 bin crate

lib crate：

- `src/lib.rs`：一个与 package 同名的库
- 可用 `cargo new --lib name` 新建库项目

---

### mod

模块层次：

```rust
crate    // 可以看作一个 root mod
   ├╴ [pub] mod
   │         ├╴ [pub] mod
   │         ├╴ [pub] fn | struct | enum
   │         └╴ ...
   ├╴ [pub] fn | struct | enum
   └╴ ...
```

- mod、fn：无 pub 则私有
- struct：任一成员都需显式 pub 才公开
- enum pub 则所有成员都公开

---

#### 实现：单文件

e.g. `src/lib.rs`

```rust
pub mod front_of_house {
    pub mod hosting {
        pub fn add_to_waitlist() {
            ...  // 内部路径：可用 super 进父
        }
    }
}

pub fn foo() {
    // 绝对路径：crate 开头
    crate::front_of_house::hosting::add_to_waitlist();
    
    // 相对路径
    front_of_house::hosting::add_to_waitlist();
}
```

---

#### 实现：多文件

- 每个文件一个模块
- 文件路径（`src/foo/bar.rs`）即模块路径（`crate::foo::bar`）
- `mod NAME;` 导入其他文件模块

就是把前面单文件中嵌套的 mod，改成同名文件、目录（注意，这样是通过文件名导入，文件中不写 `mod NAME { ... }`）

---

e.g. 多文件多模块

```rust
foobar
 ├── Cargo.toml
 └── src
     ├── foo
     │   └── bar.rs
     ├── foo.rs
     └── main.rs
```

---

`src/main.rs`:

```rust
mod foo;

fn main() {
    foo::fuzz();
    foo::bar::buzz();
}
```

`src/foo.rs`：

```rust
pub mod bar;

pub fn fuzz() {
    println!("fuzz from foo.rs");
}
```

`src/foo/bar.rs`：

```rust
pub fn buzz() {
    println!("buzz from foo/bar.rs");
}
```

---

### use

相当于把东西软连接到当前模块：

```rust
use crate::front_of_house::hosting 〔as front_hosting〕;
                                          取新名
fn bar() {
    hosting::add();
    // 相当于 crate::front_of_house::hosting::add();
}
```

---

一般 use 到：

- fn 所在的 mod（`use xxx::hosting` 而不是 `use xxx::hosting::add()`）

- struct、enum 导到类型：

  ```rust
  use std::collections:HashMap;
  
  fn main() {
      let mut map = HashMap::new()
  }
  ```

---

简写 use：合并公共路径

```rust
use std::{ cmp::Ordering, io };

// use std::cmp::Ordering;
// use std::io;
```

```rust
use std::io::{self, Write};

// use std::io;
// use std::io::Write;
```

```rust
use std::collections::*;
                      └> glob 运算符
// 导入 std::collections 中的所有 pub 项：慎用！！
```

---

### 外部包

1. 标准库：

```rust
use std::----;
```

2. 第三方包：

    ```rust
    use rand::Rng;  
    ```

    需要在 `Cargo.toml` 中定义：

    ```toml
    [dependencies]
    rand = "0.8.3"
    ```

---

## Rust 集合

- vector
- string
- HashMap

---

### vector

`Vec<T>`，变长数组，固定类型 T，但是 T 可以用 enum 来放多种值。

新建：

```rust
let mut v1: Vec<i32> = Vec::new();

let v2 = vec![1, 2, 3];
```

---

栈式访问（需要 mut）：

```rust
v.push(5);

let last = v.pop();
```

随机访问：

```rust
let third: &i32 = &v[2];
// 下标不存在会 panic
// 这里借了个 immut 引用，之后整个 v 不可 mut
```

---

遍历：

```rust
for i in &v {
    println!("{}", i);
}

for i in &mut v {
    *i += 10;
}
```

---

### string

- `&str`：字符串切片 -> 语言核心中的
- `String`：标准库提供的一种 utf-8 字符串实现

```rust
let mut s1 = String::new();
let     s2 = "hello".to_string();
let     s3 = String::from("hello");
```

---

⚠️ 注意 String 不支持索引：`s[0]` ❌

- String 是 Vec<u8> 的封装
- Rust 保证索引运算的时间复杂度是 `O(1)`
- utf-8 按字节切不合理，按字符切慢，所以不能索引

---

遍历：

```rust
for c in "...".chars() {
    println!("{}". c);
}
```

```rust
for b in "...".bytes() {
    ...
}
```

---

尾加：

```rust
s.push('l');        // 字符

s.push_str("bar");  // &str
// 注：String 可以自动转为 &str，所以这里也能传 String 对象
//    deref coercion: &s -> &s[..]
```

```rust
let s1 = String::from("foo");
let s2 = String::from("bar");
let s3 = s1 + s2;  // fn add(self, s: &str) -> String
// s1 被移动不再可用，但 s2 还能用
```

```rust
let s = format!("{} {} {}", s1, s2, s3);  // fmt.Sprintf
```

---

### HashMap

`HashMap<K, V>`：哈希表

```rust
use std::collections::HashMap;  // 需要导入

let mut scores = HashMap::new();
scores.insert(String::from("Blue"), 10);
              // 非 Copy 值入 HashMap 会移动 owner
```

---

From zip：

```rust
let keys = vec![String::from("Blue"), String::from("Red")];
let vals = vec![10, 50];
let scores = HashMap<_, _> = keys.iter().zip(vals.iter()).collect();
             // HashMap 的类型标注是必须的
             // 因为 collect 可以产出多种类型
             // 但 K 和 V 的类型可以推断
```

---

取值：

```rust
let team = String::from("Blue");
let s = scores.get(&team);  // -> Option<V>
```

遍历：

```rust
for (key, value) in &scores {
    ...
}
```

---

Insert if not exists:

```rust
scores.entry(String::from("Yellow")).or_insert(50);
```

改旧值：

```rust
let text = "hello world wonderful world";
for word in text.split_whitespace() {
    let count = map.entry(word).or_insert(0); // -> &mut V
    *count += 1;
}
```

---

## Rust 错误处理

- panic：不可恢复

- Result: 可恢复

---

### panic

```rust
fn main () {
    panic!("crash");
}
```

`panic!` 宏会导致：

- 展开：回溯栈，逐步清理
- 终止：直接退，留给 OS 清理

默认是展开，终止要在 `Cargo.toml` 中设：

```toml
[profile.release]
panic = 'abort'
```

---

### Result

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

---

用 match 处理 enum：

```rust
use std::fs::File;
fn main() {
    let f = File::open("hi.txt"); // -> Result<File, io::Err>
    let f = match f {
        Ok(file) => file,
        Err(error) => {
            panic!("problem opening file: {:?}". error)
        }
    };
}
```

---

Ok 取值，Err panic 这个模式很常用，所以有化简：

```rust
let f = File::open("hi.txt").unwrap(); // Err => panic

let f = File::open("hi.txt").expect("自定义panic信息");
```

还可以用闭包自定义处理：

```rust
let f = File::open("hi.txt").unwrap_or_else(|error| {
    if error.kind() == Errorkind::NotFound {
        File::create("hi.txt").unwrap_or_else(|error| {
            panic("...");
        })
    } else {  // 不是 NotFound
        panic("...");
    }
});
```

---

#### 错误传播

错误传播：把 Result 继续向上返回给调用者。

```rust
fn open_file () -> Result<File, io::Error> {
    let f = File::open("hi.txt");
    let f = match f {
        Ok(file) => file,
        Err(e) => return(e),
    };
}
```

简写：

```rust
let f = File::open("hi.txt")?;
// ? 运算符：只能用于返回 Result 的 fn
```

---

在 main 中用 `Result` 和 `?`：

```rust
fn main() -> Result<(), Box<dyn Error>> {
    let f = File::open("hi.txt")?;
}
```

---

## Rust 泛型

```rust
fn largest<T>(list: &[T]) -> T {...}
```

```rust
struct Point<T, U> {
    x: T,
    y: U,
}
```

```rust
enum Option<T> {
    Some(T),
    None,
}
```

---

泛型 x 方法：

```rust
impl<T> Point<T> {
    fn x(&self) -> &T {
        &self.x
    }
}
```

只对某种特定类型实现：

```rust
impl Point<f32> {
    fn distance(&self) -> f32 {
        ...
    }
}
```

---

## Rust trait

> trait：定义共享的行为（类似于 interface）

---

定义 trait：

```rust
pub trait Summary {
    fn summarize(&self) -> String;
}
```

---

实现 trait：

```rust
pub struct Foo { ... }

impl Summary for Foo {
    fn summarize(&self) -> String { ... }
}
```

注意：impl 后面的 trait 或 for 后面的类型，其中之一必须定义在本地作用域：

> 不能为外部类型实现外部 trait

---

默认实现：定义 trait 时写一种通用的实现

```rust
pub trait Summary {
    fn summarize(&self) -> String {
        ...
    }
}
```

---

trait 作为参数：

```rust
pub fn notify(item: impl Summary) { ... }

// 同时要求实现多个 trait 用 + 连接：
pub fn notify(item: impl Summary+Display) { ... }
```

```rust
pub fn notify<T: Summary+Display>(item: T) { ... }
```

```rust
fn f<T, U> (t: T, u: U) -> i32
    where T: Display + Clone,
          U: Clone + Debug
{
    ...
}
```

---

## Rust 生命周期

> 引用的 Lifetime 

---

```rust
let r;                 ─┐'a
{                ─┐'b   │
    let x = 5;    │     │
    r = &x;       │     │
}                ─┘     │
println!("{}", r);     ─┘
```

❌ `r` 在 `'a`，但引用了更小的 `'b`

---

```rust
let x = 5;               ─┐'b
let r = &x;         ─┐'a  │
println!("{}", r);  ─┘   ─┘
```

✅ `r` 在 `'a`，引用更大的 `'b` 中的 `x`

---

### 生命周期标注

生命周期标注：告诉编译器一个引用是从哪里借过来的。

---

### 函数生命周期标注

函数生命周期标注：告诉返回的引用时从哪个参数借来的。

```rust
fn main () {
    let s1 = String::from("hi");
    let s2 = "hello";
    
    let r = longest(s1.as_str(), s2);
    println!("{}". r);
}
```

TODO：实现 `longest` 函数。

---

```rust
fn longest(x: &str, y: &str) -> &str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}
```

❌ 不能编译！

- 返回的引用不知道是从 `x` 还是 `y` 借来的
- 生命周期不能确定

---

使用泛型标注：

```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    ...
}
```

- 用泛型语法声明一个 lifetime 标注
- 标注 `x`、`y` 都是生命周期 `'a` (Rust 会取二者中较小的)
- 标注返回值的 lifetime 也是 `'a`

---

调用时：

```rust
✅ {
    let s1
    {
        let s2                   ─┐'a
        let r = longest(s1, s2);  │
        print r                  ─┘     
    }
}
```

```rust
❌ {
    let s1
    let r;
    {
        let s2                   ─┐'a
        r = longest(s1, s2);      │
    }                            ─┘
    print r  // 较小的 'a 已经结束了
}
```

---

使用标注：必须让返回值与参数关联（必须在参数、返回值中同时出现）

```rust
fn f<'a>(x: &str, y:&str) -> &'a str {...}
// ❌ 'a 只在返回值有
```

若返回值生命周期与参数无关（说明不是借来的），则应该返回具有所有权的东西，而非引用。

---

### 结构体生命周期标注

包含引用的 struct 应在泛型列表中加类型标注：

```rust
struct E<'a> {
    part: &'a str,
}

impl<'a> E<'a> {
    fn foo(&self) -> i32 { ... }
}

fn main() {
    let n = String::from("call some fn");
    let first_word = n.split(' ')
        .next()
        .expect("could not find a space");
    let i = E{ part: first_word };
    // 必须在 E 用完后，n 再离域
}
```

---

### 生命周期省略

省略规则：

1. 每个引用参数都拥有自己的 lifetime；

   ```rust
   fn f(x: &str)          => fn f<'a>(x: &'a str)
   fn f(x: &str, y: &str) => f<'a, 'b>(x: &'a str, y: &'b str)
   ```

2. 若只有一个输入 lifetime，则输出 lifetime 与之同；

   ```rust
   fn f(x: &str) -> &str 
     ⬇️
   fn f<'a>(x: &'a str) -> &'a str
   ```

3. 若有一个参数是 `&self` 或 `&mut self`，即函数是一个方法，则输入 lifetime 与 self 同；

   ```rust
   规则 3 就是说：方法产出的 lifetime 同 self。
   ```

---

使用规则，一步步走，若推断出了输出的生命周期则结束：

```rust
fn f(s: &str) -> &str
  ⬇️ 规则 1
fn f<'a>(s: &'a str) -> &str
  ⬇️ 规则 2
fn f<'a>(s: &'a str) -> &'a str
  ✅ 推断成功完成：可以省略生命周期标注
```

```rust
fn f(x: &str, y: &str) -> &str
  ⬇️ 规则 1
f<'a, 'b>(x: &'a str, y: &'b str) -> &str
  ⬇️ 规则 2
❌ 不符合规则 2：不只一个输入
   不可省略标注，必须手写。
```

---

### 静态生命周期

```rust
let s: &'static str = "hello";
```

让引用在整个程序中始终可用。

（实际上：`&str` 字面量自带 `'static`）

---

## Rust 测试

```rust
#[test]    // test 属性标注 
fn it_works() {
    assert_eq!(2+2, 4);
}
```

```sh
$ cargo test
```

---

测试手段：**断言**

```rust
assert!(BOOL,  "fmt", args...)
       布尔测试  自定义失败信息

assert_eq!(A, B, ...)
assert_ne!(A, B, ...)
```

---

测试手段：**panic**

```rust
panic!("...")  // => test FAILED
```

期望 panic （不 panic 则 failed）：

```rust
#[test]
#[should_panic(expected="可选参数：期望特定 panic 信息")]
fn foo() {
    ...
}
```

---

测试手段：**Result**

- `Ok` 则测试通过
- `Err` 则 FAILED

```rust
#[test]
fn it_works() -> Result<(), String> {
    if 2 + 2 == 4 {
        Ok(())
    } else {
        Err(String::from("..."))
    }
}
```

---

**控制测试运行**：

```sh
$ cargo test  TARGET  --  --option
 给 cargo test 的参数 <-｜-> 给测试二进制的参数
                     分隔
```

- `TARGET`：测试目标：
  - 函数全名
  - 部分名称：run 所有包含该词的
- `--option`：
  - `--test-threads=1` 单线程
  - `--show-output` 显示 stdout

---

**忽略测试：**

```rust
#[test]
#[ignore]
fn expensive_test() { ... }
```

- 用 `cargo test` 会忽略该测试
- 用 `cargo test --ignored` 专门跑标记了 ignore 的测试

---

### 测试的组织

- 单元测试：测私：在隔离环境，一次一个功能
- 集成测试：测公：以外部视角，一次测多个

---

#### 单元测试

与待测代码在同一个文件中，搞一个 tests 子模块：

```rust
fn foo(a: i32) -> i32 {  // 业务代码：待测
     ... 
}

#[cfg(test)]  // 只有在 cargo test 时才编译
mod tests {
    use super::*;  // 导入待测
    
    #[test]
    fn foo_test() {  // 测试函数
        ...
    }
}
```

---

#### 集成测试

建个单独的 tests 目录，与 `src` 同级：

```sh
.
├── Cargo.toml
├── src
│   └── lib.rs
└── tests
    └── integration_test.rs
```

`integration_test.rs`：

```rust
use adder; // 待测 lib

#[test]
fn it_adds_two() {
    assert_eq!(5, adder::add_two(3));
}
```

- `cargo test` 测试所有单元、集成测试
- `cargo test --test FILE_NAME_WITHOUT_RS` 测试某集成 test 文件

---

集成测试模块中的通用代码：

```rust
// tests/common/mod.rs
pub fn setup() {
    ...
}
```

在其他 test 文件中调用：

```rust
use adder;
mod common;

#[test]
fn it_adds_two() {
    common::setup();
    ...
}
```

---

二进制 crate 的集成测试：

- `tests` 目录下不能拿 `src/main.rs` 中的代码
- 所有功能写在 `lib.rs`，成为一个可测试的库（库与 crate 同名）
- `tests` 中测试 `lib.rs`
- `main.rs` 只简单调用 `lib.rs`，无需再测

```rust
.
├── Cargo.toml
├── src
│   ├── lib.rs  # 主要功能封装成函数库
│   └── main.rs # 调用 lib.rs 中的函数
└── tests
    └── integration_test.rs  # 测 lib.rs
```

---

## 实例：minigrep

```sh
minigrep
├── Cargo.toml
└── src
    ├── lib.rs
    └── main.rs
```

---

`main.rs`：

```rust
use std::env;
use std::process;

use minigrep::Config;

fn main() {
    let args: Vec<String> = env::args().collect();

    let config = Config::new(&args).unwrap_or_else(|err| {
        eprintln!("Problem parsing arguments: {}", err);
        process::exit(1);
    });

    if let Err(e) = minigrep::run(config) {
        eprintln!("Application error: {}", e);
        process::exit(1);
    }
}
```

---

具体功能 `lib.rs`：

```rust
use std::error::Error;
use std::env;
use std::fs;

pub struct Config {
    pub query: String,
    pub filename: String,
    pub case_sensitive: bool,
}

impl Config {
    pub fn new(args: &[String]) -> Result<Config, &'static str> {
        if args.len() < 3 {
            return Err("not enough arguments");
        }

        let query = args[1].clone();
        let filename = args[2].clone();

        let case_sensitive = env::var("CASE_INSENSITIVE")
            .is_err(); // 未设置是 Err

        Ok(Config { query, filename, case_sensitive })
    }
}

pub fn run(config: Config) -> Result<(), Box<dyn Error>> {
    let contents = fs::read_to_string(config.filename)?;

    let results = if config.case_sensitive {
        search(&config.query, &contents)
    } else {
        search_case_insensitive(&config.query, &contents)
    };

    for line in results {
        println!("{}", line);
    }

    Ok(())
}

pub fn search<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    let mut results = Vec::new();

    for line in contents.lines() {
        if line.contains(query) {
            results.push(line);
        }
    }
    results
}

pub fn search_case_insensitive<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    let query = query.to_lowercase();
    let mut results = Vec::new();

    for line in contents.lines() {
        if line.to_lowercase().contains(&query) {
            results.push(line);
        }
    }
    results
}

```

---

单元测试：`lib.rs`

```rust
#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn case_sensitive() {
        let query = "duct";
        let contents = "\
Rust:
safe, fast, productive.
Pick three.
Duct tape.";

        assert_eq!(
            vec!["safe, fast, productive."],
            search(query, contents)
        );
    }

    #[test]
    fn case_insensitive() {
       let query = "rUsT";
       let contents = "\
Rust:
safe, fast, productive.
Pick three.
Trust me.";
       assert_eq!(
           vec!["Rust:", "Trust me."],
           search_case_insensitive(query, contents)
        );
    }
}
```

