---
title: Python深度学习之机器学习基础
tag:
  - Machine Learning
  - Deep Learning
categories:
  - Machine Learning
  - Deep Learning with Python
---

# Deep Learning with Python

这篇文章是我学习《Deep Learning with Python》(第二版，François Chollet 著) 时写的系列笔记之一。文章的内容是从  Jupyter notebooks 转成 Markdown 的，当我完成所以文章后，会在 GitHub 发布我写的所有  Jupyter notebooks。

你可以在这个网址在线阅读这本书的正版原文(英文)：https://livebook.manning.com/book/deep-learning-with-python

这本书的作者也给出了一套 Jupyter notebooks：https://github.com/fchollet/deep-learning-with-python-notebooks

---

本文为 **第4章 机器学习基础** (Chapter 4. Fundamentals of machine learning) 的笔记整合。

本文目录：

[TOC]

## 机器学习的四个分支

> 4.1 Four branches of machine learning

1. 监督学习
2. 无监督学习
3. 自监督学习
4. 强化学习

## 机器学习模型评估

> 4.2 Evaluating machine-learning models

### 训练集、验证集和测试集

- 训练集：用来学习参数（网络里各节点的权重）；
- 验证集：用来学习超参数（网络的权重，比如层数、层的大小这种）；
- 测试集：用来验证结果，要保证模型从未见过这些数据。

测试集必须是单独分出来的，训练集、测试集中不能和测试集有重合。

最好的做法是，先把所有数据分成训练集和测试集。然后从训练集里分一部分出来做验证集。

以下是几种选择验证集的方法：

#### 简单留出验证 

>SIMPLE HOLD-OUT VALIDATION

就是简单的从训练集里留出一部分来做验证集。

可用的数据多的时候才能用这个。不然数据少了，分出来的验证集就太小，不够一般，效果不好。

