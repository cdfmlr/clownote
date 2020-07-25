---
categories:
- Java
- Beginning
date: 2019-04-16 16:37:53
tag: Java
title: Java-变量
---

# Java 中的变量类型

## **局部变量**

> 在*方法*或*语句块*中定义的变量被称为局部变量。变量声明和初始化都是在方法中，方法结束后，变量就会自动销毁。

- 局部变量声明在方法、构造方法或者语句块中；
- 局部变量在方法、构造方法、或者语句块被执行的时候创建，当它们执行完成后，变量将会被销毁；
- 访问修饰符不能用于局部变量；
- 局部变量只在声明它的方法、构造方法或者语句块中可见；
- 局部变量是在栈上分配的。
- 局部变量没有默认值，所以局部变量被声明后，必须经过初始化，才可以使用。

## **成员变量(实例变量)**

> 成员变量是定义在类中，*方法体之外*的变量。这种变量在创建对象的时候实例化。成员变量可以被类中方法、构造方法和特定类的语句块访问。

- 实例变量声明在一个类中，但在方法、构造方法和语句块之外；
- 当一个对象被实例化之后，每个实例变量的值就跟着确定；
- 实例变量在对象创建的时候创建，在对象被销毁的时候销毁；
- 实例变量的值应该至少被一个方法、构造方法或者语句块引用，使得外部能够通过这些方式获取实例变量信息；
- 实例变量可以声明在使用前或者使用后；
- 访问修饰符可以修饰实例变量；
- 实例变量对于类中的方法、构造方法或者语句块是可见的。一般情况下应该把实例变量设为私有。通过使用访问修饰符可以使实例变量对子类可见；
- 实例变量具有默认值。数值型变量的默认值是`0`，布尔型变量的默认值是`false`，引用类型变量的默认值是`null`。变量的值可以在声明时指定，也可以在构造方法中指定；
- 实例变量可以直接通过变量名访问。但在静态方法以及其他类中，就应该使用完全限定名：`ObejectReference.VariableName`。

## **类变量**

> 类变量也声明在类中，方法体之外，但必须声明为 `static` 类型。

- 类变量也称为静态变量，在类中以 `static` 关键字声明，但必须在方法之外。
- 无论一个类创建了多少个对象，类只拥有类变量的一份拷贝。
- 静态变量除了被声明为常量外很少使用。常量是指声明为 `public` / `private`, `final` 和 `static` 类型的变量。常量初始化后不可改变。
- 静态变量储存在静态存储区。经常被声明为常量，很少单独使用 `static` 声明变量。
- 静态变量在第一次被访问时创建，在程序结束时销毁。
- 与实例变量具有相似的可见性。但为了对类的使用者可见，大多数静态变量声明为 `public` 类型。
- 默认值和实例变量相似。数值型变量默认值是 `0`，布尔型默认值是 `false`，引用类型默认值是 `null`。变量的值可以在声明的时候指定，也可以在构造方法中指定。此外，静态变量还可以在静态语句块中初始化。
- 静态变量可以通过：`ClassName.VariableName` 的方式访问。
- 类变量被声明为 `public static final` 类型时，类变量名称一般建议使用大写字母。如果静态变量不是 `public` 和 `final` 类型，其命名方式与实例变量以及局部变量的命名方式一致。

#### 关于 **类变量** 的说明：

> The static keyword in Java is used for memory management mainly. We can apply java static keyword with variables, methods, blocks and nested class. The static keyword belongs to the class than an instance of the class. The static can be: Variable (also known as a class variable) Method (also known as a class method) Block.

（部分翻译）

> Java 中的 `static` 关键字主要用于 *memory management*（谷歌翻译给出的翻译是“内存管理”, 但我对这个词的理解是：安排出一个内存空间来，供类的实例之间共享某个量）。我们可以将 java 的 `static` 关键字施用于变量、方法、语句块和嵌套类。`static` 定义的对象是属于整个类的, 而不是某个类的实例。

普通的变量属于类的某一个特定的实例，但用 `static` 关键字修饰的变量将属于一个类。也就是说，我们通过类的某一个实例去修改一个一般的变量值，将只有这个实例中的值被修改，其他实例不受影响；而若是修改一个 `static` 关键字修饰的**类变量**，这个类的所有实例的这个值都会被修改。

说起来比较麻烦，可以看一段示例代码：

```java
public class Static {
	public static void main(String[] args) {
		Example foo = new Example();
		Example bar = new Example();

		foo.staticVar = foo.normalVar = "foobar";

		System.out.println(foo.staticVar + "\t" + foo.normalVar);
		System.out.println(bar.staticVar + "\t" + bar.normalVar);
	}
}

class Example {
	static String staticVar = "Example";
	String normalVar = "Example";
}
```
输出：
```
foobar	foobar
foobar	Example
```

可以看到，我们只改变了 `foo` 实例的值，但由 `static` 修饰的类变量 `staticVar` 的改变在 `bar` 中也出现了，而普通的成员变量则不然。

利用这种特性，我们可以实现一种可以统计自己的实例个数的类，详见 [`CountingClass.java`](src/CountingClass.java)

---

相关代码：

[`Static.java`](src/Static.java)
[`CountingClass.java`](src/CountingClass.java)