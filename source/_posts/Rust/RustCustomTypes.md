---
categories:
- Rust
- Beginning
date: 2022-07-04 22:24:23.355340
tags: Rust
title: Rust 自定义类型
---
# Rust (3)自定义类型

> 学习 [Rust By Example 3. Custom Types](https://doc.rust-lang.org/stable/rust-by-example/custom_types.html)

Rust 自定义类型有结构体（`struct`）和枚举（`enum`）。

## 结构体

Rust 的结构体有三种：

- 单元结构体：没有字段的

  ```rust
  struct Unit;
  
  fn main() {
      let x = Unit; // 实例化单元结构体没有{}
      let y = Unit;
      println!("{:?}", x); // ❌ 单元结构体不能打印
      println!("{:?}", x == y); // ❌ 单元结构体不能比较
  }
  // 注: 在 struct Unit; 上面加一行 #[derive(Debug)] 是可以用 {:?} 打印出 Unit 来的。
  ```

- 元组结构体：一个有名字的元组，一个字段匿名的结构体

  ```rust
  #[derive(Debug)]
  struct Pair(i32, f32);
  
  fn main() {
      let pair = Pair(1, 0.1);  // 实例化元组结构体：圆括号传字段值
      println!("{:?}", pair);   // Pair(1, 0.1)
      println!("{:?} {:?}", pair.0, pair.1)  // .下标 取字段值：1 0.1
      
      let Pair(a, b) = pair;  // 解构
      println!("{:?} {:?}", a, b);  // 1 0.1
  }
  ```

- 正常的 C 语言风格的结构体

  ```rust
  #[derive(Debug)]
  struct Point {
      x: f32,
      y: f32,
  }
  
  fn main() {
      let p = Point{ x: 3.14, y: 6.28 };
      println!("{:?}", p);  // Point { x: 3.14, y: 6.28 }
      println!("{:?}", p.x + p.y);  // 9.42
      
      let Point{ x: x_edge, y: y_edge } = p;  // 解构
      println!("{:?} {:?}", x_edge, y_edge);  // 3.14 6.28
  }
  ```

注意元组结构体用圆括号 `()`，有字段命名的结构体用花括号 `{}`。

结构体可以通过解构，把字段绑定到变量：

```rust
let Pair(a, b) = pair;  // 元组结构体
let Point{ x: x_edge, y: y_edge } = p;  // C 结构体
```

结构体嵌套可以作为另一个的字段：

```rust
#[derive(Debug)]
struct Rectangle {
    top_left: Point,
    bottom_right: Point,
}

fn rect_area(rect: Rectangle) -> f32 {
    let Rectangle {                          // a ------ b
        top_left:     Point { x: a, y: b },  // |  rect  |
        bottom_right: Point { x: c, y: d },  // c ------ d
    } = rect;  // 解构也可以嵌套进行

    return (b - a) * (d - b);
}

fn main() {
    let rect = Rectangle {
        top_left: p,
        bottom_right: Point{x: 10.0, y: 15.0},
    };
    println!("{:?}", rect);  // Rectangle { top_left: Point { x: 3.14, y: 6.28 }, bottom_right: Point { x: 10.0, y: 15.0 } }
    println!("{:?}", rect.top_left.y);  // 6.28
    println!("{:?}", rect_area(rect));  // 27.380798
}
```

解构或者构造结构体的时候，如果`变量名`和`字段名`相同，则可以把 `name: name` 简写为 `name`：

```rust
fn square(top_left: Point, width: f32) -> Rectangle {
    let Point { x, y } = top_left;  // { x: x, y: y }
    return Rectangle {
        top_left,  // top_left: top_left
        bottom_right: Point {
            x: x + width,
            y: y + width,
        },
    };
}

fn main() {
    let s = square(Point { x: 1f32, y: 1f32 }, 3f32);
    println!("{:?}", s);  // Rectangle { top_left: Point { x: 1.0, y: 1.0 }, bottom_right: Point { x: 4.0, y: 4.0 } }
}
```

## 枚举

用 `enum`创建一个枚举，通过 `枚举名::种类` 访问枚举值。

Rust 的枚举里面的成员是各种 struct，也就是说 Rust 的枚举和 Swift 类似，可以不止是一个值，还可以带上一些参数数据。

```rust
enum WebEvent {
    PageLoad,  // 单元结构体
    KeyPress(char),  // 元组结构体
    Click { x: i64, y: i64 },  // 普通的结构体
}

fn inspect(event: WebEvent) {
    match event {  // switch-case
        WebEvent::PageLoad => println!("page loaded"),
        WebEvent::KeyPress(c) => println!("pressed '{}'", c),  // 解构出 char c
        WebEvent::Click { x, y } => {  // 解构出 x: i64, y: i64
            println!("clicked at x={}, y={}", x, y);
        }
    }
}

fn main() {
    let load = WebEvent::PageLoad;
    let pressed = WebEvent::KeyPress('x');
    let click = WebEvent::Click { x: 20, y: 80 };

    inspect(load);     // page loaded
    inspect(pressed);  // pressed 'x'
    inspect(click);    // clicked at x=20, y=80
}
```

### 简单整数枚举

也可以不用那种复杂的带参数的，而只是简单的名字对应整数值：

```rust
#[derive(Debug)]
enum Numbers { // 隐式值 0, 1, 2
    Zero,
    One,
    Two,
}

#[derive(Debug)]
enum Color { // 显式值
    Red = 0xff0000,
    Green = 0x00ff00,
    Blue = 0x0000ff,
}

// ❌ 只能是整形，浮点、字符串啥的都不行
// enum Strs {
//     A = "123",
//     B = "456"
// }

fn main() {
    println!("{:?} is {}", Numbers::Zero, Numbers::Zero as i32);
    println!("{:?} is {:#08x}", Color::Blue, Color::Blue as i32);
}
```

### 类型别名

给类型取绰号，和 Go 语言类似：

```rust
#[derive(Debug)]
enum VerboseEnumOfThingsToDoWithNumbers {
    Add,
    Subtract,
}

// 定义别名
type Operations = VerboseEnumOfThingsToDoWithNumbers;

impl Operations {
    fn run(&self, x: i32, y: i32) -> i32 {
        match self {
            Self::Add => x + y,  // Self 是 impl 中自动定义的一个别名
            Self::Subtract => x - y,
        }
    }
}

fn main() {
    let (x, y) = (10, 4);
    let op = Operations::Add;
    println!("{:?}({:?}, {:?}) == {:?}", op, x, y, op.run(x, y));
}
```

### use 声明

屑 `EnumName::KindName` 就很长很麻烦，可以用 use 声明把枚举值的名字“导入”进来，然后就不用写前缀 `EnumName::` 了。

```rust
use WebEvent::{KeyPress, PageLoad};  // 用其中几个
use WebEvent::*;  // 用枚举的全部值
use Operations::*;  // ❌ 别名不行，要写原本的名字

inspect(KeyPress('e'));
inspect(PageLoad);
```

### 用 enum 撸链表

这个例子有意思，不是 C 那种结构体字段做指针，在操作节点时，判断指针字段为 null 时做基准情况单独处理。这个是把 Nil 作为枚举的一种情况，然后正常的节点用 Lisp 那种 cons 嵌套穿起来，操作时用 match 分别处理有值和末尾情况。

```rust
#[derive(Debug)]
enum List {
    Cons(u32, Box<List>), // 一个 u32 元素，和一个指向下一节点的指针 (Box 是某种指针，以后学)
    Nil,                  // 末结点，表明链表结束
}

use List::*; // 可以直接用 Cons 和 Nil

impl List {
    fn new() -> List {
        Nil
    }

    // 头插
    fn prepend(self, elem: u32) -> List {
        Cons(elem, Box::new(self))
    }

    // 长度: 递归遍历链表
    fn len(&self) -> u32 {
        match *self {
            Cons(_, ref tail) => 1 + tail.len(), // 结构出当前元素 _ 和对下一节点 tail 的引用
            Nil => 0,
        }
    }

    fn stringify(&self) -> String {
        match *self {
            Cons(curr, ref tail) => {
                format!("{}, {}", curr, tail.stringify())
            }
            Nil => {
                format!("<Nil>") // format! 返回格式化的字符串
            }
        }
    }
}

fn main() {
    let mut list = List::new();

    list = list.prepend(1);
    list = list.prepend(2);
    list = list.prepend(3);

    println!("list: {:?}, len={}", list, list.len()); // list: Cons(3, Cons(2, Cons(1, Nil))), len=3
    println!("stringify: {}", list.stringify()); // stringify: 3, 2, 1, <Nil>
}
```

