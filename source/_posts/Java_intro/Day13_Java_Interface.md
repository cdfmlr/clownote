---
title: Java-接口
date: 2019-04-24 16:37:53
tag: Java
categories:
	- Java
	- Beginning
---

# Java 接口

根据设计，抽象方法指定一个*契约*（通过方法名、参数和返回类型）但未提供可重用的代码。当在抽象类的一个子类中实现行为的方式与另一个子类中不同时，抽象方法（在抽象类上定义）就会很有用。

当在应用程序中需要一组可分组到一起的常见行为（例如 `java.util.List`），但它们存在两个或多个实现时，可以考虑使用*接口* 定义该行为。

**接口** 像是**仅**包含抽象方法的抽象类；它们**仅**定义契约，而不定义实现。

## 定义接口

接口声明看起来像类声明，但使用了 `interface` 关键字：

```java
public interface InterfaceName {
    returnType methodName(argumentList);
}
```

接口中定义的方法没有方法主体。接口的实现者负责提供方法主体（与抽象方法一样）。

## 实现接口

要在类上定义一个接口，则需要*实现* 该接口，这意味着提供一个方法主体来进一步提供履行接口契约的行为。

可以使用 `implements` 关键字实现接口：

```java
public class Manager extends Employee implements BonusEligible, StockOptionRecipient {
  // And so on
}
```

`implements` 操作类似 继承用的 extends，接口是使用 `implements` 关键字，二者不同的是，接口可以有好多个，但继承只能有一个。

然后，我们要在 implements 了接口的类里实现该接口：

```java
public class Manager extends Employee implements StockOptionRecipient {
  public Manager() {
  }
  public void processStockOptions (int numberOfOptions, BigDecimal price) {
    log.info("I can't believe I got " + number + " options at $" +
    price.toPlainString() + "!"); 
  }
}
```

实现该接口时，需要提供该接口上的一个或多个方法的行为。注意实现的方法必须与接口中的匹配（名称、参数、返回值），还需要添加 `public` 访问修饰符。

