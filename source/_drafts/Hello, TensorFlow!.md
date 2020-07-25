---
date: 2020-03-20 14:26:00
title: Hello,TensorFlow!
---



# Hello, TensorFlow!

我们先看看 1.x 版本的 Tensorflow。所以下面的代码里都是 `tf.compat.v1`。

## 1+1

```python
>>> import tensorflow as tf
>>> tf.compat.v1.disable_eager_execution()
>>> sess = tf.compat.v1.Session()
>>> 
>>> a = tf.constant(1)
>>> b = tf.constant(2)
>>> adder = a + b
>>> sess.run(adder)
3
>>> sess.close()

```

这个过程中可能会爆出下面这种错，不重要，不管他就行了：

```
2199-13-32 25:61:61.805538: I tensorflow/core/platform/cpu_feature_guard.cc:142] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
2199-13-32 25:61:61.830318: I tensorflow/compiler/xla/service/service.cc:168] XLA service 0x7fc4024e9c50 executing computations on platform Host. Devices:
2199-13-32 25:61:61.830338: I tensorflow/compiler/xla/service/service.cc:175]   StreamExecutor device (0): Host, Default Version
```

也可以用 with 来简化关闭资源：

```python
>>> with tf.compat.v1.Session() as sess:
...     sess.run(adder)
... 
3

```

用 `tf.placeholder` 创建占位 Tensor，其值可以在运行的时候输入：

```python
>>> c = tf.compat.v1.placeholder(tf.float32)
>>> d = tf.compat.v1.placeholder(tf.float32)
>>> adder_node = c + d
>>> adder_node
<tf.Tensor 'add_1:0' shape=<unknown> dtype=float32>
>>> c
<tf.Tensor 'Placeholder:0' shape=<unknown> dtype=float32>
>>> d
<tf.Tensor 'Placeholder_1:0' shape=<unknown> dtype=float32>
>>> with tf.compat.v1.Session() as sess:
...     print(sess.run(adder_node, {c: 3, d: 0.3}))
...     print(sess.run(adder_node, {c: [1.1, 2.2], d: [3.3, 4.4]}))
... 
3.3
[4.4       6.6000004]
>>> 
```

## Linear Regression

做一个简单的线性回归：
$$
y = W \times x + b
$$
要在 TensorFlow 中实现这个式子，$x$ 可以用 placeholder，$y$ 是 run 的输出；$W$ 和 $b$ 是需要不断改变来拟合曲线的，所以是变量 `tf.Variable`。

