---
title: AndrewNg-MachineLearning-17-GradientDescentWithLargeDatasets
tags: Machine Learning
categories:
  - Machine Learning
  - AndrewNg
---

# Notes of Andrew Ng’s Machine Learning —— (17) Large Scale Machine Learning

## Gradient Descent with Large Datasets

### Learning With Large Datasets

When learning with large datasets, it can be high cost to do a gradient descent. So before we actually use this large datasets (say, $m = 100,000,000$) for model training, we'd better try to randomly pick a small part of data ($m=1,000$) from it and learning from it. If this subset works already satisfying, we'll no longer need to do a learning with large dataset.

Suppose you are facing a supervised learning problem and have a very large dataset (m = 100,000,000). How can you tell if using all of the data is likely to perform much better than using a small subset of the data (say m = 1,000)?

What er can do is plotting  a learning curve for a range of values of m and verify that the algorithm has high variance when m is small.

![image-20191210150555045](https://tva1.sinaimg.cn/large/006tNbRwgy1g9rn4jr6zxj30om07r0vl.jpg)

Facing a left-liked curve, maybe we use a large dataset can offer a better model. But if we get the curve like the right one, use a $m>1000$ can not actually improve our model effectively.

### Stochastic Gradient Descent

Before talking about the Stochastic Gradient Descent, let's take a look at the gradient descent we used (Actually, it is called *Batch Gradient Descent*), A linear regression for example:

> $J_{\textrm{train}}(\theta)=\frac{1}{2m}\sum_{i=1}^{m}(h_\theta(x^{(i)})-y^{(i)})^2$ 
>
> Repeat {
>
> ​		$\quad \theta_j:=\theta_j-\alpha\frac{1}{m}\sum_{i=1}^{m}(h_\theta(x^{(i)})-y^{(i)})x_j^{(i)}$    (for every $j=0,\cdots,n$)
>
> }

With this Batch Gradient Descent, every step we take will need to calculate the sum of derivatives of all data. If our dataset is large, the time cost will be very expensive.

To deal with a large dataset, here is the *Stochastic Gradient Descent*:

$$
\begin{array}{l}
cost\left(\theta,(x^{(i)},y^{(i)})\right)=\frac{1}{2}(h_\theta(x^{(i)})-y^{(i)})^2\\\\
J_{train}(\theta)=\frac{1}{m}\sum_{i=1}^{m}cost\left(\theta,(x^{(i)},y^{(i)})\right)\\\\

1.\quad \textrm{Randomly shuffle(reorder) training examples}\\
2.\quad \textrm{Repeat } \{ \\
\qquad\qquad \textrm{for $i:= 1, \cdots,m$ } \{ \\
\qquad\qquad\qquad\quad \theta_j:=\theta_j-\alpha(h_\theta(x^{(i)})-y^{(i)})x_j^{(i)} \quad \textrm{(for every $j=0,\cdots,n$)} \\
\qquad\qquad\qquad\quad \} \\
\qquad\qquad \} \\
\end{array}
$$
Notice that, instead of calculate the sum of all derivatives and change the whole theta, in the inner for loop, each step we only care about the cost of one theta. When the training set size m is very large, stochastic gradient descent can be much faster than gradient descent.

Learning rate $\alpha$ is typically held constant. Can slowly decrease $\alpha$ over time if we want $\theta$ to converge better. (E.g. $\alpha=\frac{CONST_1}{iterationNumber+CONST_2}$)

### Mini-Batch Gradient Descent

- Batch gradient descent: Use all $m$ examples in each iteration
- Stochastic gradient descent: Use $1$ example in each iteration
- Mini-batch gradient descent: Use $b$ examples in each iteration ($b\in[2, 100]$, Usual $10$)

Mini-batch gradient descent sometimes faster than stochastic gradient descent:
$$
\begin{array}{l}
\textrm{Say $b=10,m=1000$.}\\

\textrm{Repeat } \{ \\
\qquad \textrm{for $i:= 1, 11, 21, 31, \cdots,991$ } \{ \\
\qquad\qquad\quad \theta_j:=\theta_j-\alpha\frac{1}{10}\sum_{k=i}^{i+9}(h_\theta(x^{(i)})-y^{(i)})x_j^{(i)} \quad \textrm{(for every $j=0,\cdots,n$)} \\
\qquad\qquad\quad \} \\
\} \\
\end{array}
$$

### Stochastic Gradient Descent Convergence

#### Checking for convergence

- **Batch gradient descent**:

  Plot $J_{train}(\theta)$ as a function of the number of iterations of gradient descent.

  $J_{train}(\theta)=\frac{1}{2m}\sum_{i=1}^m(h_\theta(x^{(i)})-y^{(i)})^2$

- **Stochastic gradient descent**:

  $cost(\theta,(x^{(i)},y^{(i)}))=\frac{1}{2}(h_\theta(x^{(i)})-y^{(i)})^2$

  During learning, compute $cost(\theta,(x^{(i)},y^{(i)}))$ before updating $\theta$ using $(x^{(i)},y^{(i)})$.

  Every 1000 iterations, plot $cost(\theta,(x^{(i)},y^{(i)}))$ averaged over the last 1000 examples processed by algorithm. (If we get a plot that is too noisy to see it's converging or not, try ploting for every 5000 (or summat bigger than 1000) iterations rather than 1000)

