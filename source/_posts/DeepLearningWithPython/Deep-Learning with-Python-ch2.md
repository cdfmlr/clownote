---
categories:
- Machine Learning
- Deep Learning with Python
date: 2020-05-12 09:09:44
tag:
- Machine Learning
- Deep Learning
title: Python深度学习之初窥神经网络
---

# Deep Learning with Python

这篇文章是我学习《Deep Learning with Python》(第二版，François Chollet 著) 时写的系列笔记之一。文章的内容是从  Jupyter notebooks 转成 Markdown 的，当我完成所以文章后，会在 GitHub 发布我写的所有  Jupyter notebooks。

你可以在这个网址在线阅读这本书的正版原文(英文)：https://livebook.manning.com/book/deep-learning-with-python

这本书的作者也给出了一套 Jupyter notebooks：https://github.com/fchollet/deep-learning-with-python-notebooks

---

本文为 **第2章 开始之前：神经网络背后的数学** (Chapter 2. Before we begin: the mathematical building blocks of neural networks) 的笔记整合。

本文目录：

[TOC]

## 初窥神经网络

学编程语言从 “Hello World” 开始，学 Deep learning 从 `MINST` 开始。

MNIST 用来训练手写数字识别， 它包含 28x28 的灰度手写图片，以及每张图片对应的标签(0~9的值)。

### 导入MNIST数据集


```python
# Loading the MNIST dataset in Keras
from tensorflow.keras.datasets import mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
```

看一下训练集：


```python
print(train_images.shape)
print(train_labels.shape)
train_labels
```
输出：

    (60000, 28, 28)
    (60000,)
    
    array([5, 0, 4, ..., 5, 6, 8], dtype=uint8)



这是测试集：


```python
print(test_images.shape)
print(test_labels.shape)
test_labels
```
输出：

    (10000, 28, 28)
    (10000,)
    
    array([7, 2, 1, ..., 4, 5, 6], dtype=uint8)



### 网络构建

我们来构建一个用来学习 MNIST 集的神经网络：


```python
from tensorflow.keras import models
from tensorflow.keras import layers

network = models.Sequential()
network.add(layers.Dense(512, activation='relu', input_shape=(28 * 28, )))
network.add(layers.Dense(10, activation='softmax'))
```

神经网络是一个个「层」组成的。
一个「层」就像是一个“蒸馏过滤器”，它会“过滤”处理输入的数据，从里面“精炼”出需要的信息，然后传到下一层。

这样一系列的「层」组合起来，像流水线一样对数据进行处理。
层层扬弃，让被处理的数据，或者说“数据的表示”对我们最终希望的结果越来越“有用”。

我们刚才这段代码构建的网络包含两个「Dense 层」，这么叫是因为它们是密集连接（densely connected）或者说是 *全连接* 的。

数据到了最后一层（第二层），是一个 **10路** 的 softmax 层。
这个层输出的是一个数组，包含 10 个概率值（它们的和为1），这个输出「表示」的信息就对我们预测图片对应的数字相当有用了。
事实上这输出中的每一个概率值就分别代表输入图片属于10个数字（0～9）中的一个的概率！

### 编译

接下来，我们要 *编译* 这个网络，这个步骤需要给3个参数：

- 损失函数：评价你这网络表现的好不好的函数
- 优化器：怎么更新（优化）你这个网络
- 训练和测试过程中需要监控的指标，比如这个例子里，我们只关心一个指标 —— 预测的精度


```python
network.compile(loss="categorical_crossentropy",
                optimizer='rmsprop',
                metrics=['accuracy'])
```

### 预处理

#### 图形处理

我们还需要处理一下图形数据，把它变成我们的网络认识的样子。

MNIST 数据集里的图片是 28x28 的，每个值是属于 [0, 255] 的 uint8。
而我们的神经网络想要的是 28x28 的在 [0, 1] 中的 float32。


```python
train_images = train_images.reshape((60000, 28 * 28))
train_images = train_images.astype('float32') / 255

test_images = test_images.reshape((10000, 28 * 28))
test_images = test_images.astype('float32') / 255
```

