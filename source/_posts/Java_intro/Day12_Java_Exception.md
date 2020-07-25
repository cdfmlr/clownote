---
categories:
- Java
- Beginning
date: 2019-04-23 16:37:53
tag: Java
title: Java-异常
---

# Java 异常处理

> 没有程序能够始终正常运行，Java 语言的设计者也知道这一点。Java 平台提供了内置机制来处理代码未准确地按计划运行的情形。
> 

**异常** 是在程序执行期间发生的破坏正常的程序指令流的事件。

**异常处理** 可以使用 `try` 和 `catch` 代码块（以及 `finally`）捕获错误。

## 异常类型

在 Java 中，异常的层次结构图如下：

![4970765-1437c4660dd95f3e](http://ww1.sinaimg.cn/large/006y8mN6gy1g673rbxe34j30i50b4dk9.jpg)

* `Throwable`
  * `Error`	: 运行时环境发生的错误。例如，JVM 内存溢出。一般地，程序不会从错误中恢复。
  * `Exception`	: 程序本身可以处理的异常
    * `IOException`
    * `RuntimeException`
###  异常分层结构

Java 语言包含一个完整的异常分层结构，它由许多类型的异常组成，这些异常划分为两大主要类别：

- **已检查的异常(*checked exceptions*)**：已由编译器检查（表示编译器确定它们已在您代码中的某处处理过）。一般而言，这些异常是 `java.lang.Exception` 的直接子类。
- **未检查的异常**（也称为*运行时异常*，*unchecked / runtime exceptions*）：未由编译器检查。这些是 `java.lang.RuntimeException` 的子类。

## 使用 `try`、`catch` 和 `finally`

```java
try {
    // Try to execute
} catch (ExceptionType e) {
  	// Catch exception
} finally {
    // Always executes
}
```

⚠️【注意】`ExceptionType` 要换成具体的错误类型：如 `RuntimeException`、`IOException` 。

`try`、`catch` 和 `finally` 代码块共同形成了一张捕获异常的网: 

* 首先，`try` 语句限定可能抛出异常的代码;
* 捕获的异常会放到 `catch` 代码块（或称 *异常处理函数*） 中。捕获到异常时，可以尝试优雅地进行恢复，也可以退出程序（或方法）;
* 在所有尝试和捕获都完成后，会继续执行 `finally` 代码块，无论是否发生了异常;

例如：

```java
package mine.java.tour;

import java.util.logging.Logger;

public class Exception {
	public static void main(String[] args) {
		Logger l = Logger.getLogger("Try-Catch-Finally");

		try {
			Integer foo = null;
			System.out.println("foo: " + foo.toString());
		} catch (RuntimeException e) {
			l.severe("Caught exception: " + e);
			System.out.println("catch");
		} finally {
			System.out.println("finally");
		}
	}
}

```

运行这个程序会得到如下结果：

``` 
5月 02, 2019 11:57:04 上午 mine.java.tour.Exception main
严重: Caught exception: java.lang.NullPointerException
catch
finally
```

### 多个 `catch` 代码块

可以拥有多个 `catch`代码块，但必须采用某种特定方式来搭建它们。

如果所有异常都是其他异常的子类，那么子类会按照 `catch` 代码块的顺序放在父类前面。

``` java
try {

} catch (IndexOutOfBoundsException e) {
    System.err.println("IndexOutOfBoundsException: " + e.getMessage());
} catch (IOException e) {
    System.err.println("Caught IOException: " + e.getMessage());
}
```

### 用一个 `catch` 捕获多个类型的错误

在 Java SE 7 以后，一个 `catch` 语句可以处理不止一个类型的异常。这个特性可以让我们避免一直写重复的代码，也让我们没有理由去catch一个过度宽泛的错误类型（例如，我们本来应该逐一处理各种不同的问题，但为了避免麻烦，直接 `catch(RuntimeException e)`）。

我们可以把 catch 的小括号里的单个 ExceptionType 替换为逐个列出需要这个语句块处理的错误类型，每个类型之间用 竖线（ `|` ）分隔。

```java
catch (IOException|SQLException ex) {
    logger.log(ex);
    throw ex;
}
```

【注】在用一个 catch 捕获多个错误的时候，这个 catch 的参数会隐含地带上 `final` 属性。例如在上面的例子中，catch 的参数 ex 是一个 `final` 的变量，因此，不能在 catch 语句块里给它赋值！

##  `throws` 和 `throw`

* `throws` : 方法可能抛出异常的声明(用在声明方法时，表示该方法可能要抛出异常)。

Checked exception 通过在声明一个方法时使用 `throws` 关键字加上一个可能的异常列表 来向编译器声明：

```java
public void doSomething(int a) throws Exception1, Exception1, ... {
    ...
}
```

`throws Exception1, Exception1, ...`  只是告诉编译器这个方法可能会抛出这些异常，方法的调用者可能要处理这些异常，而这些可能异常是该函数体产生的。

* `throw` 是具体向外抛异常的动作，它抛出一个异常实例。

``` java
import java.io.*;
public class className
{
  public void deposit(double amount) throws RemoteException
  {
    // Method implementation
    throw new RemoteException();
  }
  //Remainder of class definition
}
```

## `try-with-resources` 代码块

当我们在 try 中使用一些资源时，不论出错与否我们都应该在最后关闭它，所以可以在finally 中完成这个关闭操作：

```java
static String readFirstLineFromFileWithFinallyBlock(String path)
                                                     throws IOException {
    BufferedReader br = new BufferedReader(new FileReader(path));
    try {
        return br.readLine();
    } finally {
        if (br != null) br.close();
    }
}
```

Java SE 7 开始，还有一种更简单办法来解决问题，Java 可以自动关闭资源：

```java
static String readFirstLineFromFile(String path) throws IOException {
    try (BufferedReader br =
                   new BufferedReader(new FileReader(path))) {
        return br.readLine();
    }
}
```

在 try 后面加小括号，里面声明需要的资源，在结束异常检测后（在 try 代码块超出范围时），Java 将自动处理这个资源的关闭问题。

注意，这种自动关闭的资源必须实现 java.lang.AutoCloseable 接口；如果尝试在一个没有实现该接口的资源类上实现此语法，会出错。

---

相关代码：

[Exception.java](./src/Exception.java)