---
categories:
- Machine Learning
- Deep Learning with Python
date: 2020-07-29 21:09:00
tag:
- Machine Learning
- Deep Learning
title: Python深度学习之计算机视觉
---

# Deep Learning with Python for computer vision

这篇文章是我学习《Deep Learning with Python》(第二版，François Chollet 著) 时写的系列笔记之一。文章的内容是从  Jupyter notebooks 转成 Markdown 的，你可以去 [GitHub](https://github.com/cdfmlr/Deep-Learning-with-Python-Notebooks) 或 [Gitee](https://gitee.com/cdfmlr/Deep-Learning-with-Python-Notebooks) 找到原始的 `.ipynb` 笔记本。

你可以去[这个网站在线阅读这本书的正版原文](https://livebook.manning.com/book/deep-learning-with-python)(英文)。这本书的作者也给出了配套的 [Jupyter notebooks](https://github.com/fchollet/deep-learning-with-python-notebooks)。

本文为 **第5章  深度学习用于计算机视觉** (Chapter 5. *Deep learning for computer vision*) 的笔记整合。

[TOC]

## 卷积神经网络简介

> 5.1 Introduction to convnets

卷积神经网络处理计算机视觉问题很厉害啦。

首先看一个最简单的卷积神经网络处理 MNIST 完爆第二章里的全连接网络的例子：


```python
from tensorflow.keras import layers
from tensorflow.keras import models

model = models.Sequential()

model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(64, (3, 3), activation='relu'))

model.add(layers.Flatten())
model.add(layers.Dense(64, activation="relu"))
model.add(layers.Dense(10, activation="softmax"))
```

这里我们用的 Conv2D 层要的 `input_shape` 是 `(image_height, image_width, image_channels)` 这种格式的。

Conv2D 和 MaxPooling2D 层的输出都是 3D 张量 `(height, width, channels)`， height 和 width 会逐层减小，channels 是由 Conv2D 的第一个参数控制的。

最后的三层里，我们是把最后一个 Conv2D 层的 `(3, 3, 64)` 的张量用一系列全连接层变成想要的结果向量：Flatten 层是用来把我们的 3D 张量展平(flatten，其实我想写成“压”、“降”之类的，这才是flatten的本意，但标准的中文翻译是展平)到 1D 的。 然后后面的两个 Dense 层就行我们在第二章做的那种，最后得到一个 10 路的分类。

最后，看一下模型结构：


```python
model.summary()
```

    Model: "sequential_1"
    _________________________________________________________________
    Layer (type)                 Output Shape              Param #   
    =================================================================
    conv2d_3 (Conv2D)            (None, 26, 26, 32)        320       
    _________________________________________________________________
    max_pooling2d_2 (MaxPooling2 (None, 13, 13, 32)        0         
    _________________________________________________________________
    conv2d_4 (Conv2D)            (None, 11, 11, 64)        18496     
    _________________________________________________________________
    max_pooling2d_3 (MaxPooling2 (None, 5, 5, 64)          0         
    _________________________________________________________________
    conv2d_5 (Conv2D)            (None, 3, 3, 64)          36928     
    _________________________________________________________________
    flatten_1 (Flatten)          (None, 576)               0         
    _________________________________________________________________
    dense_2 (Dense)              (None, 64)                36928     
    _________________________________________________________________
    dense_3 (Dense)              (None, 10)                650       
    =================================================================
    Total params: 93,322
    Trainable params: 93,322
    Non-trainable params: 0
    _________________________________________________________________


好了，网络就建成这样了，还是很简单的，接下来就训练它了，大致和之前第二章里的是一样的（但注意reshape的形状不一样）：


```python
# Load the TensorBoard notebook extension
# TensorBoard 可以可视化训练过程
%load_ext tensorboard
# Clear any logs from previous runs
!rm -rf ./logs/ 
```


```python
# 在 MNIST 图像上训练卷积神经网络

import datetime
import tensorflow as tf

from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

train_images = train_images.reshape((60000, 28, 28, 1))
train_images = train_images.astype('float32') / 255

test_images = test_images.reshape((10000, 28, 28, 1))
test_images = test_images.astype('float32') / 255

train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

# 准备 TensorBoard
log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

model.compile(optimizer='rmsprop',
              loss="categorical_crossentropy",
              metrics=['accuracy'])
model.fit(train_images, train_labels, epochs=5, batch_size=64,
          callbacks=[tensorboard_callback])
```

    Train on 60000 samples
    Epoch 1/5
    60000/60000 [==============================] - 36s 599us/sample - loss: 0.0156 - accuracy: 0.9953
    Epoch 2/5
    60000/60000 [==============================] - 33s 554us/sample - loss: 0.0127 - accuracy: 0.9960
    Epoch 3/5
    60000/60000 [==============================] - 31s 524us/sample - loss: 0.0097 - accuracy: 0.9971
    Epoch 4/5
    60000/60000 [==============================] - 32s 529us/sample - loss: 0.0092 - accuracy: 0.9974
    Epoch 5/5
    60000/60000 [==============================] - 31s 523us/sample - loss: 0.0095 - accuracy: 0.9971





    <tensorflow.python.keras.callbacks.History at 0x1441fa9d0>




```python
%tensorboard --logdir logs/fit
```

(这理会输出 tensorboard 显示的可视化模型训练情况)

<iframe id="tensorboard-frame-f4ae12888a3a411e" width="100%" height="800" frameborder="0">
</iframe>
<script>
  (function() {
    const frame = document.getElementById("tensorboard-frame-f4ae12888a3a411e");
    const url = new URL("/", window.location);
    url.port = 6006;
    frame.src = url;
  })();
</script>



来在测试集看一下结果：


```python
test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
print(test_loss, test_acc)
```

    10000/1 - 1s - loss: 0.0172 - accuracy: 0.9926
    0.03441549262946125 0.9926


### 卷积

#### 卷积神经网络

我们之前用的*密集连接层*是在整个输入特征空间（在 MNIST 中就是所有的像素）中学习全局模式的；而这里的卷积层是学习局部模式的。也就是说，Dense 是学整个图像的，而 Conv 是学图像的局部，比如在我们刚才写的代码里是学了 3x3 的窗口：

![卷积层学习局部模式](https://tva1.sinaimg.cn/large/007S8ZIlgy1ggo1xjvr02j315g0o6n12.jpg)

这种卷积神经网络具有两个性质：

- 卷积神经网络学到的模式是平移不变的(translation invariant)：卷积神经网络学习到某个模式之后，在其他地方又看到了这个一样的模式，它就会认出它已经学过这个了，不用再去学一次了。而对于 Dense 的网络，即使遇到有一样的局部部分依然要去重新学习一次。这个性质让卷积神经网络可以高效利用数据，它只需要更少的训练样本就可以学到泛化比较好的数据表示（一个个局部都记住了嘛，而不是靠整体去映射）。

- 卷积神经网络可以学到模式的空间层次结构(spatial hierarchies of patterns)：卷积神经网络在第一层学完了一个一个小的局部模式之后，下一层又可以用这些小局部拼出大一些的模式。然后这样多搞几层，卷积神经网络就可以学到越来越复杂、越来越抽象的视觉概念了，就是下面图片这个意思：

![卷积神经网络可以学到模式的空间层次结构](https://tva1.sinaimg.cn/large/007S8ZIlgy1ggo29tuqchj30zh0u0dn6.jpg)

#### 卷积层

我们刚才例子中用来表示图片的那种 3D 张量，包括两个空间轴 height、width 和一个深度轴 depth（也叫 channels 轴），对于 RGB 图片，深度轴的维度就是3，分别表示3种颜色嘛；而对于 MNIST 这种灰度图片，深度就是1，只用一个数去表示灰度值。在这种3D张量和在上面做的卷积运算的结果被称作 *feature map*（特征图）。

卷积运算会从输入特征图中提取出一个个小分块，并对所有这些分块施加一个相同的变换，得到输出特征图。输出特征图仍是一个 3D 张量：具有宽度和高度，其深度可能是任意值，深度的大小是该层的一个参数，深度轴里的每个 channel 都代表一个 filter (过滤器)。filter 会对输入数据的某一方面进行编码，比如，某个过滤器可以编码“输入中包含一张脸”这种概念。

在刚才的 MNIST 例子中，第一个卷积层接受尺寸为 `(28, 28, 1)` 的输入特征图，输出一个尺寸为 `(26, 26, 32)` 的特征图。这个输出中包含 32 个 filter，在每个深度轴中的 channel 都包含有 26x26 的值，叫做 filter 对输入的响应图(response map)，表示 filter 在输入中不同位置上的运算结果。这也就是特征图为什么叫特征图的原因了：深度轴的每个维度都是一个特征(或过滤器)，而 2D 张量 `output[:, :, n]` 是这个过滤器在输入上的响应的二维空间图。

![响应图的示意图](https://tva1.sinaimg.cn/large/007S8ZIlgy1ggo5m7eb85j31jy0jgagx.jpg)

#### 卷积运算

关于卷积，，emmm，复变没怎么听懂，我主要是看[「知乎: 如何通俗易懂地解释卷积?」](https://www.zhihu.com/question/22298352)来理解的。这里我们主要用的是这种作用：

![卷积](https://tva1.sinaimg.cn/large/007S8ZIlgy1ggo6h1a5wfg30f30f4n2g.gif)

Keras 的 Conv2D 层初始化写成：

```python
Conv2D(output_depth, (window_height, window_width))
```

其中包含了卷积运算有两个核心参数：

- 输出特征图的深度：在我们刚才的 MNIST 例子里用了 32 和 64；
- 从输入中提取的每个块（滑窗）的尺寸：一般是 3x3 或者 5x5；

卷积运算会像滑动窗口一样的遍历所有可能的位置，把输入中每一小块的特征 `(window_height, window_width, input_depth)` 通过与一个称作卷积核(convolution kernel)的要学习的权重矩阵做点乘，变化得到一个向量 `(output_depth, )`。所有的这种结果向量拼在一起就得到了一个 3D 的最终输出 `(height, width, output_depth)`，其中的每个值就是输入对应过来的，比如取 3x3 的滑窗，则 `output[i, j, :]` 来自 `input[i-1:i+1, j-1:j+1, :]`。

![卷积的工作原理](https://tva1.sinaimg.cn/large/007S8ZIlgy1ggo6cg398tj30t40w8n2u.jpg)

关于卷积和 CNN 可以去看看这篇文章：[Convolutional Neural Networks - Basics, An Introduction to CNNs and Deep Learning](https://mlnotebook.github.io/post/CNN1/)

注意，因为边界效应(border effects)和使用了步幅(strides)，我们输出的宽度和高度可能与输入的宽度和高度不同。

##### 边界效应和填充

边界效应就是你在做滑窗之后得到的矩阵大小会缩小一圈（边界没了）。例如现输入一个 5x5 的图片，取 3x3 的小块只能取出 9 块来，因此输出的结果为 3x3 的：

![边界效应](https://tva1.sinaimg.cn/large/007S8ZIlgy1ggo9oanxxcj31h60rc76w.jpg)

之前我们做的 MNIST 也是类似的，一开始输入 28x28，第一层取 3x3 的，结果就是 26x26 了。

如果不希望这种减小发生，即希望保持输出的空间维度与输入的一致，则需要做填充(padding)。填充就是在输入的图片边界上加一些行和列，3x3 加1圈，5x5 要加2圈：

![填充](https://tva1.sinaimg.cn/large/007S8ZIlgy1ggo9vytgefj31fa0kote4.jpg)

Keras 的 Conv2D 层里可以用 `padding` 参数来设置使用填充。`padding` 可以设为：

- `"valid"`（默认值）：不做填充，只取“有效”的块。例如在 5×5 的输入特征图中，可以提取 3×3 图块的有效位置；
- `"same"`： 做填充，使输出和输入的 width、height 相等。

##### 卷积步幅

卷积的步幅就是一次滑窗移多少，之前我们一直做的都是步幅为1的。我们把步幅大于 1 的卷积叫做**步进卷积**(strided convolution)，比如下面这个是步幅为 2 的：

![步幅为 2 的步进卷积](https://tva1.sinaimg.cn/large/007S8ZIlgy1ggp4beuceuj31dw0pu76q.jpg)

然而步进卷积在实际里面用的并不多😂，要做这种对特征图的下采样（downsampled）我们一般用最大池化。

> 注：
>
> **下采样**：对于一个样值序列间隔几个样值取样一次，这样得到新序列就是原序列的下采样。
>
> From [百度百科](https://baike.baidu.com/item/下采样)
> 


### 最大池化

与步进卷积类似，最大池化是用来对特征图进行下采样的。在一开始的 MNIST 例子中，我们用了 MaxPooling2D 层之后，特征图的尺寸就减半了。

最大池化是在一个窗口里，从输入特征图取出每个 channel 的最大值，然后输出出来。这个运算和卷积很类似，不过施加的函数是一个 max。

最大池化我们一般都是用 2x2 的窗口，步幅为 2，这样取可以将特征图下采样2倍。（卷积是一般取3x3窗口和步幅1）

如果不用最大池化，直接把一大堆卷积层堆起来，会有两个问题：

- 特征图尺寸下降的慢，搞到后面参数太多了，会加重过拟合；
- 不利于空间层级结构的学习：一直一小点一小点的用卷积层去学，不利于看到更抽象的整体。

除了最大池化，下采样的方式还有很多：比如步进卷积、平均池化之类的。但一般用最大池化效果比较好，我们要的是知道有没有某个特征嘛，如果用平均去就把这个特征“减淡”了，如果用步进卷积又可能把这个信息错过了。

总而言之，使用最大池化/其他下采样的原因，一是减少需要处理的特征图的元素个数，二是通过让一系列的卷积层观察到越来越大的窗口(看到的覆盖越来越多比例的原始输入)，从而学到空间层级结构。




## 在小型数据集上从头训练一个卷积神经网络

> 5.2 Training a convnet from scratch on a small dataset

我们搞计算机视觉的时候，经常要处理的问题就是在很小的数据集上训练一个图像分类的模型。emmm，这里的“很小”可以是几百到几万。

从这一节开始到后面几节，我们要搞的就是从头开始训练一个小型模型、使用预训练的网络做特征提取、对预训练的网络进行微调，这些步骤合起来就可以用于解决小型数据集的图像分类问题了。

我们这一节要做的是从头开始训练一个小型模型来分类猫狗的图片。不做正则化，先不管过拟合的问题。


### 下载数据

我们将使用 Dogs vs. Cats dataset 来训练模型，这个数据集里面是一大堆猫、狗的照片。这个数据集就不是 Keras 内置的了，我们可以从 Kaggle 下载：[https://www.kaggle.com/c/dogs-vs-cats/data](https://www.kaggle.com/c/dogs-vs-cats/data)

下载下来解压缩，，，（emmmm有点大我的 MBP 都装不下了，放移动硬盘上才解出来的😂，emmmm，又想起来该买个新固态了）。

然后来创建我们要用的数据集：训练集猫狗各1000个样本，验证集各500个，测试集各500个。编程来完成这个工作：


```python
# 将图像复制到训练、验证和测试的目录
import os, shutil

original_dataset_dir = '/Volumes/WD/Files/dataset/dogs-vs-cats/dogs-vs-cats/train'    # 原始数据集

base_dir = '/Volumes/WD/Files/dataset/dogs-vs-cats/cats_and_dogs_small'    # 将要保存的较小数据集的位置
os.mkdir(base_dir)


# 创几个目录放划分后的训练、验证和测试集
train_dir = os.path.join(base_dir, 'train')
os.mkdir(train_dir)
validation_dir = os.path.join(base_dir, 'validation')
os.mkdir(validation_dir)
test_dir = os.path.join(base_dir, 'test')
os.mkdir(test_dir)

# 分开放猫狗
train_cats_dir = os.path.join(train_dir, 'cats')
os.mkdir(train_cats_dir)
train_dogs_dir = os.path.join(train_dir, 'dogs')
os.mkdir(train_dogs_dir)

validation_cats_dir = os.path.join(validation_dir, 'cats')
os.mkdir(validation_cats_dir)
validation_dogs_dir = os.path.join(validation_dir, 'dogs')
os.mkdir(validation_dogs_dir)

test_cats_dir = os.path.join(test_dir, 'cats')
os.mkdir(test_cats_dir)
test_dogs_dir = os.path.join(test_dir, 'dogs')
os.mkdir(test_dogs_dir)

# 复制猫的图片
fnames = [f'cat.{i}.jpg' for i in range(1000)]    # 这里用了 f-String，要求 Python >= 3.6，老版本可以用 'cat.{}.jpg'.format(i)
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(train_cats_dir, fname)
    shutil.copyfile(src, dst)
    
fnames = [f'cat.{i}.jpg' for i in range(1000, 1500)]
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(validation_cats_dir, fname)
    shutil.copyfile(src, dst)
    
fnames = [f'cat.{i}.jpg' for i in range(1500, 2000)]
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(test_cats_dir, fname)
    shutil.copyfile(src, dst)
    
# 复制狗的图片
fnames = [f'dog.{i}.jpg' for i in range(1000)]
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(train_dogs_dir, fname)
    shutil.copyfile(src, dst)
    
fnames = [f'dog.{i}.jpg' for i in range(1000, 1500)]
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(validation_dogs_dir, fname)
    shutil.copyfile(src, dst)
    
fnames = [f'dog.{i}.jpg' for i in range(1500, 2000)]
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(test_dogs_dir, fname)
    shutil.copyfile(src, dst)
    
# 检查
print('total training cat images:', len(os.listdir(train_cats_dir)))
print('total validation cat images:', len(os.listdir(validation_cats_dir)))
print('total test cat images:', len(os.listdir(test_cats_dir)))

print('total training dog images:', len(os.listdir(train_dogs_dir)))
print('total validation dog images:', len(os.listdir(validation_dogs_dir)))
print('total test dog images:', len(os.listdir(test_dogs_dir)))
```

    total training cat images: 1000
    total validation cat images: 500
    total test cat images: 500
    total training dog images: 1000
    total validation dog images: 500
    total test dog images: 500


### 构建网络

在几乎所有的卷积神经网络里，我们都是让特征图的深度逐渐增大，而尺寸逐渐减小。所以这次我们也是这样的。

我们现在的这个问题是个二分类，所以最后一层用一个1单元的 sigmoid 激活的 Dense：


```python
# 将猫狗分类的小型卷积神经网络实例化

from tensorflow.keras import layers
from tensorflow.keras import models

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Flatten())
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))
```

看一下网络的结构：


```python
model.summary()
```

    Model: "sequential_4"
    _________________________________________________________________
    Layer (type)                 Output Shape              Param #   
    =================================================================
    conv2d_16 (Conv2D)           (None, 148, 148, 32)      896       
    _________________________________________________________________
    max_pooling2d_16 (MaxPooling (None, 74, 74, 32)        0         
    _________________________________________________________________
    conv2d_17 (Conv2D)           (None, 72, 72, 64)        18496     
    _________________________________________________________________
    max_pooling2d_17 (MaxPooling (None, 36, 36, 64)        0         
    _________________________________________________________________
    conv2d_18 (Conv2D)           (None, 34, 34, 128)       73856     
    _________________________________________________________________
    max_pooling2d_18 (MaxPooling (None, 17, 17, 128)       0         
    _________________________________________________________________
    conv2d_19 (Conv2D)           (None, 15, 15, 128)       147584    
    _________________________________________________________________
    max_pooling2d_19 (MaxPooling (None, 7, 7, 128)         0         
    _________________________________________________________________
    flatten_4 (Flatten)          (None, 6272)              0         
    _________________________________________________________________
    dense_8 (Dense)              (None, 512)               3211776   
    _________________________________________________________________
    dense_9 (Dense)              (None, 1)                 513       
    =================================================================
    Total params: 3,453,121
    Trainable params: 3,453,121
    Non-trainable params: 0
    _________________________________________________________________


然后就要编译这个网络了，做二分类嘛，所以损失函数用 binary crossentropy（二元交叉熵），优化器还是用 RMSprop (我们之前都是写 `optimizer='rmsprop'`，这次要传点参数，所以用 `optimizers.RMSprop` 实例)：


```python
from tensorflow.keras import optimizers

model.compile(loss='binary_crossentropy',
              optimizer=optimizers.RMSprop(lr=1e-4),
              metrics=['acc'])
```

### 数据预处理

我们要把那些图片搞成浮点数张量才能喂给神经网络。步骤如下：

1. 读取图片文件
2. 把 JPEG 文件内容解码成 RGB 像素网格
3. 转化成浮点数张量
4. 把像素的值从 `[0, 255]` 缩放到 `[0, 1]`

Keras 提供了一些工具可以自动完成这些：


```python
# 使用 ImageDataGenerator 从目录中读取图像

from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(150, 150),
    batch_size=20,
    class_mode='binary')    # 用二分类的标签

validation_generator = test_datagen.flow_from_directory(
    validation_dir,
    target_size=(150, 150),
    batch_size=20,
    class_mode='binary')
```

    Found 2000 images belonging to 2 classes.
    Found 1000 images belonging to 2 classes.


这个搞出来的 train_generator 和 validation_generator 就是 Python 的那种 Generator，惰性计算的那种。这个生成器一次 yield 出来一个 batch，所以把它叫做“batch generator”，迭代出一个来看一下：


```python
for data_batch, labels_batch in train_generator:
    print('data batch shape:', data_batch.shape)
    print('labels batch shape:', labels_batch.shape)
    print('labels_batch:', labels_batch)
    break
```

    data batch shape: (20, 150, 150, 3)
    labels batch shape: (20,)
    labels_batch: [1. 1. 1. 1. 1. 1. 1. 1. 1. 0. 1. 1. 1. 1. 0. 0. 1. 1. 0. 1.]



```python
# 利用 batch 生成器拟合模型
history = model.fit_generator(
    train_generator,
    steps_per_epoch=100,
    epochs=30,
    validation_data=validation_generator,
    validation_steps=50)
```

    Epoch 1/30
    100/100 [==============================] - 97s 967ms/step - loss: 0.6901 - acc: 0.5450 - val_loss: 0.6785 - val_acc: 0.5270
    Epoch 2/30
    100/100 [==============================] - 86s 865ms/step - loss: 0.6661 - acc: 0.5875 - val_loss: 0.6525 - val_acc: 0.6060
    ......
    Epoch 29/30
    100/100 [==============================] - 160s 2s/step - loss: 0.0533 - acc: 0.9860 - val_loss: 0.9298 - val_acc: 0.7310
    Epoch 30/30
    100/100 [==============================] - 162s 2s/step - loss: 0.0460 - acc: 0.9885 - val_loss: 1.0609 - val_acc: 0.7150


这里因为是从 generator 读取 batch 来 fit，所以把我们平时用的 fit 改成了 `fit_generator`。里面传训练数据生成器、一个轮次要从 train_generator 里 yield 出来的次数(steps_per_epoch)、轮次、验证集生成器、一个轮次要从 validation_generator 里 yield 出来的次数(validation_steps)。

```
steps_per_epoch = 训练集数据总数 / 构建generator时指定的batch_size
```

validation_steps 和 steps_per_epoch 类似，只是是对验证集的。

用下面这行代码把训练好的模型保存下来：


```python
# 保存模型
model.save('/Volumes/WD/Files/dataset/dogs-vs-cats/cats_and_dogs_small_1.h5')
```

然后把训练过程画出图来看一下：


```python
# 绘制训练过程中的损失曲线和精度曲线
import matplotlib.pyplot as plt

acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(acc) + 1)

plt.plot(epochs, acc, 'bo-', label='Training acc')
plt.plot(epochs, val_acc, 'sr-', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()

plt.figure()

plt.plot(epochs, loss, 'bo-', label='Training loss')
plt.plot(epochs, val_loss, 'sr-', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()

plt.show()
```


![png](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh85zaz7caj30af07ct8s.jpg)



![png](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh85zd7wcrj30af07cwek.jpg)


不出所料，过拟合了，从差不多第5轮就开始过了。

接下来，我们要用 data augmentation (数据增强) 来降低过拟合。

### 数据增强

data augmentation (数据增强) 是用深度学习处理图像一般都会用到的一个方法。

过拟合是由于训练的数据太少导致的（只要样本足够多，模型就能看遍几乎所以可能，从而几乎不会犯错）。数据增强是一种以现有的样本为基础生成更多的训练数据的一种方法，这个方法利用多种能够生成可信图像的随机变换来增加。

在 Keras 中，我们用 ImageDataGenerator 的时候设几个参数就可以完成数据增强了：


```python
datagen = ImageDataGenerator(
      rotation_range=40,      # 随机旋转图片的范围，0~180
      width_shift_range=0.2,  # 随机水平移动的比例
      height_shift_range=0.2, # 随机竖直移动的比例
      shear_range=0.2,        # 随机错切变换(shearing transformations)的角度
      zoom_range=0.2,         # 随机缩放的范围
      horizontal_flip=True,   # 是否做随机水平反转
      fill_mode='nearest')    # 填充新创建像素的方法
```

找张图片增强了试试：


```python
from tensorflow.keras.preprocessing import image

fnames = [os.path.join(train_cats_dir, fname) for 
          fname in os.listdir(train_cats_dir)]

img_path = fnames[3]
img = image.load_img(img_path, target_size=(150, 150))    # 读取图片

x = image.img_to_array(img)    # shape (150, 150, 3)
x = x.reshape((1,) + x.shape)  # shape (1, 150, 150, 3)

i=0
for batch in datagen.flow(x, batch_size=1):
    plt.figure(i)
    imgplot = plt.imshow(image.array_to_img(batch[0]))
    i += 1
    if i % 4 == 0:
        break

plt.show()
```


![png](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh85zfrydzj307907075h.jpg)



![png](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh85zk2m49j3079070myh.jpg)



![png](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh85zhn5dcj3079070aba.jpg)



![png](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh85zrkbkej30790703zv.jpg)


注意数据增强并没有带来新的信息，只是把原本就有的信息 remix 一下。所以在数据特别少的情况下，光用数据增强不足以消除过拟合，所以我们还需要在 Dense 层之前用上 Dropout。


```python
# 定义一个包含 dropout 的新卷积神经网络

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Flatten())

model.add(layers.Dropout(0.5))    # 👈 新增的 Dropout

model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', 
              optimizer=optimizers.RMSprop(lr=1e-4), 
              metrics=['acc'])
```


```python
# 利用数据增强生成器来训练卷积神经网络

# 数据生成器
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,)

test_datagen = ImageDataGenerator(rescale=1./255)    # 测试集不增强哦

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary')

validation_generator = test_datagen.flow_from_directory(
    validation_dir,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary')

# 训练
history = model.fit_generator(
    train_generator,
    steps_per_epoch=100,
    epochs=100,
    validation_data=validation_generator,
    validation_steps=50)

# 保存模型
model.save('/Volumes/WD/Files/dataset/dogs-vs-cats/cats_and_dogs_small_2.h5')
```

    Found 2000 images belonging to 2 classes.
    Found 1000 images belonging to 2 classes.
    Epoch 1/100
    100/100 [==============================] - 142s 1s/step - loss: 0.6909 - acc: 0.5265 - val_loss: 0.6799 - val_acc: 0.5127
    Epoch 2/100
    100/100 [==============================] - 123s 1s/step - loss: 0.6817 - acc: 0.5474 - val_loss: 0.6561 - val_acc: 0.6320
    ......
    100/100 [==============================] - 131s 1s/step - loss: 0.3225 - acc: 0.8612 - val_loss: 0.4465 - val_acc: 0.7976
    Epoch 99/100
    100/100 [==============================] - 134s 1s/step - loss: 0.3391 - acc: 0.8501 - val_loss: 0.5455 - val_acc: 0.7836
    Epoch 100/100
    100/100 [==============================] - 130s 1s/step - loss: 0.3140 - acc: 0.8624 - val_loss: 0.4295 - val_acc: 0.8274



```python
# 绘制训练过程中的损失曲线和精度曲线
import matplotlib.pyplot as plt

acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(acc) + 1)

plt.plot(epochs, acc, 'bo-', label='Training acc')
plt.plot(epochs, val_acc, 'r-', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()

plt.figure()

plt.plot(epochs, loss, 'bo-', label='Training loss')
plt.plot(epochs, val_loss, 'r-', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()

plt.show()
```


![png](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh85zupxk2j30al07cjro.jpg)



![png](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh85zwpa4hj30al07c0t2.jpg)


👌用了 Data Augmentation 和 Dropout 之后，过拟合就好多了，精度也有所提升。

接下来，我们还会用一些技术来进一步优化模型。

## 使用预训练的卷积神经网络

> 5.3 Using a pretrained convnet

对于小型图像数据集，我们常用的一种高效的方法是利用预训练网络（pretrained network）来构建深度学习模型。预训练网络是之前在大型数据集上训练好的网络（通常是在大型图片分类任务上训练好的）。如果预训练集用的数据足够多，模型足够泛化，那么预训练网络学到的空间层次结构就可以有效地作为通用模型来反应现实的视觉世界，因此就可用于各种不同的计算机视觉问题，哪怕新的问题和原始任务完全扯不上关系。

例如，我们可以用一个在 ImageNet (这个数据集有140万张图像，1000个不同的类别，主要是动物和各种日常用品)完成预训练的网络来处理猫狗分类的问题。我们将使用的是 VGG16 这个架构。

使用预训练网络有两种方法：*特征提取*(feature extraction)和*微调模型*(fine-tuning)。

### 特征提取

特征提取是使用之前的网络学到的表示来从新样本中提取出需要的特征，输入一个新的分类器，从头开始训练。

在前面的卷积神经网络例子中，我们知道，我们用来图片分类的模型可以分成两部分：

- 卷积基（convolutional base）：前面的卷积、池化层；
- 分类器（classifier）：后面的密连接层；

所以对于卷积神经网络，**特征提取**就是取出之前训练好的网络的卷积基，把新的数据输入进去跑，然后拿其输出去训练一个新的分类器：

![保持卷积基不变，改变分类器](https://tva1.sinaimg.cn/large/007S8ZIlgy1ggvimux4ttj314l0u0jv4.jpg)

注意，只复用卷积基，而不复用分类器。卷积基是用来提取特征的，这个可以相同；但由于每个问题的分类不同，理应使用不同的分类器；并且有的问题中特征的位置是有用的，而我们把特征图转到 Dense 层的时候这些位置特征就丢失了，所以并不是所有问题都是用 Dense 去简单的完成分类的，所以不应该无脑套用分类器。

在预训练网络中，能提取的特征表示的通用程度取决于于其深度。越少的层越通用（比如，图片的颜色、边缘、纹理之类的），越多的层就会包含越多的抽象信息（比如，有一个猫的眼睛啊之类的）。所以如果预训练网络处理的原始问题和我们当前要处理的问题差距太大，就只因该使用比较少的前几层，而不要用整个卷积基。

现在，来做实践了，我们要用在 ImageNet 上预训练的 VGG16 模型来处理猫狗分类的问题，我们将保持卷积基不变，改变分类器。

VGG16 模型是 Keras 有内置的，直接用就好了：


```python
from tensorflow.keras.applications import VGG16

conv_base = VGG16(weights='imagenet',        # 指定模型初始化的权重检查点
                  include_top=False,         # 是否包含最后的密集连接层分类器
                  input_shape=(150, 150, 3)) # 输入的形状，不传的话能处理任意形状的输入
```

模型是要从这里下载的：[https://github.com/fchollet/deep-learning-models/releases](https://github.com/fchollet/deep-learning-models/releases)

如果让他自己下比较慢的话，可以考虑手动下载安装。参考 vgg16 的源码: `/usr/local/lib/python3.7/site-packages/keras_applications/vgg16.py`，发现它是调用一个 get_file 来获取模型的：

```python
weights_path = keras_utils.get_file(
    'vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5',
    WEIGHTS_PATH_NO_TOP,
    cache_subdir='models',
    file_hash='6d6bbae143d832006294945121d1f1fc')
```

这里看到他是从一个子目录 `models` 里读取模型的，还有这个 `keras_utils.get_file` 就是 `/usr/local/lib/python3.7/site-packages/tensorflow_core/python/keras/utils/data_utils.py` 第 150 行左右的 get_file 函数，文档注释里写了，东西默认是放到 `~/.keras` 这个目录的。

总之，就是把模型下载下来放到 `~/.keras/models` 里就好了。

还有注意加不加top(最后的分类器)，下载的模型大小差距还是很大的：

![不同配置的VGG16预训练模型的大小](https://tva1.sinaimg.cn/large/007S8ZIlgy1ggw35kvawgj30t407uta8.jpg)

总之，最后完了会得到一个 conv_base 模型，这个模型还是很容易理解的，用到的都是我们之前已经学过的东西：


```python
conv_base.summary()
```

    Model: "vgg16"
    _________________________________________________________________
    Layer (type)                 Output Shape              Param #   
    =================================================================
    input_1 (InputLayer)         [(None, 150, 150, 3)]     0         
    _________________________________________________________________
    block1_conv1 (Conv2D)        (None, 150, 150, 64)      1792      
    _________________________________________________________________
    block1_conv2 (Conv2D)        (None, 150, 150, 64)      36928     
    _________________________________________________________________
    block1_pool (MaxPooling2D)   (None, 75, 75, 64)        0         
    _________________________________________________________________
    block2_conv1 (Conv2D)        (None, 75, 75, 128)       73856     
    _________________________________________________________________
    block2_conv2 (Conv2D)        (None, 75, 75, 128)       147584    
    _________________________________________________________________
    block2_pool (MaxPooling2D)   (None, 37, 37, 128)       0         
    _________________________________________________________________
    block3_conv1 (Conv2D)        (None, 37, 37, 256)       295168    
    _________________________________________________________________
    block3_conv2 (Conv2D)        (None, 37, 37, 256)       590080    
    _________________________________________________________________
    block3_conv3 (Conv2D)        (None, 37, 37, 256)       590080    
    _________________________________________________________________
    block3_pool (MaxPooling2D)   (None, 18, 18, 256)       0         
    _________________________________________________________________
    block4_conv1 (Conv2D)        (None, 18, 18, 512)       1180160   
    _________________________________________________________________
    block4_conv2 (Conv2D)        (None, 18, 18, 512)       2359808   
    _________________________________________________________________
    block4_conv3 (Conv2D)        (None, 18, 18, 512)       2359808   
    _________________________________________________________________
    block4_pool (MaxPooling2D)   (None, 9, 9, 512)         0         
    _________________________________________________________________
    block5_conv1 (Conv2D)        (None, 9, 9, 512)         2359808   
    _________________________________________________________________
    block5_conv2 (Conv2D)        (None, 9, 9, 512)         2359808   
    _________________________________________________________________
    block5_conv3 (Conv2D)        (None, 9, 9, 512)         2359808   
    _________________________________________________________________
    block5_pool (MaxPooling2D)   (None, 4, 4, 512)         0         
    =================================================================
    Total params: 14,714,688
    Trainable params: 14,714,688
    Non-trainable params: 0
    _________________________________________________________________


注意，最前面的输入已经调成了我们希望的`(150, 150, 3)`，最后的输出是`(4, 4, 512)`，在后面我们要连上我们自己的分类器。有两种办法：

1. 在这个卷积基上跑我们现在的数据集，然后把结果放到个 Numpy 数组里面，保存到磁盘，然后以这个数组为输入，扔到个密连接的网络里面去训练。这种办法比较简单，也只需要计算一次消耗最大的卷积基部分。但是，这种办法不能使用数据增强。
2. 拓展 conv_base，往它后面加 Dense 层，然后在输入数据上端到端运行整个网络，这样可以使用数据增强，但计算代价比较大。

首先，我们做第一种。

#### 不数据增强的快速特征提取

重述一般，这种方法保存我们的数据通过 conv_base 后的输出，然后将这些输出作为输入放到一个新模型里。

这里还是用 ImageDataGenerator 把图片、标签提取到 Numpy 数组。然后调用 conv_base 的 predict 方法来用预训练模型提取特征。


```python
# 使用预训练的卷积基提取特征

import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator

base_dir = '/Volumes/WD/Files/dataset/dogs-vs-cats/cats_and_dogs_small'
train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'validation')
test_dir = os.path.join(base_dir, 'test')

datagen = ImageDataGenerator(rescale=1./255)
batch_size = 20

def extract_features(directory, sample_count):
    features = np.zeros(shape=(sample_count, 4, 4, 512))    # 这个要符合之前 conv_base.summary() 最后一层的输出的形状
    labels = np.zeros(shape=(sample_count))
    generator = datagen.flow_from_directory(
        directory,
        target_size=(150, 150),
        batch_size=batch_size,
        class_mode='binary')
    i = 0
    for inputs_batch, labels_batch in generator:    # 一批一批加数据
        features_batch = conv_base.predict(inputs_batch)
        features[i * batch_size : (i + 1) * batch_size] = features_batch
        labels[i * batch_size : (i + 1) * batch_size] = labels_batch
        i += 1
        if i * batch_size >= sample_count:    # generator 会生成无限的数据哦，break 要自己控制
            break
    return features, labels

train_features, train_labels = extract_features(train_dir, 2000)
validation_features, validation_labels = extract_features(validation_dir, 1000)
test_features, test_labels = extract_features(test_dir, 1000)
```

    Found 2000 images belonging to 2 classes.
    Found 1000 images belonging to 2 classes.
    Found 1000 images belonging to 2 classes.


之后我们是要接密连接层的分类器来着，所以这里先把张量压扁了：


```python
train_features = np.reshape(train_features, (2000, 4 * 4 * 512))
validation_features = np.reshape(validation_features, (1000, 4 * 4 * 512))
test_features = np.reshape(test_features, (1000, 4 * 4 * 512))
```

然后就是做密连接的分类器了，还是用 dropout 正则化：


```python
from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras import optimizers

model = models.Sequential()
model.add(layers.Dense(256, activation='relu', input_dim=4 * 4 * 512))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(1, activation='sigmoid'))

model.compile(optimizer=optimizers.RMSprop(lr=2e-5),
              loss='binary_crossentropy',
              metrics=['acc'])

history = model.fit(train_features, train_labels,
                    epochs=30,
                    batch_size=20,
                    validation_data=(validation_features, validation_labels))
```

    Train on 2000 samples, validate on 1000 samples
    Epoch 1/30
    2000/2000 [==============================] - 3s 1ms/sample - loss: 0.5905 - acc: 0.6840 - val_loss: 0.4347 - val_acc: 0.8430
    Epoch 2/30
    2000/2000 [==============================] - 1s 640us/sample - loss: 0.4339 - acc: 0.8060 - val_loss: 0.3566 - val_acc: 0.8620
    ......
    Epoch 29/30
    2000/2000 [==============================] - 1s 686us/sample - loss: 0.0928 - acc: 0.9755 - val_loss: 0.2390 - val_acc: 0.9010
    Epoch 30/30
    2000/2000 [==============================] - 1s 687us/sample - loss: 0.0889 - acc: 0.9715 - val_loss: 0.2401 - val_acc: 0.9010


看结果了：


```python
import matplotlib.pyplot as plt

acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(acc) + 1)

plt.plot(epochs, acc, 'bo-', label='Training acc')
plt.plot(epochs, val_acc, 'rs-', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()

plt.figure()

plt.plot(epochs, loss, 'bo-', label='Training loss')
plt.plot(epochs, val_loss, 'rs-', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()

plt.show()
```


![png](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh861ydynej30al07cwek.jpg)



![png](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh862078xaj30af07cglo.jpg)


可以看到，效果还是很不错的接近 90% 的准确率。但问题也还是有，因为没有数据增强，过拟合还是严重的，基本从一开始就在过拟合了。对这种太小的图片数据集，没有数据增强，一般都是不太行的。

#### 带数据增强的特征提取

第二种办法，拓展 conv_base，往它后面加 Dense 层，然后在输入数据上端到端运行整个网络。

这个办法计算代价非！常！高！，基本只能用 GPU 跑。没 GPU 就被用这个了。

在 Keras 里，我们可以像添加层一样把一个模型添加到 Sequential model 里：


```python
# 在卷积基的基础上添加密集连接分类器

from tensorflow.keras import models
from tensorflow.keras import layers

model = models.Sequential()
model.add(conv_base)
model.add(layers.Flatten())
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))
```

看一下模型的样子：


```python
model.summary()
```

    Model: "sequential_1"
    _________________________________________________________________
    Layer (type)                 Output Shape              Param #   
    =================================================================
    vgg16 (Model)                (None, 4, 4, 512)         14714688  
    _________________________________________________________________
    flatten (Flatten)            (None, 8192)              0         
    _________________________________________________________________
    dense_2 (Dense)              (None, 256)               2097408   
    _________________________________________________________________
    dense_3 (Dense)              (None, 1)                 257       
    =================================================================
    Total params: 16,812,353
    Trainable params: 16,812,353
    Non-trainable params: 0
    _________________________________________________________________


注意，在用这种用预训练模型的方法时，一定要**冻结卷积基**，也就是告诉网络，在训练过程种不要去更新卷积基的参数！这个很重要，不这么做的话预训练好的模型就会被破坏，到头来相当于你是从头训练的，那样就失去用预训练的意义了。


```python
# 冻结卷积基
conv_base.trainable = False
```

这样做之后，训练模型时就只会去不断更新 Dense 层的权重了：


```python
model.summary()
```

    Model: "sequential_1"
    _________________________________________________________________
    Layer (type)                 Output Shape              Param #   
    =================================================================
    vgg16 (Model)                (None, 4, 4, 512)         14714688  
    _________________________________________________________________
    flatten (Flatten)            (None, 8192)              0         
    _________________________________________________________________
    dense_2 (Dense)              (None, 256)               2097408   
    _________________________________________________________________
    dense_3 (Dense)              (None, 1)                 257       
    =================================================================
    Total params: 16,812,353
    Trainable params: 2,097,665
    Non-trainable params: 14,714,688
    _________________________________________________________________


接下来，就可以上数据增强，训练模型了：


```python
# 利用冻结的卷积基端到端地训练模型

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import optimizers

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')

test_datagen = ImageDataGenerator(rescale=1./255)    # 注意 test 不增强

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(150, 150),
    batch_size=20,
    class_mode='binary')

validation_generator = test_datagen.flow_from_directory(
    validation_dir,
    target_size=(150, 150),
    batch_size=20,
    class_mode='binary')

model.compile(loss='binary_crossentropy',
              optimizer=optimizers.RMSprop(lr=2e-5),
              metrics=['acc'])

history = model.fit_generator(
    train_generator,
    steps_per_epoch=100,
    epochs=30,
    validation_data=validation_generator,
    validation_steps=50)
```

P.S. 这个在我的 CPU 上跑，一轮大概要15分钟，30轮，，我放弃了。我用 Kaggle 跑了这个，一轮才30秒😭：

```
Found 2000 images belonging to 2 classes.
Found 1000 images belonging to 2 classes.
Epoch 1/30
100/100 [==============================] - 30s 300ms/step - loss: 0.5984 - acc: 0.6855 - val_loss: 0.4592 - val_acc: 0.8250
Epoch 2/30
100/100 [==============================] - 30s 302ms/step - loss: 0.4854 - acc: 0.7815 - val_loss: 0.3660 - val_acc: 0.8710
......
Epoch 29/30
100/100 [==============================] - 30s 300ms/step - loss: 0.2774 - acc: 0.8825 - val_loss: 0.2402 - val_acc: 0.9040
Epoch 30/30
100/100 [==============================] - 30s 302ms/step - loss: 0.2693 - acc: 0.8900 - val_loss: 0.2401 - val_acc: 0.9070
```

![运行结果图](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh5lk985mvj30m60vqtcp.jpg)

### Fine-tuning 微调模型

（我比较喜欢 Fine-tuning 这个词，“微调”反而没内味儿了。）

Fine-tuning 是补充特征提取，进一步优化模型的。Fine-tuning 做的是将卷积基顶部(靠后面的)的几层**解冻**，把解冻的几层和新增加的部分(全连接分类器)联合训练。这个方法稍微调整了预训练模型里面那些高级抽象的表示(也就是那些接近顶层的)，使之更适合我们手头的问题。

![Fine-tuning 示意图，微调了 VGG16 的最后一个卷积块](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh5nq823wfj30ik0t0tbf.jpg)

注意，必须先把最后的全连接分类器训练好，才能去 Fine-tune 卷积基顶部的 Conv 块，不然就会把预训练的成果完全破坏调。

所以，Fine-tuning 需要按照以下步骤：

1. 在已经训练好的网络(base network，基网络)上添加我们自己的网络(比如分类器);
2. 冻结基网络;
3. 训练自己添加的那一部分;
4. 解冻基网络的部分层;
5. 联合训练解冻的层和自己的那部分;

前三步都和特征提取做的是一样的，所以我们从第四步开始。首先再看一下我们的 VGG16 卷积基：


```python
conv_base.summary()
```

    Model: "vgg16"
    _________________________________________________________________
    Layer (type)                 Output Shape              Param #   
    =================================================================
    input_1 (InputLayer)         [(None, 150, 150, 3)]     0         
    _________________________________________________________________
    block1_conv1 (Conv2D)        (None, 150, 150, 64)      1792      
    _________________________________________________________________
    block1_conv2 (Conv2D)        (None, 150, 150, 64)      36928     
    _________________________________________________________________
    block1_pool (MaxPooling2D)   (None, 75, 75, 64)        0         
    _________________________________________________________________
    block2_conv1 (Conv2D)        (None, 75, 75, 128)       73856     
    _________________________________________________________________
    block2_conv2 (Conv2D)        (None, 75, 75, 128)       147584    
    _________________________________________________________________
    block2_pool (MaxPooling2D)   (None, 37, 37, 128)       0         
    _________________________________________________________________
    block3_conv1 (Conv2D)        (None, 37, 37, 256)       295168    
    _________________________________________________________________
    block3_conv2 (Conv2D)        (None, 37, 37, 256)       590080    
    _________________________________________________________________
    block3_conv3 (Conv2D)        (None, 37, 37, 256)       590080    
    _________________________________________________________________
    block3_pool (MaxPooling2D)   (None, 18, 18, 256)       0         
    _________________________________________________________________
    block4_conv1 (Conv2D)        (None, 18, 18, 512)       1180160   
    _________________________________________________________________
    block4_conv2 (Conv2D)        (None, 18, 18, 512)       2359808   
    _________________________________________________________________
    block4_conv3 (Conv2D)        (None, 18, 18, 512)       2359808   
    _________________________________________________________________
    block4_pool (MaxPooling2D)   (None, 9, 9, 512)         0         
    _________________________________________________________________
    block5_conv1 (Conv2D)        (None, 9, 9, 512)         2359808   
    _________________________________________________________________
    block5_conv2 (Conv2D)        (None, 9, 9, 512)         2359808   
    _________________________________________________________________
    block5_conv3 (Conv2D)        (None, 9, 9, 512)         2359808   
    _________________________________________________________________
    block5_pool (MaxPooling2D)   (None, 4, 4, 512)         0         
    =================================================================
    Total params: 14,714,688
    Trainable params: 0
    Non-trainable params: 14,714,688
    _________________________________________________________________


我们将解冻 block5_conv1, block5_conv2 和 block5_conv3 来完成 Fine-turning：


```python
# 冻结直到某一层的所有层

conv_base.trainable = True

set_trainable = False
for layer in conv_base.layers:
    if layer.name == 'block5_conv1':
        set_trainable = True
    if set_trainable:
        layer.trainable = True
    else:
        layer.trainable = False
        
# 微调模型

model.compile(loss='binary_crossentropy',
              optimizer=optimizers.RMSprop(lr=1e-5),    # 这里用的学习率(lr)很小，是希望让微调的三层表示变化范围不要太大
              metrics=['acc'])

history = model.fit_generator(
    train_generator,
    steps_per_epoch=100,
    epochs=100,
    validation_data=validation_generator,
    validation_steps=50)
```

这个也是在 Kaggle 跑的：

![在 Kaggle 训练的最后几轮输出](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh6fkf1r4hj31jw0gaq87.jpg)

![训练历史图线](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh6flamoy7j30o60wkdl5.jpg)

我不知道为什么我做出来的和书上差距很大，我反复看了好过错都没发现有什么问题，即使我用作者给的 Notebook 来跑也是😂，不知道哪里出问题了。不管了？就这样吧。

最后，来看看在测试集上的结果：

```python
test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=(150, 150),
        batch_size=20,
        class_mode='binary')
test_loss, test_acc = model.evaluate_generator(test_generator, steps=50)
print('test acc:', test_acc)
```

书上的结果准确率有 97% 了，，我，我的还不到 95%，害。

## 卷积神经网络的可视化

> 5.4 Visualizing what convnets learn

我们常说深度学习是黑箱，我们很难从其学习的过程中提取出 human-readable 的表示。但是，做计算机视觉的卷积神经网络不是这样，卷积神经网络是能可视化的，我们看得懂的，因为卷积神经网络本来就是提取“视觉概念的表示”的嘛。

现在已经有很多种不同的方法可以从不同角度把卷积神经网络可视化，并合理解释其意义。下面介绍其中几种。

### 可视化中间激活

**可视化中间激活**（Visualizing intermediate activations），也就是可视化卷积神经网络的中间输出。这个可视化可以帮助我们理解一系列连续得多卷积层是如何变换处理输入数据的、以及每个过滤器的基本意义。

这个其实就是把卷积/池化层输出的 feature maps 显示出来看看（层的输出也可以叫做 activation，激活）。具体的做法就是把输出的各个 channel 都做成二维的图像显示出来看。

我们用一个之前生成的模型来作为例子：


```python
from tensorflow.keras.models import load_model

model = load_model('/Volumes/WD/Files/dataset/dogs-vs-cats/cats_and_dogs_small_2.h5')
model.summary()
```

    Model: "sequential_5"
    _________________________________________________________________
    Layer (type)                 Output Shape              Param #   
    =================================================================
    conv2d_20 (Conv2D)           (None, 148, 148, 32)      896       
    _________________________________________________________________
    max_pooling2d_20 (MaxPooling (None, 74, 74, 32)        0         
    _________________________________________________________________
    conv2d_21 (Conv2D)           (None, 72, 72, 64)        18496     
    _________________________________________________________________
    max_pooling2d_21 (MaxPooling (None, 36, 36, 64)        0         
    _________________________________________________________________
    conv2d_22 (Conv2D)           (None, 34, 34, 128)       73856     
    _________________________________________________________________
    max_pooling2d_22 (MaxPooling (None, 17, 17, 128)       0         
    _________________________________________________________________
    conv2d_23 (Conv2D)           (None, 15, 15, 128)       147584    
    _________________________________________________________________
    max_pooling2d_23 (MaxPooling (None, 7, 7, 128)         0         
    _________________________________________________________________
    flatten_5 (Flatten)          (None, 6272)              0         
    _________________________________________________________________
    dropout (Dropout)            (None, 6272)              0         
    _________________________________________________________________
    dense_10 (Dense)             (None, 512)               3211776   
    _________________________________________________________________
    dense_11 (Dense)             (None, 1)                 513       
    =================================================================
    Total params: 3,453,121
    Trainable params: 3,453,121
    Non-trainable params: 0
    _________________________________________________________________


然后我们找一张训练的时候网络没见过的图片：


```python
img_path = '/Volumes/WD/Files/dataset/dogs-vs-cats/cats_and_dogs_small/test/cats/cat.1750.jpg'

from tensorflow.keras.preprocessing import image    # 把图片搞成 4D 张量
import numpy as np

img = image.load_img(img_path, target_size=(150, 150))
img_tensor = image.img_to_array(img)
img_tensor = np.expand_dims(img_tensor, axis=0)
img_tensor /= 255.

print(img_tensor.shape)
```

    (1, 150, 150, 3)


显示图片：


```python
import matplotlib.pyplot as plt

plt.imshow(img_tensor[0])
plt.show()
```


![png](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh8669nh8uj3079070js1.jpg)


要提取特征图，就要用一个输入张量和一个输出张量列表来实例化一个模型：


```python
from tensorflow.keras import models

layer_outputs = [layer.output for layer in model.layers[:8]]    # 提取前 8 层的输出
activation_model = models.Model(inputs=model.input, outputs=layer_outputs)
```

当输入一张图像时，这个模型就会返回原始模型前 8 层的激活值。我们之前的模型都是给一个输入，返一个输出的，但其实一个模型是可以给任意个输入，返任意个输出的。

接下来在把刚才找的图片输入进去：


```python
activations = activation_model.predict(img_tensor)
# 返回 8 个 Numpy 数组组成的列表，每层一个，里面放着激活
```


```python
first_layer_activation = activations[0]
print(first_layer_activation.shape)
```

    (1, 148, 148, 32)


这东西有 32 个 channel，我们随便打一个出来看看：


```python
# 将第 4 个 channel 可视化

import matplotlib.pyplot as plt
plt.matshow(first_layer_activation[0, :, :, 4], cmap='viridis')
```




    <matplotlib.image.AxesImage at 0x13f7b3d10>




![png](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh8676bpw7j307f076wex.jpg)


这个每个 channel 是干嘛的基本是随机的，我这个就和书上不一样。

下面，来绘制整个网络中完整的、所有激活的可视化。我们将 8 个 feature maps，每个其中的所有 channels 画出来了，排到一张大图上：


```python
# 将每个中间激活的所有通道可视化

layer_names = []
for layer in model.layers[:8]:
    layer_names.append(layer.name)
    
images_per_row = 16

for layer_name, layer_activation in zip(layer_names, activations):
    # 对于每个 layer_activation，其形状为 (1, size, size, n_features)
    n_features = layer_activation.shape[-1]    # 特征图里特征(channel)的个数
    
    size = layer_activation.shape[1]    # 图的大小
    
    n_cols = n_features // images_per_row
    display_grid = np.zeros((size * n_cols, images_per_row * size))    # 分格
    
    for col in range(n_cols):
        for row in range(images_per_row):
            channel_image = layer_activation[0, :, :, col * images_per_row + row]
            
            # 把图片搞好看一点
            channel_image -= channel_image.mean()
            channel_image /= channel_image.std()
            channel_image *= 64
            channel_image += 128
            channel_image = np.clip(channel_image, 0, 255).astype('uint8')
            display_grid[col * size : (col + 1) * size,
                         row * size : (row + 1) * size] = channel_image

    scale = 1. / size
    plt.figure(figsize=(scale * display_grid.shape[1], 
                        scale * display_grid.shape[0]))

    plt.title(layer_name)
    plt.grid(False)
    plt.imshow(display_grid, aspect='auto', cmap='viridis')

```

    /usr/local/lib/python3.7/site-packages/ipykernel_launcher.py:24: RuntimeWarning: invalid value encountered in true_divide



![png](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh866jmct8j30q004c40i.jpg)



![png](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh8674iooxj30q004cdhw.jpg)



![png](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh866chv4nj30q007cdjl.jpg)



![png](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh866c10xej30q007cgpf.jpg)



![png](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh866ewppaj30q00dejxf.jpg)



![png](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh8666s9lfj30q00den33.jpg)



![png](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh866djarhj30q00dejul.jpg)



![png](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh866go1kzj30pu0dewhm.jpg)


可以看到，特征越来越抽象。同时，黑的也越来越多（稀疏度越来越大），那些都是输入图像中找不到这些过滤器所编码的模式，所以就空白了。

这里表现出来一个重要普遍特征：随着层数的加深，层所提取的特征变得越来越抽象。更高的层激活包含关于特定输入的信息越来越少，而关于目标的信息越来越多。

与人类和动物感知世界的方式类似：人类观察一个场景几秒钟后，可以记住其中有哪些抽象物体(比如自行车、树)，但记不住这些物体的具体外观。你的大脑会自动将视觉输入完全抽象化，即将其转换为更高层次的视觉概念，同时过滤掉不相关的视觉细节。

深度神经网络利用信息蒸馏管道 (information distillation pipeline)，将输入原始数据(本例中是 RGB 图像)，反复进行变换，将无关信息过滤掉(比如图像的具体外观)，并放大和细化有用的信息(比如图像的类别)，最终完成对信息的利用（比如判断出图片是猫还是狗）。


### 可视化卷积神经网络的过滤器

**可视化卷积神经网络的过滤器**（Visualizing convnets filters），帮助理解各个过滤器善于接受什么样的视觉模式(pattern，我觉得“模式”这个词并不能很好的诠释 pattern 的意思)或概念。

要观察卷积神经网络学到的过滤器，我们可以显示每个过滤器所响应的视觉模式。这个可以在输入空间上用 gradient ascent（梯度上升）来实现：

为了从空白输入图像开始，让某个过滤器的响应最大化，可以将梯度下降应用于卷积神经网络输入图像的值。得到的输入图像即为对过滤器具有最大响应的图像。

这个做起来很简单，构建一个损失函数，其目的是让某个卷积层的某个过滤器的值最大化。然后，使用随机梯度下降来调节输入图像的值，使之激活值最大化。

例如，在 ImageNet 上预训练的 VGG16 网络的 block3_conv1 层第 0 个过滤器激活的损失就是：


```python
from tensorflow.keras.applications import VGG16
from tensorflow.keras import backend as K

model = VGG16(weights='imagenet', include_top=False)

layer_name = 'block3_conv1'
filter_index = 0

layer_output = model.get_layer(layer_name).output
loss = K.mean(layer_output[:, :, :, filter_index])

print(loss)
```

    Tensor("Mean_11:0", shape=(), dtype=float32)


要做梯度下降嘛，所以要得到 loss 相对于模型输入的梯度。用 Keras 的 backend 的 gradients 函数来完成这个：


```python
import tensorflow as tf
tf.compat.v1.disable_eager_execution()  # See https://github.com/tensorflow/tensorflow/issues/33135

grads = K.gradients(loss, model.input)[0]
# 这东西返回的是一个装着一系列张量的 list，在此处，list 长度为1，所以取 [0] 就是一个张量
print(grads)
```

    Tensor("gradients_1/block1_conv1_4/Conv2D_grad/Conv2DBackpropInput:0", shape=(None, None, None, 3), dtype=float32)


这里可以用一个小技巧来让梯度下降过程平顺地进行：将梯度张量除以其 L2 范数(张量的平方的平均值的平方根)来标准化。这种操作可以使输入图像更新地大小始终保持在同一个范围里：


```python
grads /= (K.sqrt(K.mean(K.square(grads))) + 1e-5)    # + 1e-5 防止除以0
print(grads)
```

    Tensor("truediv_1:0", shape=(None, None, None, 3), dtype=float32)


现在需要接近的问题是，给定输入图像，计算出 loss 和 grads 的值。这个可以用 iterate 函来做：它将一个 Numpy 张量转换为两个 Numpy 张量组成的列表，这两个张量分别是损失值和梯度值：


```python
iterate = K.function([model.input], [loss, grads])

import numpy as np
loss_value, grads_value = iterate([np.zeros((1, 150, 150, 3))])
print(loss_value, grads_value)
```

    0.0 [[[[0. 0. 0.]
       [0. 0. 0.]
       [0. 0. 0.]
       ...
       ...
       [0. 0. 0.]
       [0. 0. 0.]
       [0. 0. 0.]]]]


然后，就来写梯度下降了：


```python
# 通过随机梯度下降让损失最大化

input_img_data = np.random.random((1, 150, 150, 3)) * 20 + 128.   # 随便一个有燥点的灰度图

plt.imshow(input_img_data[0, :, :, :] / 225.)
plt.figure()

step = 1.    # 梯度更新的步长
for i in range(40):
    loss_value, grads_value = iterate([input_img_data])
    input_img_data += grads_value * step    # 沿着让损失最大化的方向调节输入图像
    
plt.imshow(input_img_data[0, :, :, :] / 225.)
plt.show()
```

    Clipping input data to the valid range for imshow with RGB data ([0..1] for floats or [0..255] for integers).



![png](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh8673z1cwj30790700sy.jpg)



![png](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh86752ufkj307907074x.jpg)

Emmm，刚才这个画图是我随便写的啦，所以爆了个 Warning，为了正规地画出图来,下面好好处理一下：

```python
# 将张量转换为有效图像的 utility 函数

def deprocess_image(x):
    # 标准化，均值为 0， 标准差为 0.1
    x -= x.mean()
    x /= (x.std() + 1e-5)
    x *= 0.1
    
    # 裁剪到 [0, 1]
    x += 0.5
    x = np.clip(x, 0, 1)
    
    # 将 x 转换为 RGB 数组
    x *= 255
    x = np.clip(x, 0, 255).astype('uint8')
    return x

```

把上面那些东西全部拼起来就可以得到完整的生成过滤器可视化的函数了：


```python
# 生成过滤器可视化的函数

import tensorflow as tf
tf.compat.v1.disable_eager_execution()  # See https://github.com/tensorflow/tensorflow/issues/33135

def generate_pattern(layer_name, filter_index, size=150):
    # 构建一个损失函数，将 layer_name 层第 filter_index 个过滤器的激活最大化
    layer_output = model.get_layer(layer_name).output
    loss = K.mean(layer_output[:, :, :, filter_index])
    
    # 计算损失相对于输入图像的梯度，并将梯度标准化
    grads = K.gradients(loss, model.input)[0]
    grads /= (K.sqrt(K.mean(K.square(grads))) + 1e-5)
    
    # 返回给定输入图像的损失和梯度
    iterate = K.function([model.input], [loss, grads])
    
    # 从带有噪声的灰度图开始，梯度上升 40 次
    input_img_data = np.random.random((1, size, size, 3)) * 20 + 128.
    step = 1.
    for i in range(40):
        loss_value, grads_value = iterate([input_img_data])
        input_img_data += grads_value * step
    
    # 输出结果
    img = input_img_data[0]
    return deprocess_image(img)
```

然后就可以用了，还是那刚才那个例子是一下|：


```python
plt.imshow(generate_pattern('block3_conv1', 1))
```




    <matplotlib.image.AxesImage at 0x167d78950>




![png](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh866foirwj3079070t9a.jpg)


这个图就是 block3_conv1 层第 0 个过滤器的响应了。这种 pattern 叫做 polka-dot（波尔卡点图案）。

接下来我们把每一层的每个过滤器都可视化。为了快一点，我们只可视化每个卷积块的第一层的前64个过滤器（防止也没什么意义，就是看看，随便搞几个就行了）：


```python
# 生成一层中所有过滤器响应模式组成的网格
def generate_patterns_in_layer(layer_name, size=64, margin=5):
    results = np.zeros((8 * size + 7 * margin, 8 * size + 7 * margin, 3), dtype=np.int)
    for i in range(8):
        for j in range(8):
            filter_img = generate_pattern(layer_name, i + (j * 8), size=size)
            
            horizontal_start = i * size + i * margin
            horizontal_end = horizontal_start + size
            
            vertical_start = j * size + j * margin
            vertical_end = vertical_start + size
            
            results[horizontal_start: horizontal_end,
                    vertical_start: vertical_end, :] = filter_img
            
    return results


layer_names = ['block1_conv1', 'block2_conv1', 'block3_conv1', 'block4_conv1']
for layer in layer_names:
    img = generate_patterns_in_layer(layer)
    plt.figure(figsize=(20, 20))
    plt.title(layer)
    plt.imshow(img)
```


![png](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh86676843j30q00den33.jpg)



![png](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh8668h3n8j30u00u44d3.jpg)



![png](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh866aay9sj30u00u4du6.jpg)



![png](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh866b9rihj30u00u4nbg.jpg)


这些图里就表现了卷积神经网络的层如何观察图片中的信息的：卷积神经网络中每一层都学习一组过滤器，然后输入会被表示成过滤器的组合，这个其实类似于傅里叶变换的过程。随着层数的加深，卷积神经网络中的过滤器变得越来越复杂，越来越精细，所以就可以提取、“理解”根据抽象的信息了。

### 可视化图像中类激活的热力图

**可视化图像中类激活的热力图**（Visualizing heatmaps of class activation in an image），用来了解网络是靠哪部分图像来识别一个类的，也有助于知道物体在图片的哪个位置。

用来对输入图像生成类激活的热力图的一种技术叫 CAM (class activation map 类激活图)可视化。类激活热力图对任意输入的图像的每个位置进行计算，表示出每个位置对该类别的重要程度。比如我们的猫狗分类网络里，对一个猫的图片生成类激活热力图，可以得到这个图片的各个不同的部位有多像猫（对模型认为这是猫的图片起了过大的作用）。

具体来说，我们用 [Grad-CAM](https://arxiv.org/abs/ 1610.02391.) 这个方法：给定一张输入图像，对于一个卷积层的输出特征图，用类别相对于通道的梯度对这个特征图中的每个通道进行加权。说人话就是用「每个通道对分类的重要程度」对「输入图像对不同通道的激活的强弱程度」的空间图进行加权，从而得到「输入图像对类别的激活强度」的空间图。（emmm，这种超长的句子看原文比较好😭：Intuitively, one way to understand this trick is that you’re weighting a spatial map of “how intensely the input image activates different channels” by “how important each channel is with regard to the class,” resulting in a spatial map of “how intensely the input image activates the class.”）

我们在 VGG16 模型来演示这个方法：


```python
# 加载带有预训练权重的 VGG16 网络

from tensorflow.keras.applications.vgg16 import VGG16

model = VGG16(weights='imagenet')    # 注意这个是带有分类器的，比较大，下载稍慢（有500+MB）
```



```python
model.summary()
```

    Model: "vgg16"
    _________________________________________________________________
    Layer (type)                 Output Shape              Param #   
    =================================================================
    input_1 (InputLayer)         [(None, 224, 224, 3)]     0         
    _________________________________________________________________
    block1_conv1 (Conv2D)        (None, 224, 224, 64)      1792      
    _________________________________________________________________
    block1_conv2 (Conv2D)        (None, 224, 224, 64)      36928     
    _________________________________________________________________
    block1_pool (MaxPooling2D)   (None, 112, 112, 64)      0         
    _________________________________________________________________
    block2_conv1 (Conv2D)        (None, 112, 112, 128)     73856     
    _________________________________________________________________
    block2_conv2 (Conv2D)        (None, 112, 112, 128)     147584    
    _________________________________________________________________
    block2_pool (MaxPooling2D)   (None, 56, 56, 128)       0         
    _________________________________________________________________
    block3_conv1 (Conv2D)        (None, 56, 56, 256)       295168    
    _________________________________________________________________
    block3_conv2 (Conv2D)        (None, 56, 56, 256)       590080    
    _________________________________________________________________
    block3_conv3 (Conv2D)        (None, 56, 56, 256)       590080    
    _________________________________________________________________
    block3_pool (MaxPooling2D)   (None, 28, 28, 256)       0         
    _________________________________________________________________
    block4_conv1 (Conv2D)        (None, 28, 28, 512)       1180160   
    _________________________________________________________________
    block4_conv2 (Conv2D)        (None, 28, 28, 512)       2359808   
    _________________________________________________________________
    block4_conv3 (Conv2D)        (None, 28, 28, 512)       2359808   
    _________________________________________________________________
    block4_pool (MaxPooling2D)   (None, 14, 14, 512)       0         
    _________________________________________________________________
    block5_conv1 (Conv2D)        (None, 14, 14, 512)       2359808   
    _________________________________________________________________
    block5_conv2 (Conv2D)        (None, 14, 14, 512)       2359808   
    _________________________________________________________________
    block5_conv3 (Conv2D)        (None, 14, 14, 512)       2359808   
    _________________________________________________________________
    block5_pool (MaxPooling2D)   (None, 7, 7, 512)         0         
    _________________________________________________________________
    flatten (Flatten)            (None, 25088)             0         
    _________________________________________________________________
    fc1 (Dense)                  (None, 4096)              102764544 
    _________________________________________________________________
    fc2 (Dense)                  (None, 4096)              16781312  
    _________________________________________________________________
    predictions (Dense)          (None, 1000)              4097000   
    =================================================================
    Total params: 138,357,544
    Trainable params: 138,357,544
    Non-trainable params: 0
    _________________________________________________________________


然后我们照一张用来测试的图片：

![creative_commons_elephant](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh83vzik31j30oz0goq7t.jpg)

这是两只亚洲象🐘哦，把这个图片处理成 VGG16 模型需要的样子：

```python
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions
import numpy as np

img_path = './creative_commons_elephant.jpg'
img = image.load_img(img_path, target_size=(224, 224))

img = image.load_img(img_path, target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)
```

预测一下图片里的是啥：


```python
preds = model.predict(x)
print('Predicted:', decode_predictions(preds, top=3)[0])
```

    Predicted: [('n02504458', 'African_elephant', 0.909421), ('n01871265', 'tusker', 0.086182885), ('n02504013', 'Indian_elephant', 0.0043545826)]


有 90% 的把握是亚洲象，不错。接下来就要用 Grad-CAM 算法来显示图像中哪些部分最像非洲象了。


```python
from tensorflow.keras import backend as K

import tensorflow as tf
tf.compat.v1.disable_eager_execution()  # See https://github.com/tensorflow/tensorflow/issues/33135

african_elephant_output = model.output[:, 386]    # 这个是输出向量中代表“非洲象”的元素

last_conv_layer = model.get_layer('block5_conv3')   # VGG16 最后一个卷积层的输出特征图

grads = K.gradients(african_elephant_output, last_conv_layer.output)[0]

pooled_grads = K.mean(grads, axis=(0, 1, 2))    # 特定特征图通道的梯度平均大小，形状为 (512,) 

iterate = K.function([model.input], [pooled_grads, last_conv_layer.output[0]])

pooled_grads_value, conv_layer_output_value = iterate([x])    # 对刚才的测试🐘图片计算出梯度和特征图

for i in range(512):
    # 将特征图数组的每个 channel 乘以「这个 channel 对‘大象’类别的重要程度」
    conv_layer_output_value[:, :, i] *= pooled_grads_value[i]
    
heatmap = np.mean(conv_layer_output_value, axis=-1)  # 处理后的特征图的逐通道平均值即为类激活的热力图
```

把它画出来看看：


```python
import matplotlib.pyplot as plt

heatmap = np.maximum(heatmap, 0)
heatmap /= np.max(heatmap)
plt.matshow(heatmap)
```




    <matplotlib.image.AxesImage at 0x13d935210>




![png](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh8669908hj3078076mx8.jpg)


emmmm，看不懂啊，所以，我们用 OpenCV 把这个叠加到原图上去看：


```python
import cv2

img = cv2.imread(img_path)    # 加载原图
heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))    # 调整热力图大小，符合原图
heatmap = np.uint8(255 * heatmap)    # 转换为 RGB 格式
heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
superimposed_img = heatmap * 0.4 + img    # 叠加
cv2.imwrite('./elephant_cam.jpg', superimposed_img)    # 保存
```




    True



得到的图像如下：

![叠加到原图的热力图](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh84yvepspj30oz0go7a9.jpg)

可以看出，VGG16 网络其实只识别了那只小的象，注意，小象头部的激活强度很大，这可能就是网络找到的非洲象的独特之处。