#### 标签处理

同样，标签也是需要处理一下的。


```python
from tensorflow.keras.utils import to_categorical

train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)
```

### 训练网络


```python
network.fit(train_images, train_labels, epochs=5, batch_size=128)
```
输出：

    Train on 60000 samples
    Epoch 1/5
    60000/60000 [==============================] - 3s 49us/sample - loss: 0.2549 - accuracy: 0.9254
    Epoch 2/5
    60000/60000 [==============================] - 2s 38us/sample - loss: 0.1025 - accuracy: 0.9693
    Epoch 3/5
    60000/60000 [==============================] - 2s 35us/sample - loss: 0.0676 - accuracy: 0.9800
    Epoch 4/5
    60000/60000 [==============================] - 2s 37us/sample - loss: 0.0491 - accuracy: 0.9848
    Epoch 5/5
    60000/60000 [==============================] - 2s 42us/sample - loss: 0.0369 - accuracy: 0.9888
    
    <tensorflow.python.keras.callbacks.History at 0x13a7892d0>



可以看到，训练很快，一会儿就对训练集有 98%+ 的精度了。

再用测试集去试试：


```python
test_loss, test_acc = network.evaluate(test_images, test_labels, verbose=2)    # verbose=2 to avoid a looooong progress bar that fills the screen with '='. https://github.com/tensorflow/tensorflow/issues/32286
print('test_acc:', test_acc)
```
输出：

    10000/1 - 0s - loss: 0.0362 - accuracy: 0.9789
    test_acc: 0.9789


我们训练好的网络在测试集下的表现并没有之前在训练集中那么好，这是「过拟合」的锅。

## 神经网络的数据表示

Tensor，张量，任意维的数组（我的意思是编程的那种数组）。矩阵是二维的张量。

我们常把「张量的维度」说成「轴」。

### 认识张量

#### 标量 (0D Tensors)

Scalars，标量是 0 维的张量（0个轴），包含一个数。

标量在 numpy 中可以用 float32 或 float64 表示。


```python
import numpy as np

x = np.array(12)
x
```

输出：

    array(12)




```python
x.ndim    # 轴数（维数）
```

输出：

    1



#### 向量 (1D Tensors)

Vectors，向量是 1 维张量（有1个轴），包含一列标量（就是搞个array装标量）。


```python
x = np.array([1, 2, 3, 4, 5])
x
```

输出：


    array([1, 2, 3, 4, 5])




```python
x.ndim
```

输出：


    1



我们把这样有5个元素的向量叫做“5维向量”。
但注意**5D向量**可不是**5D张量**！

- 5D向量：只有1个轴，在这个轴上有5个维度。
- 5D张量：有5个轴，在每个轴上可以有任意维度。

这个就很迷，这“维度”有的时候是指轴数，有的时候是指轴上的元素个数。

所以，我们最好换种说法，用「阶」来表示轴数，说 **5阶张量**。

#### 矩阵 (2D Tensors)

Matrices，矩阵是 2 阶张量（2个轴，就是我们说的「行」和「列」），包含一列向量（就是搞个array装向量）。


```python
x = np.array([[5, 78, 2, 34, 0],
              [6, 79, 3, 35, 1],
              [7, 80, 4, 36, 2]])
x
```

输出：


    array([[ 5, 78,  2, 34,  0],
           [ 6, 79,  3, 35,  1],
           [ 7, 80,  4, 36,  2]])




```python
x.ndim
```

输出：


    2



#### 高阶张量

你搞个装矩阵的 array 就得到了3阶张量。

再搞个装3阶张量的 array 就得到了4阶张量，依次类推，就有高阶张量了。


```python
x = np.array([[[5, 78, 2, 34, 0],
               [6, 79, 3, 35, 1],
               [7, 80, 4, 36, 2]],
              [[5, 78, 2, 34, 0],
               [6, 79, 3, 35, 1],
               [7, 80, 4, 36, 2]],
              [[5, 78, 2, 34, 0],
               [6, 79, 3, 35, 1],
               [7, 80, 4, 36, 2]]])
x.ndim
```

