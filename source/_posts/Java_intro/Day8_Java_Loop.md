---
categories:
- Java
- Beginning
date: 2019-04-19 16:37:53
tag: Java
title: Java-循环
---

# Java 循环

Java中有三种主要的循环结构：

* `while` 循环
* `do...while` 循环
* `for` 循环

## `while` 循环

```
while( 布尔表达式 ) {
    // 循环内容
}
```

## `do...while` 循环

```
do {
    // 循环内容
} while( 布尔表达式 );
```

## `for` 循环

和 C++ 11 一样，Java有两种 for 循环，一种是类似与 C 的：

```
for( 初始化; 布尔表达式; 更新 ) {
    // 代码语句
}
```

还有一种用于数组迭代的：

```
for(type element: array)
{
    System.out.println(element);
}
```

声明语句：声明新的局部变量，该变量的类型必须和数组元素的类型匹配。其作用域限定在循环语句块，其值与此时数组元素的值相等。
表达式：表达式是要访问的数组名，或者是返回值为数组的方法。

例如：

```java
public class Test {
   public static void main(String args[]){
      int [] numbers = {10, 20, 30, 40, 50};
 
      for(int x : numbers ){
         System.out.print( x );
         System.out.print(",");
      }
      System.out.print("\n");
      String [] names = {"James", "Larry", "Tom", "Lacy"};
      for( String name : names ) {
         System.out.print( name );
         System.out.print(",");
      }
   }
}
```

## 循环控制

`break`、`continue` 在 Java 中也同样有效。