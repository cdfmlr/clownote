---
title: Andrew Ng 机器学习笔记总结
tags: Machine Learning
categories:
  - Machine Learning
  - AndrewNg
date: 2020-01-16 12:39:27
---


# 机器学习

Emmmm，这学期在 Coursera 学完了 Andrew Ng 的 Machine Learning 课程。我对这个课程一向是不以为意的，却不小心报了个名，还手贱申请了个经济援助，学完就可以免费拿证书（卖几百块哒），课程期间还送正版的 Matlab Online，这一系列的偶(占)然(小)事(便)件(宜)促使我开始刷这个课了。越学越觉得，嗯，真香，是真的很香！这个课真的是很好的机器学习入门，难怪那么多人推荐。

Coursera 里课程笔记有每一章的总结，总结的非常好，推荐学完之后看一看。但我还是喜欢自己写自己的，所以我之前边看视频边写了几乎涵盖整个课程的[笔记](https://clownote.github.io/categories/Machine-Learning/AndrewNg/)，其实好多是在抄老师的原话和PPT😂，就当练习打字、英语还有 $\LaTeX$ 了。放假回家在火车上~~百无聊赖~~心血来潮，想到了应该整理一下课程里面学到的东西，就有了这篇文章。

这里我主要是写了各种算法的描述，还从编程作业里提取了算法大概的代码实现，方便日后快速查阅吧。一开始的回归比较简单，所以我写的很少，就堆了点公式（其实是硬卧上铺空调太冷致使我生病了，思路堵塞写不出东西来😷）；后面SVM、推荐系统什么的比较复杂就多写了一些（其实是我掌握的不好，归纳不出重点🤯）。至于课程里老师花大力气讲的关于机器学习系统的设计、优化、debug 还有各种~~奇技淫巧~~ ~~骚操作~~ 实用技巧 以及 Octave 入门哪一块我就一概不提了，这些东西还是要看老师的视频才能体会到精髓（...优(挂)秀(科)的大学生自然是不能承认原因是自己懒惰的😎）。

由于我看课程的时候全程没有开中文字幕，平时查阅的中文资料也比较少，所以好多术语我都不知道要怎么翻译，写这篇文章的时候我大概查了一些自己难以表达的，其他的全靠臆测，我不保证正确。

Emmm，不小心就写了几百字的废话😂下面就开始吧。



## 监督学习

监督学习是给x、y数据去训练的。

![image-20191105144318970](https://tva1.sinaimg.cn/large/006y8mN6gy1g8n5s7zmffj30lv0ca40u.jpg)

### 回归问题

> 做预测，值域为连续的数（例如区间$[0,100]$）

数学模型：

* **预测函数**：
$$
  h_\theta(x)
  =
  \sum_{i=0}^m \theta_ix_i
  =
  \left[\begin{array}{c}\theta_0 & \theta_1 & \ldots & \theta_n\end{array}\right]
  \left[\begin{array}{c}x_0 \\ x_1 \\ \vdots \\ x_n \end{array}\right]
  =
  \theta^TX
$$

* **待求参数**：$\theta=\left[\begin{array}{c}\theta_0 & \theta_1 & \ldots & \theta_n\end{array}\right]$

* **代价函数**：
$$
J(\theta)=\frac{1}{2m}\sum_{i=1}^m(h(x^{(i)})-y^{(i)})^2
  =\frac{(\sum_{i=1}^mh_\theta(X)-Y)^2}{2m}
$$

👉代码实现：

```matlab
  function J = computeCostMulti(X, y, theta)
  %COMPUTECOSTMULTI Compute cost for linear regression with multiple variables
  %   J = COMPUTECOSTMULTI(X, y, theta) computes the cost of using theta as the
  %   parameter for linear regression to fit the data points in X and y
  
  m = length(y); % number of training examples
  
  J = 0;
  
  J = 1 / (2*m) * (X*theta - y)' * (X*theta - y);
  
  % or less vectorizedly: 
  % predictions = X * theta;
  % sqrErrors = (predictions - y) .^ 2;
  % J = 1 / (2*m) * sum(sqrErrors);
  
  end
```

* **优化目标**：找到一组$\theta$使$J$最小。

求解方法：

#### 梯度下降

（这里暂且只讨论 batch gradient descent）

$$
\begin{array}{ll}
\textrm{repeat until convergence } \{ \\
\qquad \theta_j:=\theta_j-\alpha\frac{\partial}{\partial\theta_j}J(\theta)\\
\qquad\quad:= \theta_j - \alpha \frac{1}{m} \sum^m_{i=1}[h_\theta(x^{(i)})-y^{(i)}] \cdot x_j^{(i)}\qquad \textrm{for }j:=0, ..., n \\
\}
\end{array}
$$

向量化表示：$\theta=\theta-\frac{\alpha}{m}X^T(h_\theta(X)-Y)$

👉代码实现：

```matlab
function [theta, J_history] = gradientDescentMulti(X, y, theta, alpha, num_iters)
%GRADIENTDESCENTMULTI Performs gradient descent to learn theta
%   theta = GRADIENTDESCENTMULTI(x, y, theta, alpha, num_iters) updates theta by
%   taking num_iters gradient steps with learning rate alpha

m = length(y); % number of training examples
J_history = zeros(num_iters, 1);

for iter = 1:num_iters

    predictions = X * theta;
    errors = (predictions - y);
    theta = theta - alpha / m * (X' * errors);
    
    % Save the cost J in every iteration    
    J_history(iter) = computeCostMulti(X, y, theta);

end

end
```

#### 正规方程

$$
\theta = (X^TX)^{-1}X^Ty
$$
👉代码实现：

```matlab
function [theta] = normalEqn(X, y)
%NORMALEQN Computes the closed-form solution to linear regression 
%   NORMALEQN(X,y) computes the closed-form solution to linear 
%   regression using the normal equations.

theta = zeros(size(X, 2), 1);

theta = pinv(X' * X) * X' * y;

end
```

这里我们求伪逆以确保正常运行。通常造成$X^TX$不可逆的原因是：

1. 存在可约特征，即给定的某两/多个特征线性相关，只保留一个删除其他即可解决。（e.g. there are the size of house in feet^2 and the size of house in meter^2, where we know that 1 meter = 3.28 feet）
2. 给定特征过多，($m \le n$). 可以删除一些不重要的特征（考虑PCA算法）

#### 梯度下降vs正规方程

| | Gradient Descent           | Normal Equation                                           |
| -- | -------------------------- | --------------------------------------------------------- |
| 需要选择 alpha | ✅            | -                                                         |
| 第三方 | ✅     | -                                                         |
| 时间复杂度     |$O(kn^2)$      | 求$X^TX$的伪逆需要$O(n^3)$ |
| n 相当大时 | 可以工作         | 十分缓慢甚至不可计算                       |

实际上，当 $n>10,000$ 时，我们通常更倾向于使用梯度下降，否则正规方程一般都表现得更好。

#### 注：特征缩放

我们可以通过使输入值大概在一定的范围内来使梯度下降运行更快，比如说，我们可以把所有值变到 $[-1,1]$ 的范围内，同时，我们还可以通过处理让输入值之间的差距不要太大（例如，输入值中同时有 0.000001 和 1 这样差距大的值会影响梯度下降的效率）。

在实践中，我们通常想要保证变量值在 $[-3,-\frac{1}{3}) \cup (+\frac{1}{3}, +3]$ 这个范围内取值。

为达成该目标，我们做如下操作：

1. Feature scaling

$$
\begin{array}{rl}
\textrm{Range:} & s_i = max(x_i)-min(x_i)\\
\textrm{Or Range:} & s_i = \textrm{standard deviation of } x_i\\
\textrm{Scaling:} & x_i:=\frac{x_i}{s_i}
\end{array}
$$

2. Mean normalizaton

$$
\begin{array}{rl}
\textrm{Mean(Average):} & \mu_i = \frac{sum(x_i)}{m}\\
\textrm{normalizing:} & x_i:=x_i-\mu_i
\end{array}
$$

把两个操作和在一起，即：
$$
x_i:=\frac{x_i-\mu_i}{s_i}
$$
其中，$\mu_i$ 是特征(i)的值的平均，$s_i$是值的范围。

👉代码实现：

```matlab
function [X_norm, mu, sigma] = featureNormalize(X)
%FEATURENORMALIZE Normalizes the features in X 
%   FEATURENORMALIZE(X) returns a normalized version of X where
%   the mean value of each feature is 0 and the standard deviation
%   is 1. This is often a good preprocessing step to do when
%   working with learning algorithms.

X_norm = X;
mu = zeros(1, size(X, 2));
sigma = zeros(1, size(X, 2));

mu = mean(X);
sigma = std(X);
X_norm = (X - mu) ./ sigma;

end
```



### 分类问题

> 做预测，值域为离散的几个特定值（例如 0 或 1；0/1/2/3）

#### 逻辑回归

假设函数：
$$
\left\{\begin{array}{l}
h_\theta(x) = g(\theta^Tx)\\
z = \theta^T x\\
g(z) = \frac{1}{1+e^{-z}}\\
\end{array}\right.
$$
其中，$g(z)$ 称为 Simoid 函数，或逻辑函数，其图像如下：

![image-20190917162504420](https://tva1.sinaimg.cn/large/006tNbRwly1gauxvtzb5qj30ur0g8wgd.jpg)

👉代码实现：

```matlab
function g = sigmoid(z)
%SIGMOID Compute sigmoid functoon
%   J = SIGMOID(z) computes the sigmoid of z.

g = 1.0 ./ (1.0 + exp(-z));
end
```


上式可化简得：
$$
h_\theta(x) = \frac{1}{1+e^{-\theta^Tx}}
$$

$h_\theta$ 的输出是预测值为1的可能性，并有下两式成立：
$$
h_\theta(x)=P(y=1 \mid x;\theta)=1-P(y=0 \mid x; \theta)
$$

$$
P(y=0 \mid x;\theta) + P(y=1 \mid x;\theta) = 1
$$

**决策边界**：逻辑回归的决策边界就是将区域分成$y=0$和 $y=1$ 两部分的一个超平面。

决策边界由假设函数决定。这是由于要完成分类，需用$h_\theta$的输出来决定结果是 0 还是 1。定 0.5 为分界，即：
$$
\begin{array}{rcl}
h_\theta(x) \ge 0.5 &\Rightarrow& y=1\\
h_\theta(x) < 0.5 &\Rightarrow& y=0
\end{array}
$$
由 Simoid 函数的性质，上式等价为：
$$
\begin{array}{rcl}
\theta^TX \ge 0 &\Rightarrow& y=1\\
\theta^TX \le 0 &\Rightarrow& y=0\\
\end{array}
$$
那么对于给定的一组 $\theta$，例如$\theta=\left[\begin{array}{c}5\\-1\\0\end{array} \right]$，有 $y=1$ 当且仅当 $5+(-1)x_1+0x_2 \ge 0$，这时决策边界为 $x_1=5$。

![image-20190917173722734](https://tva1.sinaimg.cn/large/006tNbRwly1gauyq6oc10j306e04umx0.jpg)

决策边界也可以是下面这种复杂的情况：

![image-20190917174144868](https://tva1.sinaimg.cn/large/006tNbRwly1gauyt0wbq3j30mv08xwfh.jpg)

**逻辑回归模型**：
$$
\begin{array}{rcl}
\textrm{Training set} &:& \{(x^{(1)},y^{(1)}), (x^{(2)},y^{(2)}), \ldots, (x^{(m)},y^{(m)})\}\\
\\
\textrm{m examples} &:&
x \in \left[\begin{array}{c}
x_0\\x_1\\ \vdots \\ x_n
\end{array}\right] \textrm{where }(x_0=1)
,\quad y \in \{0,1\}\\
\\
\textrm{Hypothesis} &:& h_\theta(x)=\frac{1}{1+e^{-\theta^Tx}}\\\\
\textrm{Cost Function} &:&
J(\theta)=-\frac{1}{m}\sum_{i=1}^m\Bigg[y^{(i)}log\Big(h_\theta(x)\Big)+(1-y^{(i)})log\Big(1-h_\theta(x^{(i)})\Big)\Bigg]
\end{array}
$$
向量化表示：
$$
\begin{array}{l}
h=g(X\theta)\\
J(\theta)=\frac{1}{m}\cdot\big(-y^T log(h) -(1-y)^T log(1-h)\big)
\end{array}
$$
**梯度下降**：
$$
\begin{array}{l}
Repeat \quad \{\\
\qquad \theta_j:=\theta_j-\frac{\alpha}{m}\sum_{i=1}^m(h_\theta(x^{(i)})-y^{(i)})\cdot x_j^{(i)}\\
\}
\end{array}
$$
向量化表示：
$$
\theta:=\theta-\frac{\alpha}{m}X^T(g(X\theta)-\overrightarrow{y})
$$
👉代码实现（使用Advanced Optimization）：

1. 提供$J(\theta), \frac{\partial}{\partial\theta_j}J(\theta)$

```matlab
function [J, grad] = costFunction(theta, X, y)
%COSTFUNCTION Compute cost and gradient for logistic regression
%   J = COSTFUNCTION(theta, X, y) computes the cost of using theta as the
%   parameter for logistic regression and the gradient of the cost
%   w.r.t. to the parameters.

m = length(y); % number of training examples

J = 0;
grad = zeros(size(theta));

h = sigmoid(X*theta);

J = 1/m * (-y'*log(h) - (1-y)'*log(1-h));

grad = 1/m * X'*(h-y);

end
```

2. 调用 Advanced Optimization 函数解决优化问题：

```matlab
options = optimset('GradObj', 'on', 'MaxIter', 100);
initialTheta = zeros(2, 1);

[optTheta, functionVal, exitFlag] = fminunc(@costFunction, initialTheta, options);
```

##### 多元分类

我们采用一系列的单元（逻辑）分类来完成多元分类：
$$
\begin{array}{l}
y \in \{0,1,\cdots,n\}\\\\
h_\theta^{(0)}(x)=P(y=0|x;\theta)\\
h_\theta^{(0)}(x)=P(y=0|x;\theta)\\
\vdots\\
h_\theta^{(0)}(x)=P(y=0|x;\theta)\\\\
prediction = \mathop{max}\limits_{\theta}\big(h_\theta^{(i)}(x)\big)
\end{array}
$$

![img](https://tva1.sinaimg.cn/large/006y8mN6ly1g78nj8fvy4j30d507agmp.jpg)

#### 注：过拟合

![img](https://tva1.sinaimg.cn/large/006y8mN6ly1g7aopbltb1j30f0046dg2.jpg)

过拟合对训练集中的数据预测的很好，但对没见过的新样本预测效果不佳。

解决过拟合的方法有：

1. 减少特征数量（PCA）

2. 正则化：在代价函数中加入 $\theta$ 的权重：

   $\mathop{min}\limits_{\theta} \dfrac{1}{2m}\ \sum_{i=1}^m (h_\theta(x^{(i)}) - y^{(i)})^2 + \lambda\ \sum_{j=1}^n \theta_j^2$

   > 注意，$\theta_0$是我们加上的常数项，不应该被正则化。

   代码实现：

```matlab
   function [J, grad] = lrCostFunction(theta, X, y, lambda)
   %LRCOSTFUNCTION Compute cost and gradient for logistic regression with 
   %regularization
   %   J = LRCOSTFUNCTION(theta, X, y, lambda) computes the cost of using
   %   theta as the parameter for regularized logistic regression and the
   %   gradient of the cost w.r.t. to the parameters. 
   
   m = length(y); % number of training examples
   
   J = 0;
   grad = zeros(size(theta));
   
   % Unregularized cost function & gradient for logistic regression
   h = sigmoid(X * theta);
   J = 1/m * (-y'*log(h) - (1-y)'*log(1-h));
   grad = 1/m * X'*(h-y);
   
   % Regularize
   temp = theta;
   temp(1) = 0;
   J = J + lambda/(2*m) * sum(temp.^2);
   grad = grad + lambda/m * temp;
   
   grad = grad(:);
   
   end
```

#### 神经网络

$$
\left[\begin{array}{c}x_0 \\ x_1 \\ x_2 \\ x_3\end{array}\right]
\rightarrow
\left[\begin{array}{c}a_1^{(2)} \\ a_2^{(2)} \\ a_3^{(2)} \\ \end{array}\right]
\rightarrow
\left[\begin{array}{c}a_1^{(3)} \\ a_2^{(3)} \\ a_3^{(3)} \\ \end{array}\right]
\rightarrow 
h_\theta(x)
$$

第一层是数据集，称为输入层，可以看作 $a^{(0)}$ ；中间是数个隐藏层，最终得到的就是预测函数，这一层叫做输出层。

$$
z^{(j)} = \Theta^{(j-1)}a^{(j-1)}
$$

$$
a^{(j)} = g(z^{(j)})
$$

假设有 c 个层，则:

$$
h_\Theta(x)=a^{(c+1)}=g(z^{(c+1)})
$$

例如，用一层的神经网络，我们可以建立一些表达逻辑函数的神经网络：
$$
\begin{array}{l}AND:\\&\Theta^{(1)} &=\begin{bmatrix}-30 & 20 & 20\end{bmatrix} \\ NOR:\\&\Theta^{(1)} &= \begin{bmatrix}10 & -20 & -20\end{bmatrix} \\ OR:\\&\Theta^{(1)} &= \begin{bmatrix}-10 & 20 & 20\end{bmatrix} \\\end{array}
$$

##### 多元分类

$$
y^{(i)}=\begin{bmatrix}1\\0\\0\\0\end{bmatrix},\begin{bmatrix}0\\1\\0\\0\end{bmatrix},\begin{bmatrix}0\\0\\1\\0\end{bmatrix},\begin{bmatrix}0\\0\\0\\1\end{bmatrix}
$$

$$
\left[\begin{array}{c}x_0 \\ x_1 \\ x_2 \\ x_3\end{array}\right]
\rightarrow
\left[\begin{array}{c}a_1^{(2)} \\ a_2^{(2)} \\ a_3^{(2)} \\ ... \end{array}\right]
\rightarrow
\left[\begin{array}{c}a_1^{(3)} \\ a_2^{(3)} \\ a_3^{(3)} \\ ... \end{array}\right]
\rightarrow 
\cdots
\rightarrow 
\left[\begin{array}{c}h_\Theta(x)_1 \\ h_\Theta(x)_2 \\ h_\Theta(x)_3 \\ h_\Theta(x)_4 \end{array}\right]
$$

##### 神经网络的拟合

| Notation | Represent                              |
| -------- | -------------------------------------- |
| $L$      | 神经网络中的总层数                     |
| $s_l$    | 第$l$层中的节点数（不算偏移单元$a_0$） |
| $K$      | 输出节点数                             |

**代价函数**：
$$
J(\Theta)=-\frac{1}{m}\sum_{i=1}^{m}\sum_{k=1}^{K}\Big[
y_k^{(i)}log\Big(\big(h_\Theta(x^{(i)})\big)_k\Big)+
(1-y_k^{(i)})log\Big(1-\big(h_\Theta(x^{(i)})\big)_k\Big)
\Big]+
\frac{\lambda}{2m}\sum_{l=1}^{L-1}\sum_{i=1}^{s_l}\sum_{j=1}^{s_{l+1}}\Big(\Theta_{j,i}^{(l)}\Big)^2
$$
**向后传播算法**：
$$
\begin{array}{lll}
\textrm{Give training set }{(x^{(1)},y^{(1)}),...,(x^{(m)},y^{(m)})}\\
\textrm{Set }\Delta_{i,j}^{(l)}:=0\textrm{ for each } l,i,j \textrm{ (get a matrix full of zeros)}\\
\mathop{\textrm{For}} \textrm{ training example $t=1$ to $m$}:\\
\qquad a^{(1)}:= x^{(t)}\\
\qquad \textrm{Compute $a^{(l)}$ for $l=2,3,\cdots,L$ by forward propagation}\\
\qquad \textrm{Using $y^{(t)}$ to compute } \delta^{(L)}=a^{(L)}-y^{(t)}\\
\qquad \textrm{Compute } \delta^{(l)}=\big((\Theta^{(l)})^T\delta^{(l+1)}\big).*a^{(l)}.*(1-a^{(l)}) \textrm{ for } \delta^{(L-1)},\delta^{(L-2)},...,\delta^{(2)}\\
\qquad \Delta^{(l)}:=\Delta^{(l)}+\delta^{(l+1)}(a^{(l)})^T\\
\textrm{End For}\\
D_{i,j}^{(l)}:=\frac{1}{m}\Delta_{i,j}^{(l)}\textrm{ if } j=0\\
D_{i,j}^{(l)}:=\frac{1}{m}\big(\Delta_{i,j}^{(l)}+\lambda\Theta_{i,j}^{(l)}\big) \textrm{ if } j\neq 0 \\
\textrm{Get }
\frac{\partial}{\partial\Theta_{i,j}^{(l)}}J(\Theta)=D_{i,j}^{(l)}
\end{array}
$$
注：上式中 $.*$ 代表 Matlab/Octave 中的 element-wise 的乘法。

**向后传播的使用**：

先看几个涉及到的方法：

* 参数展开：为使用优化函数，我们需要把所有的$\Theta$矩阵展开并拼接成一个长向量：

```matlab
thetaVector = [ Theta1(:); Theta2(:); Theta3(:) ];
deltaVector = [ D1(:); D2(:); D3(:) ];
```

在得到优化结果后返回原来的矩阵：

```matlab
Theta1 = reshape(thetaVector(1:110),10,11)
Theta2 = reshape(thetaVector(111:220),10,11)
Theta3 = reshape(thetaVector(221:231),1,11)
```

* 梯度检查：利用 $\frac{\partial}{\partial\Theta_j}J(\Theta) \approx \frac{J(\Theta_1,...,\Theta_j+\epsilon,...,\Theta_n)-J(\Theta_1,...,\Theta_j-\epsilon,...,\Theta_n)}{2\epsilon}$ 取一个小的邻域如 $\epsilon=10^{-4}$，可以检查我们用向后传播求出的梯度是否正确（若正确，有 gradApprox ≈ deltaVector 成立）。代码实现：

```matlab
epsilon = 1e-4;
for i = 1 : n
	thetaPlus = theta;
	thetaPlus(i) += epsilon;
	thetaMinus = theta;
	thetaMinus(i) += epsilon;
	gradApprox(i) = (J(thetaPlus) - J(thetaMinus)) / (2*epsilon);
end
```

* 随即初始化：在开始时，将 $\Theta_{ij}^{(l)}$ 随机初始化，应保证随机值的取值在一个 $[-\epsilon,\epsilon]$ 的范围内（这个 $\epsilon$ 与梯度检查中的无关）。代码实现：

```matlab
# If the dimensions of Theta1 is 10x11, Theta2 is 10x11 and Theta3 is 1x11.

Theta1 = rand(10,11) * (2 * INIT_EPSILON) - INIT_EPSILON;
Theta2 = rand(10,11) * (2 * INIT_EPSILON) - INIT_EPSILON;
Theta3 = rand(1,11) * (2 * INIT_EPSILON) - INIT_EPSILON;
```

将上述技巧与向后传播算法结合，我们就得到了了训练神经网络的方法：

1. 随机初始化
2. 向前传播得到 $h_\Theta(x^{(i)})$ 对任意 $x^{(i)}$
3. 计算代价函数
4. 使用向后传播计算偏导
5. 利用梯度检查验证向后传播是否正确，若没问题则关闭梯度检查功能
6. 使用梯度下降或优化函数得到$\Theta$

👉代码实现：

1. 随机初始化

```matlab
function W = randInitializeWeights(L_in, L_out)
%RANDINITIALIZEWEIGHTS Randomly initialize the weights of a layer with L_in
%incoming connections and L_out outgoing connections
%   W = RANDINITIALIZEWEIGHTS(L_in, L_out) randomly initializes the weights 
%   of a layer with L_in incoming connections and L_out outgoing 
%   connections. 
%
%   Note that W should be set to a matrix of size(L_out, 1 + L_in) as
%   the first column of W handles the "bias" terms
%

W = zeros(L_out, 1 + L_in);

% epsilon_init = 0.12
epsilon_init = sqrt(6 / (L_in + L_out));
W = rand(L_out, 1 + L_in) * (2 * epsilon_init) - epsilon_init;

end
```

2. 计算代价

```matlab
function [J grad] = nnCostFunction(nn_params, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, ...
                                   X, y, lambda)
%NNCOSTFUNCTION Implements the neural network cost function for a two layer
%neural network which performs classification
%   [J grad] = NNCOSTFUNCTON(nn_params, hidden_layer_size, num_labels, ...
%   X, y, lambda) computes the cost and gradient of the neural network. The
%   parameters for the neural network are "unrolled" into the vector
%   nn_params and need to be converted back into the weight matrices. 
% 
%   The returned parameter grad should be a "unrolled" vector of the
%   partial derivatives of the neural network.
%

% Reshape nn_params back into the parameters Theta_1 and Theta_2, the weight matrices
% for our 2 layer neural network
Theta_1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
                 hidden_layer_size, (input_layer_size + 1));

Theta_2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
                 num_labels, (hidden_layer_size + 1));

% Setup some useful variables
m = size(X, 1);
K = num_labels;

J = 0;
Theta_1_grad = zeros(size(Theta_1));
Theta_2_grad = zeros(size(Theta_2));

% y(5000x1) -> Y(5000x10)
Y = zeros(m, K);
for i = 1 : m
    Y(i, y(i)) = 1;
end

% Feedforward
a_1 = X;
a_1_bias = [ones(m, 1), a_1];

z_2 = a_1_bias * Theta_1';
a_2 = sigmoid(z_2);
a_2_bias = [ones(m, 1), a_2];

z_3 = a_2_bias * Theta_2';
a_3 = sigmoid(z_3);
h = a_3;

% Cost Function
% for i = 1 : K
%     yK = Y(:, i);
%     hK = h(:, i);
%     J += 1/m * (-yK'*log(hK) - (1-yK)'*log(1-hK));

% J can be get by element-wise compute more elegantly.
J = 1/m * sum(sum((-Y.*log(h) - (1-Y).*log(1-h))));

% Regularize
J = J + lambda/(2*m) * (sum(sum(Theta_1(:, 2:end).^2)) + sum(sum(Theta_2(:, 2:end).^2)));

% Backpropagation

delta_3 = a_3 .- Y;
delta_2 = (delta_3 * Theta_2) .* sigmoidGradient([ones(m, 1), z_2]);
% sigmoidGradient: return g = sigmoid(z) .* (1 - sigmoid(z));
delta_2 = delta_2(:, 2:end);

Delta_1 = delta_2' * a_1_bias;
Delta_2 = delta_3' * a_2_bias;

Theta_1_grad = Delta_1 ./ m + lambda/m * [zeros(size(Theta_1, 1), 1), Theta_1(:, 2:end)];
Theta_2_grad = Delta_2 ./ m + lambda/m * [zeros(size(Theta_2, 1), 1), Theta_2(:, 2:end)];

% Unroll gradients
grad = [Theta_1_grad(:) ; Theta_2_grad(:)];

end
```

3. 预测

```matlab
function p = predict(Theta1, Theta2, X)
%PREDICT Predict the label of an input given a trained neural network
%   p = PREDICT(Theta1, Theta2, X) outputs the predicted label of X given the
%   trained weights of a neural network (Theta1, Theta2)

% Useful values
m = size(X, 1);
num_labels = size(Theta2, 1);

p = zeros(size(X, 1), 1);

h1 = sigmoid([ones(m, 1) X] * Theta1');
h2 = sigmoid([ones(m, 1) h1] * Theta2');
[dummy, p] = max(h2, [], 2);

end
```

4. 驱动

```matlab
input_layer_size  = 400;  % 20x20 Input Images of Digits
hidden_layer_size = 25;   % 25 hidden units
num_labels = 10;          % 10 labels, from 1 to 10   
                          % (note that we have mapped "0" to label 10)

fprintf('\nInitializing Neural Network Parameters ...\n')

load('Xy.mat');

fprintf('\nTraining Neural Network... \n')

%  value to see how more training helps.
options = optimset('MaxIter', 1000);

lambda = 1;

% Create "short hand" for the cost function to be minimized
costFunction = @(p) nnCostFunction(p, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, X, y, lambda);

% Now, costFunction is a function that takes in only one argument (the
% neural network parameters)
[nn_params, cost] = fmincg(costFunction, initial_nn_params, options);

% Obtain Theta1 and Theta2 back from nn_params
Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
                 hidden_layer_size, (input_layer_size + 1));

Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
                 num_labels, (hidden_layer_size + 1));

pred = predict(Theta1, Theta2, X);

fprintf('\nTraining Set Accuracy: %f\n', mean(double(pred == y)) * 100);
```

#### 支持向量机

优化目标：
$$
\min_\theta 
C\sum_{i=1}^m \large[ y^{(i)} \mathop{\textrm{cost}_1}(\theta^Tx^{(i)})
+ (1 - y^{(i)})\ \mathop{\textrm{cost}_0}(\theta^Tx^{(i)})\large]
+ \frac{1}{2}\sum_{j=1}^n \theta_j^2
$$
当 $C$ 值比较大时，这个优化目标会选择将第一个求和项趋于零，这样优化目标就变成了：
$$
\begin{array}{l}
	\min_\theta \frac{1}{2}\sum_{j=1}^{n}\theta_j^2\\\\
	s.t. \quad \begin{array}{l}
		\theta^Tx^{(i)} \ge 1 & \textrm{if } y^{(i)}=1\\
		\theta^Tx^{(i)} \le -1 & \textrm{if } y^{(i)}=0
	\end{array}
\end{array}
$$
由欧氏空间的知识：
$$
\begin{array}{ccl}
||u|| &=& \textrm{length of vector } u= \sqrt{u_1^2+u_2^2}\\
p &=& \textrm{length of projection of } v \textrm{ onto } u \textrm{ (signed)} \\ \\
u^Tv &=& p \cdot ||u||
\end{array}
$$
上式可表示为：
$$
\begin{array}{l}
	\min_\theta \frac{1}{2}\sum_{j=1}^{n}\theta_j^2
	=\frac{1}{2}\Big(\sqrt{\sum_{j=1}^n\theta_j^2}\Big)^2
	=\frac{1}{2}||\theta||^2 \\\\
	s.t. \quad \begin{array}{l}
		p^{(i)}\cdot ||\theta|| \ge 1 & \textrm{if } y^{(i)}=1\\
		p^{(i)}\cdot ||\theta|| \le -1 & \textrm{if } y^{(i)}=0
	\end{array}\\\\
	\textrm{where $p^{(i)}$ is the projection of $x^{(i)}$ onto the vector $\theta$.}
\end{array}
$$
SVM 会选择最大的间隙：

![屏幕快照 2019-10-31 12.58.43](https://tva1.sinaimg.cn/large/006tNbRwgy1gax9ziqe3sj324i0nu0z9.jpg)

##### 核方法

面对如下分类问题：

![image-20191102114127170](https://tva1.sinaimg.cn/large/006tNbRwgy1gaxa3eq7zuj30c5083gm3.jpg)

我们可以使用多项式来回归，例如，当 $\theta_0+\theta_1x_1+\theta_2x_2+\theta_3x_1x_2+\theta_4x_1^2+\theta_5x_2^2+\cdots\ge 0$ 时预测 $y=1$；

这样有太多多项式比较麻烦，我们可以考虑如下方法：
$$
\begin{array}{lcl}
\textrm{Predict } y=1 &\textrm{if}&\theta_0+\theta_1f_1+\theta_2f_2+\theta_3f_3+\cdots\ge 0
\end{array}
$$
这里的 $f_1=x_1,f_2=x_2,f_3=x_1x_2,f_4=x_1^2,...$

我们用 $f_i$ 替换了多项式，避免了高次项的麻烦，那么如何确定 $f_i$？大概的思想如下：

![image-20191102124615797](https://tva1.sinaimg.cn/large/006y8mN6ly1g8jljliww8j30o90dmwjt.jpg)

为方便描述，假设我们只有 $x_0,x_1,x_2$，并且只打算构造 $f_1,f_2,f_3$。那么，不管 $x_0$（偏移项），我们从 $x_1$-$x_2$ 的图像中选择 3 个点，记为 $l^{(1)},l^{(2)},l^{(3)}$，称之为*标记点*。任给 $x$，我们通过计算其与各标记点的临近程度得到一组 $f_i$：
$$
f_i = \mathop{\textrm{similarity}}(x,l^{(i)}) = \exp(-\frac{||x-l^{(i)}||^2}{2\sigma^2}) = \exp(-\frac{\sum_{j=1}^n(x_j-l_j^{(i)})^2}{2\sigma^2})
$$
这里具体的 similarity 函数称为*核函数*，核函数多种多样。我们这里写的是很常用的 $\exp(-\frac{\sum_{j=1}^n(x_j-l_j^{(i)})^2}{2\sigma^2})$ ，称为 Gaussian Kernel，他的代码实现如下：

由这种方法，我们知道，给定 $x$，对每个 $l^{(i)}$ 我们会得到一个 $f_i$，满足：

1. 当 $x$ 接近 $l^{(i)}$ 时

$$
f_i \approx \lim_{x\to l^{(i)}}\exp(-\frac{||x-l^{(i)}||^2}{2\sigma^2}) = \exp(-\frac{0^2}{2\sigma^2}) = 1
$$

2. 当 $x$ 远离 $l^{(i)}$ 时

$$
f_i \approx \lim_{||x-l^{(i)}||\to +\infin}\exp(-\frac{||x-l^{(i)}||^2}{2\sigma^2}) = \exp(-\frac{\infin^2}{2\sigma^2}) = 0
$$

$\sigma$ 的选择会影响 $f_i$ 值随 $x$ 远离 $l^{(i)}$ 而下降的速度，$\sigma^2$ 越大，$f_i$减小地越慢：

![image-20191102132852867](https://tva1.sinaimg.cn/large/006y8mN6ly1g8jmrwo86pj30ph0dwwm1.jpg)

使用核方法，我们可以做出这种预测：

![image-20191102133600603](https://tva1.sinaimg.cn/large/006y8mN6ly1g8jmzc2qq4j30ot0ditej.jpg)

当且仅当给定$x$临近$l^{(1)}$ 或 $l^{(2)}$ 时预测 1，否则预测 0.

##### SVM 中使用核

1. 给定训练集 $(x^{(1)},y^{(1)}),(x^{(2)},y^{(2)}),...,(x^{(m)},y^{(m)})$

2. 选择标记点：$l^{(i)}=x^{(i)} \quad \textrm{for }i=1,2,\cdots,m$

3. 对于样本 $x$，计算核：$f_i=\mathop{\textrm{similarity}}(x,l^{(i)}) \quad \textrm{for }i=1,2,\cdots,m$

4. 令 $f=[f_0,f_1,f_2,\cdots,f_m]^T$，其中 $f_0 \equiv 1$。

预测：
   * 给定 $x$，计算 $f\in\R^{m+1}$
   * 预测 $y=1$ 如果 $\theta^Tf=\theta_0f_0+\theta_1f_1+\cdots\ge 0$

训练：
$$
\min_\theta 
C\sum_{i=1}^m \large[ y^{(i)} \mathop{\textrm{cost}_1}(\theta^Tf^{(i)})
+ (1 - y^{(i)})\ \mathop{\textrm{cost}_0}(\theta^Tf^{(i)})\large]
+ \frac{1}{2}\sum_{j=1}^n \theta_j^2
$$
实现：

我们可以利用诸如 liblinear, libsvm 之类的库来得到 SVM 的 参数 $\theta$，要使用这些库，我们一般需要做以下工作：

* 选择参数 $C$
* 选择核函数
  * **No kernel**（即线性核，亦即做逻辑回归：Predict $y=1$ if $\theta^Tx\ge0$），适用于 **n大 m小** 的情况（避免过拟合）
  * **Gaussian kernel**（$f_i=\exp(-\frac{||x-l^{(i)}||^2}{2\sigma^2})\textrm{ where } l^{(i)}=x^{(i)} \textrm{ for } i=1,\cdots,m$）适用于 **m大 n小** 的情况（可拟合更复杂的非线性边界）
* 提供核函数（Gaussian kernel 为例）：

$$
\begin{array}{l}
\textrm{function f = kernel(x1, x2)}\\
\qquad \textrm{f} = \exp(-\frac{||\textrm{x1}-\textrm{x2}||^2}{2\sigma^2})\\
\textrm{return}
\end{array}
$$

注意：使用 Gaussian Kernel 前务必做特征缩放！

👉无核函数的代码实现：

```matlab
function sim = linearKernel(x1, x2)
%LINEARKERNEL returns a linear kernel between x1 and x2
%   sim = linearKernel(x1, x2) returns a linear kernel between x1 and x2
%   and returns the value in sim

% Ensure that x1 and x2 are column vectors
x1 = x1(:); x2 = x2(:);

% Compute the kernel
sim = x1' * x2;  % dot product

end
```

👉高斯核的代码实现：

```matlab
function sim = gaussianKernel(x1, x2, sigma)
%RBFKERNEL returns a radial basis function kernel between x1 and x2
%   sim = gaussianKernel(x1, x2) returns a gaussian kernel between x1 and x2
%   and returns the value in sim

% Ensure that x1 and x2 are column vectors
x1 = x1(:); x2 = x2(:);

sim = 0;

sim = exp(-sum((x1 - x2).^2) / (2 * sigma ^ 2));

end
```

👉SVM 示例：

```matlab
% Load X, y, Xtest and ytest
load('data.mat');

% SVM Parameters
C = 1;         % C = 1 ~ 100 is fine
sigma = 0.1;    % sigma = 0.03 ~ 0.1 gives somewhat good boundary, less is better

% We set the tolerance and max_passes lower here so that the code will run
% faster. However, in practice, you will want to run the training to
% convergence.
model= svmTrain(X, y, C, @(x1, x2) gaussianKernel(x1, x2, sigma)); 
p = svmPredict(model, Xtest);

fprintf('Test Accuracy: %f\n', mean(double(p == ytest)) * 100);
```

##### 多元分类

![image-20191102171432072](https://tva1.sinaimg.cn/large/006y8mN6ly1g8jul8myufj30mv0cz0xu.jpg)

#### 逻辑回归 vs 神经网络 vs SVM

$n$ = 特征数（$x\in\R^{n+1}$）

$m$ = 训练样本数

* n相对于m大 （e.g. $n=10,000, m=10 \sim 1000$）
  * 逻辑回归，或 无核SVM
* n小、m适中（e.g. $n=1\sim1000,m=50,000$）
  * 用 Gaussian 核 SVM
* n小、m大
  * 创造/添加特征，然后用 逻辑回归或无核SVM

神经网络通常可以解决上述任何一种情况，但可能相对较慢。



## 无监督学习

无监督学习是只给x数据的，不给y。

![屏幕快照 2019-11-05 14.49.05](https://tva1.sinaimg.cn/large/006y8mN6gy1g8n62mi54pj30lw0catay.jpg)

### K-Means 聚类

> 把一堆东西自动分成K堆。

输入：

* $K$：聚类的个数
* $\{x^{(1)},x^{(2)},\cdots,x^{(m)}\}$：训练集

输出：

* $K$ 个类

K-Means算法：
$$
\begin{array}{l}

\textrm{Randomly initialize $K$ cluster centroids $\mu_1, \mu_2,...\mu_k \in \R^n$}\\
\textrm{Repeat }\{\\
\qquad \textrm{for $i=1$ to $m$:}\qquad\textrm{// Cluster assignment step}\\
\qquad\qquad c^{(i)} := k \ \textrm{ s.t. } \min_k||x^{(i)}-\mu_k||^2 \\
\qquad \textrm{for $k=1$ to $K$:}\qquad\textrm{// Move centroid step}\\
\qquad\qquad \mu_k:= \textrm{average (mean) of points assigned to cluster $k$}\\
\}\\

\end{array}
$$
代价函数：
$$
J(c^{(1)},\cdots,c^{(m)},\mu_1,\cdots,\mu_K)=\frac{1}{m}\sum_{i=1}^{m}||x^{(i)}-\mu_{c^{(i)}}||^2
$$
优化目标：
$$
\min_{
\begin{array}{c}
	{1}c^{(1)},\cdots,c^{(m)},\\
	\mu_1,\cdots,\mu_K
\end{array}}
J(c^{(1)},\cdots,c^{(m)},\mu_1,\cdots,\mu_K)
$$
得到较优解(不一定能得到最优解)的算法：
$$
\begin{array}{l}
\textrm{For $i=1$ to $100$ <or 50~1000> \{}\\
\qquad\textrm{Randomly initialize K-means.}\\
\qquad\textrm{Run K-means. Get $c^{(1)},\cdots,c^{(m)},\mu_1,\cdots,\mu_k$}\\
\qquad\textrm{Compute cost function (distortion):}\\
\qquad\qquad J(c^{(1)},\cdots,c^{(m)},\mu_1,\cdots,\mu_K)\\
\textrm{\}}\\
\textrm{pick clustering that gave lowest $J$.}
\end{array}
$$
$K$的选择：

1. 更具实际问题的需求易得；
2. 选择拐点：![image-20191106171612460](https://tva1.sinaimg.cn/large/006tNbRwgy1gaxja4d68ej30cb0c3jro.jpg)

👉**代码实现**

1. 找最近的类中心：

```matlab
function idx = findClosestCentroids(X, centroids)
%FINDCLOSESTCENTROIDS computes the centroid memberships for every example
%   idx = FINDCLOSESTCENTROIDS (X, centroids) returns the closest centroids
%   in idx for a dataset X where each row is a single example. idx = m x 1 
%   vector of centroid assignments (i.e. each entry in range [1..K])
%

% Set K
K = size(centroids, 1);

idx = zeros(size(X,1), 1);

for i = 1 : size(X, 1)
    min_j = 0;
    min_l = Inf;
    for j = 1 : size(centroids, 1)
        l = sum((X(i, :) - centroids(j, :)) .^ 2);
        if l <= min_l
            min_j = j;
            min_l = l;
        end
    end
    idx(i) = min_j;
end

end
```

2. 计算中心:

```matlab
function centroids = computeCentroids(X, idx, K)
%COMPUTECENTROIDS returns the new centroids by computing the means of the 
%data points assigned to each centroid.
%   centroids = COMPUTECENTROIDS(X, idx, K) returns the new centroids by 
%   computing the means of the data points assigned to each centroid. It is
%   given a dataset X where each row is a single data point, a vector
%   idx of centroid assignments (i.e. each entry in range [1..K]) for each
%   example, and K, the number of centroids. You should return a matrix
%   centroids, where each row of centroids is the mean of the data points
%   assigned to it.
%

% Useful variables
[m n] = size(X);

centroids = zeros(K, n);

for i = 1 : K
    ck = find(idx == i);
    centroids(i, :) = sum(X(ck,:)) / size(ck, 1);
end

end
```

3. 运行K-Means

```matlab
function [centroids, idx] = runkMeans(X, initial_centroids, ...
                                      max_iters, plot_progress)
%RUNKMEANS runs the K-Means algorithm on data matrix X, where each row of X
%is a single example
%   [centroids, idx] = RUNKMEANS(X, initial_centroids, max_iters, ...
%   plot_progress) runs the K-Means algorithm on data matrix X, where each 
%   row of X is a single example. It uses initial_centroids used as the
%   initial centroids. max_iters specifies the total number of interactions 
%   of K-Means to execute. plot_progress is a true/false flag that 
%   indicates if the function should also plot its progress as the 
%   learning happens. This is set to false by default. runkMeans returns 
%   centroids, a Kxn matrix of the computed centroids and idx, a m x 1 
%   vector of centroid assignments (i.e. each entry in range [1..K])
% 若使用 plot_progress 需要额外的画图函数实现，这里没有给出.
%

% Set default value for plot progress
if ~exist('plot_progress', 'var') || isempty(plot_progress)
    plot_progress = false;
end

% Plot the data if we are plotting progress
if plot_progress
    figure;
    hold on;
end

% Initialize values
[m n] = size(X);
K = size(initial_centroids, 1);
centroids = initial_centroids;
previous_centroids = centroids;
idx = zeros(m, 1);

% Run K-Means
for i=1:max_iters
    
    % Output progress
    fprintf('K-Means iteration %d/%d...\n', i, max_iters);
    if exist('OCTAVE_VERSION')
        fflush(stdout);
    end
    
    % For each example in X, assign it to the closest centroid
    idx = findClosestCentroids(X, centroids);
    
    % Optionally, plot progress here
    if plot_progress
        plotProgresskMeans(X, centroids, previous_centroids, idx, K, i);
        previous_centroids = centroids;
        fprintf('Press enter to continue.\n');
        input("...");
    end
    
    % Given the memberships, compute new centroids
    centroids = computeCentroids(X, idx, K);
end

% Hold off if we are plotting progress
if plot_progress
    hold off;
end

end
```

4. 驱动脚本：

```matlab
% Load an example dataset
load('data.mat');

% Settings for running K-Means
K = 3;
max_iters = 10;

% For consistency, here we set centroids to specific values
% but in practice you want to generate them automatically, such as by
% settings them to be random examples (as can be seen in
% kMeansInitCentroids).
initial_centroids = [3 3; 6 2; 8 5];

% Run K-Means algorithm. The 'true' at the end tells our function to plot
% the progress of K-Means
[centroids, idx] = runkMeans(X, initial_centroids, max_iters, true);
fprintf('\nK-Means Done.\n\n');
```

### PCA 维数约减

> 主成分分析：把n维的数据(投影)降到k维，略去不重要的部分(k<=n)。

**PCA算法**：

1) 数据预处理

   训练集：$x^{(1)},x^{(2)},\cdots,x^{(m)}$

   预处理(feature scaling & mean normalization):

   - $\mu_j=\frac{1}{m}\sum_{i=1}^m x_j^{(i)},\qquad s_j=\textrm{standard deviation of feature }j$

   - Replace each $x_j^{(i)}$ with $\frac{x_j-\mu_j}{s_j}$

2)降维

   1. 计算协方差矩阵$\Sigma$（这个矩阵记做大Sigma，注意和求和号区分）：
$$
\Sigma = \frac{1}{m}\sum_{i=1}^n(x^{(i)})(x^{(i)})^T
$$
   2. 求$\Sigma$的特征值(实际上是奇异值分解)：`[U, S, V] = svd(Sigma);`
   3. 从上一步svd得到:
$$
   U = \left[\begin{array}{cccc}
   | & | &  & |\\
   u^{(1)} & u^{(2)} & \cdots & u^{(n)}\\
   | & | &  & |
   \end{array}\right]
   \in \R^{n\times n}
   \Rightarrow 
   U_{reduce}=\left[\begin{array}{cccc}
   | & | &  & |\\
   u^{(1)} & u^{(2)} & \cdots & u^{(k)}\\
   | & | &  & |
   \end{array}\right]
$$
   4. 完成降维：$x\in\R^n\to z\in\R^k$:
$$
   z = U_{reduce}^Tx
   =\left[\begin{array}{ccc}
   -- & (u^{(1)})^T & --\\
    & \vdots & \\ 
   -- & (u^{(k)})^T & --\\
   \end{array}\right]x
$$

👉代码实现：

```matlab
% do feature scaling & mean normalization

Sigma = 1/m * X' * X;
[U, S, V] = svd(Sigma);

Ureduce = U(:, 1:K);
Z = X * Ureduce;
```

**数据复原**：将数据还原到原来的维度（$z\in\R^k \to x_{approx}\in\R^n$）：
$$
x_{approx}=U_{reduce}z
$$
一般情况下 $x \neq x_{approx}$，我们只能期望 $x_{approx}$ 尽量接近 $x$. 

![image-20191110215011122](https://tva1.sinaimg.cn/large/006y8mN6gy1g8ta88gafkj30oz0djaeo.jpg)

**$k$(主成分个数)的选择**

一般，选择 $k$ 为使得下式成立的最小值：
$$
\frac{\frac{1}{m}\sum_{i=1}^m||x^{(i)}-x_{approx}^{(i)}||^2}{\frac{1}{m}\sum_{i=1}^{m}||x^{(i)}||^2}\le0.01
$$
算法：
$$
\begin{array}{l}
\textrm{Try PCA with } k=1,\cdots,n:\\
\quad \textrm{Compute } U_{reduce},z^{(1)},\cdots,z^{(m)},x_{approx}^{(1)},\cdots,x_{approx}^{m}\\
\quad \textrm{Check if } \frac{\frac{1}{m}\sum_{i=1}^m||x^{(i)}-x_{approx}^{(i)}||^2}{\frac{1}{m}\sum_{i=1}^{m}||x^{(i)}||^2}\le0.01
\end{array}
$$

### 异常检测

> 从一堆数据中找出异常于其他的。

问题描述：给定数据集 $\{x^{(1)},x^{(2)},\cdots,x^{(m)}\}$，通过训练，判断 $x_{test}$ 是否异常。

要解决这个问题，我们可以对$p(x)$（概率）建立一个模型，选择一个临界值 $\epsilon$，使：
$$
\begin{array}{l}
p(x_{test})<\epsilon \Rightarrow \textrm{anomaly}\\
p(x_{test})\ge\epsilon \Rightarrow \textrm{OK}
\end{array}
$$
这样问题可以转化为*密度值估计*。我们常用高斯分布解决这个问题。

#### 高斯分布

$x$ 服从高斯分布：$x \sim \mathcal{N}(\mu,\sigma^2)$

则，$x$ 的概率为：
$$
p(x) = \frac{1}{\sqrt{2\pi}\sigma}\exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)
$$
其中参数 $\mu$ 和 $\sigma$ 由下式确定（这是在机器学习里常用的格式，不一定和数学里的一样）：
$$
\mu=\frac{1}{m}\sum_{i=1}^{m}x^{(i)}
$$

$$
\sigma^2=\frac{1}{m}\sum_{i=1}^{m}\left(x^{(i)}-\mu\right)^2
$$

👉代码实现：

```matlab
function [mu sigma2] = estimateGaussian(X)
%ESTIMATEGAUSSIAN This function estimates the parameters of a 
%Gaussian distribution using the data in X
%   [mu sigma2] = estimateGaussian(X), 
%   The input X is the dataset with each n-dimensional data point in one row
%   The output is an n-dimensional vector mu, the mean of the data set
%   and the variances sigma^2, an n x 1 vector
% 

% Useful variables
[m, n] = size(X);

mu = zeros(n, 1);
sigma2 = zeros(n, 1);

mu = mean(X);
sigma2 = var(X) * (m - 1) / m;

end
```



借此我们便可得到异常检查算法：

##### 异常检查算法

1. 选择认为可能表现出样本异常的数据特征 $x_i$
2. 计算参数 $\mu_1,\cdots,\mu_n,\sigma_1^2,\cdots,\sigma_n^2$ 

$$
\mu=\frac{1}{m}\sum_{i=1}^{m}x^{(i)}
$$

$$
\sigma^2=\frac{1}{m}\sum_{i=1}^{m}\left(x^{(i)}-\mu\right)^2
$$

3. 对于新给的样本 $x$，计算 $p(x)$：

$$
p(x)=\prod_{j=1}^{n}p(x_j;\mu_j,\sigma_j^2)=\prod_{j=1}^{n}\frac{1}{\sqrt{2\pi}\sigma_j}\exp\left(-\frac{(x_j-\mu_j)^2}{2\sigma_j^2}\right)
$$

4. 如果$p(x)<\epsilon$，则预测异常。

#### 多元高斯分布

$$
p(x;\mu,\Sigma)=\frac
{\exp\left(-\frac{1}{2}(x-\mu)^T\Sigma^{-1}(x-\mu)\right)}
{\sqrt{(2\pi)^{n}|\Sigma|}}
$$

参数：

* $\mu\in\R^n$
* $\Sigma\in\R^{n\times n}$ (covariance matrix, `Sigma = 1/m * X' * X;`)

参数的计算：
$$
\mu=\frac{1}{m}\sum_{i=1}^mx^{(i)} \qquad
\Sigma=\frac{1}{m}\sum_{i=1}^m\left(x^{(i)}-\mu\right)\left(x^{(i)}-\mu\right)^T
$$

👉代码实现：

```matlab
function p = multivariateGaussian(X, mu, Sigma2)
%MULTIVARIATEGAUSSIAN Computes the probability density function of the
%multivariate gaussian distribution.
%    p = MULTIVARIATEGAUSSIAN(X, mu, Sigma2) Computes the probability 
%    density function of the examples X under the multivariate gaussian 
%    distribution with parameters mu and Sigma2. If Sigma2 is a matrix, it is
%    treated as the covariance matrix. If Sigma2 is a vector, it is treated
%    as the \sigma^2 values of the variances in each dimension (a diagonal
%    covariance matrix)
%

k = length(mu);

if (size(Sigma2, 2) == 1) || (size(Sigma2, 1) == 1)
    Sigma2 = diag(Sigma2);
end

X = bsxfun(@minus, X, mu(:)');
p = (2 * pi) ^ (- k / 2) * det(Sigma2) ^ (-0.5) * ...
    exp(-0.5 * sum(bsxfun(@times, X * pinv(Sigma2), X), 2));

end
```

##### 用多元高斯分布的异常检查

1. 拟合多元高斯分布的 $p(x)$ 模型，通过参数：

$$
\mu=\frac{1}{m}\sum_{i=1}^mx^{(i)} \qquad
\Sigma=\frac{1}{m}\sum_{i=1}^m\left(x^{(i)}-\mu\right)\left(x^{(i)}-\mu\right)^T
$$

2. 对于新给 $x$，计算：

$$
p(x)=\frac
{\exp\left(-\frac{1}{2}(x-\mu)^T\Sigma^{-1}(x-\mu)\right)}
{\sqrt{(2\pi)^{n}|\Sigma|}}
$$

3. 如果$p(x)<\epsilon$，则预测异常。

#### 门槛选择

通过计算 $F_1$ 值可以得到最适合的 $\epsilon$。

$F_1$ 值由 precision ($prec$) 和 recall ($rec$) 给出：
$$
F_1=\frac{2\cdot prec \cdot rec}{prec+rec}
$$
其中：
$$
prec = \frac{tp}{tp+fp}
$$

$$
rec = \frac{tp}{tp+fn}
$$

* $tp$ 是 true positives：预测为正，实际也为正
* $fp$ 是 false positives：预测为正，实际为负
* $fn$ 是 false negatives：预测为负，实际为正

![image-20191026152903469](https://tva1.sinaimg.cn/large/006y8mN6ly1g8bmwqbebxj30po0dgahc.jpg)

👉代码实现：

```matlab
function [bestEpsilon bestF1] = selectThreshold(yval, pval)
%SELECTTHRESHOLD Find the best threshold (epsilon) to use for selecting
%outliers
%   [bestEpsilon bestF1] = SELECTTHRESHOLD(yval, pval) finds the best
%   threshold to use for selecting outliers based on the results from a
%   validation set (pval) and the ground truth (yval).
%

bestEpsilon = 0;
bestF1 = 0;
F1 = 0;

stepsize = (max(pval) - min(pval)) / 1000;
for epsilon = min(pval):stepsize:max(pval)

    cvPredictions = pval < epsilon;
    
    tp = sum((cvPredictions == 1) & (yval == 1));
    fp = sum((cvPredictions == 1) & (yval == 0));
    fn = sum((cvPredictions == 0) & (yval == 1));

    prec = tp / (tp + fp);
    rec = tp / (tp + fn);

    F1 = (2 * prec * rec) / (prec + rec);

    if F1 > bestF1
       bestF1 = F1;
       bestEpsilon = epsilon;
    end
end

end
```



### 推荐系统

> 通过评分，推荐用户新内容。

符号说明：（假设我们要推荐的东西是电影）

- $n_u$ = 用户数
- $n_m$ = 电影数
- $r(i,j)=1$ 若用户 $j$ 对电影 $i$ 评过分，否则为 0
- $y^{(i,j)}$ = 用户 $j$ 给电影 $i$ 的评分(只有当 $r(i,j)=1$ 时才有定义)

#### 基于内容推荐

**预测模型**：

![屏幕快照 2019-11-26 16.04.26](https://tva1.sinaimg.cn/large/006y8mN6gy1g9bi5bv4etj30nz06lac1.jpg)

* $r(i,j)=1$ 若用户 $j$ 对电影 $i$ 评过分
* $y^{(i,j)}$ = 用户 $j$ 给电影 $i$ 的评分(如果有定义)
* $\theta^{(j)}$ 用户 $j$ 的参数（向量）
* $x^{(i)}$ 电影 $i$ 的特征（向量）

对于用户 $j$，电影 $i$，预测评分：$(\theta^{(j)})^T(x^{(i)})$。

**优化目标**：

1. 优化 $\theta^{(j)}$ （对于单个用户 $j$ 的参数）

$$
\min_{\theta^{(j)}}\sum_{i:r(i,j)=1}\left((\theta^{(j)})^Tx^{(i)}-y^{(i,j)}\right)^2+\frac{\lambda}{2}\sum_{k=1}^n \left(\theta_k^{(j)}\right)^2
$$

2. 优化 $\theta^{(1)},\theta^{(2)},\cdots,\theta^{(n_u)}$（对所有用户）

$$
\min_{\theta^{(1)},\cdots,\theta^{(n_u)}}
\sum_{j=1}^{n_u}\sum_{i:r(i,j)=1}\left((\theta^{(j)})^Tx^{(i)}-y^{(i,j)}\right)^2 +
\frac{\lambda}{2}\sum_{j=1}^{n_u}\sum_{k=1}^n \left(\theta_k^{(j)}\right)^2
$$

我们可以用梯度下降解决问题：
$$
\begin{array}{l}
Repeat\quad\{\\
\qquad \theta_0^{(j)}:=\theta_0^{(j)}-\alpha\sum_{i:r(i,j)=1} \big((\theta^{(j)})^T(x^{(i)})-y^{(i,j)}\big)x_0^{(i)}\\
\qquad \theta_k^{(j)}:=\theta_k^{(j)}-\alpha\Big[\Big(\sum_{i:r(i,j)=1}\big((\theta^{(j)})^T(x^{(i)})-y^{(i)}\big)x_k^{(i)}\Big)+\lambda\theta_k^{(j)}\Big]\qquad (\textrm{for } k \neq 0)\\
\}
\end{array}
$$

#### 协同过滤

在基于内容推荐中我们有时会很难把握电影（我们要推荐的东西）有哪些特征（$x^{(i)}$），我们想让机器学习自己找特征，这就用到协同过滤。

**新加的优化目标**：（之前在基于内容推荐里面的优化目标仍需考虑）

* 给定 $\theta^{(1)},\theta^{(2)},\cdots,\theta^{(n_u)}$，学习 $x^{(i)}$:

$$
\min_{x^{(i)}}\frac{1}{2}\sum_{i:r(i,j)=1}\left((\theta^{(j)})^Tx^{(i)}-y^{(i,j)}\right)^2+\frac{\lambda}{2}\sum_{k=1}^n \left(x_k^{(i)}\right)^2
$$

* 给定 $\theta^{(1)},\theta^{(2)},\cdots,\theta^{(n_u)}$ ，学习 $x^{(1)},\cdots,x^{(n_m)}$ ：

$$
\min_{x^{(1)},\cdots,x^{(n_m)}}\frac{1}{2}
\sum_{i=1}^{n_m}\sum_{i:r(i,j)=1}\left((\theta^{(j)})^Tx^{(i)}-y^{(i,j)}\right)^2 +
\frac{\lambda}{2}\sum_{i=1}^{n_m}\sum_{k=1}^n \left(x_k^{(i)}\right)^2
$$

**协同过滤**：

现在我们的问题是即没有训练好的 $\theta$，又没有一组充分优化的 $x$，但学习 $\theta$ 要先有 $x$，学习 $x$ 要先有 $\theta$。这就变成了一个类似鸡生蛋、蛋生鸡的问题。

我们可以考虑这样解决这个难题：

首先随机猜一组 $\theta$，然后用这组 $\theta$ 就可以得到一组 $x$；用这组得到的 $x$ 又可以优化 $\theta$，优化后的 $\theta$ 又拿来优化 $x$ ...... 不断重复这个过程，我们可以期望得到一组 $x$ 和 $\theta$ 都充分优化的解（事实上它们最终是会收敛的）。

![屏幕快照 2019-11-28 15.20.59](https://tva1.sinaimg.cn/large/006y8mN6ly1g9ds8xkjatj30ob0bd0w0.jpg)
$$
\begin{array}{l}

\textrm{Given }
x^{(1)},\cdots,x^{(n_m)}
\textrm{ , estimate } 
\theta^{(1)},\cdots,\theta^{(n_u)}:\\
\quad
\min_{\theta^{(1)},\cdots,\theta^{(n_u)}}
\sum_{j=1}^{n_u}\sum_{i:r(i,j)=1}\left((\theta^{(j)})^Tx^{(i)}-y^{(i,j)}\right)^2 +
\frac{\lambda}{2}\sum_{j=1}^{n_u}\sum_{k=1}^n \left(\theta_k^{(j)}\right)^2\\

\textrm {Given }
\theta^{(1)},\cdots,\theta^{(n_u)}
\textrm{ , estimate } 
x^{(1)},\cdots,x^{(n_m)}:\\
\quad
\min_{x^{(1)},\cdots,x^{(n_m)}}\frac{1}{2}
\sum_{i=1}^{n_m}\sum_{i:r(i,j)=1}\left((\theta^{(j)})^Tx^{(i)}-y^{(i,j)}\right)^2 +
\frac{\lambda}{2}\sum_{i=1}^{n_m}\sum_{k=1}^n \left(x_k^{(i)}\right)^2
\end{array}
$$
我们随机初始化一组参数，然后重复来回计算 $\theta$ 和 $x$，最终会得到解，但这样比较麻烦，我们可以做的更高效：

**同时**优化 $x^{(1)},\cdots,x^{(n_m)}$ 和 $\theta^{(1)},\cdots,\theta^{(n_u)}$:
$$
J(x^{(1)},\cdots,x^{(n_m)},\theta^{(1)},\cdots,\theta^{(n_u)})=
\frac{1}{2}
\sum_{(i,j):r(i,j)=1}\left((\theta^{(j)})^Tx^{(i)}-y^{(i,j)}\right)^2+
\frac{\lambda}{2}\sum_{i=1}^{n_m}\sum_{k=1}^n \left(x_k^{(i)}\right)^2+
\frac{\lambda}{2}\sum_{i=1}^{n_m}\sum_{k=1}^n \left(x_k^{(i)}\right)^2
$$

$$
\min_{\begin{array}{c}x^{(1)},\cdots,x^{(n_m)}\\\theta^{(1)},\cdots,\theta^{(n_u)}\end{array}}
J(x^{(1)},\cdots,x^{(n_m)},\theta^{(1)},\cdots,\theta^{(n_u)})
$$



**协同过滤算法**：

1. 将 $x^{(1)},\cdots,x^{(n_m)},\theta^{(1)},\cdots,\theta^{(n_u)}$ 随机初始化为一些比较小的随机值
2. 优化 $J(x^{(1)},\cdots,x^{(n_m)},\theta^{(1)},\cdots,\theta^{(n_u)})$
3. 对于给定用户，该用户的参数是 $\theta$，则用训练得到的某电影的特征 $x$ ，我们可以预测该用户可能为此电影评分：$\theta^Tx$。

**低秩矩阵分解**：

我们可以看到，我们最终的预测是这样的：
$$
Predict = \left[\begin{array}{ccccc} (x^{(1)})^T(\theta^{(1)}) & \ldots & (x^{(1)})^T(\theta^{(n_u)})\\ \vdots & \ddots & \vdots \\ (x^{(n_m)})^T(\theta^{(1)}) & \ldots & (x^{(n_m)})^T(\theta^{(n_u)})\end{array}\right]
$$
考虑到几乎不可能有用户把接近所有的电影都评分，这个预测矩阵是稀疏的，存储这个矩阵会造成大量浪费，不妨令：
$$
X = \left[\begin{array}{ccc}
- & (x^{(1)})^T & - \\
  & \vdots & \\
- & (x^{(n_m)})^T & - \\
\end{array}\right],
\qquad
\Theta = \left[\begin{array}{ccc}
- & (\theta^{(1)})^T & - \\
  & \vdots & \\
- & (\theta^{(n_u)})^T & - \\
\end{array}\right]
$$
则有：
$$
Predict=X\Theta^T
$$
我们便将它分为了两部分。用这个方法求取 $X$ 和 $\Theta$，获得推荐系统需要的参数，称之为**低秩矩阵分解**。该方法不仅能在编程时直接通过向量化的手法获得参数，还通过矩阵分解节省了内存空间。

**寻找相关电影**：

我们常需要推荐与电影 $i$ 相关的电影 $j$，可以这样找到：
$$
\mathop{\textrm{smallest}} ||x^{(i)}-x^{(j)}||
$$
**均值归一化处理**：

再电影推荐问题中，由于评分总是1到5分（或其他范围），故不用特征缩放，但可以做 mean normalization：
$$
\mu_i=\mathop{\textrm{average}} y^{(i,:)}
$$

$$
Y_i = Y_i-\mu_i
$$

对用户 $j$, 电影 $i$, 预测:
$$
\left(\Theta^{(j)}\right)^T\left(x^{(i)}\right)+\mu_i
$$
👉**代码实现**：

1. 代价函数：

```matlab
function [J, grad] = cofiCostFunc(params, Y, R, num_users, num_movies, ...
                                  num_features, lambda)
%COFICOSTFUNC Collaborative filtering cost function
%   [J, grad] = COFICOSTFUNC(params, Y, R, num_users, num_movies, ...
%   num_features, lambda) returns the cost and gradient for the
%   collaborative filtering problem.
%

% Unfold the U and W matrices from params
X = reshape(params(1:num_movies*num_features), num_movies, num_features);
Theta = reshape(params(num_movies*num_features+1:end), ...
                num_users, num_features);

            
J = 0;
X_grad = zeros(size(X));
Theta_grad = zeros(size(Theta));

h = X * Theta';
er = (h - Y) .* R;

J = 1/2 * sum(sum(er.^2));
X_grad = er * Theta;
Theta_grad = er' * X; 

% Regularized

J += lambda/2 *(sum(sum(Theta.^2)) + sum(sum(X.^2)));
X_grad += lambda * X;
Theta_grad += lambda * Theta;
grad = [X_grad(:); Theta_grad(:)];

end
```

2. 均值归一

```matlab
function [Ynorm, Ymean] = normalizeRatings(Y, R)
%NORMALIZERATINGS Preprocess data by subtracting mean rating for every 
%movie (every row)
%   [Ynorm, Ymean] = NORMALIZERATINGS(Y, R) normalized Y so that each movie
%   has a rating of 0 on average, and returns the mean rating in Ymean.
%

[m, n] = size(Y);
Ymean = zeros(m, 1);
Ynorm = zeros(size(Y));
for i = 1:m
    idx = find(R(i, :) == 1);
    Ymean(i) = mean(Y(i, idx));
    Ynorm(i, idx) = Y(i, idx) - Ymean(i);
end

end
```

3. 驱动脚本

```matlab
%  Normalize Ratings
[Ynorm, Ymean] = normalizeRatings(Y, R);

%  Useful Values
num_users = size(Y, 2);
num_movies = size(Y, 1);
num_features = 10;

% Set Initial Parameters (Theta, X)
X = randn(num_movies, num_features);
Theta = randn(num_users, num_features);

initial_parameters = [X(:); Theta(:)];

% Set options for fmincg
options = optimset('GradObj', 'on', 'MaxIter', 100);

% Set Regularization
lambda = 10;
theta = fmincg (@(t)(cofiCostFunc(t, Ynorm, R, num_users, num_movies, ...
                                num_features, lambda)), ...
                initial_parameters, options);

% Unfold the returned theta back into U and W
X = reshape(theta(1:num_movies*num_features), num_movies, num_features);
Theta = reshape(theta(num_movies*num_features+1:end), ...
                num_users, num_features);

fprintf('Recommender system learning completed.\n');

p = X * Theta';
my_predictions = p(:,1) + Ymean;
```

---

EOF