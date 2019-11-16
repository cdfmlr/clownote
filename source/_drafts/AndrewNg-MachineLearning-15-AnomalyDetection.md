---
title: AndrewNg-MachineLearning-15-AnomalyDetection
tags: Machine Learning
categories:
  - Machine Learning
  - AndrewNg
---

# Notes of Andrew Ng’s Machine Learning —— (15) Anomaly Detection

## Density Estimation

### Problem Motivation

*Anomaly Detection* is a type of machine learning problem.

Imagine that you're a manufacturer of aircraft engines, and let's say that as your aircraft engines roll off the assembly line, you're doing quality assurance testing, and as part of that testing you measure features of your aircraft engine, like the heat generated, the vibrations and so on. So you now have a data set of $x_1$ through $x_m$, if you have manufactured $m$ aircraft engines and plot your data. Then, given a new engine $x_{test}$, you want to know is $x_{test}$ anomalous? This problem is called **Anomaly Detection**.

![image-20191114105935962](https://tva1.sinaimg.cn/large/006y8mN6ly1g8xdwc6zf8j30p10c2gpb.jpg)

Here is want we are going to do:

> Dataset: $\{x^{(1)},x^{(2)},\cdots,x^{(m)}\}$
>
> Is $x_{test}$ anomalous?

To solve this problem, we will train a model for $p(x)$ (i.e. a model for the **probability** of $x$, where $x$ are these features of, say, aircraft engines). We're then going to say that for the new aircraft engine, if $p(x_{test})$ is less than some $\epsilon$ then we flag this as an anomaly:
$$
\begin{array}{l}
p(x_{test})<\epsilon \Rightarrow \textrm{anomaly}\\
p(x_{test})\ge\epsilon \Rightarrow \textrm{OK}
\end{array}
$$
This problem of estimating this distribution $p(x)$ are sometimes called the problem of *density estimation*.

![image-20191114111418858](https://tva1.sinaimg.cn/large/006y8mN6ly1g8xebhrku9j30nl0d7gqi.jpg)

#### Anomaly detection example

**Anomaly detec-on example** 

Fraud detection

- $x^{(i)}$= features of user $i$’s actvities 
- Model $p(x)$ from data.
- Idenify unusual users by checking which have $p(x)<\epsilon$

Manufacturing  (Monitoring computers in a data center )

- $x^{(i)}$ = features of machine $i$

- $x_1$ = memory use, $x_2$ = number of disk accesses/sec, $x_3$ = CPU load, $x_4$ = CPU load/network traffic ...

### Gaussian Distribution

**Gaussian distribution** which is also called the *normal distribution*.

If $x$ is a distributed Gaussian with mean $\mu$, variance $\sigma^2$, we will write it as:
$$
x \sim \mathcal{N}(\mu,\sigma^2)
$$
In this case, the probability of $x$ is:
$$
p(x) = \frac{1}{\sqrt{2\pi}\sigma}\exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)
$$


There is some example of Gaussian distribution:

![image-20191115172344685](https://tva1.sinaimg.cn/large/006y8mN6ly1g8yum81cydj30je0c3410.jpg)

We can see that the "center" of these plots is actually the value of $\mu$. And with our $\sigma$ increasing,  the plots is more and more "flat". Or, it will be "thin & tall" if $\sigma$ is small.

#### Parameter estimation

Given a dataset: $\{x^{(1)},x^{(2)},\cdots,x^{(m)}\}$, we can get our $\mu$ and $\sigma$ by:
$$
\mu=\frac{1}{m}\sum_{i=1}^{m}x^{(i)}
$$

$$
\sigma^2=\frac{1}{m}\sum_{i=1}^{m}\left(x^{(i)}-\mu\right)^2
$$

P.S. this is what people turn to use when handling a machine learning problem, it's a little different from what we normally utilize in mathematics.

### Anomaly detection algorithm

1. Choose features $x_i$ that you think might be indicative of anomalous examples.

2. Fit parameters $\mu_1,\cdots,\mu_n,\sigma_1^2,\cdots,\sigma_n^2$: (I wrote the vectorilized version)
   $$
   \mu=\frac{1}{m}\sum_{i=1}^{m}x^{(i)}
   $$

   $$
   \sigma^2=\frac{1}{m}\sum_{i=1}^{m}\left(x^{(i)}-\mu\right)^2
   $$

3. Given new example $x$, compute $p(x)$:
   $$
   p(x)=\prod_{j=1}^{n}p(x_j;\mu_j,\sigma_j^2)=\prod_{j=1}^{n}\frac{1}{\sqrt{2\pi}\sigma_j}\exp\left(-\frac{(x_j-\mu_j)^2}{2\sigma_j^2}\right)
   $$

4. Anomaly if $p(x)<\epsilon$

### Building an Anomaly Detection System

#### Developing and Evaluating an Anomaly Detection System

**The importance of real-number evalua-on** 

When developing a learning algorithm (choosing features, etc.), making decisions is much easier if we have a way of evalua-ng our learning algorithm. 

Assume we have some labeled data, of anomalous and non- anomalous examples. ($y=0$ if normal, $y=1$ if anomalous). 

- `Training set`: $x^{(1)},x^{(2)},\cdots,x^{(m)}$ (assume normal examples/not anomalous)

- `Cross validation set`: $\left(x_{cv}^{(1)},y_{cv}^{(1)}\right),\cdots,\left(x_{cv}^{(m_{cv})},y_{cv}^{(m_{cv})}\right)$

- `Test set`: $\left(x_{test}^{(1)},y_{test}^{(1)}\right),\cdots,\left(x_{test}^{(m_{test})},y_{test}^{(m_{test})}\right)$

**Aircraft engines motivating example** 

Say, what we have is:

* 10000 good (normal) engines  ($y=0$)
* 20 flawed engines (anomalous)   ($y=1$)

Than we are going to choose:

- Training set: 6000 good engines
- CV: 2000 good engines ($y=0$), 10 anomalous ($y=1$)
- Test: 2000 good engines ($y=0$), 10 anomalous ($y=1$) 

**Algorithm evaluation**

Fit model $p(x)$ on training set $\{x^{(1)},\cdots,x^{(m)}\}$

On a cross validation/test example $x$, predict:
$$
y = \left\{\begin{array}{ll}
1 & \textrm{if } p(x) < \epsilon \quad \textrm{(anomaly)}\\
0 & \textrm{if } p(x) \ge \epsilon \quad \textrm{(normal)}\\
\end{array}\right.
$$
Possible evaluation matrices:

- True positive, false positive, false negative, true negative 
- Precision/Recall
- $F_1$-score 

Can also use cross valida-on set to choose parameter $\epsilon$.

