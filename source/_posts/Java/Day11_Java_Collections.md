---
title: Java-11-集合
date: 2019-04-22 16:37:53
tag: Java
categories:
	- Java
	- Beginning
---

# Java 集合

> 大多数真实应用程序都会处理像文件、变量、来自文件的记录或数据库结果集这样的集合。

最常见的集合就是数组，我们之前已经单独讨论过它，现在我们主要研究其他的集合类型。

## 列表 `List`

`List` 是一种有序集合，也称为*序列*。

`List` 集合只能包含对象（不能包含像 `int` 这样的原语类型）。

要使用 List，我们需要先把它 import 到程序中：

```java
import java.util.List;
```

`List` 是一个接口，所以不能直接实例化它（即，不可以 `new List<E>` ！），要声明一个 `List` ，使用如下语法：

```java
List<String> listOfStrings = new ArrayList<String>();
```

或

``` java
List<String> listOfStrings = new ArrayList<>();
```

这样，我们声明了一个种比较常用的 List —— `ArrayList`。

> 【注】
> 1. 要使用上面的代码，首先要 ：
> ```java
> import java.util.List;
> import java.util.ArrayList;
> ```
> 2. 我们将 `ArrayList` 对象赋给了一个 `List` 类型的变量。在 Java 编程中，可以将某种类型的变量赋给另一种类型，只要被赋值的变量是赋值变量所实现的超类或接口。

### 正式类型

前面的代码段中尖括号（ `<>`） 中的类型被称为*正式类型（formal type）*，即这个 List 是一个包含何种类型的集合。

如前例中正式类型为 `String`，这个`List` 仅能包含 `String` 实例。

如果把正式类型写为`<Object>`，就意味着可将任何实体放在该 `List` 中。

### 使用列表

- 将实体放入  `List`  中
  * `add(E element)` 方法将元素 element 添加到 `List` 的末尾处。
  * `add(int index, E e ` 方法将元素 element 添加到 `List` 的索引为 `index` 处（`index <= List.size()`）。
- 询问  `List` 目前有多大
  - 要询问 `List` 有多大，可调用 `size()`
- 从  `List` 中获取实体
  - 要从 `List` 中**检索**某一项，可调用 `get()` 并向它传递想要的项的索引
- 从  `List` 中删除实体
  - 要从 `List` 中**删除**某一项，可调用 `remove()` 并向它传递想要的项的索引

```java
Logger l = Logger.getLogger("Test")
// 声明 List
List<Integer> listOfIntegers = new ArrayList<>();
// 插入数据
listOfIntegers.add(Integer.valueOf(238));
listOfIntegers.add(0, Integer.valueOf(987));
// 查看大小
l.info("Current List size: " + listOfIntegers.size());
// 获取元素
l.info("Item at index 0 is: " listOfIntegers.get(0));
// 删除元素
listOfIntegers.remove(0);
```

相关代码: [UsrList.java](./src/UsrList.java)

关于 List 的更多说明，详见 [JDK文档](https://docs.oracle.com/en/java/javase/12/docs/api/java.base/java/util/List.html)。

## 迭代变量 `Iterable`

如果一个集合实现了 `java.lang.Iterable`，那么该集合被称为*迭代变量集合*。

 `Iterable` 可从一端开始，逐项地处理集合，直到处理完所有项。

它的使用形式就是在 循环 中提及过的 for-echo 循环：

```java
for (objectType varName : collectionReference) {
    // Start using objectType (via varName) right away...
}
```

因为 `List` 扩展了 `java.util.Collection`（它实现 `Iterable`），所以可以使用简写语法来迭代任何 `List` :

``` java
List<Integer> listOfIntegers = obtainSomehow();
Logger l = Logger.getLogger("Test");
for (Integer i : listOfIntegers) {
    l.info("Integer value is : " + i);
}
```

这段代码实现的效果和如下的 for 循环处理等效：

```java
List<Integer> listOfIntegers = obtainSomehow();
Logger l = Logger.getLogger("Test");
for (int aa = 0; aa < listOfIntegers.size(); aa++) {
    Integer I = listOfIntegers.get(aa);
    l.info("Integer value is : " + i);
}
```

## 集 `Set`

`Set` 是一种没有重复元素的集合结构。它可保证其元素中的唯一性，但不关心元素的顺序。

`List` 可包含同一个对象数百次，而 `Set` 仅可包含某个特定实例一次。

`Set` 也仅可包含对象，不能直接包含内置类型。

与 `List` 一样，不能直接实例化 `Set` (不能 `new Set<E>()`) ，但可以用继承自 `Set` 的 `HashSet` 等来实现。

#### 操作 `Set`

* 增
  * `add(E e)`
* 删
  * `remove(Object o)`
* 获取大小
  * `size()`
* 获取实体
  * 使用在 "迭代变量 (`Iterable`)" 中介绍的 for-each 循环可以把元素从 `Set` 中取出来。但注意对象可能按照不同于添加它们的顺序打印被取出来。

``` java
import java.util.Set;
import java.util.HashSet;
import java.util.logging.Logger;

public class TrySet {	
	public static void main(String[] arg) {
		Logger l = Logger.getLogger("Tset");

		Set<Integer> setOfIntegers = new HashSet<>();

		setOfIntegers.add(Integer.valueOf(12));
		setOfIntegers.add(Integer.valueOf(20));
		setOfIntegers.add(Integer.valueOf(5));
		
		setOfIntegers.add(Integer.valueOf(5));

		l.info(setOfIntegers.toString());

		setOfIntegers.remove(Integer.valueOf(20));

		l.info("" + setOfIntegers.size());

		for (Integer i : setOfIntegers) {
			i += 100;
			System.out.println(i);
		}
		l.info(setOfIntegers.toString());
	}
}
```

输出结果：

```
... TrySet main
信息: [20, 5, 12]
... TrySet main
信息: 2
105
112
... TrySet main
信息: [5, 12]
```

## 映射 `Map`

`Map` 是一种方便的集合构造，可以使用它将一个对象（*键*）与另一个对象（*值*）相关联。

`Map` 的键必须是唯一的，而且可在以后用于检索值。

和 List、Set 一样，`Map` 集合仅可包含对象，且 `Map` 是一个接口，所以不能直接实例化它，我们常用 `HashMap` 来实现一个 `Map`。

#### 常用操作

* 添加元素：`put(K key, V value)`
* 取出元素：`get(Object key)`
* 删除元素：`remove (Object key, [Object value])`
* 获取大小：`size()`
* 获取一个 Key 的 `Set`：`keySet()`，可以利用这个方法，结合使用 Set 和 Map，实现遍历 `Map`。

```java
// 声明
Map<String, Integer> mapOfIntegers = new HashMap<>();
// 添加
mapOfIntegers.put("168", Integer.valueOf(168));
// 取值
Integer oneHundred68 = mapOfIntegers.get("168");
```

```java
Set<String> keys = mapOfIntegers.keySet();
Logger l = Logger.getLogger("Test");
for (String key : keys) {
    Integer  value = mapOfIntegers.get(key);
    l.info("Value keyed by '" + key + "' is '" + value + "'");
}
```

相关代码：[TryMap.java](./src/TryMap.java)

----

相关代码：

[TryList.java](./src/UsrList.java)

[TrySet.java](./src/TrySet.java)

[TryMap.java](./src/TryMap.java)

