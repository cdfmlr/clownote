---
categories:
- Machine Learning
- Deep Learning with Python
date: 2020-08-19 10:12:36.840073
tag:
- Machine Learning
- Deep Learning
title: Python深度学习之模型优化
---

# Deep Learning with Python

这篇文章是我学习《Deep Learning with Python》(第二版，François Chollet 著) 时写的系列笔记之一。文章的内容是从  Jupyter notebooks 转成 Markdown 的，你可以去 [GitHub](https://github.com/cdfmlr/Deep-Learning-with-Python-Notebooks) 或 [Gitee](https://gitee.com/cdfmlr/Deep-Learning-with-Python-Notebooks) 找到原始的 `.ipynb` 笔记本。

你可以去[这个网站在线阅读这本书的正版原文](https://livebook.manning.com/book/deep-learning-with-python)(英文)。这本书的作者也给出了配套的 [Jupyter notebooks](https://github.com/fchollet/deep-learning-with-python-notebooks)。

本文为 **第7章  高级的深度学习最佳实践** (Chapter 7. *Advanced deep-learning best practices*) 的笔记之一。

[TOC]

## 7.3 Getting the most out of your models

> 让模型性能发挥到极致

如果你只是想搞出个还不错的模型，无脑随便尝试各种网络架构基本就可以了。但如果你要开发出性能卓越、做到极致的模型，你就需要考虑一下后文给出的技巧。

### 高级架构模式

想要构架卓越的模型，你应该认识「残差连接」、「标准化」和「深度可分离卷积」这几个常用的“设计模式”。

#### 残差连接

> 注：这一段是在 7.1 里写的，这里只是复制过来让这一部分更加完整。

残差连接(residual connection) 是一种现在很常用的组件，它解决了大规模深度学习模型梯度消失和表示瓶颈问题。通常，向任何多于 10 层的模型中添加残差连接，都可能会有所帮助。

- 梯度消失：就是经过的层多了，之前学到的表示变得模糊，甚至完全丢失，导致网络无法训练。
- 表示瓶颈：堆叠起来层，后一层只能访问到前一层学到的东西。如果某一层太小（激活中能够塞入的信息少）就把信息卡下来，出现瓶颈了。

残差连接是让前面某层的输出作为后面某层的输入（在网络中创造捷径）。前面层的输出并没有与后面层的激活连接在一起，而是与后面层的激活相加（若形状不同，用线性变换将前面层的激活改变成目标形状）。

> 注：线性变换可以用不带激活的 Dense 层，或着在 CNN 中用不带激活 1×1 卷积。

```python
from keras import layers

x = ...

y = layers.Conv2D(128, 3, activation='relu', padding='same')(x)
y = layers.Conv2D(128, 3, activation='relu', padding='same')(y)
y = layers.MaxPooling2D(2, strides=2)(y)

# 形状不同，要做线性变换：
residual = layers.Conv2D(128, 1, strides=2, padding='same')(x)  # 使用 1×1 卷积，将 x 线性下采样为与 y 具有相同的形状

y = layers.add([y, residual])
```

#### 标准化

标准化(normalization)，用于让模型看到的不同样本彼此之间更加相似，有助于模型的优化和泛化。

最常见的数据标准化，就是使数据均值为 0、方差为 1：

```python
normalized_data = (data - np.mean(data, axis=...)) / np.std(data, axis=...)
```

我们都知道在将数据输入模型之前对数据做标准化。但在网络的每一次变换之后，我们也应该考虑数据标准化。每一层输出之后，可能之前的标准化就被破坏了，我们需要考虑这个问题。

**批标准化**(batch normalization)就是解决这个问题的一种方法：训练过程中，它会在内部保存已读取每批数据均值和方差的指数移动平均值。因此，训练过程中均值和方差随时间发生变化，批标准化也可以适应性地将数据标准化。这个方法有助于梯度传播，允许更深的网络（类似于残差连接）。

Keras 中批标准化用 `BatchNormalization` 层实现，通常在卷积层或密集连接层之后使用:

```python
# Conv
conv_model.add(layers.Conv2D(32, 3, activation='relu'))
conv_model.add(layers.BatchNormalization())

# Dense
dense_model.add(layers.Dense(32, activation='relu'))
dense_model.add(layers.BatchNormalization())
```

BatchNormalization 层接收一个 axis 参数，它指定应该对哪个特征轴做标准化，默认值是 -1。对于 Keras 默认的 Dense、Conv1D、RNN 和 Conv2D 这个都是对的。但对于 `data_format` 设为 `"channels_first"` 的 Conv2D，特征轴是 1，所以需要设置 `axis=1`。

#### 深度可分离卷积

深度可分离卷积层(depthwise separable convolution)，在 Keras 中叫写作 `SeparableConv2D`，作用和普通的 Conv2D 是一样的。但 SeparableConv2D 比 Conv2D 更轻量、训练更快、精度更高。

SeparableConv2D 层对输入的每个通道分别执行空间卷积，然后通过逐点卷积(1×1 卷积)整合输出结果。这么做就将空间特征学习和通道特征学习分开了，往往能够使用更少的数据学到更好的表示。（这和以前提过的 Xception 模型很类似。事实上，深度可分离卷积是 Xception 架构的基础）

![深度可分离卷积: 深度卷积 + 逐点卷积](https://tva1.sinaimg.cn/large/007S8ZIlgy1ghpi4ytqqvj318a0koadm.jpg)

对于数据比较少的数据，从头开始训练的画，这个东西很有用，例如下面是个图像分类任务：


```python
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras import layers

height = 64
width = 64
channels = 3
num_classes = 10

model = Sequential()
model.add(layers.SeparableConv2D(32, 3, 
                                 activation='relu', 
                                 input_shape=(height, width, channels,)))
model.add(layers.SeparableConv2D(64, 3, activation='relu'))
model.add(layers.MaxPooling2D(2))

model.add(layers.SeparableConv2D(64, 3, activation='relu'))
model.add(layers.SeparableConv2D(128, 3, activation='relu'))
model.add(layers.MaxPooling2D(2))

model.add(layers.SeparableConv2D(64, 3, activation='relu'))
model.add(layers.SeparableConv2D(128, 3, activation='relu'))
model.add(layers.GlobalAveragePooling2D())

model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(num_classes, activation='softmax'))

model.compile(optimizer='rmsprop', loss='categorical_crossentropy')
```

对于更大型的任务时，上 Xception 就更好了。

### 超参数优化

除了使用高级架构模式，超参数优化也是个值得一提的工作。我们写模型的时候需要决定很多超参数：

模型中堆叠多少层，每层包含多少个单元，用什么激活函数......

调节这些超参数并没有固定的规则，主要是靠直觉和反复实验。这种反复实验，可能性太多，各种超参数的组合，太复杂了。一天到晚调超参数就不是人干的事，这种事情还是给机器自己去做比较好。所以我们要指定一个可以程序化的超参数调节流程：

1. 选择一组超参数
2. 构建相应的模型
3. 将模型在小批量数据上拟合、验证性能
4. 选择要尝试的下一组超参数
4. 重复上述过程（2～4）
5. 选出上面实验中的最佳超参数

这个过程的关键在于，给定多组可选的超参数，利用「历史验证性能」来自动选择下一组需要评估的超参数。可以用「简单随机搜索」、「贝叶斯优化」、「遗传算法」等算法完成这个工作。

更新超参数其实是很难的，每次尝试的计算代价太大，每次都要从头训练一次；而且超参数是不连续、不可微的，不能用梯度下降之类的算法。

所以，其实自动的超参数优化现在还不成熟，可用的工具十分有限。不过还是有好些库可以用来自动调节 Keras 的超参数的:

- [Hyperas](https://github.com/maxpumperla/hyperas)，这个库比较老牌，也是书上提到的，但截止 2020 年 8 月，已经好几个月没提交了；
- [Keras Tuner](https://github.com/keras-team/keras-tuner) ，这个库比较新，是我前几天看到的，Star 数已经和 Hyperas 持平了。
- ...

**注意**：自动超参数的调节，本质上是在验证数据上训练超参数。在做大规模超参数自动优化时，一定要注意，验证集过拟合的问题！

### 模型集成

模型集成(model ensembling)，也是一种很强大的技术。模型集成，是指将一系列不同模型的预测结果汇集到一起，从而得到更好的预测结果。

对于同一个问题，不同的模型，虽然可能都能比较好的解决问题，但正如盲人摸象，可能每个模型都得到了数据真相的一部分，但不是全部真相。将各种观点汇集在一起，就可能得到对数据更加准确的描述。在这种想法下，可以说，将很多模型集成到一起，必然可以打败任何单个模型。

对于模型集成，使用的模型的多样性十分重要。Diversity is strength. 用来集成的模型应该尽可能好，同时尽可能不同。相同的网络，使用不同的随机初始化多次独立训练，然后集成，这样意义就不大了。更好的做法应该是使用架构非常不同的模型去集成，这样各个模型的偏差在不同方向上，集成让偏差会彼此抵消，结果才会更加稳定、准确。

以分类问题为例，首先，我们有了一些不同的模型：

```python
preds_a = model_a.predict(x_val)
preds_b = model_b.predict(x_val)
preds_c = model_c.predict(x_val)
preds_d = model_d.predict(x_val)
```

可以用多种不同的方法来集成它们，最简单的办法是，取平均：

```python
final_preds = 0.25 * (preds_a + preds_b + preds_c + preds_d)
```

由于每一个模型的性能会有差距，所以更好的办法是加权平均：

```python
final_preds = 0.5 * preds_a + 0.25 * preds_b + 0.1 * preds_c + 0.15 * preds_d
```

其中的权重，可以使用基于经验给出、使用随机搜索或者其他优化算法得到。
