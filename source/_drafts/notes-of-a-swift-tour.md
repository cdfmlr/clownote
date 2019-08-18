---
title: notes_of_a_swift_tour
tags: Swift
---

# Notes of *A Swift Tour*

Swift 入门，学习 [A Swift Tour](https://docs.swift.org/swift-book/GuidedTour/GuidedTour.html#) 的笔记。

## Hello World

让 Swift 打印 "Hello, world!"

```swift
print("Hello, world!")
```

## Simple Values

### 常数 & 变量

* `let` 声明 **常数**
* `var` 声明 **变量**

```swift
let myConstant = 0
var myVariable = 1
myVariable = 2
```

### 类型

#### 声明类型

* 不指明类型，让 Swift 通过赋的初值来推测：

```swift
let implicitInteger = 70
let implicitDouble = 70.0
```

* 指明类型，可以给浮点数赋整形值（不能倒过来）：

```swift
let explicitDouble: Double = 70
```

指定了类型后可以暂时不赋初值：

```swift
var a: Int
a = 1
```

#### 类型转换

- 隐式转换

  在 Swift 中，值的类型**不会**被 *隐式* 转换。

  形如 `"Hello" + 123` 的代码会得到 *`error: binary operator '+' cannot be applied to operands of type 'String' and 'Int'`*

- 显式转换

  ```swift
  let label = "The width is "
  let width = 94
  let widthLabel = label + String(width)
  ```

- 在字符串中包含其他类型的值

  可以在字符串中包含 `\(<语句>)`，Swift 会计算出语句的返回值，插入字符串中：

  ```swift
  let apples = 3
  let oranges = 5
  let appleSummary = "I have \(apples) apples."		// I have 3 apples.
  let fruitSummary = "I hava \(apples + oranges) pieces of fruit."		// I hava 8 pieces of fruit.
  ```

  