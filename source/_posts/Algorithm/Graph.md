---
date: 2019-05-07 22:52:57
tags: Algorithm
title: 数据结构「图」的基础
---

这（可能）是你能找到的最简单的讲图的文章。

> 这篇文章是我以前学习「图」数据结构的时候写的。今天上课讲图，我翻了好久才翻到这个😂
>
> 
>
> 注：文中代码均为伪代码，其语法比较类似于 Python + BASIC，你可以用你喜欢的任何语言去做具体实现。在最后，我会附上我的 Python 实现源码。

## 网络的表示

0. 邻接矩阵

   （略，这个是数学，我不懂）

1. 把链路作为引用储存在类里（连带其他数据）：

``` basic
Class Node
	String: name
	List<Node>: neighbors
	List<Integer>: costs
End Node
```

2. 链路和节点单独（更常用）：

```basic
Class Node:
	String: name
	List<Link>: links
End Node

Class Link:
	Integer: cost
	Node: nodes[2]		// 无向
	/* Node: toNode		// 有向 */
ENd Link
```

无向，链路包含两个 Node，顺序任意。

有向，只包含一个 Node，指向目标节点，也可以用两个，一个指向来源，另一个指向目标。

## 网络的遍历

### 深度优先

> 在一次深度优先遍历中，算法首先访问一些离初始节点很远的节点，之后才是离初始节点较近的节点。

直接像树一样遍历，在图中是不行的：

``` basic
badTraverse():
	<处理节点>
	For Each link In links:
		link.nodes[1].Traverse()
	Next link
End badTraverse
```

如果图包含了回路，这个算法会死循环。

解决的方法是让算法知道自己访问过的节点，可以给类中加一个 `visited` 属性来纪录自己有没有被访问：

```basic
slowTraverse():
	<处理节点>
	Self.visited = True
	
	For Each link In links:
		If Not link.nodes[1].visited:
			link.nodes[1].Traverse()
		End If
	Next link
End slowTraverse
```

这个算法理论上可行，但消耗太大，容易爆栈。

要解决这个问题，可以用栈来替换递归：

```basic
depthFirstTraverse(Node: startNode):
	// 访问当前节点
	startNode.visited = True
	
	// 创建栈，把初始节点压入栈
	Stack<Node>: stack
	stack.push(stareNode)
	
	// 循环处理直到栈为空
	While Not stack.isEmpty():
		Node node = stack.pop()		// 从栈中获取下一节点
		// 循环处理节点中的链路
		For Each link In node.links:
			If Not link.nodes[1].visited:
				link.nodes[1].visited = True
				stack.push(link.node[1])
			End If
		Next link
	Loop		// 继续处理直到栈为空
End depthFirstTraverse
```

### 广度优先

> 在一次广度优先遍历中，离初始节点较近的节点首先被访问，然后才是离初始节点较远的节点。

在**深度优先遍历**中，由于使用*后进先出*的栈来存放节点，所以遍历了一些离初始节点较远的节点然后才遍历较近的节点。

如果使用**队列**（*Queues*，FIFO）代替**栈**（*Stacks*，FILO），则节点会按先进先出的顺序被处理，离初始节点较近的节点就首先被处理了，即**广度优先遍历**。

### 遍历的应用

#### 无向图连通性测试

对于一个无向图，如果连通，一个遍历算法从初识节点出发，可达所有节点。

```basic
Boolean: isConnected(Node: startNode):
	// 从初识节点开始遍历网络
	Traverse(start_node)
	
	// 查看有无没被访问的
	For Each node In <所有节点>
		If Not node.visited: Return False
	Next node
	
	// 所有节点都访问过了，连通
	Return True
End isConnected
```

#### 寻找所有连通分量

利用深度遍历，一直遍历直到所有连通的节点都已经访问过，就找到了所有连通分量：

``` basic
List<List<Node>>: getConnectedComponents:
	// 跟踪记录已经访问过的节点数
	Integer: numVisited = 0
	// 创建连通分量列表
	List<Lidt<Node>>: components
	
	// 循环直到所有节点都在连通分量中
	While numVisited < 节点个数:
		// 查找一个还未访问过的节点
		Node: startNode = 第一个未访问过的节点
		
		// 将初始值压入栈
		Stack<Node>: stack
		stack.push(startNode)
		startNode.Visited = True
		numVisited += 1
		
		// 将节点添加到一个新的连通分量中
		List<Node>: component
		component.add(startNode)
		components.add(component)
		
		// 不断处理，直到它为空
		While Not stack.isEmpty():
			// 从栈中获取下一个节点
			Node: node = stack.pop()
			
			// 依次处理该节点所有对应的链路
			For Each link In node.links:
				If Not link.nodes[1].visited:
					link.nodes[1].visited = True
					component.add(link.nodes[1])
					stack.push(link.nodes[1])
					// 将链路标记为树的一部分，生成树
					link.visited = True
					numVisited += 1
				End If
			Next link
		Loop	// Not stack.isEmpty()
	Loop	// numVisited < 节点个数
	
	Return components				
End getConnectedComponents
```

#### 生成树

如果一个无向图是连通的，就可以以一节点为根建立一棵树，表示根节点到网络中其他节点到路径。这颗树称为**生成树**。

要实现这一点，在前面的程序里标记新节点被访问后，将链路标记为树的一部分，就行了：

```basic
link.visited = True
```

##### 最小生成树

具有最少可能代价的生成树称为**最小生成树**。

要得到一颗生成树，可以用如下贪心策略：

```
1. 添加根节点R以初始化生成树
2. 对每个节点重复直到得到生成树：
		a. 发现在生成树中节点到未在树中节点到最小代价链接
		b. 将该链接到目标节点添加到生成树
```



## Python实现

文中涉及的代码还是比较多的，我写了其中一些的 Python 实现，放到了 GitHub：

* [https://github.com/cdfmlr/Graph_Python](https://github.com/cdfmlr/Graph_Python)

