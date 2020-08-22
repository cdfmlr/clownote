---
categories:
- Machine Learning
- Deep Learning with Python
date: 2020-08-22 11:19:34
tag:
- Machine Learning
- Deep Learning
title: Python深度学习之神经风格迁移
---



# Deep Learning with Python

这篇文章是我学习《Deep Learning with Python》(第二版，François Chollet 著) 时写的系列笔记之一。文章的内容是从  Jupyter notebooks 转成 Markdown 的，你可以去 [GitHub](https://github.com/cdfmlr/Deep-Learning-with-Python-Notebooks) 或 [Gitee](https://gitee.com/cdfmlr/Deep-Learning-with-Python-Notebooks) 找到原始的 `.ipynb` 笔记本。

你可以去[这个网站在线阅读这本书的正版原文](https://livebook.manning.com/book/deep-learning-with-python)(英文)。这本书的作者也给出了配套的 [Jupyter notebooks](https://github.com/fchollet/deep-learning-with-python-notebooks)。

本文为 **第8章  生成式深度学习** (Chapter 8. *Generative deep learning*) 的笔记之一。

[TOC]

## 8.3 Neural style transfer

> 神经风格迁移

神经风格迁移(neural style transfer)，基于深度学习的神经网络，将参考图像的风格应用于目标图像，同时保留目标图像的内容，创造出新的图像。

![一个风格迁移的示例](https://tva1.sinaimg.cn/large/007S8ZIlgy1ghsqybmpeij314y0cgarv.jpg)

神经风格迁移的思想很简单：定义一个损失函数来指定要实现的目标，然后将这个损失最小化。这里的目标就是保存原始图像的内容，同时采用参考图像的风格。

假设有函数 content 和 style 分别可以计算出输入图像的内容和风格，以及有范式函数 distance，则神经风格迁移的损失可以表达为：

```python
loss = distance(content(original_image) - content(generated_image)) +
       distance(style(reference_image) - style(generated_image))
```

事实上，利用深度卷积神经网络，是可以从数学上定义 style 和 content 函数的。

#### 损失定义

1. **内容损失**

卷积神经网络靠底部（前面）的层激活包含关于图像的局部信息，靠近顶部（后面）的层则包含更加全局、抽象的信息。内容就是图像的全局、抽象的信息，所以可以用卷积神经网络靠顶部的层激活来表示图像的内容。

因此，给定一个预训练的卷积神经网络，选定一个靠顶部的层，内容损失可以使用「该层在目标图像上的激活」和「该层在生成图像上的激活」之间的 L2 范数。

2. **风格损失**

不同于内容只用一个层即可表达，风格需要多个层才能定义。风格是多种方面的，比如笔触、线条、纹理、颜色等等，这些内容会出现在不同的抽象程度上。所以风格的表达就需要捕捉所有空间尺度上提取的外观，而不仅仅是在单一尺度上。

在这种思想下，风格损失的表达，可以借助于层激活的 Gram 矩阵。这个 Gram 矩阵就是某一层的各个特征图的内积，表达了层的特征间相互关系(correlation)的映射，它就对应于这个尺度上找到的纹理(texture)的外观。而在不同的层激活内保存相似的内部相互关系，就可以认为是“风格”了。

那么，我们就可以用生成图像和风格参考图像在不同层上保持的纹理，来定义风格损失了。

#### 神经风格迁移的 Keras 实现

神经风格迁移可以用任何预训练卷积神经网络来实现，这里选用 VGG19。

神经风格迁移的步骤如下：

1. 创建一个网络，同时计算风格参考图像、目标图像和生成图像的 VGG19 层激活;
2. 使用这三张图像上计算的层激活来定义之前所述的损失函数;
3. 梯度下降来将这个损失函数最小化。

在开始构建网络前，先定义风格参考图像和目标图像的路径。如果图像尺寸差异很大，风格迁移会比较困难，所以这里我们还统一定义一下尺寸：


```python
# 不使用及时执行模式

import tensorflow as tf

tf.compat.v1.disable_eager_execution()
```


```python
# 定义初始变量

from tensorflow.keras.preprocessing.image import load_img, img_to_array

target_image_path = 'img/portrait.jpg'
style_referencce_image_path = 'img/transfer_style_reference.jpg'

width, height = load_img(target_image_path).size
img_height = 400
img_width = width * img_height // height
```

这里图片我选择了：

- transfer_style_reference: 文森特·梵高《麦田里的丝柏树》（*A Wheatfield, with Cypresses*），1889年，收藏于纽约大都会博物馆。
- portrait: 保罗·高更《不列塔尼牧人》(*The Swineherd, Brittany*)，1888年，收藏于美国加州洛杉矶郡立美术馆。

![麦田里的丝柏树与不列塔尼牧人](https://tva1.sinaimg.cn/large/007S8ZIlgy1ghtv5qecwtj31g20n1u0x.jpg)

接下来，我们需要一些辅助函数，用于图像的加载、处理。


```python
# 辅助函数

import numpy as np
from tensorflow.keras.applications import vgg19

def preprocess_image(image_path):
    img = load_img(image_path, target_size=(img_height, img_width))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = vgg19.preprocess_input(img)
    return img

def deprocess_image(x):
    # vgg19.preprocess_input 会减去ImageNet的平均像素值，使其中心为0。这里做逆操作：
    x[:, :, 0] += 103.939
    x[:, :, 1] += 116.779
    x[:, :, 2] += 123.680
    
    # BGR -> RGB
    x = x[:, :, ::-1]
    x = np.clip(x, 0, 255).astype('uint8')
    
    return x
```

下面构建 VGG19 网络：接收三张图像的 batch 作为输入，三张图像分别是风格参考图像、 目标图像的 constant 和一个用于保存生成图像的 placeholder。


```python
from tensorflow.keras import backend as K

target_image = K.constant(preprocess_image(target_image_path))
style_reference_image = K.constant(preprocess_image(style_referencce_image_path))
combination_image = K.placeholder((1, img_height, img_width, 3))

input_tensor = K.concatenate([target_image,
                              style_reference_image,
                              combination_image], axis=0)

model = vgg19.VGG19(input_tensor=input_tensor,
                    weights='imagenet',
                    include_top=False)

print('Model loaded.')
```

    Model loaded.


定义内容损失，保证目标图像和生成图像在网络顶层的结果相似：


```python
# 内容损失

def content_loss(base, combination):
    return K.sum(K.square(combination - base))
```

然后是风格损失，计算输入矩阵的 Gram 矩阵，借助用 Gram 矩阵计算风格损失：


```python
# 风格损失

def gram_matrix(x):
    features = K.batch_flatten(K.permute_dimensions(x, (2, 0, 1)))
    gram = K.dot(features, K.transpose(features))
    return gram

def style_loss(style, combination):
    S = gram_matrix(style)
    C = gram_matrix(combination)
    channels = 3
    size = img_height * img_width
    return K.sum(K.square(S - C)) / (4.0 * (channels ** 2) * (size ** 2))
```

这里我们再额外定义一个「总变差损失」(total variation loss)，促使生成图像具有空间连续性，避免结果过度像素化，相当于一个正则化。


```python
# 总变差损失

def total_variation_loss(x):
    a = K.square(
        x[:, :img_height - 1, :img_width - 1, :] - 
        x[:, 1:, :img_width - 1, :])
    b = K.square(
        x[:, :img_height - 1, :img_width - 1, :] - 
        x[:, :img_height - 1, 1:, :])
    return K.sum(K.pow(a + b, 1.25))
```

现在考虑具体的损失计算：在计算内容损失时，我们需要一个靠顶部的层；对于风格损失，我们需要使用一系列层，既包括顶层也包括底层；最后还需要添加总变差损失。最终的损失就是这三类损失的加权平均。


```python
# 定义需要最小化的最终损失

outputs_dict = {layer.name: layer.output for layer in model.layers}

content_layer = 'block5_conv2'
style_layers = [f'block{i}_conv1' for i in range(1, 6)]

total_variation_weight = 1e-4
style_weight = 1.0
content_weight = 0.025  # content_weight越大，目标内容更容易在生成图像中越容易识别

# 内容损失
loss = K.variable(0.)
layer_features = outputs_dict[content_layer]
target_image_features = layer_features[0, :, :, :]
combination_features = layer_features[2, :, :, :]
loss = loss + content_weight * content_loss(target_image_features, combination_features)

# 风格损失
for layer_name in style_layers:
    layer_features = outputs_dict[layer_name]
    style_reference_features = layer_features[1, :, :, :]
    combination_features = layer_features[2, :, :, :]
    sl = style_loss(style_reference_features, combination_features)
    loss = loss + (style_weight / len(style_layers)) * sl
    
# 总变差损失
loss = loss + total_variation_weight * total_variation_loss(combination_image)
```

最后就是梯度下降过程了。这里调用 scipy，用 `L-BFGS` 算法进行最优化。

为了快速计算，我们创建一个 Evaluator 类，同时计算损失值和梯度值，在第一次调用时会返回损失值，同时缓存梯度值用于下一次调用。


```python
# 设置梯度下降过程

grads = K.gradients(loss, combination_image)[0]
fetch_loss_and_grads = K.function([combination_image], [loss, grads])

class Evaluator(object):
    def __init__(self):
        self.loss_value = None
        self.grads_values = None
        
    def loss(self, x):
        assert self.loss_value is None
        x = x.reshape((1, img_height, img_width, 3))
        outs = fetch_loss_and_grads([x])
        loss_value = outs[0]
        grad_values = outs[1].flatten().astype('float64')
        self.loss_value = loss_value
        self.grads_values = grad_values
        return self.loss_value
    
    def grads(self, x):
        assert self.loss_value is not None
        grad_values = np.copy(self.grads_values)
        self.loss_value = None
        self.grad_values = None
        return grad_values
        
evaluator = Evaluator()
```

最后的最后，调用 SciPy 的 L-BFGS 算法来运行梯度上升过程，每一次迭代(20 步梯度上升)后都保存当前的生成图像：


```python
from scipy.optimize import fmin_l_bfgs_b
from imageio import imsave
import time

iterations = 20

def result_fname(iteration):
    return f'results/result_at_iteration_{iteration}.png'

x = preprocess_image(target_image_path)
x = x.flatten()

for i in range(iterations):
    print('Start of iteration', i)
    start_time = time.time()
    
    x, min_val, info = fmin_l_bfgs_b(evaluator.loss,
                                     x,
                                     fprime=evaluator.grads,
                                     maxfun=20)
    print('  Current loss value:', min_val)
    
    img = x.copy().reshape((img_height, img_width, 3))
    img = deprocess_image(img)
    fname = result_fname(i)
    imsave(fname, img)
    print('  Image saved as', fname)
    
    end_time = time.time()
    print(f'  Iteration {i} completed in {end_time - start_time} s')
```

    Start of iteration 0
      Current loss value: 442468450.0
      Image saved as results/result_at_iteration_0.png
      Iteration 0 completed in 177.57321500778198 s
    ...
    Start of iteration 19
      Current loss value: 44762796.0
      Image saved as results/result_at_iteration_19.png
      Iteration 19 completed in 177.95070385932922 s


把结果和原图放在一起比较一下：

![结果1](https://tva1.sinaimg.cn/large/007S8ZIlgy1ghu38838haj317h0u0b2b.jpg)

再看一个例子：风格参考还是用梵高的《麦田里的丝柏树》，内容用米勒的《拾穗者》(Des glaneuses，1857年，巴黎奥塞美术馆)。比较有意思的是，梵高本人画过一幅部分模仿《拾穗者》的《夕阳下两位农妇开掘积雪覆盖的田地》(Zwei grabende Bäuerinnen auf schneebedecktem Feld)：

![结果2](https://tva1.sinaimg.cn/large/007S8ZIlgy1ghu6d9c19jj30vr0u0u0x.jpg)

可以看到，我们的机器只是简单粗暴的风格迁移，而大师本人会在模仿中再创作。

最后，补充一点。这个风格迁移算法的运行比较慢，但足够简单。要实现快速风格迁移，可以考虑：首先利用这里介绍的方法，固定一张风格参考图像，给不同的内容图像，生成一大堆「输入-输出」训练样例，拿这些「输入-输出」去训练一个简单的卷积神经网络来学习这个特定风格的变换(输入->输出)。完成之后，对一张图像进行特定风格的迁移就非常快了，做一次前向传递就完成了。
