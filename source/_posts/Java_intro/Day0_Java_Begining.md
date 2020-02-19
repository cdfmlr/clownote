---
title: Java-起步
date: 2019-04-11 16:37:53
tag: Java
categories:
	- Java
	- Beginning
---

# Java 起步 

## Java 简介（废话） 
Java 是由Sun Microsystems公司于1995年5月推出的高级程序设计语言（现属于Oracle）。 
Java可运行于多个平台，如Windows, Mac OS，及其他多种UNIX版本的系统。 

## Java 开发环境配置 

### JDK (Java Development Kit) 

> Java 是一种跨平台的编程语言，想要让你的计算机能够运行 Java 程序那么就需要安装 JRE，而想要开发 Java 程序，那么就需要安装 JDK。   

* [官网下载JDK](https://www.oracle.com/technetwork/java/javase/downloads/index.html) 
* 安装 
* 配置（[Windows 下需要配置几个环境变量](https://docs.oracle.com/en/java/javase/12/install/installation-jdk-microsoft-windows-platforms.html)） 

### Eclipse (IDE) 

> Eclipse 是一个很好的 Java 开发环境。   

* [官网](https://www.eclipse.org)下载 
* 安装 (不再推荐使用 Eclipse，要安装的话方法自寻)

（Update 2020.02.19👆对 Eclipse 的推荐时很长很长时间前写的了，那时候我还没有接触过 IDEA。时至今日，我不否为 Eclipse 仍然还是强大的 IDE，但我现在更喜欢更加现代化、人性化、更加优雅强大的IDEA）

### IntelliJ IDEA （推荐）

[JetBrains](https://www.jetbrains.com) 出品的强大现代化 IDE。

* [官网](https://www.jetbrains.com/idea/)

## Hello World 

#### 代码 
```java 
public class HelloWorld { 
	public static void main(String[] args) { 
		System.out.println("Hello, world!"); 
	} 
} 
```

#### 运行方法 
```
$ vim HelloWorld.java 
$ javac hello.java 
$ java HelloWorld 
```

**`javac`** 后面跟着的是java文件的文件名，例如 `HelloWorld.java`。 该命令用于将 java 源文件编译为 class 字节码文件，如： `javac HelloWorld.java`。 
运行javac命令后，如果成功编译没有错误的话，会出现一个 `HelloWorld.class` 的文件。

**`java`** 后面跟着的是java文件中的类名(后面不加`.class`)，如: `java HelloWorld`。 

⚠️【注意】文件名必须和类名一致！否则会出现如下错误： 
`错误: 类 HelloWorld 是公共的, 应在名为 HelloWorld.java 的文件中声明` 