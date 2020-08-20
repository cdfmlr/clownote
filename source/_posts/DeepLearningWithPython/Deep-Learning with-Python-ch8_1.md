---
categories:
- Machine Learning
- Deep Learning with Python
date: 2020-08-20 11:21:34
tag:
- Machine Learning
- Deep Learning
title: Python深度学习之LSTM文本生成
---

# Deep Learning with Python

这篇文章是我学习《Deep Learning with Python》(第二版，François Chollet 著) 时写的系列笔记之一。文章的内容是从  Jupyter notebooks 转成 Markdown 的，你可以去 [GitHub](https://github.com/cdfmlr/Deep-Learning-with-Python-Notebooks) 或 [Gitee](https://gitee.com/cdfmlr/Deep-Learning-with-Python-Notebooks) 找到原始的 `.ipynb` 笔记本。

你可以去[这个网站在线阅读这本书的正版原文](https://livebook.manning.com/book/deep-learning-with-python)(英文)。这本书的作者也给出了配套的 [Jupyter notebooks](https://github.com/fchollet/deep-learning-with-python-notebooks)。

本文为 **第8章  生成式深度学习** (Chapter 8. *Generative deep learning*) 的笔记之一。

[TOC]

## 8.1 Text generation with LSTM

> 使用 LSTM 生成文本

以前有人说过：“generating sequential data is the closest computers get to dreaming”，让计算机生成序列是很有魅力的事情。我们将以文本生成为例，探讨如何将循环神经网络用于生成序列数据。这项技术也可以用于音乐的生成、语音合成、聊天机器人对话生成、甚至是电影剧本的编写等等。

其实，我们现在熟知的 LSTM 算法，最早被开发出来的时候，就是用于逐字符地生成文本的。

### 序列数据的生成

用深度学习生成序列的通用方法，就是训练一个网络(一般用 RNN 或 CNN)，输入前面的 Token，预测序列中接下来的 Token。

说的术语化一些：给定前面的 Token，能够对下一个 Token 的概率进行建模的网络叫作「语言模型(language model)」。语言模型能够捕捉到语言的统计结构 ——「潜在空间(latent space)」。训练好一个语言模型，输入初始文本字符串（称为「条件数据」，conditioning data），从语言模型中采样，就可以生成新 Token，把新的 Token 加入条件数据中，再次输入，重复这个过程就可以生成出任意长度的序列。

我们从一个简单的例子开始：用一个 LSTM 层，输入文本语料的 N 个字符组成的字符串，训练模型来生成第 N+1 个字符。模型的输出是做 softmax，在所有可能的字符上，得到下一个字符的概率分布。这个模型叫作「字符级的神经语言模型」(character-level neural language model)。

![使用语言模型逐个字符生成文本的过程](https://tva1.sinaimg.cn/large/007S8ZIlgy1ghq58v9qd6j319c0ka41y.jpg)

### 采样策略

使用字符级的神经语言模型生成文本时，最重要的问题是如何选择下一个字符。这里有几张常用方法：

- 贪婪采样(greedy sampling)：始终选择可能性最大的下一个字符。这个方法很可能得到重复的、可预测的字符串，而且可能意思不连贯。（输入法联想）
- 纯随机采样：从均匀概率分布中抽取下一个字符，其中每个字符的概率相同。这样随机性太高，几乎不会生成出有趣的内容。（就是胡乱输出字符的组合）
- 随机采样(stochastic sampling)：根据语言模型的结果，如果下一个字符是 e 的概率为 0.3，那么你会有 30% 的概率选择它。有一点的随机性，让生成的内容更~~随意~~富有变化，但又不是完全随机，输出可以比较有意思。

随机采样看上去很好，很有创造性，但有个问题是无法控制随机性的大小：随机性越大，可能富有创造性，但可能胡乱输出；随机性越小，可能更接近真实词句，但太死板、可预测。

为了在采样过程中控制随机性的大小，引入一个参数：「softmax 温度」(softmax temperature)，用于表示采样概率分布的熵，即表示所选择的下一个字符会有多么出人意料或多么可预测：

- 更高的温度：熵更大的采样分布，会生成更加出人意料、更加无结构的数据；
- 更低的温度：对应更小的随机性，会生成更加可预测的数据。

![对同一个概率分布进行不同的重新加权：更低的温度=更确定，更高的温度=更随机](https://tva1.sinaimg.cn/large/007S8ZIlgy1ghq692zm1nj316f0u0k9r.jpg)

具体的实现是，给定 temperature 值，对模型的 softmax 输出重新加权，得到新的概率分布：


```python
import numpy as np

def rewight_distribution(original_distributon, temperature=0.5):
    '''
    对于不同的 softmax 温度，对概率分布进行重新加权
    '''
    distribution = np.log(original_distribution) / temperature
    distribution = np.exp(distribution)
    return distribution / np.sum(distribution)
```

### 字符级 LSTM 文本生成实现

理论就上面那些了，现在，我们要用 Keras 来实现字符级的 LSTM 文本生成了。

#### 数据准备

首先，我们需要大量的文本数据(语料，corpus)来训练语言模型。可以去找足够大的一个或多个文本文件：维基百科、各种书籍等都可。这里我们选择用一些尼采的作品（英文译本），这样我们学习出来的语言模型将是有尼采的写作风格和主题的。（插：我，我以前自己写野生模型玩，都是用鲁迅😂）


```python
# 下载语料，并将其转换为全小写

from tensorflow import keras
import numpy as np

path = keras.utils.get_file(
    'nietzsche.txt', 
    origin='https://s3.amazonaws.com/text-datasets/nietzsche.txt')
text = open(path).read().lower()
print('Corpus length:', len(text))
```

    /usr/local/Cellar/python/3.7.6_1/Frameworks/Python.framework/Versions/3.7/lib/python3.7/importlib/_bootstrap.py:219: RuntimeWarning: numpy.ufunc size changed, may indicate binary incompatibility. Expected 192 from C header, got 216 from PyObject
      return f(*args, **kwds)
    /usr/local/Cellar/python/3.7.6_1/Frameworks/Python.framework/Versions/3.7/lib/python3.7/importlib/_bootstrap.py:219: RuntimeWarning: numpy.ufunc size changed, may indicate binary incompatibility. Expected 192 from C header, got 216 from PyObject
      return f(*args, **kwds)


    Downloading data from https://s3.amazonaws.com/text-datasets/nietzsche.txt
    606208/600901 [==============================] - 430s 709us/step
    Corpus length: 600893


接下来，我们要把文本做成数据 (向量化)：从 text 里提取长度为 `maxlen` 的序列(序列之间存在部分重叠)，进行 one-hot 编码，然后打包成 `(sequences, maxlen, unique_characters)` 形状的。同时，还需要准备数组 `y`，包含对应的目标，即在每一个所提取的序列之后出现的字符(也是 one-hot 编码的)：


```python
# 将字符序列向量化

maxlen = 60     # 每个序列的长度
step = 3        # 每 3 个字符采样一个新序列
sentences = []  # 保存所提取的序列
next_chars = [] # sentences 的下一个字符

for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i+maxlen])
    next_chars.append(text[i+maxlen])
print('Number of sequences:', len(sentences))

chars = sorted(list(set(text)))
char_indices = dict((char, chars.index(char)) for char in chars)
# 插：上面这两行代码 6
print('Unique characters:', len(chars))

print('Vectorization...')

x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)

for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1
```

    Number of sequences: 200278
    Unique characters: 57
    Vectorization...


#### 构建网络

我们要用到的网络其实很简单，一个 LSTM 层 + 一个 softmax 激活的 Dense 层就可以了。其实并不一定要用 LSTM，用一维卷积层也是可以生成序列的。


```python
# 用于预测下一个字符的单层 LSTM 模型

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

model = Sequential()
model.add(LSTM(128, input_shape=(maxlen, len(chars))))
model.add(Dense(len(chars), activation='softmax'))
```


```python
# 模型编译配置

from tensorflow.keras import optimizers

optimizer = optimizers.RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy',
              optimizer=optimizer)
```

#### 训练语言模型并从中采样

给定一个语言模型和一个种子文本片段，就可以通过重复以下操作来生成新的文本：

1. 给定目前已有文本，从模型中得到下一个字符的概率分布；
2. 根据某个温度对分布进行重新加权；
3. 根据重新加权后的分布对下一个字符进行随机采样；
4. 将新字符添加到文本末尾。

在训练模型之前，我们先把「采样函数」写了：


```python
def sample(preds, temperature=1.0):
    '''
    对模型得到的原始概率分布重新加权，并从中抽取一个字符索引
    '''
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)
```

最后，再来训练并生成文本。我们在每轮完成后都使用一系列不同的温度值来生成文本，这样就可以看到，随着模型收敛，生成的文本如何变化，以及温度对采样策略的影响：


```python
# 文本生成循环

import random

for epoch in range(1, 60):    # 训练 60 个轮次
    print(f'👉\033[1;35m epoch {epoch} \033[0m')    # print('epoch', epoch)
    
    model.fit(x, y,
              batch_size=128,
              epochs=1)
    
    start_index = random.randint(0, len(text) - maxlen - 1)
    generated_text = text[start_index: start_index + maxlen]
    print(f'  📖 Generating with seed: "\033[1;32;43m{generated_text}\033[0m"')    # print(f' Generating with seed: "{generated_text}"')
    
    for temperature in [0.2, 0.5, 1.0, 1.2]:
        print(f'\n   \033[1;36m 🌡️ temperature: {temperature}\033[0m')    # print('\n  temperature:', temperature)
        print(generated_text, end='')
        for i in range(400):    # 生成 400 个字符
            # one-hot 编码目前有的文本
            sampled = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(generated_text):
                sampled[0, t, char_indices[char]] = 1
            
            # 预测，采样，生成下一字符
            preds = model.predict(sampled, verbose=0)[0]
            next_index = sample(preds, temperature)
            next_char = chars[next_index]
            print(next_char, end='')
            
            generated_text = generated_text[1:] + next_char
            
    print('\n' + '-' * 20)
```

    👉 epoch 1 
    1565/1565 [==============================] - 170s 108ms/step - loss: 1.4089
      📖 Generating with seed: "ary!--will at least be entitled to demand in return that
    psy"
    
        🌡️ temperature: 0.2
    ary!--will at least be entitled to demand in return that
    psychological senses of the the most comprehensed that is a sense of a perhaps the experience of the heart the present that the profound that the experience of the exploition and present that is a self and the present that is a more of the senses of a more and the sense of a more art and the the exploition and self-contempt of a perhaps the superiom and perhaps the contempt of the superiom and all th
        🌡️ temperature: 0.5
    superiom and perhaps the contempt of the superiom and all the instance and plays place of comprehensed and so in morals and all the auther to present mettoral of the senses and fellines to have the conceive that the
    possibility of the expendeness, the hasters as how to really expendened and
    all that the forenies; and all the most consequently comes that the most constanter to constantering only all the expearated the expendeness is in the delight and one w
        🌡️ temperature: 1.0
    l the expearated the expendeness is in the delight and one would be persists more and world, others which in the utility of the fellows
    among and deceeth, virtuery, mode. one
    soul the most conterrites and ly under that conservate to mapt of the own toweration here old taste inilt, the "frew-well
    to openhanss"--and the way could easily hamint; becoming being, thrien himself, very deteruence who usked slaver and own scientification, of the eever," wand
    undou
        🌡️ temperature: 1.2
    ed slaver and own scientification, of the eever," wand
    undoupible "befost suldeces." it weim even astreated drwadged,
    owing parits, word of hister"
    enocest.-
    sychea, that that words in the savery: 
    y allverowed", when and liqksis felling, them soperation of clentous
    and blendiers.
    the pleasrvation humiturring, likeford of feit-rum. i must "nrightenmy," beneveral man." the goods-
    the cerses is christrantss and lightence--not man goemin love,
    frro-akem.y tix
    --------------------
    ...
    👉 epoch 30 
    1565/1565 [==============================] - 452s 289ms/step - loss: 1.2692
      📖 Generating with seed: "y system of morals, is that it is a
    long constraint. in orde"
    
        🌡️ temperature: 0.2
    y system of morals, is that it is a
    long constraint. in order to be stronger and according to the same the standand, as a men and sanctity, and all the sense of the strength to the sense of the strong the striving of the strong the striving of the sense of the same this consequently and something and in a man with the sense of the sense of the same the strong of the same the sense of the strength to the sense of the same the artist the strong more and the 
        🌡️ temperature: 0.5
    to the sense of the same the artist the strong more and the intellectually in the called bet of the more of such as something of standand, the experience and profound, and in the delusions of the morality of the propeted and the more of a good and one has a sorts of the constitute in the same the religion
    in the same the human condition, the old proper all this taste which seeming and the standand, and are to the person of the strength and the latten more 
        🌡️ temperature: 1.0
    , and are to the person of the strength and the latten more matter, fith, niquet of nature of rove seemsion and proxible is itself, it has
     final "genion" in coptent,
    and un so larmor, romant.
    
    bicident, with which fur one remain echo of
    called in this acqueis forceek of consciate convoled,
    asceticilies
    invaluable demardinatid.
    
              he in respons himons, which, a engliches bad hope feels these see,
    fermines "only he will"n--as stapty pullens of bad a
        🌡️ temperature: 1.2
    se see,
    fermines "only he will"n--as stapty pullens of bad adaval inexcepning at the unvery in all, whose in--that is a power be many trainitg prtunce--by the crueled him is every
    noble,
    as he society of this
    sneke viged, has to telless all juscallers. we megnant cominghik, as gray illow and of holy este, "the knowing" how videly upon the adventive. there is discived and it attine to jesubuc'--the .=--what
    lived
    a! iapower, profoundc: of himself, it is lie
    --------------------
    ...
    👉 epoch 59 
    1565/1565 [==============================] - 173s 110ms/step - loss: 1.2279
      📖 Generating with seed: "inward self-contempt, seek to get out of
    the business, no ma"
    
        🌡️ temperature: 0.2
    inward self-contempt, seek to get out of
    the business, no may be only and the ascetiably sense of the real and the sense of the more sense of the community of the moral and profound the way there is the sense of the most contempt of the spirit in a perceive, and the interpreting the sense of the world as it is the soul is the artist of the sense and the world as in the entire
    complication of the world as it is the strong of the most profound to the world a
        🌡️ temperature: 0.5
    orld as it is the strong of the most profound to the world as the self nowadays to me that all the artifure in the mother of significance of the roman and we are this from the strength of existing and faith enthurable to the discover of the contrain to
    religious were and self-grades the world with the way to the present think there are also all the plato-pit firels made a weart for the person of the rank on a way of the ethical prombates, to reason of the 
        🌡️ temperature: 1.0
    he rank on a way of the ethical prombates, to reason of the mortand: that pureon good lack as has refree, in a herore proposition is
    pronounce
    the last the reasonably book of will calued and vexeme, and no means mentary honour pertimate our new, conversations. it is that
    the sense ciertably with our distins of the remare of counter that german "miswome centurially instinct" in course,.
     hsyaulity he in their minds and matter of mystimalsing of itplupetin
        🌡️ temperature: 1.2
    y he in their minds and matter of mystimalsing of itplupeting.t his asserated approysely to special,
    are devial.; the finerevings
    in orieicalous also mistakeng time, a :     this
    benurion and
    european voightry
    ands centuries: it problem as place into the errords for triubtly etsibints, vetter after distrinitionn, where it lacking sole .=-vow accorded.
    
    12u borany utmansishe and diffire being savest his
    cardij(l qualition. neeked upon this
    essentially, his 
    --------------------

 利用更多的数据训练更大的模型，训练时间更长，生成的样本会更连贯、更真实。但是，这样生成的文本并没有任何意义。机器所做的仅仅是从统计模型中对数据进行采样，它并没有理解人类的语言，也不知道自己在说什么。



### 附：基于词嵌入的文本生成

如果要生成中文文本，我们的汉字太多了，逐字符去做我认为不是很好的选择。所以可以考虑基于词嵌入来生成文本。在之前的字符级 LSTM 文本生成的基础上，将编码/解码方式稍作修改、添加 Embedding 层即可实现一个初级的基于词嵌入的文本生成：

```python
import random
import tensorflow as tf
from tensorflow.keras import optimizers
from tensorflow.keras import layers
from tensorflow.keras import models
from tensorflow import keras
import numpy as np

import jieba    # 使用 jieba 做中文分词
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# 导入文本

path = '~/Desktop/txt_zh_cn.txt'
text = open(path).read().lower()
print('Corpus length:', len(text))

# 将文本序列向量化

maxlen = 60     # 每个序列的长度
step = 3        # 每 3 个 token 采样一个新序列
sentences = []  # 保存所提取的序列
next_tokens = []  # sentences 的下一个 token

token_text = list(jieba.cut(text))

tokens = list(set(token_text))
tokens_indices = {token: tokens.index(token) for token in tokens}
print('Number of tokens:', len(tokens))

for i in range(0, len(token_text) - maxlen, step):
    sentences.append(
        list(map(lambda t: tokens_indices[t], token_text[i: i+maxlen])))
    next_tokens.append(tokens_indices[token_text[i+maxlen]])
print('Number of sequences:', len(sentences))

# 将目标 one-hot 编码
next_tokens_one_hot = []
for i in next_tokens:
    y = np.zeros((len(tokens),), dtype=np.bool)
    y[i] = 1
    next_tokens_one_hot.append(y)

# 做成数据集
dataset = tf.data.Dataset.from_tensor_slices((sentences, next_tokens_one_hot))
dataset = dataset.shuffle(buffer_size=4096)
dataset = dataset.batch(128)
dataset = dataset.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)


# 构建、编译模型

model = models.Sequential([
    layers.Embedding(len(tokens), 256),
    layers.LSTM(256),
    layers.Dense(len(tokens), activation='softmax')
])

optimizer = optimizers.RMSprop(lr=0.1)
model.compile(loss='categorical_crossentropy',
              optimizer=optimizer)

# 采样函数

def sample(preds, temperature=1.0):
    '''
    对模型得到的原始概率分布重新加权，并从中抽取一个 token 索引
    '''
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

# 训练模型

callbacks_list = [
    keras.callbacks.ModelCheckpoint(  # 在每轮完成后保存权重
        filepath='text_gen.h5',
        monitor='loss',
        save_best_only=True,
    ),
    keras.callbacks.ReduceLROnPlateau(  # 不再改善时降低学习率
        monitor='loss',
        factor=0.5,
        patience=1,
    ),
    keras.callbacks.EarlyStopping(  # 不再改善时中断训练
        monitor='loss',
        patience=3,
    ),
]

model.fit(dataset, epochs=30, callbacks=callbacks_list)

# 文本生成

start_index = random.randint(0, len(text) - maxlen - 1)
generated_text = text[start_index: start_index + maxlen]
print(f' 📖 Generating with seed: "{generated_text}"')

for temperature in [0.2, 0.5, 1.0, 1.2]:
    print('\n  🌡️ temperature:', temperature)
    print(generated_text, end='')
    for i in range(100):    # 生成 100 个 token
        # 编码当前文本
        text_cut = jieba.cut(generated_text)
        sampled = []
        for i in text_cut:
            if i in tokens_indices:
                sampled.append(tokens_indices[i])
            else:
                sampled.append(0)

        # 预测，采样，生成下一个 token
        preds = model.predict(sampled, verbose=0)[0]
        next_index = sample(preds, temperature)
        next_token = tokens[next_index]
        print(next_token, end='')

        generated_text = generated_text[1:] + next_token

```

我用一些鲁迅的文章去训练，得到的结果大概是这样的：

> 忘却一样，佳作有些这就……在未庄一阵，但游街正是倒不如是几年攻击罢一堆去再的是有怕就准的话是未庄指也添未庄不朽大家９转５，公共未庄他的他了虽然还成了，但豆种他女人是未庄很的窜的寻也的并我—水生是但收正是本但太爷两个要五是几乎太爷终于硬辫子

可以看到，这些句子都说不通，看着很难受。所以我们还可以把分 token 的方法改一改，不是分词，而是去分句子：

```python
text = text.replace('，', ' ，').replace('。', ' 。').replace('？', ' ？').replace('：', ' ：')
token_text = tf.keras.preprocessing.text.text_to_word_sequence(text, split=' ')
```

其他的地方基本不变，这样也可以得到比较有意思的文本。比如这是我用一些余秋雨的文章去训练的结果：

> 几个短衣人物也和他同坐在一处这车立刻走动了，贝壳天气还早，赊了两碗酒没有吃过人的孩子，米要钱买这一点粗浅事情都不知道……天气还早不妨事么他……全屋子都很静这时红鼻子老拱的小曲，而且又破费了二十千的赏钱，他一定须在夜里的十二点钟才回家。

---

By("CDFMLR", "2020-08-20");

