---
categories:
- Machine Learning
- Deep Learning with Python
date: 2020-08-17 10:31:34
tag:
- Machine Learning
- Deep Learning
title: Python深度学习之Keras函数式API
---



# Deep Learning with Python

这篇文章是我学习《Deep Learning with Python》(第二版，François Chollet 著) 时写的系列笔记之一。文章的内容是从  Jupyter notebooks 转成 Markdown 的，你可以去 [GitHub](https://github.com/cdfmlr/Deep-Learning-with-Python-Notebooks) 或 [Gitee](https://gitee.com/cdfmlr/Deep-Learning-with-Python-Notebooks) 找到原始的 `.ipynb` 笔记本。

你可以去[这个网站在线阅读这本书的正版原文](https://livebook.manning.com/book/deep-learning-with-python)(英文)。这本书的作者也给出了配套的 [Jupyter notebooks](https://github.com/fchollet/deep-learning-with-python-notebooks)。

本文为 **第7章  高级的深度学习最佳实践** (Chapter 7. *Advanced deep-learning best practices*) 的笔记之一。

[TOC]

## 7.1 Going beyond the Sequential model: the Keras functional API

> 不用 Sequential 模型的解决方案：Keras 函数式 API

我们之前用的 Sequential 模型是最基础、但常用的一种模型，它只有一个输入和一个输出，整个网络由层线性堆叠而成。

![Sequential 模型:层的线性堆叠](https://tva1.sinaimg.cn/large/007S8ZIlgy1ghntkt18rxj30co0hi0tn.jpg)

但是，有时我们的网络需要多个输入。比如预测衣服价格，输入商品信息、文本描述、图片，这三类信息应该分别用 Dense、RNN、CNN 处理，提取出信息后用一个合并模块把所有各种信息综合起来最终预测价格：

![一个多输入模型](https://tva1.sinaimg.cn/large/007S8ZIlgy1ghntomauikj30vo0c03zu.jpg)

也有时，我们的网络需要多个输出（多个头）。比如输入一个小说，我们希望得到小说的分类，并推测写作时间。这个问题应该使用一个共用的模块去处理文本，提取信息，然后分别交给小说分类器、日期回归器去预测分类、写作时间：

![一个多输出(或多头)模型](https://tva1.sinaimg.cn/large/007S8ZIlgy1ghntrygsgsj30oq0jstak.jpg)

还有时，有些复杂的网络会使用非线性的网络拓扑结构。比如一种叫 Inception 的东西，输入会被多个并行的卷积分支处理，然后将这些分支的输出合并为单个张量；还有种叫 residual connection （残差连接）的方法，将前面的输出张量与后面的输出张量相加，从而将前面的表示重新注入下游数据流中，防止信息处理流程中的信息损失：

![Inception 模块:层组成的子图，具有多个并行卷积分支；残差连接:通过特征图相加将前面的信息重新注入下游数据
](https://tva1.sinaimg.cn/large/007S8ZIlgy1ghntzbsxzoj31880miaic.jpg)

这些网络都是图状(graph-like)的，是个网络结构，而不是 Sequential 那样的线性堆叠。要在 Keras 中实现这种复杂的模型，就需要使用 Keras 的函数式 API。

### 函数式 API

Keras 的函数式 API 把层当作函数来使用，接收张量并返回张量：


```python
from tensorflow.keras import Input, layers

input_tensor = Input(shape=(32, ))    # 输入张量
dense = layers.Dense(32, activation='relu')    # 层函数
output_tensor = dense(input_tensor)   # 输出张量 
```

我们来用函数式 API 构建一个简单网络，和 Sequential 做比较：


```python
# Sequential 模型

from tensorflow.keras.models import Sequential
from tensorflow.keras import layers

seq_model = Sequential()
seq_model.add(layers.Dense(32, activation='relu', input_shape=(64, )))
seq_model.add(layers.Dense(32, activation='relu'))
seq_model.add(layers.Dense(10, activation='softmax'))

seq_model.summary()
```

    Model: "sequential"
    _________________________________________________________________
    Layer (type)                 Output Shape              Param #   
    =================================================================
    dense_1 (Dense)              (None, 32)                2080      
    _________________________________________________________________
    dense_2 (Dense)              (None, 32)                1056      
    _________________________________________________________________
    dense_3 (Dense)              (None, 10)                330       
    =================================================================
    Total params: 3,466
    Trainable params: 3,466
    Non-trainable params: 0
    _________________________________________________________________



```python
# 函数式 API 模型

from tensorflow.keras.models import Model
from tensorflow.keras import Input
from tensorflow.keras import layers

input_tensor = Input(shape=(64, ))
x = layers.Dense(32, activation='relu')(input_tensor)
x = layers.Dense(32, activation='relu')(x)
output_tensor = layers.Dense(10, activation='softmax')(x)

func_model = Model(input_tensor, output_tensor)

func_model.summary()
```

    Model: "functional_1"
    _________________________________________________________________
    Layer (type)                 Output Shape              Param #   
    =================================================================
    input_2 (InputLayer)         [(None, 64)]              0         
    _________________________________________________________________
    dense_4 (Dense)              (None, 32)                2080      
    _________________________________________________________________
    dense_5 (Dense)              (None, 32)                1056      
    _________________________________________________________________
    dense_6 (Dense)              (None, 10)                330       
    =================================================================
    Total params: 3,466
    Trainable params: 3,466
    Non-trainable params: 0
    _________________________________________________________________


Model 对象实例化的时候，只需给出输入张量和输入张量变换(经过各种层)得到的输出张量。Keras 会在自动找出从 input_tensor 到 output_tensor 所包含的每一层，并将这些层组合成一个图状的数据结构——一个 Model。

注意，output_tensor 必须是由对应的 input_tensor 变换得到的。如果用不相关的输入张量和输出张量来构建 Model，会爆 Graph disconnected 的 ValueError (书上写的 keras 是 RuntimeError，tf.keras 是 ValueError)：

```python
>>> unrelated_input = Input(shape=(32,))
>>> bad_model = Model(unrelated_input, output_tensor)
... # Traceback
ValueError: Graph disconnected: cannot obtain value for tensor Tensor("input_2:0", shape=(None, 64), dtype=float32) at layer "dense_4". The following previous layers were accessed without issue: []
```

也就是说，无法从指定的输入连接到输出形成一张图（Graph，那种数据结构，网络的那种）啦。

对这种函数式 API 构建的网络，编译、训练或评估都和 Sequential 相同。


```python
# 编译
func_model.compile(optimizer='rmsprop', loss='categorical_crossentropy')

# 随机训练数据
import numpy as np
x_train = np.random.random((1000, 64))
y_train = np.random.random((1000, 10))

# 训练
func_model.fit(x_train, y_train, epochs=10, batch_size=128)

# 评估
score = func_model.evaluate(x_train, y_train)
```

    Epoch 1/10
    8/8 [==============================] - 0s 1ms/step - loss: 33.5245
    Epoch 2/10
    8/8 [==============================] - 0s 1ms/step - loss: 38.1499
    Epoch 3/10
    8/8 [==============================] - 0s 2ms/step - loss: 42.0662
    Epoch 4/10
    8/8 [==============================] - 0s 1ms/step - loss: 46.1707
    Epoch 5/10
    8/8 [==============================] - 0s 813us/step - loss: 50.6095
    Epoch 6/10
    8/8 [==============================] - 0s 1ms/step - loss: 54.8778
    Epoch 7/10
    8/8 [==============================] - 0s 1ms/step - loss: 59.6547
    Epoch 8/10
    8/8 [==============================] - 0s 1ms/step - loss: 64.5255
    Epoch 9/10
    8/8 [==============================] - 0s 1ms/step - loss: 69.2659
    Epoch 10/10
    8/8 [==============================] - 0s 685us/step - loss: 74.5707
    32/32 [==============================] - 0s 617us/step - loss: 78.1296


### 多输入模型

函数式 API 可用于构建具有多个输入的模型。多个输入的模型，通常会在某个点把不同分支用一个可以组合张量的层合并起来。组合张量，可以用相加、连接等，在 keras 中提供了诸如 `keras.layers.add`、`keras.layers.concatenate` 等的层来完成这些操作。

看一个具体的例子，做一个问答模型。典型的问答模型要使用两个输入：

- 问题文本
- 提供用于回答问题的信息文本(比如相关的新闻文章)

模型要生成（输出）一个回答。最简单的情况是只回答一个词，我们可以通过面向某些预定义的词表，把输出做 softmax 得到结果。

![问答模型](https://tva1.sinaimg.cn/large/007S8ZIlgy1ghnvld5q4aj310q0imq4k.jpg)

用函数式 API 来实现这个模型，我们先构建两个独立分支，将 reference text 和 question 分别表示成向量，然后连接这两个向量，在连接完成等到的表示上添加一个 softmax 分类器：


```python
from tensorflow.keras.models import Model
from tensorflow.keras import layers
from tensorflow.keras import Input

text_vocabulary_size = 10000
question_vocabulary_size = 10000
answer_vocabulary_size = 500

# 参考
text_input = Input(shape=(None, ), dtype='int32', name='text')
embedded_text = layers.Embedding(text_vocabulary_size, 64)(text_input)
encoded_text = layers.LSTM(32)(embedded_text)

# 问题
question_input = Input(shape=(None, ), dtype='int32', name='question')
embedded_question = layers.Embedding(question_vocabulary_size, 32)(question_input)
encoded_question = layers.LSTM(16)(embedded_question)

# 合并参考、问题分支
concatenated = layers.concatenate([encoded_text, encoded_question], axis=-1)

# 顶层分类器
answer = layers.Dense(anser_vocabulary_size, activation='softmax')(concatenated)

model = Model([text_input, question_input], answer, name='QA')

model.summary()

model.compile(optimizer='rmsprop', 
              loss='categorical_crossentropy', 
              metrics=['acc'])
```

    Model: "QA"
    __________________________________________________________________________________________________
    Layer (type)                    Output Shape         Param #     Connected to                     
    ==================================================================================================
    text (InputLayer)               [(None, None)]       0                                            
    __________________________________________________________________________________________________
    question (InputLayer)           [(None, None)]       0                                            
    __________________________________________________________________________________________________
    embedding_13 (Embedding)        (None, None, 64)     640000      text[0][0]                       
    __________________________________________________________________________________________________
    embedding_14 (Embedding)        (None, None, 32)     320000      question[0][0]                   
    __________________________________________________________________________________________________
    lstm_13 (LSTM)                  (None, 32)           12416       embedding_13[0][0]               
    __________________________________________________________________________________________________
    lstm_14 (LSTM)                  (None, 16)           3136        embedding_14[0][0]               
    __________________________________________________________________________________________________
    concatenate_6 (Concatenate)     (None, 48)           0           lstm_13[0][0]                    
                                                                     lstm_14[0][0]                    
    __________________________________________________________________________________________________
    dense_13 (Dense)                (None, 500)          24500       concatenate_6[0][0]              
    ==================================================================================================
    Total params: 1,000,052
    Trainable params: 1,000,052
    Non-trainable params: 0
    __________________________________________________________________________________________________


在训练这种多输入模型的时候，可以传输入组成的列表，对于指定了 name 的 input 也可以传一个字典：


```python
import numpy as np

num_samples = 1000
max_length = 100

text = np.random.randint(1, text_vocabulary_size, 
                         size=(num_samples, max_length))
question = np.random.randint(1, question_vocabulary_size, 
                             size=(num_samples, max_length))
answers = np.random.randint(0, 1, 
                            size=(num_samples, answer_vocabulary_size)) # one-hot 编码的

# 方法1. 传列表
model.fit([text, question], answers, epochs=2, batch_size=128)

# 方法2. 传字典
model.fit({'text': text, 'question': question}, answers, epochs=2, batch_size=128)
```

    Epoch 1/2
    8/8 [==============================] - 0s 54ms/step - loss: 0.0000e+00 - acc: 0.0000e+00
    Epoch 2/2
    8/8 [==============================] - 0s 57ms/step - loss: 0.0000e+00 - acc: 0.0000e+00
    Epoch 1/2
    8/8 [==============================] - 0s 53ms/step - loss: 0.0000e+00 - acc: 0.0000e+00
    Epoch 2/2
    8/8 [==============================] - 0s 54ms/step - loss: 0.0000e+00 - acc: 0.0000e+00





    <tensorflow.python.keras.callbacks.History at 0x13e55f9d0>



### 多输出模型

用函数式 API 来构建具有多个输出(多头)的模型也很方便。例如，我们要做一个试图同时预测数据的不同性质的网络：输入某人的一些社交媒体发帖，尝试预测该人的年龄、性别和收入水平属性：

![具有三个头的社交媒体模型](https://tva1.sinaimg.cn/large/007S8ZIlgy1gho2fgeqwrj30q40bit9u.jpg)

具体的实现很简单，在最后分别写 3 个不同的输出就行了：


```python
from tensorflow.keras.layers import Conv1D, MaxPooling1D, GlobalMaxPool1D, Dense
from tensorflow.keras import Input
from tensorflow.keras.models import Model

vocabulary_size = 50000
num_income_groups = 10

posts_input = Input(shape=(None,), dtype='int32', name='posts')
embedded_post = layers.Embedding(256, vocabulary_size)(posts_input)
x = Conv1D(128, 5, activation='relu')(embedded_post)
x = MaxPooling1D(5)(x)
x = Conv1D(256, 5, activation="relu")(x)
x = Conv1D(256, 5, activation="relu")(x)
x = MaxPooling1D(5)(x)
x = Conv1D(256, 5, activation="relu")(x)
x = Conv1D(256, 5, activation="relu")(x)
x = GlobalMaxPool1D()(x)
x = Dense(128, activation='relu')(x)

# 定义多个头（输出）
age_prediction = Dense(1, name='age')(x)
income_prediction = Dense(num_income_groups, activation='softmax', name='income')(x)
gender_prediction = Dense(1, activation='sigmoid', name='gender')(x)

model = Model(posts_input, [age_prediction, income_prediction, gender_prediction])

model.summary()
```

    Model: "functional_6"
    __________________________________________________________________________________________________
    Layer (type)                    Output Shape         Param #     Connected to                     
    ==================================================================================================
    posts (InputLayer)              [(None, None)]       0                                            
    __________________________________________________________________________________________________
    embedding_15 (Embedding)        (None, None, 50000)  12800000    posts[0][0]                      
    __________________________________________________________________________________________________
    conv1d (Conv1D)                 (None, None, 128)    32000128    embedding_15[0][0]               
    __________________________________________________________________________________________________
    max_pooling1d (MaxPooling1D)    (None, None, 128)    0           conv1d[0][0]                     
    __________________________________________________________________________________________________
    conv1d_1 (Conv1D)               (None, None, 256)    164096      max_pooling1d[0][0]              
    __________________________________________________________________________________________________
    conv1d_2 (Conv1D)               (None, None, 256)    327936      conv1d_1[0][0]                   
    __________________________________________________________________________________________________
    max_pooling1d_1 (MaxPooling1D)  (None, None, 256)    0           conv1d_2[0][0]                   
    __________________________________________________________________________________________________
    conv1d_3 (Conv1D)               (None, None, 256)    327936      max_pooling1d_1[0][0]            
    __________________________________________________________________________________________________
    conv1d_4 (Conv1D)               (None, None, 256)    327936      conv1d_3[0][0]                   
    __________________________________________________________________________________________________
    global_max_pooling1d (GlobalMax (None, 256)          0           conv1d_4[0][0]                   
    __________________________________________________________________________________________________
    dense_14 (Dense)                (None, 128)          32896       global_max_pooling1d[0][0]       
    __________________________________________________________________________________________________
    age (Dense)                     (None, 1)            129         dense_14[0][0]                   
    __________________________________________________________________________________________________
    income (Dense)                  (None, 10)           1290        dense_14[0][0]                   
    __________________________________________________________________________________________________
    gender (Dense)                  (None, 1)            129         dense_14[0][0]                   
    ==================================================================================================
    Total params: 45,982,476
    Trainable params: 45,982,476
    Non-trainable params: 0
    __________________________________________________________________________________________________


**多头模型的编译**

在编译这种模型的时候，由于是有不同的目标，所以要注意需要对网络的各个头指定不同的损失函数。

但梯度下降的作用只能是将一个标量最小化，所以在 Keras 中，编译时为不同输出指定的不同损失，到了训练中，会被相加得到一个全局损失，训练过程就是将这个全局损失最小化。

在这种情况下，如果损失贡献严重不平衡，模型就会优先去优化损失数值最大的任务，而不考虑其他任务。为了解决这个问题，可以为不同的损失加权。例如 mse 的损失值通常是 3~5，binary_crossentropy 的损失值通常低至 0.1，为了平衡损失贡献，我们可以让 binary_crossentropy 的权重取 10、mse 损失的权重取 0.5。

多个损失以及加权的指定都是使用列表或字典来完成：

```python
model.compile(optimizer='rmsprop',
              loss=['mse', 'categorical_crossentropy', 'binary_crossentropy'],
              loss_weights=[0.25, 1., 10.])

# 或者如果有对输出层命名的话，可以用字典：
model.compile(optimizer='rmsprop',
              loss={'age': 'mse',
                    'income': 'categorical_crossentropy',
                    'gender': 'binary_crossentropy'},
              loss_weights={'age': 0.25,
                            'income': 1.,
                            'gender': 10.})
```

**多头模型的训练**

训练这种模型的时候，把目标输出用列表或字典传递就好了：

```python
model.fit(posts, [age_targets, income_targets, gender_targets],
          epochs=10, batch_size=64)

# or

model.fit(posts, {'age': age_targets,
                  'income': income_targets,
                  'gender': gender_targets},
          epochs=10, batch_size=64)
```

### 层的有向无环图

利用函数式 API，除了构建多输入和多输出的模型，我们还可以实现具有复杂的内部拓扑结构的网络。

实际上 Keras 中的神经网络可以是由层组成的任意有向无环图。比较著名的图结构的组件有 Inception 模块和残差连接。

#### Inception 模块

Inception 是模块的堆叠，其中的每个模块看起来像是小型的独立网络，这些模块被分为多个并行分支，最后将所得到的特征连接到一起。这种操作可以让网络分别学习图片的空间特征和逐通道的特征，这样会比用一个网络去同时学习这些特征更加有效。

下图是一个简化的 Inception V3 模块：

![Inception 模块](https://tva1.sinaimg.cn/large/007S8ZIlgy1gho3zlsj9bj31200j6act.jpg)

> 注：这里用的 1x1 的卷积，叫作逐点卷积(pointwise convolution)，是 Inception 模块的特色。
> 它一次只查看一个像素，计算得到的特征就能够将输入的各通道中的信息混合在一起，但又不会混入空间信息。
> 这样就实现了区分开通道特征学习和空间特征学习。

用函数式 API 可以实现它：


```python
from tensorflow.keras import layers

x = Input(shape=(None, None, 3))    # RGB 图片

branch_a = layers.Conv2D(128, 1, activation='relu', strides=2, padding='same')(x)

branch_b = layers.Conv2D(128, 1, activation='relu', padding='same')(x)
branch_b = layers.Conv2D(128, 3, activation='relu', strides=2, padding='same')(branch_b)

branch_c = layers.AveragePooling2D(3, strides=2, padding='same')(x)
branch_c = layers.Conv2D(128, 3, activation='relu', padding='same')(branch_c)

branch_d = layers.Conv2D(128, 1, activation='relu', padding='same')(x)
branch_d = layers.Conv2D(128, 3, activation='relu', padding='same')(branch_d)
branch_d = layers.Conv2D(128, 3, activation='relu', strides=2, padding='same')(branch_d)

output = layers.concatenate([branch_a, branch_b, branch_c, branch_d], axis=-1)
```

其实，Keras 内置了完整的 Inception V3 架构。可以通过 `keras.applications.inception_v3.InceptionV3` 去调用。

与 Inception 相关的，还有一个叫做 **Xception** 的东西。Xception 这个词是 extreme inception（极端 Inception）的意思，它是一种比较极端的 Inception，它将通道特征学习与空间特征学习完全分离开。Xception 的参数个数与 Inception V3 大致相同，但它对参数的使用效率更高，所以在大规模数据集上的运行性能更好、精度更高。

#### 残差连接

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

#### 共享层权重

使用函数式 API，还有一种操作是**多次使用一个层实例**。对同一个层实例调用多次，则可以重复使用相同的权重。利用这种特性，可以构建出具有共享分支的模型，即几个分支全都共享相同的知识并执行相同的运算。

例如，我们想要评估两个句子之间的语义相似度。这个模型有输入两个句子，输出一个范围在 0~1 的分数，值越大则句意越相似。

在这个问题中，两个输入句子是可以互换的（句子 A 相对于 B 的相似度等于 B 相对于 A 的相似度）。因此，不应该学习两个单独的模型来分别处理两个输入句子。而应该用一个 LSTM 层来处理两个句子。这个 LSTM 层的表示(权重)是同时从两个输入学习来的。这种模型称为连体 LSTM (Siamese LSTM)或共享 LSTM (shared LSTM)。

这样的模型使用 Keras 函数式 API 中的层共享实现：


```python
from tensorflow.keras import layers
from tensorflow.keras import Input
from tensorflow.keras.models import Model

lstm = layers.LSTM(32)  # 只示例化一个 LSTM

left_input = Input(shape=(None, 128))
left_output = lstm(left_input)

right_input = Input(shape=(None, 128))
right_output = lstm(right_input)

merged = layers.concatenate([left_output, right_output], axis=-1)
predictions = layers.Dense(1, activation='sigmoid')(merged)

model = Model([left_input, right_input], predictions)

model.summary()
```

    Model: "functional_8"
    __________________________________________________________________________________________________
    Layer (type)                    Output Shape         Param #     Connected to                     
    ==================================================================================================
    input_13 (InputLayer)           [(None, None, 128)]  0                                            
    __________________________________________________________________________________________________
    input_14 (InputLayer)           [(None, None, 128)]  0                                            
    __________________________________________________________________________________________________
    lstm_15 (LSTM)                  (None, 32)           20608       input_13[0][0]                   
                                                                     input_14[0][0]                   
    __________________________________________________________________________________________________
    concatenate_13 (Concatenate)    (None, 64)           0           lstm_15[0][0]                    
                                                                     lstm_15[1][0]                    
    __________________________________________________________________________________________________
    dense_15 (Dense)                (None, 1)            65          concatenate_13[0][0]             
    ==================================================================================================
    Total params: 20,673
    Trainable params: 20,673
    Non-trainable params: 0
    __________________________________________________________________________________________________


#### 将模型作为层

在 Keras 中，我们可以把模型当作层使用（把模型现象为一个大的层），Sequential 类和 Model 类都可以当层用。直接像层一样去函数式地调用就行了：

```python
y = model(x)
y1, y2 = model_with_multi_inputs_and_outputs([x1, x2])
```

例如，我们处理双摄像头作为输入的视觉模型（这种模型可以感知深度）。我们一个用 applications.Xception 模型作为层，并使用前面的共享层的方法来实现这个网络：


```python
from tensorflow.keras import layers
from tensorflow.keras import Input
from tensorflow.keras import applications

xception_base = applications.Xception(weights=None, include_top=False)

left_input = Input(shape=(250, 250, 3))
right_input = Input(shape=(250, 250, 3))

left_features = xception_base(left_input)
right_input = xception_base(right_input)

merged_features = layers.concatenate([left_features, right_input], axis=-1)

```

---

```c
By("CDFMLR", "2020-08-17");
```