![简单留出验证的示意图](https://tva1.sinaimg.cn/large/007S8ZIlgy1ggkhlemz7cj31io0k0n02.jpg)


```python
# Hold-out validation

num_validation_samples = 10000

np.random.shuffle(data)    # 洗牌，打乱数据

validation_data = data[:num_validation_samples]    #定义验证集
data = data[num_validation_samples:]

training_data = data[:]    # 定义训练集

# 在训练集训练模型，在验证集评估
model = get_model()
model.train(training_data)
validation_score = model.evaluate(validation_data)

## 然后这里可以根据结果调整模型，
## 然后重新训练、评估，然后再次调整...

# 在调整好超参数之后，用除了测试集的所有数据来训练最终模型
model = get_model()
model.train(np.concatenate([training_data, validation_data]))

# 用测试集来评估最终模型
test_score = model.evaluate(test_data)
```

#### K折验证

> K-FOLD VALIDATION

这个方法是把数据等分成 K 份。对每个部分 i，在剩下的 K-1 个部分里训练，在 i 上验证评估。最终验证的结果取 K 次的验证值的平均。

这种方法对不同的训练、验证集划分对结果影响比较大时会很有效（比如数据比较少的时候）

![K折验证示意图](https://tva1.sinaimg.cn/large/007S8ZIlgy1ggki8sc8x0j31os0u0q90.jpg)

emmm，我觉得这个图有点问题，应该除了那些灰色的是 Validation，白的应该都是 Training。（中文译本上就是这种）


```python
# K-fold cross-validation

k = 4
num_validation_samples = len(data) // k

np.random.shuffle(data)

validation_scores = []
for fold in range(k):
    # 选择验证集
    validation_data = data[num_validation_samples * fold:
                           num_validation_samples * (fold + 1)]
    # 用剩下的做训练集
    training_data = data[:num_validation_samples * fold] + 
                    data[num_validation_samples * (fold + 1):]
    
    model = get_model()    # 注意是用个全新的模型
    
    model.train(training_data)
    
    validation_score = model.evaluate(validation_data)
    validation_scores.append(validation_score)

# 总的验证值是所有的平均
validation_score = np.average(validation_scores)

# 然后根据结果做各种超参数调整啦

# 最后在除了测试集的所有数据上训练
model = get_model()
model.train(data)
test_score = model.evaluate(test_data)
```

#### 带有打乱数据的重复K折验证 
> ITERATED K-FOLD VALIDATION WITH SHUFFLING

就是重复跑 P 次 K折验证，每次开始前洗牌。

这个是数据比较少，又要求尽可能精确的时候用的。要跑 P*K 次，所以比较耗时。

书上没给这个的代码，就是在 K折 的基础上再加一层循环：


```python
# ITERATED K-FOLD VALIDATION WITH SHUFFLING

p = 10

k = 4
num_validation_samples = len(data) // k

total_validation_scores = []

for i in range(p):
    np.random.shuffle(data)
    
    validation_scores = []
    for fold in range(k):
        # TODO: K折验证的那堆代码
    
    validation_score = np.average(validation_scores)
    total_validation_scores.append(validation_score)
    
# 总的验证值是所有的平均
validation_score = np.average(total_validation_scores)

# 然后根据结果做各种超参数调整啦

# 最后在除了测试集的所有数据上训练
model = get_model()
model.train(data)
test_score = model.evaluate(test_data)
```

### 划分时的注意事项

- **数据代表性**：训练集和测试集都要可以代表所有数据。比如做数字识别，不能训练集里只有 0～7，测试集里全是 8～9。做这种之前要把所有数据随机洗牌打乱，然后再分训练集和测试集。
- **时间箭头**：如果是那种做跟时间有关的预测（给过去的，预测未来的），开始之前**不要打乱数据**，要保持数据的时间顺序（打乱了会时间泄露，就是模型从“未来”学习了），并且测试集的数据要晚于训练集。
- **数据冗余**：如果数据有重复，随机打乱之后，同样的数据就可能同时出现在训练、验证、测试集里了。这种情况会影响结果，训练和验证集不能有交集。


## 数据预处理、特征工程和特征学习

> 4.3 Data preprocessing, feature engineering, and feature learning

### 数据预处理

1. VECTORIZATION 向量化：喂给神经网络的数据都要是浮点数的张量（有时候也可以是整数的），我们要把各种真实的数据，比如文本、图像全变成张量。

2. VALUE NORMALIZATION 值标准化：为了利于训练和结果，我们要让数据符合以下标准：
    - 取值小，一般就 0~1；
    - 同质性，即所有特征的取值范围大致相等；
    

如果严格一点（但不是必须的），我们可以把数据里的特征分别处理成平均值为 0，标准差为 1 的。用 Numpy 搞这个很简单：

```python
# x 是二维的：(samples, features)
x -= x.mean(axis=0)
x /= x.std(axis=0)
```

3. HANDLING MISSING VALUES 缺失值处理：一般来说，只要 0 不是有意义的值，就可以用 0 来代替缺失值。网络可以学会 0 是缺失的这种意思的。还有如果你的测试集是有缺失情况的，但训练集没有，就要手动加些人工数据去让网络学会缺失情况。

### 特征工程

特征工程(feature engineering)，就是在开始训练之前，手动对数据进行处理，得到一种易于机器学习模型从中学习的数据表示。

我们的机器学习模型一般不能从任意的真实数据里面高效地自动学习，所以我们需要特征工程。特征工程的本质就是用更简单的方式表达问题，从而使问题变得更容易解决。

![特征工程示意图](https://tva1.sinaimg.cn/large/007S8ZIlgy1ggkzvwdlyaj30vc0u0jwu.jpg)

特征工程在深度学习之前都至关重要，浅层的学习一般都没有足够的假设空间去自己学习出关键的特征。但现在我们用深度学习可以免去大多数的特征工程了，深度学习可以自己从数据里学出有用的特征来，但是利用特征工程，我们的深度学习过程可以更加优雅、高效。

```java
Clown0te("防盗文爬:)虫的追踪标签，读者不必在意").by(CDFMLR)
```

## 过拟合和欠拟合

> 4.4 Overfitting and underfitting

机器学习里面有一组问题：**优化**（optimization）和**泛化**（generalization）。

优化不足就是欠拟合，泛化无力即为过拟合。

欠拟合就要接着训练，深度学习网络总是可以优化到一定精度的，关键的问题是泛化。处理过拟合用正则化（regularization），以下是几种正则化的手段：

### 增加训练数据

增加训练集的数据，emmmmm，找更多的数据给它看呀，见多识广啊，这就泛化了。

### 减小网络大小

减小层数和层的单元数，即减小总的参数个数（叫做模型的容量，capacity），这样就可以缓解过拟合。

参数越多，记忆容量越大，就是会死记硬背啦，不利于泛化，题目稍变它心态就崩了。但如果参数太少，记忆容量小，它又学不会、记不住知识，会欠拟合（这知识它不进脑子呀）。

我们要在容量过大和过小之间找个平衡，但这个没有万能公式可以套。要自己多做些尝试，用验证集去评估不同的选择，最终选出最好的来。确定这个的一般方法是：从一个相对较小的值开始，逐步增加，直到对结果基本没有影响了。

### 添加权重正则化

和奥卡姆剃刀原理一致，一个简单模型比一个复杂模型更不容易过拟合。这里说的简单模型是指一个参数取值的分布熵更小的模型。

因此，我们可以强制模型权重取较小的值，从而限制模型的复杂度，来降低过拟合。这种使权重值的分布更加规则(regular)的方法叫作权重正则化
(weight regularization)。具体的实现方法是在损失函数中添加与较大权重值相关的成本。

添加这个成本的方法主要有两种：

- L1 regularization：添加与权重系数的绝对值成正比的值（权重的 L1 范数，the L1 norm of the weights）；
- L2 regularization：添加与权重系数的平方值成正比的值（权重的 L2 范数，the L2 norm of the weights），在神经网络中，L2 正则化也叫权重衰减(weight decay)。

在 Keras 里，添加权重正则化可以通过在层里传一个权重正则化实例来实现：

```python
from keras import regularizers

model = models.Sequential()

model.add(layers.Dense(16, kernel_regularizer=regularizers.l2(0.001), 
                       activation='relu', input_shape=(10000,)))
model.add(layers.Dense(16, kernel_regularizer=regularizers.l2(0.001),
                       activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))
```

`regularizers.l2(0.001)` 的意思是在损失函数中添加一项惩罚 `0.001 * weight_coefficient_value`。这个东西只在训练的时候被添加，在用测试集评估的时候不会生效，所以你看到的训练时的损失值要远大于测试时的。

这里也可以把 L2 换成用 L1：`regularizers.l1(0.001)`，或者 L1、L2 同时上：`regularizers.l1_l2(l1=0.001, l2=0.001)`。

### 添加 dropout

对于神经网络的正则化，Dropout 其实才是是最常用、有效的方法。

对某一层使用 dropout，就是在训练过程中随机舍弃一些层输出的特征(就是把值设为 0)。

比如：`[0.2, 0.5, 1.3, 0.8, 1.1]` -> `[0, 0.5, 1.3, 0, 1.1]`，变成 0 的位置是随机的哦。

这里有一个 dropout rate，表示把多少比例的特征置为0，这个比例通常取 0.2~0.5。还有，在测试的时候不 dropout 啊，但测试时的输出要按照 dropout rate 来缩小，以平衡测试和训练时的结果。

也就是说，比如我们搞一个 dropout rate 为 0.5 的，即在训练的时候扔一半：

```python
# training case
layer_output *= np.random.randint(0, high=2, size=layer_output.shape)
```

然后测试的时候，相应的缩小50%：

```python
# testing case
layer_output *= 0.5
```

但通常，我们不是在测试的时候缩小；而是在训练的时候扩大，然后测试的时候就不用动了：

```python
# training case
layer_output *= np.random.randint(0, high=2, size=layer_output.shape)
layer_output /= 0.5
```

![训练时对激活矩阵使用 dropout，并在训练时成比例增大。测试时激活矩阵保持不变](https://tva1.sinaimg.cn/large/007S8ZIlgy1ggl4f43cguj31iy0dc77b.jpg)

在 Keras 里，我们可以通过添加 Dropout 层来实现这个东西：

```python
model.add(layers.Dropout(0.5))
```

例如，我们在我们 IMDB 的网络里面加上 Dropout：

```python
model = models.Sequential()

model.add(layers.Dense(16, activation='relu', input_shape=(10000,)))
model.add(layers.Dropout(0.5))

model.add(layers.Dense(16, activation='relu'))
model.add(layers.Dropout(0.5))

model.add(layers.Dense(1, activation='sigmoid'))
```


## 机器学习的通用工作流程

> 4.5 The universal workflow of machine learning

1. 定义问题，收集数据集：定义问题与要训练的数据。收集这些数据，有需要的话用标签来标注数据。

2. 选择衡量成功的指标：选择衡量问题成功的指标。你要在验证数据上监控哪些指标?

3. 确定评估方法：留出验证? K 折验证?你应该将哪一部分数据用于验证?

4. 准备数据：预处理啦，特征工程啦。。

6. 开发比基准(比如随机预测)更好的模型，即一个具有统计功效的模型。

最后一层和损失的选择：
![最后一层和损失的选择](https://tva1.sinaimg.cn/large/007S8ZIlgy1gglyp8zx9jj31jc0iiq75.jpg)

7. 扩大规模，开发出过拟合的模型：加层、加单元、加轮次

8. 调节超参数，模型正则化：基于模型在验证数据上的性能来进行模型正则化与调节超参数。





