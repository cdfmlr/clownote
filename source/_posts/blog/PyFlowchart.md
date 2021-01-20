---
date: 2020-10-24 12:42:44.471978
tags: Python
title: Python 代码转流程图
---
# Python 代码转流程图

在设计程序时，类图、流程图都是很有用的工具，我们有很多工具来绘制这些图纸，甚至还能用它们生成最基本的框架代码。也有时候我们需要把已经写好的代码反向转成类图、流程图，比如~~写作业~~和别人分享设计的时候。

代码转类图也有挺多工具的，VS Code、IntelliJ IDEA 这些常用的 IDE 都可以装插件来完成这一工作。而如果你做微软家的开发，Visual Studio 可选安装的“类设计器”，更是强到不像话，轻松吊打我见过的其他任何同类工具，就这一点来说， VS 对得起「宇宙第一 IDE」的称号。

然而，代码转流程图，相对来说，这个需求少一些，工具也没那么丰富。最近我突然需要把一些 Python 代码转成流程图，Google 翻了两页，GitHub 搜了几个项目，发现现有的实现都不太行：要么用的技术太怪（那些用「正则表达式」正面上的可震撼了我一下午），要么跑不起来（依赖条件苛刻，比如某些项目用了对 macOS 不太友好的 PyGame），要么跑出来太丑（凌乱的线条、奇怪的颜色，不是新丑风，是丑到抽风）。 当我看到某高赞项目 [Vatsha/code_to_flowchart](https://github.com/Vatsha/code_to_flowchart) 甚至集合了上述三大“优点”时，，，我选择了自己动手撸一个 python to flowchart 的工具。

当然，我不是喷 [Vatsha/code_to_flowchart](https://github.com/Vatsha/code_to_flowchart)，只是其一些细节真的欠优，有很大的改进空间。但不得不说，他的设计简单有效 ，用 PyGame 做可视化也很有新意。其实，我在做自己的实现时也大量参考了这个项目。

---

我的解决方案 [PyFlowchart](https://github.com/cdfmlr/pyflowchart) 基于大名鼎鼎的 flowchart.js。

（本来我是取名叫做 PyFlow 的，上传 PyPi 的时候发现重名了🤦‍♂️。所以改成了 PyFlowchart）

## flowchart.js

如果你使用 Typora，可能知道在 Typora 中用  \`\`\`flow 可以用一种简单的文本语言来写流程图，根据 [Typora 的文档](https://support.typora.io/Draw-Diagrams-With-Markdown/#flowcharts)，这个功能来自开源的 [flowchart.js](https://github.com/adrai/flowchart.js)。

我的方案就是把 Python 代码转化成这种 flowchart 语言，然后你就可以借助  [flowchart.js.org](http://flowchart.js.org/)、[Typora](https://www.typora.io)、 [francoislaberge/diagrams](https://github.com/francoislaberge/diagrams/#flowchart) 等等工具来生成流程图了。

```
st=>start: Start
op=>operation: Your Operation
cond=>condition: Yes or No?
e=>end

st->op->cond
cond(yes)->e
cond(no)->op
```

![flowchart](https://tva1.sinaimg.cn/large/0081Kckwly1gk07vvnullj30uo0luaa3.jpg)

## PyFlowchart

下面简要介绍如何使用我实现的 PyFlowchart，更详细的说明请看项目的 [README](https://github.com/cdfmlr/pyflowchart/blob/master/README.md)。

安装 PyFlowchart：

```sh
$ pip3 install pyflowchart
```

写一个 `simple.py` 文件：

```python
def foo(a, b):
    if a:
        print("a")
    else:
        for i in range(3):
            print("b")
    return a + b
```

运行 PyFlowchart：

```sh
$ python3 -m pyflowchart simple.py
```

它会输出 flowchart 代码：

```
st4439920016=>start: start foo
io4439920208=>inputoutput: input: a, b
cond4439920592=>condition: if a
sub4439974736=>subroutine: print('a')
io4439974672=>inputoutput: output:  (a + b)
e4439974352=>end: end function return
cond4439974224=>operation: print('b') while  i in range(3)

st4439920016->io4439920208
io4439920208->cond4439920592
cond4439920592(yes)->sub4439974736
sub4439974736->io4439974672
io4439974672->e4439974352
cond4439920592(no)->cond4439974224
cond4439974224->io4439974672
```

访问 [flowchart.js.org](http://flowchart.js.org)，把上面生成的代码粘贴到文本框里，右边就会自动生成流程图了：

![flowchart.js.org 截图，左边的输入框里粘贴了生成的代码，右边是画出的流程图](https://tva1.sinaimg.cn/large/0081Kckwly1gk083edrrgj312j0sc4d2.jpg)

当然，你也可以直接把这些代码放到 Typora 的 flow 代码块里，也会自动生成流程图。如果你喜欢使用命令行，也可以用 [francoislaberge/diagrams](https://github.com/francoislaberge/diagrams/#flowchart) 来生成流程图。

如果生成的流程图有让人不满意的地方（比如，线条重叠）或者你喜欢指定样式，参考 [flowchart.js.org](http://flowchart.js.org)，手动修改一下生成的 flowchart 就可以了，非常方便。

## 实现原理

```flow
st=>start: start PyFlowchart
in=>inputoutput: input python source code
sub1=>subroutine: code to ast
sub2=>subroutine: ast to node graph
sub3=>subroutine: node graph to flowchart
out=>inputoutput: output flowchart
e=>end: end

st->in->sub1(right)->sub2(right)->sub3->out->e
```

![实现原理流程图](https://tva1.sinaimg.cn/large/0081Kckwly1gk0bxkyis0j31k00u0tb8.jpg)

PyFlowchart 利用 Python 内置的 [ast](https://docs.python.org/zh-cn/3/library/ast.html) 包，把代码转化成 AST（抽象语法树），然后把 AST 转化成自己定义的 Node 组成的图，每个 Node 对应一个 flowchart 中的 node，遍历这个图就可以得到流程图了。

关于 ast 包，可以看看这篇文章：[AST 模块：用 Python 修改 Python 代码](https://pycoders-weekly-chinese.readthedocs.io/en/latest/issue3/static-modification-of-python-with-python-the-ast-module.html)，虽然很老，但十分简单易懂。总而言之，利用 ast 包，我们可以把一段 Python 代码转化为一个数据结构：

```python
>>> import ast
>>> expr = """
... def add(a, b):
...     return a + b
... """
>>> expr_ast = ast.parse(expr)
>>> expr_ast
<_ast.Module object at 0x10c773e10>
>>> ast.dump(expr_ast)
# p.s. 这里手动做了格式化
Module(body=[FunctionDef(name='add',
  args=arguments(
    args=[
      arg(arg='a', annotation=None),
      arg(arg='b', annotation=None)],
    vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]),
  body=[Return(value=BinOp(
    left=Name(id='a', ctx=Load()),
    op=Add(),
    right=Name(id='b', ctx=Load())))],
  decorator_list=[],
  returns=None)])
```

学会了这个东西，接下来的工作就是把这个 expr_ast (_ast.Module 对象) 翻译成流程图了。我们用面向对象来的方法来实现：

![pyflowchart.node](https://tva1.sinaimg.cn/large/0081Kckwly1gk0b5o486pj31hz0u042n.jpg)

`Node` 是最最基础的类，表示流程图中的一个节点，其他一切都继承自它。Node 有节点类型、名称、内容等属性，提供的 `fc_definition()`、`fc_connection()` 方法可以把自己转化为 flowchart 语言的字符串。另外的 `__visited` 和 `_traverse()` 是用来遍历图的。与 flowchart 中的 node types 对应，我们实现了各种 Node 的子类：StartNode、EndNode、OperationNode......

`NodesGroup` 是一个特殊的 Node，它自己不会出现在生成的 flowchart 中，但它可以包含一些其他 Node。这个设计是受到 Android 的 View、ViewGroup 的启发，有了这个 NodesGroup，if 语句、for / while 循环这样有嵌套的 body 的情况就很容易处理了。

`AstNode` 表示一个从 AST 对象得到的 Node。构造 AstNode，就是把某个 AST 对象翻译成一个 Node（也可以是 NodesGroup）。其子类就和各种 ast 对象对应（也就和 Python 的各种语句对应）： If、Loop、Return .......

`Flowchart` 代表一张流程图。流程图就是一堆连在一起的节点嘛，所以 Flowchart 是 NodesGroup 的子类。在其 `from_code()` 中方法中，实现了用 ast 包解析 Python 代码，得到 ast 对象的工作。在 `flowchart()` 方法中，遍历图，拿到所有节点的 flowchart 表示，汇总成一张完整的 flowchart 流程图。 

其实这个东西很简单，更具体的实现看源码就很好理解了，在此不做赘述。总结一下：

- Flowchart 中利用 ast 包实现了 code to ast；
- AstNode 及其子类实现了 ast to node graph；
- Node 及其子类实现了 node graph to flowchart。

附上项目地址与完整实现的类图：

- https://github.com/cdfmlr/pyflowchart/

![pyflowchart](https://tva1.sinaimg.cn/large/0081Kckwly1gk09oeitndj33xl0u0wx7.jpg)

```python
by('CDFMLR', '2020.10.24')
# 🎉
```
