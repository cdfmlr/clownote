---
categories:
- Machine Learning
- Deep Learning with Python
date: 2020-08-24 21:16:34
tag:
- Machine Learning
- Deep Learning
title: Python深度学习之GAN
---

# Deep Learning with Python

这篇文章是我学习《Deep Learning with Python》(第二版，François Chollet 著) 时写的系列笔记之一。文章的内容是从  Jupyter notebooks 转成 Markdown 的，你可以去 [GitHub](https://github.com/cdfmlr/Deep-Learning-with-Python-Notebooks) 或 [Gitee](https://gitee.com/cdfmlr/Deep-Learning-with-Python-Notebooks) 找到原始的 `.ipynb` 笔记本。

你可以去[这个网站在线阅读这本书的正版原文](https://livebook.manning.com/book/deep-learning-with-python)(英文)。这本书的作者也给出了配套的 [Jupyter notebooks](https://github.com/fchollet/deep-learning-with-python-notebooks)。

本文为 **第8章  生成式深度学习** (Chapter 8. *Generative deep learning*) 的笔记之一。

[TOC]


## 8.5 Introduction to generative adversarial networks

> 生成式对抗网络简介

GAN，中文是~~淦~~，错了，生成式对抗网络(Generative Adversarial Network)。和 VAE 一样，是用来学习图像的潜在空间的。这东西可以使生成图像与真实图像“在统计上”别无二致，说人话就是，生成的图像相当逼真。但与 VAE 不同，GAN 的潜在空间无法保证具有有意义的结构，并且是不连续的。

GAN 由两部分组成：

- 生成器网络(generator network)：输入一个随机向量(潜在空间中的一个随机点)，并将其解码为图像。
- 判别器网络(discriminator network)：输入一张图像(真实的或生成器画的)，预测该图像是真实的还是由生成器网络创建的。（判别器网络也叫「对手」，adversary）

训练 GAN 的目的是使「生成器网络」能够欺骗「判别器网络」。

直观理解 GAN 是一个很励志的故事：就是说有两个人，一个伪造者，一个鉴定师。伪造者仿造大师的画，然后把自己的仿制品混在真迹里交给鉴定师鉴定，鉴定师评估每一幅画的真伪，一样看穿了哪些是伪造的。好心的鉴定师反馈了伪造者，告诉他真迹有哪些特征。伪造者根据鉴定师的意见，一步步提升自己的仿造能力。两人不厌其烦地重复这个过程，伪造者变得越来越擅长复制大师的画，鉴定师也越来越擅长找出假画。到最后，伪造者造出了一批鉴定师也无可挑剔的“仿制正品”。

![生成器将随机潜在向量转换成图像，判别器试图分辨真实图像与生成图像。生成器的训练是为了欺骗判别器](https://tva1.sinaimg.cn/large/007S8ZIlgy1ghva0rve82j31ec0tcthm.jpg)

GAN 的训练方式很特殊，它的优化最小值是不固定的。我们通常的「梯度下降」是沿着静态的损失地形滚下山，但 GAN 训练时每下山一步都会对整个地形造成改变。它是一个动态系统，其最优化过程是两股力量之间的平衡。所以，GAN 很难训练。想要让 GAN 正常运行，需要进行大量的模型构建、超参数调节工作。

### 深度卷积生成式对抗网络

我们来尝试用 Keras 实现最最最简单的 GAN。具体来说，我们会做一个**深度卷积生成式对抗网络**（deep convolutional GAN，DCGAN），这种东西的生成器和判别器都是深度卷积神经网络。

我们将用 CIFAR10 数据集中“frog”类别的图像训练 DCGAN。这个数据集包含 50000 张 32×32 的 RGB 图像，这些图像属于 10 个类别(每个类别 5000 张图像)。

#### 实现流程

1. `generator` 网络将形状为 `(latent_dim,)` 的向量映射到形状为 `(32, 32, 3)` 的图像。
2. `discriminator` 网络将形状为 `(32, 32, 3)` 的图像映射到一个二进制得分(a binary score)，用于评估图像为真的概率。
3. `gan` 网络将 `generator` 和 `discriminator` 连接在一起: `gan(x) = discriminator(generator(x))`。这个网络是将潜在向量映射到判别器的评估结果。
4. 使用带有 `"real"` 或 `"fake"` 标签的真假图像样本来训练判别器，用常规训练普通的图像分类模型的方法。
5. 为了训练生成器，使用 `gan` 模型的损失相对于生成器权重的梯度。在每一步都要向「让判别器更有可能将生成器解码的图像划分为“真”」移动生成器的权重，即训练生成器来欺骗判别器。

#### 实用技巧

训练和调节 GAN 的过程非常困难。所以我们需要记住一些前人总结出的实用技巧。这些技巧一般很有用，但并不能适用于所有情况。这些东西都没有理论依据，都是玄学，所以不解释直接写结论：

- 使用 tanh 作为生成器最后一层的激活，而不用 sigmoid。
- 使用正态分布(高斯分布)对潜在空间中的点进行采样，而不用均匀分布。
- 随机性能够提高稳健性。GAN 训练时可能以各种方式“卡住”(达到错误的动态平衡)，在训练过程中引入随机性有助于防止出现这种情况，引入随机性的方式有两种：
    1. 在判别器中使用 dropout;
    2. 向判别器的标签添加随机噪声;
- 稀疏的梯度会妨碍 GAN 的训练。「最大池化运算」和 「ReLU 激活」可能导致梯度稀疏，所以推荐：
    1. 使用「步进卷积」代替「最大池化」来进行下采样;
    2. 使用 LeakyReLU 层来代替 ReLU 激活;
- 在生成的图像中，常会见到棋盘状伪影，这是由于生成器中像素空间覆盖不均匀。解决这个问题的办法是：每当在生成器和判别器中都使用步进 Conv2DTranpose 或 Conv2D 时，内核大小要能够被步幅整除。



由于步幅大小和内核大小不匹配而导致的棋盘状伪影示例图:

![由于步幅大小和内核大小不匹配而导致的棋盘状伪影](https://tva1.sinaimg.cn/large/007S8ZIlgy1ghvayd7ipwj31560ggazl.jpg)

#### 生成器的实现

开始构建年轻人的第一个 GAN 了！！

首先开发 generator 模型：将来自潜在空间的向量转换为一张候选图像。

为了避免训练时“卡住”，在判别器和生成器中都使用 dropout。


```python
# GAN 生成器网络

from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

height = 32
width = 32
channels = 3

latent_dim = 32

generator_input = keras.Input(shape=(latent_dim,))

# 将输入转换为大小为 16×16 的 128 个通道的特征图
x = layers.Dense(128 * 16 * 16)(generator_input)
x = layers.LeakyReLU()(x)
x = layers.Reshape((16, 16, 128))(x)

x = layers.Conv2D(256, 5, padding='same')(x)
x = layers.LeakyReLU()(x)

# 上采样为 32×32
x = layers.Conv2DTranspose(256, 4, strides=2, padding='same')(x)
x = layers.LeakyReLU()(x)

x = layers.Conv2D(256, 5, padding='same')(x)
x = layers.LeakyReLU()(x)
x = layers.Conv2D(256, 5, padding='same')(x)
x = layers.LeakyReLU()(x)

# 生成大小为 32×32 的特征图(CIFAR10 图像的形状)
x = layers.Conv2D(channels, 7, activation='tanh', padding='same')(x)

generator = keras.models.Model(generator_input, x)
generator.summary()
```

    Model: "functional_1"
    _________________________________________________________________
    Layer (type)                 Output Shape              Param #   
    =================================================================
    input_1 (InputLayer)         [(None, 32)]              0         
    _________________________________________________________________
    dense (Dense)                (None, 32768)             1081344   
    _________________________________________________________________
    leaky_re_lu (LeakyReLU)      (None, 32768)             0         
    _________________________________________________________________
    reshape (Reshape)            (None, 16, 16, 128)       0         
    _________________________________________________________________
    conv2d (Conv2D)              (None, 16, 16, 256)       819456    
    _________________________________________________________________
    leaky_re_lu_1 (LeakyReLU)    (None, 16, 16, 256)       0         
    _________________________________________________________________
    conv2d_transpose (Conv2DTran (None, 32, 32, 256)       1048832   
    _________________________________________________________________
    leaky_re_lu_2 (LeakyReLU)    (None, 32, 32, 256)       0         
    _________________________________________________________________
    conv2d_1 (Conv2D)            (None, 32, 32, 256)       1638656   
    _________________________________________________________________
    leaky_re_lu_3 (LeakyReLU)    (None, 32, 32, 256)       0         
    _________________________________________________________________
    conv2d_2 (Conv2D)            (None, 32, 32, 256)       1638656   
    _________________________________________________________________
    leaky_re_lu_4 (LeakyReLU)    (None, 32, 32, 256)       0         
    _________________________________________________________________
    conv2d_3 (Conv2D)            (None, 32, 32, 3)         37635     
    =================================================================
    Total params: 6,264,579
    Trainable params: 6,264,579
    Non-trainable params: 0
    _________________________________________________________________


#### 判别器的实现

接下来，开发 discriminator 模型，输入一张图像(真实的或合成的)，将其划分为「真」（来自训练集的真实图像）或「假」（生成器画的图像）。


```python
# GAN 判别器网络

discriminator_input = layers.Input(shape=(height, width, channels))

x = layers.Conv2D(128, 3)(discriminator_input)
x = layers.LeakyReLU()(x)

x = layers.Conv2D(128, 4, strides=2)(x)
x = layers.LeakyReLU()(x)

x = layers.Conv2D(128, 4, strides=2)(x)
x = layers.LeakyReLU()(x)

x = layers.Conv2D(128, 4, strides=2)(x)
x = layers.LeakyReLU()(x)

x = layers.Flatten()(x)
x = layers.Dropout(0.4)(x)

x = layers.Dense(1, activation='sigmoid')(x)

discriminator = keras.models.Model(discriminator_input, x)
discriminator.summary()

discriminator_optimizer = keras.optimizers.RMSprop(
    lr=0.0008,
    clipvalue=1.0,
    decay=1e-8)

discriminator.compile(optimizer=discriminator_optimizer,
                      loss='binary_crossentropy')
```

    Model: "functional_3"
    _________________________________________________________________
    Layer (type)                 Output Shape              Param #   
    =================================================================
    input_2 (InputLayer)         [(None, 32, 32, 3)]       0         
    _________________________________________________________________
    conv2d_4 (Conv2D)            (None, 30, 30, 128)       3584      
    _________________________________________________________________
    leaky_re_lu_5 (LeakyReLU)    (None, 30, 30, 128)       0         
    _________________________________________________________________
    conv2d_5 (Conv2D)            (None, 14, 14, 128)       262272    
    _________________________________________________________________
    leaky_re_lu_6 (LeakyReLU)    (None, 14, 14, 128)       0         
    _________________________________________________________________
    conv2d_6 (Conv2D)            (None, 6, 6, 128)         262272    
    _________________________________________________________________
    leaky_re_lu_7 (LeakyReLU)    (None, 6, 6, 128)         0         
    _________________________________________________________________
    conv2d_7 (Conv2D)            (None, 2, 2, 128)         262272    
    _________________________________________________________________
    leaky_re_lu_8 (LeakyReLU)    (None, 2, 2, 128)         0         
    _________________________________________________________________
    flatten (Flatten)            (None, 512)               0         
    _________________________________________________________________
    dropout (Dropout)            (None, 512)               0         
    _________________________________________________________________
    dense_1 (Dense)              (None, 1)                 513       
    =================================================================
    Total params: 790,913
    Trainable params: 790,913
    Non-trainable params: 0
    _________________________________________________________________


#### 对抗网络

最后，设置 GAN，将生成器和判别器连接在一起，将潜在空间的点转换为一个真或假的分类判断。

这个模型训练时，需要将「判别器」冻结(使之不可被训练)，只让「生成器」向「提高欺骗判别器的能力」的方向移动。

训练 gan 时，我们使用的全部都是“真实图像”的标签，所以如果在训练过程中可以对「判别器」的权重进行更新，训练会使得判别器始终预测“真”。


```python
# 对抗网络

discriminator.trainable = False    # 这个只会作用于 gan

gan_input = keras.Input(shape=(latent_dim,))
gan_output = discriminator(generator(gan_input))
gan = keras.models.Model(gan_input, gan_output)

gan_optimizer = keras.optimizers.RMSprop(
    lr=0.0004,
    clipvalue=1.0,
    decay=1e-8)
gan.compile(optimizer=gan_optimizer,
            loss='binary_crossentropy')
```

#### 训练 DCGAN

训练循环的流程如下:

1. 从潜在空间中抽取随机的点(随机噪声)。
2. 把这个随机噪声给 generator 生成图像。
3. 将生成图像与真实图像混合。
4. 使用这些混合后的图像以及相应的标签(真实图像为“真”，生成图像为“假”)来训练 discriminator。
5. 在潜在空间中随机抽取新的点。
6. 使用这些随机向量以及全部是「真实图像」的标签来训练gan。

具体的代码实现：


```python
# GAN 的训练、

import os
import time
from tensorflow.keras.preprocessing import image

# 导入 CIFAR10 数据
(x_train, y_train), (_, _) = keras.datasets.cifar10.load_data()
# 选出青蛙🐸的图片
x_train = x_train[y_train.flatten() == 6]

x_train = x_train.reshape(
    (x_train.shape[0],) + (height, width, channels)
).astype('float32') / 255.


iterations = 10000
batch_size = 20
save_dir = 'gan_save'

start = 0
for step in range(iterations+1):
    start_time = time.time()
    
    # 随机采样潜在点
    random_latent_vectors = np.random.normal(size=(batch_size, latent_dim))
    
    # 生成图像
    generated_images = generator.predict(random_latent_vectors)
    
    # 选取真实图像
    stop = start + batch_size
    real_images = x_train[start: stop]
    
    # 合并生成、真实图像，给出标签
    combined_images = np.concatenate([generated_images, real_images])
    labels = np.concatenate([np.ones((batch_size, 1)),
                             np.zeros((batch_size, 1))])
    labels += 0.05 * np.random.random(labels.shape)  # 向标签中添加随机噪声
    
    # 训练判别器
    d_loss = discriminator.train_on_batch(combined_images, labels)
    
    # 随机采样潜在点
    random_latent_vectors = np.random.normal(size=(batch_size, latent_dim))
    
    misleading_targets = np.zeros((batch_size, 1))  # 谎称全部都是真实图片
    
    # 通过 gan 模型训练生成器
    a_loss = gan.train_on_batch(random_latent_vectors, misleading_targets)
    
    end_time = time.time()
    
    start += batch_size
    if start > len(x_train) - batch_size:
        start = 0
        
    if step % 50 == 0:
        gan.save_weights('gan.h5')
        
        print(f'step {step}: discriminator loss: {d_loss}, adversarial loss: {a_loss}')
        
        img = image.array_to_img(generated_images[0] * 255., scale=False)
        img.save(os.path.join(save_dir, f'generated_frog_{step}.png'))
        
        img = image.array_to_img(real_images[0] * 255., scale=False)
        img.save(os.path.join(save_dir, f'real_frog_{step}.png'))
    else:
        time_cost = end_time - start_time
        time_eta = time_cost * (iterations - step)
        print(f'{step}/{iterations}: {time_cost:.2f}s - ETA: {time_eta:.0f}s', end='\r')
        
```

    step 0: discriminator loss: 0.6944685578346252, adversarial loss: 0.7566524744033813
    ...
    step 500: discriminator loss: 0.7020201683044434, adversarial loss: 0.7446410059928894
    ...
    step 1000: discriminator loss: 0.7096449136734009, adversarial loss: 0.752526581287384


最后输出的图像：

![最后输出的图像](https://tva1.sinaimg.cn/large/007S8ZIlgy1gi27n2ulptj300w00w0si.jpg)

效果相当差。这个东西训练消耗太大了，又是 CPU 劝退，我只跑了 1000 轮，还太少了。。。不愧为全书最后一题，压轴，这封青蛙图我不要了。😂