输出：


    3



深度学习里，我们一般就用0～4阶的张量。

### 张量的三要素

- 阶数（轴的个数）：3，5，...
- 形状（各轴维数）：(2, 1, 3)，(6, 5, 5, 3, 6)，...
- 数据类型：float32，uint8，...

我们来看看 MNIST 里的张量数据：


```python
from tensorflow.keras.datasets import mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

print(train_images.ndim)
print(train_images.shape)
print(train_images.dtype)
```
输出：

    3
    (60000, 28, 28)
    uint8


所以 train_images 是个8位无符号整数的3阶张量。

打印个里面的图片看看：


```python
digit = train_images[0]

import matplotlib.pyplot as plt

print("image:")
plt.imshow(digit, cmap=plt.cm.binary)
plt.show()
print("label: ", train_labels[0])
```

输出：

![一张图片，显示了一个位于图像中央的数字5](https://tva1.sinaimg.cn/large/007S8ZIlgy1gepeqfrnx9j3073070747.jpg)


    label:  5


### Numpy张量操作

#### 张量切片：


```python
my_slice = train_images[10:100]
print(my_slice.shape)
```
输出：

    (90, 28, 28)


等价于：


```python
my_slice = train_images[10:100, :, :]
print(my_slice.shape)
```
输出：

    (90, 28, 28)


也等价于


```python
my_slice = train_images[10:100, 0:28, 0:28]
print(my_slice.shape)
```
输出：

    (90, 28, 28)


选出 **右下角** 14x14 的：


```python
my_slice = train_images[:, 14:, 14:]
plt.imshow(my_slice[0], cmap=plt.cm.binary)
plt.show()
```
输出：


![一张图片，在左上角有数字5的一部分](https://tva1.sinaimg.cn/large/007S8ZIlgy1gepeimx6pwj3073070a9v.jpg)


选出 中心处 14x14 的：


```python
my_slice = train_images[:, 7:-7, 7:-7]
plt.imshow(my_slice[0], cmap=plt.cm.binary)
plt.show()
```
输出：

![一张图片，显示了一个数字5，占满了整个图片](https://tva1.sinaimg.cn/large/007S8ZIlgy1gepeiqkaq6j3073070jr7.jpg)


#### 数据批量

深度学习的数据里，一般第一个轴（index=0）叫做「样本轴」（或者说「样本维度」）。

深度学习里，我们一般不会一次性处理整个数据集，我们一批一批地处理。

在 MNIST 中，我们的一个批量是 128 个数据：


```python
# 第一批
batch = train_images[:128]
# 第二批
batch = train_images[128:256]
# 第n批
n = 12
batch = train_images[128 * n : 128 * (n+1)]
```

所以，在使用 batch 的时候，我们也把第一个轴叫做「批量轴」。

### 常见数据张量表示

| 数据 | 张量维数 | 形状 |
| :--: | :--: | :-- |
| 向量数据 | 2D | (samples,features) |
| 时间序列 | 3D | (samples, timesteps, features) |
| 图像 | 4D | (samples, height, width, channels) 或 (samples, channels, height, width) |
| 视频 | 5D | (samples, frames, height, width, channels) 或 (samples, frames, channels, height, width) |



## 神经网络的“齿轮”: 张量运算

在我们的第一个神经网络例子中(MNIST)，我们的每一层其实都是对输入数据做了类似如下的运算：

```
output = relu(dot(W, input) + b)
```

input 是输入，
W 和 b 是层的属性，
output 是输出。

这些东西之间做了 relu、dot、add 运算，
接下来我们会解释这些运算。

### 逐元素操作(Element-wise)

Element-wise 的操作，就是分别对张量中的每一个元素作用。
比如，我们实现一个简单的 `relu` （`relu(x) = max(x, 0)`）:


```python
def naive_relu(x):
    assert len(x.shape) == 2    # x is a 2D Numpy tensor.
    x = x.copy()    # Avoid overwriting the input tensor.
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            x[i, j] = max(x[i, j], 0)
    return x
```

加法也是逐元素操作：


```python
def naive_add(x, y):
    # assert x and y are 2D Numpy tensors and have the same shape.
    assert len(x.shape) == 2
    assert x.shape == y.shape
    
    x = x.copy()    # Avoid overwriting the input tensor.
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            x[i, j] += y[i, j]
    return x
```

在 Numpy 里，这些都写好了。 具体的运算是交给 C 或 Fortran 写的 BLAS 进行的，速度很高。

你可以这样查看有没有装 BLAS：


```python
import numpy as np

np.show_config()
```
输出：

    blas_mkl_info:
      NOT AVAILABLE
    blis_info:
      NOT AVAILABLE
    openblas_info:
        libraries = ['openblas', 'openblas']
        library_dirs = ['/usr/local/lib']
        language = c
        define_macros = [('HAVE_CBLAS', None)]
    blas_opt_info:
        libraries = ['openblas', 'openblas']
        library_dirs = ['/usr/local/lib']
        language = c
        define_macros = [('HAVE_CBLAS', None)]
    lapack_mkl_info:
      NOT AVAILABLE
    openblas_lapack_info:
        libraries = ['openblas', 'openblas']
        library_dirs = ['/usr/local/lib']
        language = c
        define_macros = [('HAVE_CBLAS', None)]
    lapack_opt_info:
        libraries = ['openblas', 'openblas']
        library_dirs = ['/usr/local/lib']
        language = c
        define_macros = [('HAVE_CBLAS', None)]


下面是如何使用 numpy 的逐元素 relu、add：


```python
a = np.array([[1, 2, 3],
              [-1, 2, -3],
              [3, -1, 4]])
b = np.array([[6, 7, 8], 
              [-2, -3, 1], 
              [1, 0, 4]])

c = a + b    # Element-wise addition
d = np.maximum(c, 0)    # Element-wise relu

print(c)
print(d)
```
输出：

    [[ 7  9 11]
     [-3 -1 -2]
     [ 4 -1  8]]
    [[ 7  9 11]
     [ 0  0  0]
     [ 4  0  8]]


### 广播(Broadcasting)

当进行逐元素运算时，如果两个张量的形状不同，在可行的情况下，较小的张量会「广播」成和较大的张量一样的形状。

具体来说，可以通过广播，对形状为 `(a, b, ..., n, n+1, ..., m)` 和 `(n, n+1, ..., m)` 的两个张量进行逐元素运算。

比如：


```python
x = np.random.random((64, 3, 32, 10))    # x is a random tensor with shape (64, 3, 32, 10).
y = np.random.random((32, 10))    # y is a random tensor with shape (32, 10).
z = np.maximum(x, y)    # The output z has shape (64, 3, 32, 10) like x.
```

广播的操作如下：

1. 小张量增加轴（广播轴），加到和大的一样（ndim）
2. 小张量的元素在新轴上重复，加到和大的一样（shape）

E.g. 
        
    x: (32, 10), y: (10,)
    Step 1: add an empty first axis to y: Y -> (1, 10)
    Step 2: repeat y 32 times alongside this new axis: Y -> (32, 10)

在完成后，有 `Y[i, :] == y for i in range(0, 32)`

当然，在实际的实现里，我们不这样去复制，这样太浪费空间了，
我们是直接在算法里实现这个“复制的”。
比如，我们实现一个简单的向量和矩阵相加：


```python
def naive_add_matrix_and_vector(m, v):
    assert len(m.shape) == 2    # m is a 2D Numpy tensor.
    assert len(v.shape) == 1    # v is a Numpy vector.
    assert m.shape[1] == v.shape[0]
    
    m = m.copy()
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            m[i, j] += v[j]
    return m

naive_add_matrix_and_vector(np.array([[1 ,2, 3], [4, 5, 6], [7, 8, 9]]), 
                            np.array([1, -1, 100]))
```
输出：




    array([[  2,   1, 103],
           [  5,   4, 106],
           [  8,   7, 109]])



### 张量点积(dot)

张量点积，或者叫张量乘积，在 numpy 里用 `dot(x, y)` 完成。

点积的操作可以从如下的简单程序中看出：


```python
# 向量点积
def naive_vector_dot(x, y):
    assert len(x.shape) == 1
    assert len(y.shape) == 1
    assert x.shape[0] == y.shape[0]
    
    z = 0.
    for i in range(x.shape[0]):
        z += x[i] * y[i]
    return z


# 矩阵与向量点积
def naive_matrix_vector_dot(x, y):
    z = np.zeros(x.shape[0])
    for i in range(x.shape[0]):
        z[i] = naive_vector_dot(x[i, :], y)
    return z


# 矩阵点积
def naive_matrix_dot(x, y):
    assert len(x.shape) == 2
    assert len(y.shape) == 2
    assert x.shape[1] == y.shape[0]
    
    z = np.zeros((x.shape[0], y.shape[1]))
    for i in range(x.shape[0]):
        for j in range(y.shape[1]):
            row_x = x[i, :]
            column_y = y[:, j]
            z[i, j] = naive_vector_dot(row_x, column_y)
    return z
```


```python
a = np.array([[1, 2, 3],
              [-1, 2, -3],
              [3, -1, 4]])
b = np.array([[6, 7, 8], 
              [-2, -3, 1], 
              [1, 0, 4]])
naive_matrix_dot(a, b)
```
输出：




    array([[  5.,   1.,  22.],
           [-13., -13., -18.],
           [ 24.,  24.,  39.]])



对于高维的张量点积，其实也是一样的。
例如，(这说的是shape哈)：

```
(a, b, c, d) . (d,) -> (a, b, c)
(a, b, c, d) . (d, e) -> (a, b, c, e)
```

### 张量变形(reshaping)

这个操作，简言之就是，，，还是那些元素，只是排列的方式变了。


```python
x = np.array([[0., 1.],
              [2., 3.],
              [4., 5.]])
print(x.shape)
```
输出：

    (3, 2)



```python
x.reshape((6, 1))
```
输出：



    array([[0.],
           [1.],
           [2.],
           [3.],
           [4.],
           [5.]])




```python
x.reshape((2, 3))
```
输出：



    array([[0., 1., 2.],
           [3., 4., 5.]])



「转置」(transposition) 是一种特殊的矩阵变形，
转置就是行列互换。

原来的 `x[i, :]`，转置后就成了 `x[:, i]`。


```python
x = np.zeros((300, 20))
y = np.transpose(x)
print(y.shape)
```
输出：

    (20, 300)



## 神经网络的“引擎”: 基于梯度的优化

再看一次我们的第一个神经网络例子中(MNIST)，每一层对输入数据做的运算：

```
output = relu(dot(W, input) + b)
```

这个式子里：W 和 b 是层的属性（权重，或着说可训练参数）。
具体来说，

- `W` 是 kernel 属性；
- `b` 是 bias 属性。

这些「权重」就是神经网络从数据中学习到的东西。

一开始，这些权重被随机初始化成一些较小的值。然后从这次随机的输出开始，反馈调节，逐步改善。

这个改善的过程是在「训练循环」中完成的，只有必要，这个循环可以一直进行下去：

1. 抽取一批训练数据 x 以及对应的 y
2. 向前传播，得到 x 经过网络算出来的预测 y_pred
3. 通过 y_pred 与 y，计算出损失
4. 通过某种方式调整参数，减小损失

前三步都比较简单，第4步更新参数比较复杂，一种比较有效、可行的办法就是利用可微性，通过计算梯度，向梯度的反方向移动参数。

### 导数(derivative)

这一节解释了导数的定义。

(直接去看书吧。)

知道了导数，那要更新 x 来最小化一个函数 `f(x)`，其实只需将 x 向导数的反方向移动。

### 梯度(gradient)

「梯度」是张量运算的导数。或者说「梯度」是「导数」在多元函数上的推广。
某点的梯度代表的是该点的曲率。

考虑:

```
y_pred = dot(W, x)
loss_value = loss(y_pred, y)
```

若固定 x 和 y，则 loss_value 将是一个 W 的函数：

```
loss_value = f(W)
```

设当前点为 `W0`，
则 f 在 W0 的导数(梯度)记为 `gradient(f)(W0)`，
这个梯度值与 W 同型。
其中每个元素 `gradient(f) (W0)[i, j]` 代表改变 `W0[i, j]` 时，f 的变化方向及大小。

所以，要改变 W 的值来实现 `min f`，就可以向梯度的反方向（即**梯度下降**的方向）移动：

```
W1 = W0 - step * gradient(f)(W0)
```


### 随机梯度下降(Stochastic gradient descent)

理论上，给定一个可微函数，其最小值一定在导数为0的点中取到。所以我们只有求出所有导数为0的点，比较其函数值，就可以得到最小值。

这个方法放到神经网络中，就需要解一个关于 `W` 的方程 `gradient(f)(W) = 0`，这是个 N 元方程（N=神经网络中参数个数），而实际上N一般不会少于1k，这使得解这个方程变得几乎不可行。


所以面对这个问题，我们利用上面介绍的4步法，其中第四步使用梯度下降，逐步往梯度的反方向更新参数，一小步一小步地朝减小损失的方向前进：

1. 抽取一批训练数据 x 以及对应的 y
2. 向前传播，得到 x 经过网络算出来的预测 y_pred
3. 通过 y_pred 与 y，计算出损失
4. 通过某种方式调整参数，减小损失
    1. 向后传播，计算损失函数关于网络参数的梯度
    2. 朝梯度的反方向稍微移动参数即可减小损失（W -= step * gradient）

这个方法叫做「小批量随机梯度下降」（mini-batch stochastic gradient descent，mini-batch SGD）。
随机一词是指我们在第1步抽取数据是随机抽取的。

有一些变种的 SGD 不只看当前梯度就更新值了，它们还要看上一次的权重更新。这些变体被称作「优化方法(optimization method)」或者「优化器(optimizer)」。在很多这些变体中，都会使用一个叫「动量(momentum)」的概念。

「动量」主要处理 SGD 中的两个问题：收敛速度和局部极小点。
用动量可以避免在 learning rate 比较小时收敛到局部最优解，而不是向全局最优解继续前进。

这里的动量就是来自物理的那个动量概念。我们可以想象，一个小球在损失曲面上往下(梯度下降的方向)滚，如果有足够的动量，它就可以“冲过”局部最小值，不被困在那里。
在这个例子中，小球的运动不但被当前位置的坡度（当前的加速度）决定，还受当前的速度（这取决于之前的加速度）的影响。

这个思想放到神经网络中，也就是，一次权重值的更新，不但看当前的梯度，还要看上一次权重更新：

```python
# naive implementation of Optimization with momentum
past_velocity = 0.
momentum = 0.1    # Constant momentum factor
while loss > 0.01:    # Optimization loop
    w, loss, gradient = get_current_parameters()
    velocity = past_velocity * momentum + learning_rate * gradient
    w = w + momentum * velocity - learning_rate * gradient
    past_velocity = velocity
    update_parameter(w)
```

### 反向传播算法：链式求导

神经网络是一大堆张量操作链式和在一起的，比如：

```
f(W1, W2, W3) = a(W1, b(W2, c(W3)))    # 其中 W1, W2, W3 是权重
```

微积分里有个「链式法则(chain rule)」可以给这种复合函数求导：`f(g(x)) = f'(g(x)) * g'(x)`

把这个链式法则用到神经网络就搞出了一个叫「反向传播(Backpropagation)」的算法，
这个算法也叫「反式微分(reverse-mode differentiation)」。

反向传播从最终算出的损失出发，从神经网络的最顶层反向作用至最底层，用这个链式法则算出每层里每个参数对于损失的贡献大小。

现在的 TensorFlow 之类的框架，都有种叫「符号微分(symbolic differentiation)」的能力。
这使得这些框架可以自动求出给定神经网络里操作的梯度函数，然后我们就不用手动实现反向传播了（虽然有意思，但写起来真的烦），直接从梯度函数取值就行了。