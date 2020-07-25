---
categories:
- Java
- Beginning
date: 2019-04-21 16:37:53
tag: Java
title: Java-数组
---

# Java 数组

Java 语言中提供的数组是用来存储**固定大小**的**同类型元素**的。

## 声明数组变量

欲使用数组，首先必须声明数组变量，用来存放数组对象。

```java
dataType[] arrayRefVar;   // 首选的方法
/* 或 */
dataType arrayRefVar[];  // 效果相同，但不是首选方法，这种风格来自 C/C++，只是为了让 C/C++ 程序员能够快速理解java语言
```

## 创建数组

与其他类型相似，我们可以用 `new` 创建一个数组对象。

```java
arrayRefVar = new dataType[arraySize];
```

与 C 不同的是，arraySize 可以是一个变量，而不必使用字面值常量。

或者，如果我们预先知道了数组的内容，可以像 C 一样用 数组的字面值常量 (`{...}`) 来创建一个数组：

```java
String [] names;
names = {"James", "Larry", "Tom", "Lacy"};
```

正如其他类型的变量，我们常把声明和创建写在一起：

```java
dataType[] arrayRefVar = new dataType[arraySize];
```

## 使用数组

### 数组大小

对于一个数组 `arrayRefVar` ，我们可以使用 `arrayRefVar.length` 来获取其长度。

### 索引访问

数组的元素是通过索引访问的。数组索引从 `0` 开始 到 `arrayRefVar.length-1`。

例如，我们用一个长度为 n 的数组来表示出 *斐波那契数列* 的前 n 项，然后把它们输出：

```java
public class FibonacciArray {
	public static void main(String[] args) {
		// 创建数组
		int size = 10;
		int[] fib = new int[10];

		// 填装数列
		fib[0] = 0;
		fib[1] = 1;
		for (int i = 2; i < size; i++) {
			fib[i] = fib[i-1] + fib[i-2];
		}

		// 输出
		for (int i = 1; i < size; i++) {
			System.out.println(fib[i]);
		}
	}
}
```

### 数组迭代

正如上面的程序，我们常用循环来处理一个数组，我们可以使用传统的 for 或者是 for-each 循环来迭代一个数组：

```java
int arr[] = new int[5];
// for
for (int i = 0; i < arr.length; i++) {
    arr[i] = i * 2;
}
// for-each
for (int element: arr) {
    System.out.println(element);
}
```

### 数组与函数

我们可以把一个数组看成是和其他任何实例一样的对象，所以我们当然也可以把它当作参数传递给函数，或作为函数的返回值返回。

#### 数组作为函数的返回值

```java
public static int[] returnArray(int base) {
	int[] result = new int[10];
	for (int i = 0; i < result.length; i++) {
		result[i] = base << i;
	}
	return result;
}
```

#### 数组作为函数的参数

```java
public static void printArray(int[] arr) {
	for (int i: arr) {
		System.out.print(i + ", ");
	}
	System.out.print("\n");
}
```

事实上，我们常用到的 `main` 函数，就是使用数组作为函数的参数的良好例子。

`main` 是这样的：`public static void main(String[] args) { ... }`, 它接收一个 String 的数组作为参数，这个数组的元素就是在运行 java 程序时给出的命令行参数。
例如 `java Example.java Arg1 Arg2`，对应的args将是：`{"Arg1", "Arg2"}`。

参考示例代码 [ArrayAndFunction.java](./src/ArrayAndFunction.java)。


## 多维数组

我们可以声明一个元素是数组的数组，即多维数组。
例如：

```java
int a[][] = new int[2][3];
```

这将生成一个有两个元素的数组，这两个元素又分别是包含 3 个 int 的数组。

我们可以这样使用它：

```java
public class MultArr {
	public static void main(String[] args) {
		int a[][] = new int[2][3];
		for (int i = 0; i < a.length; i++) {
			for (int j = 0; j < a[i].length; j++) {
				a[i][j] = i*10 + j;
			}
		}
		for(int i[]: a) {
			for (int j: i) {
				System.out.println(j);
			}
		}
	}
}
```

## Arrays 类

`Arrays` 类（`java.util.Arrays`）是 Java 提供的一个处理数组的类，它包含了一系列常用的数组操作，可以对内建类型的数组方便地操作。

要使用 `Arrays` 类，首先要导入它，即在代码开头使用：

```java
import java.util.Arrays;
```

然后，就可以调用它的这些主要的方法：

* `Arrays.fill(ArrayObject, [begin, end,] Num)`

把 `Num` 赋值给 `ArrayObject` 中下标属于 `[begin, end)` (可选，缺省为整个数组) 的元素。

* `Arrays.sort(ArrayObject, [begin, end])`

对 `ArrayObject` 中下标属于 `[begin, end)` (可选，缺省为整个数组) 的元素排序。

* `Arrays.equals(Arr1, Arr2)`

判断数组 `Arr1` 和 `Arr2` 是否相同。

* `Arrays.binarySearch(ArrayObject, Key)`

在 数组 `ArrayObject` 中用 **二分搜索**（注意要排序后的才有意义）搜索值Key，
找到会返回首个对应的索引，
找不到会返回负值。

* `Arrays.toString(ArrayObject)`

用字符串来表示一个数组（如 `{1, 2, 3}` 表示为 `"[1, 2, 3]"`），
**返回**得到的字符串。

用例：

```java
import java.util.Arrays;

public class UseArrays {
	public static void main(String[] args) {
		int[] a = new int[5];
		int[] b = {9, 2, 1, 3, 7};

		// toString
		System.out.println(Arrays.toString(a));
		System.out.println(Arrays.toString(b));

		// fill
		Arrays.fill(a, 6);
		System.out.println(Arrays.toString(a));
		
		Arrays.fill(a, 2, 4, 8);
		System.out.println(Arrays.toString(a));

		// sort
		Arrays.sort(b, 1, 4);
		System.out.println(Arrays.toString(b));

		Arrays.sort(b);
		System.out.println(Arrays.toString(b));

		// equals
		System.out.println(
				Arrays.equals(a, a)
				);
		System.out.println(
				Arrays.equals(a, b)
				);

		// binarySearch
		System.out.println(
				Arrays.binarySearch(b, 3)
				);
		System.out.println(
				Arrays.binarySearch(b, 99)
				);
	}
}
```

输出：

```
[0, 0, 0, 0, 0]
[9, 2, 1, 3, 7]
[6, 6, 6, 6, 6]
[6, 6, 8, 8, 6]
[9, 1, 2, 3, 7]
[1, 2, 3, 7, 9]
true
false
2
-6
```

Arrays 类还有很多方法，可以参考 [官方文档](https://docs.oracle.com/javase/10/docs/api/java/util/Arrays.html)

---

相关代码:

* [FibonacciArray.java](./src/FibonacciArray.java)
* [ArrayAndFunction.java](./src/ArrayAndFunction.java)
* [MultArr.java](./src/MultArr.java)
* [UseArrays.java](./src/UseArrays.java)