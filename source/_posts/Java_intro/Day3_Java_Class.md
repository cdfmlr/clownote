---
categories:
- Java
- Beginning
date: 2019-04-14 16:37:53
tag: Java
title: Java-类和对象
---

# Java 中的类和对象

> 类可以看成是创建Java对象的模板

## 类的定义

```java
public class Dog {
    String name;
    int age;

    void eat() {
    }
    void sleep() {
    }
}
```

## 类中变量的类型

* **局部变量**：在*方法*或*语句块*中定义的变量被称为局部变量。变量声明和初始化都是在方法中，方法结束后，变量就会自动销毁。

* **成员变量(实例变量)**：成员变量是定义在类中，*方法体之外*的变量。这种变量在创建对象的时候实例化。成员变量可以被类中方法、构造方法和特定类的语句块访问。

* **类变量**：类变量也声明在类中，方法体之外，但必须声明为 `static` 类型。

> 这里只是简单介绍，详见 [Day5_Java_Variable.md](./Day5_Java_Variable.md)

## 构造方法

构造方法的名称必须与类同名，一个类可以有多个构造方法。

在创建一个对象的时候，至少要调用一个构造方法。
如果没有显式地为类定义构造方法，Java编译器将会为该类提供一个默认构造方法。

```java
public class Dog {
	public Dog() {
		System.out.println("构造Dog");
	}
}
```

## 重载方法

创建两个具有相同名称和不同参数列表（即不同的参数数量或类型）的方法时，就拥有了一个*重载* 方法。

在运行时，JRE 基于传递给它的参数来决定调用您的重载方法的哪个变体。

我们甚至可以在一个方法中调用另一个同名的重载方法。

但要注意：在使用重载方法时，

- 不能仅通过更改一个方法的返回类型来重载它。
- 不能拥有两个具有相同名称和相同参数列表的方法。

## 继承

要表示一个类继承自某一个超类，我们可以在声明类时，在 className 后加上 `extends`，例如：

```java
public class Employee extends Person {
		// Employee 继承自 Person
		public Employee() {
				super();
    }
  
    public Employee(String name, int age, int height, int weight,
  String eyeColor, String gender) {
        super(name, age, height, weight, eyeColor, gender);
  }
}
```

在构造函数中，调用 `super([args])` 来初始化父类。

### 重写方法

如果一个子类提供其父类中定义的方法的自有实现，这被称为*方法重写*。

重写的形式类似于重载，但需要加上一个 `@Override`。例如，当父类中有一个 `foo()` 方法时，我们可以在子类中这样重写它：

```java
@Override
public int foo() {
	// TODO Auto-generated method stub
	return super.foo();
}
```

【注】这段代码是使用 Eclipse 自动生成的，它只是调用了父类中的方法（`super.foo()`），没有任何改变，但实际中我们不会这么使用。

重写后，**在类中**直接使用 `method()`调用重写后的函数，但我们任然可以通过 `super.method()` 调用父类中的（重写前的）方法。

## 创建对象

对象是根据类创建的。
创建对象需要以下三步：

* 声明：声明一个对象，包括对象名称和对象类型。
* 实例化：使用关键字 `new` 来创建一个对象。
* 初始化：使用 `new` 创建对象时，会调用构造方法初始化对象。

```java
public class Dog {
	public static void main(String[] args) {
		Dog Dog0 = new Dog();
	}
}
```

## 访问实例变量和方法

* 访问实例的变量：`实例名.变量名`
* 调用实例的方法：`实例名.方法名()`

```java
public class Dog {
	String name;
	int age;

	void eat(String food) {
		System.out.println(name + " is eating " + food + ".");
	}

	public Dog() {
		name = "Dog";
		age = 0;

		System.out.println("构造()：");
		System.out.println(name + "\t" + age);
	}
	public Dog(String dogName, int dogAge) {
		name = dogName;
		age = dogAge;
		System.out.println("构造(name, age)：");
		System.out.println(name + "\t" + age);
	}

	public static void main(String[] args) {
		Dog Dog0 = new Dog();
		Dog Dog1 = new Dog("FooBar", 3);

		// 访问变量 
		Dog0.name = "Ana";
		System.out.println(Dog0.name);

		// 访问方法
		Dog1.eat("cat");

	}
}
```

运行👆上面代码将输出：

```
构造()：
Dog	0
构造(name, age)：
FooBar	3
Ana
FooBar is eating cat.
```

## 比较对象

Java 语言提供了两种比较对象的方法：

- `==` 运算符 
- `equals()` 方法

### 使用 `==` 比较对象

`==` 语法比较对象是否相等，只有在 `a` 和 `b` 相等时，`a == b` 才返回 `true`。

对于内置基本类型，需要*它们的值相等*。

对于对象，需要两个对象引用*同一个对象实例*。

例如：

```java
import java.util.logging.Logger;

public class Equals {
	public static void main(String[] args) {
		Logger l = Logger.getLogger("Test");

		int i = 12,
			j = 12,
			k = 99;
        
		Integer a = new Integer(12);
		Integer b = a;
		Integer c = new Integer(12);

		l.info("i == j: " + (i == j));
		l.info("i == k: " + (i == k));

		l.info("a == b: " + (a == b));
		l.info("a == c: " + (a == c));
	}
}
```

运行这段代码将得到如下结果：

```
i == j: true
i == k: false
a == b: true
a == c: false
```

⚠️【注】若使用 `a = Integer.valueOf(12);` 与 `c = Integer.valueOf(12);` 分别得到 a 和 c，则 `a == c` 将是 `true` ！

### 使用 `equals()` 比较对象

> `equals()` 是每种 Java 语言对象都可以自由使用的方法，因为它被定义为 `java.lang.Object` 的一个实例方法（每个 Java 对象都继承该对象）。

调用 `equals()` 的方法如下：

```java
a.equals(b);
```

此语句调用对象 `a` 的 `equals()` 方法，向它传递对象 `b` 的引用。

默认情况下，Java 程序使用 `==` 语法检查两个对象是否相同。但是因为 `equals()` 是一种方法，所以它可以被重写。这样，对于任何对象，我们都可定义适合的 `equals()` 的含义。

【注】在重写 `equals()` 时，我们可以利用 `object.hashCode()`（ to return a hash code value for the object.）

---

相关代码：

[`Dog.java`](./src/Dog.java)

参考：

[菜鸟教程 | Java 对象和类](https://www.runoob.com/java/java-object-classes.html)

[Java 编程入门 |  第 13 单元：对象的后续处理 ](https://www.ibm.com/developerworks/cn/java/j-perry-next-steps-with-objects/index.html)