---
title: Java-9-条件
date: 2019-04-20 16:37:53
tag: Java
categories:
	- Java
	- Beginning
---

# Java 条件语句

## if-else 语句

Java 的 `if` 条件语句和 C 完全一致。

```java
if (expression_0) {
    // statements
} else if (expression_1) {
    // statements
} else {
    // statements
}
```

~~无需解释~~

## switch-case 语句

```java
switch(expression){
    case value_0 :
       //语句
       break;   //可选
    case value_1 :
       //语句
       break;   //可选
    //你可以有任意数量的case语句
    default :   //可选
       //语句
}
```

Java 中的 `switch` 大体上和 C 的相同，但也有不同的地方。值得一提的是如下几点：

* 同 C 一样，
    * case 语句中的值的数据类型必须与变量的数据类型相同，而且只能是常量或者字面常量。
    * 同时需要注意 `case` 后一直执行到 `break` 才会停止（或者执行到全部结束），不会在一个 case 结束后自动停止！
* 与 C 不同的是，
    * Java 中 `switch` 后面的 expression 可以是 `byte`、`short`、`int` 或者 `char`。从 Java SE 7 开始，switch 支持字符串 `String` 类型了。