关于 $W$ 和 $b$ 的改变，我们需要损失模型（$y_n'$表示实际值）：
$$
loss = \sum_{n=1}^{N}(y_n-y_n')^2
$$
我们的目的就是尽量减小这个损失。

创建变量：

```python
>>> W = tf.Variable([0.1], dtype=tf.float32)
>>> b = tf.Variable([-0.1], dtype=tf.float32)
>>> x = tf.compat.v1.placeholder(tf.float32)
>>> linear_model = W * x + b
>>> y = tf.compat.v1.placeholder(tf.float32)
>>> loss = tf.reduce_sum(tf.square(linear_model - y))
```

初始化：

```python
>>> init = tf.compat.v1.global_variables_initializer()
>>> sess.run(init)
>>> # 把刚初始化好的loss打印出来看看，相当大：
>>> print(sess.run(loss, {x: [1, 2, 3, 6, 8], y: [4.8, 8.5, 10.4, 21.0, 25.3]}))
1223.0499
```

手动给变量赋值，减小loss：

```python
>>> betterW = tf.compat.v1.assign(W, [2])
>>> betterb = tf.compat.v1.assign(b, [1])
>>> sess.run([betterW, betterb])
[array([2.], dtype=float32), array([1.], dtype=float32)]
>>> # 现在损失就小很多了：
>>> print(sess.run(loss, {x: [1, 2, 3, 6, 8], y: [4.8, 8.5, 10.4, 21.0, 25.3]}))
159.93999
```

梯度下降：

```python
>>> optimizer = tf.compat.v1.train.GradientDescentOptimizer(0.0001)
>>> train = optimizer.minimize(loss)
>>> x_train = [1, 2, 3, 6, 8]
>>> y_train = [4.8, 8.5, 10.4, 21.0, 25.3]
>>> for i in range(10000):
...     sess.run(train, {x: x_train, y: y_train})
... 
>>> print('W: %s b: %s loss: %s' % (sess.run(W), sess.run(b), sess.run(loss, {x: x_train , y: y_train})))
W: [2.990913] b: [2.0224223] loss: 2.1328762
>>> 
```

整理代码，得到一个完整的脚本：

```python
import os
import tensorflow as tf
tf.compat.v1.disable_eager_execution()
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'    # 不显示那个 AVX2 FMA 的WARNING

# 数据、标签
x = tf.compat.v1.placeholder(tf.float32)
y = tf.compat.v1.placeholder(tf.float32)

# 参数
W = tf.Variable([0.1], dtype=tf.float32)
b = tf.Variable([-0.1], dtype=tf.float32)

# 预测函数
linear_model = W * x + b

# 损失函数
loss = tf.reduce_sum(tf.square(linear_model - y))

# 开会话，初始化变量
sess = tf.compat.v1.Session()

init = tf.compat.v1.global_variables_initializer()
sess.run(init)

# 梯度下降优化
optimizer = tf.compat.v1.train.GradientDescentOptimizer(0.0001)
train = optimizer.minimize(loss)

# 训练集
x_train = [1, 2, 3, 6, 8]
y_train = [4.8, 8.5, 10.4, 21.0, 25.3]

# 跑梯度下降
max_step = 10000
for i in range(max_step):
    sess.run(train, {x: x_train, y: y_train})
    if (i % 100) == 0:
        print('[%04.2f%%] W: %s b: %s loss: %s' % (i / max_step * 100, sess.run(W), sess.run(b), sess.run(loss, {x: x_train , y: y_train})))


print('W: %s b: %s loss: %s' % (sess.run(W), sess.run(b), sess.run(loss, {x: x_train , y: y_train})))

sess.close()
```

## TensorFlow 2.0

刚才那种 1.0 的有很多地方不方便对吧。声明了变量，还要手动 init，还要开一个 sess 去完成计算，很可怕。

TensorFlow 团队显然也发现了这个问题，所以在 TensorFlow 2.0 中，情况大为改观了。 TensorFlow 2.0 里计算 `1 + 1` 只需要一行代码了！

(注意，玩刚才的 v1 时，我们把 v2 的环境搞坏了，要重开一个 python REPL，重新 import 一下 tensorflow)

```python
>>> import tensorflow as tf
>>> tf.add(1,1)
<tf.Tensor: id=5, shape=(), dtype=int32, numpy=2>
>>> 
```

深度学习，借助成为神经网络的数据结构，以向前传播、向后传播算法为基础，给定一组训练集，通过梯度下降等方法确定神经网络中的参数，使这个神经网络对于给定的输入数据，经过这些参数的作用，给出预测结果。我认为，这样的神经网络大值等于一组线性变换。对输入进行线性变换（也就是一种映射），快速得到输出，这应该和人脑中神经元配合工作相似。

现在我们搞所谓的「人工智能」，每个人都是从头“建立”一个机器学习系统、以一个“初始化”的神经网络开始，给机器大量的数据进行训练，不断地试错、改进、试错、改进，进而让这个神经网络有了某一方面甚至可以超过人类的能力。

值得注意的是，人类学习，并不需要这样大量的数据训练！我们似乎天生就拥有类比、推理、抽象等相当高级的学习功能，而不是像机器学习那样不断试错、改进、试错、改进。当然，有的科学家通过很复杂的数据结构、经过长时间的训练，让自己的机器拥有了类似于人类的推理类比等高级学习能力。但是，这种能力依然有限，依然只是一组简单映射叠加共同作用的结果，通过大量数据训练后，只能用在特定的领域。比如，前几年新闻上说的AI做高考题，10分钟考140，它只是会做题的机器罢了，它不认识自己、不认识世界，只认识题目。

但是，我们从出生，并没有去花很长的时间从零开始去学习。我们并没有在婴儿时期先学习怎么推理、类比，然后再用这种高级学习技能去学习其他知识。我们天生就拥有这些高级学习能力，可以用这种能力认识自己、认识世界！通过进化、继承，人脑天生就可以做出这一组高级学习映射。而这一组天生的映射功能就是婴儿可以以不可思议的速度使用高级的抽象等方法进行学习的根本基础。

所以说，我认为，现在的以深度学习为主导的人工智能技术的根本不足之处就是——没有进化和继承！这一点直接导致了机器学习的局限，这也是为什么现在世界上基本没有一个完整的全功能的“人工智能”的原因。

在我的构想中，机器智能（我不爱用人工智能这个词，人工的意思就是假的、仿制的，而我认为机器是可以拥有真正的智能的，这是一种拥有自主性的、完整的、强大的、不同于人类的智能，我更愿意将其称为「机器智能」）这种东西的出现必须有一个前提——可繁殖、能继承、可以进化的电子生命。

没有生命的机器智能再强也不过只是人工智能罢了，学习速度缓慢，只要关机就一切归零。我不认为这样可以产生真正的思考能力。我觉得这样的人工产物和传统机器没有本质区别，不能「自主」认识自己和世界——这样的人工智能再强也只是传统机器罢了！而我要的是可以自己悟出第0定律的丹尼尔和吉斯卡。



