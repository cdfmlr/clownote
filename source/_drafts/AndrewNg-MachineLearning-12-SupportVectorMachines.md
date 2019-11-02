---
title: AndrewNg-MachineLearning-12-SupportVectorMachines
tags: Machine Learning
categories:
  - Machine Learning
  - AndrewNg
---

# Notes of Andrew Ng’s Machine Learning —— (12) Support Vector Machines

## Large Margin Classification

### Optimization Objective

The *Support Vector Machine* (or *SVM*) is a powerful algorithm that is widely used in both industry and academia. Compared to both logistic regression and neural networks, the SVM somethimes gives a cleaner and more powerful way of learning complex non-linear functions.

What the **cost** of example in our logistic regression is as:
$$
-y\log\Big(\frac{1}{1+e^{-\theta^Tx}}\Big)-(1-y)\log\Big(1-\frac{1}{1+e^{-\theta^Tx}}\Big)
$$
It looks like this:

![屏幕快照 2019-09-19 23.23.39](https://tva1.sinaimg.cn/large/006y8mN6ly1g8f4rfgycnj31lc0mqjsr.jpg)

With SVM, we'd like to make a little change of them so that:

![image-20191029161946046](https://tva1.sinaimg.cn/large/006y8mN6ly1g8f58f0dolj31ao0h6wpq.jpg)

We set a $\textrm{cost}_1$ instead of $-\log(h)$ and set a $\textrm{cost}_0$ instead of $-\log(1-h)$.

So, for logistic regression, we are going to:
$$
\min_\theta\frac{1}{m} \sum_{i=1}^m \large[ -y^{(i)}\ \log (h_\theta (x^{(i)})) - (1 - y^{(i)})\ \log (1 - h_\theta(x^{(i)}))\large] + \frac{\lambda}{2m}\sum_{j=1}^n \theta_j^2
$$
And for Support Vector Machine, we change it to:
$$
\min_\theta 
C\sum_{i=1}^m \large[ y^{(i)} \mathop{\textrm{cost}_1}(\theta^Tx^{(i)})
+ (1 - y^{(i)})\ \mathop{\textrm{cost}_0}(\theta^Tx^{(i)})\large]
+ \frac{1}{2}\sum_{j=1}^n \theta_j^2
$$
We dropped the $\frac{1}{m}$ in both terms, then multiplied a $C=\lambda$ to them. In this case we can promise that we can get the same min $\theta$ with those two operators.

![image-20191029164223055](https://tva1.sinaimg.cn/large/006y8mN6ly1g8f5vx0x43j31dm0ni156.jpg)

### Large Margin Intuition

Let's say the SVM decision boundary:
$$
\min_\theta 
C\sum_{i=1}^m \large[ y^{(i)} \mathop{\textrm{cost}_1}(\theta^Tx^{(i)})
+ (1 - y^{(i)})\ \mathop{\textrm{cost}_0}(\theta^Tx^{(i)})\large]
+ \frac{1}{2}\sum_{j=1}^n \theta_j^2
$$
If we set $C$ a very  large value, $100000$ for example, when this optimization objective , we're going to be highly motivated to choose a value, so that **the first term is equal to zero**. And our goal become:
$$
\begin{array}{l}
	\min_\theta \frac{1}{2}\sum_{j=1}^{n}\theta_j^2 \\\\
	s.t. \quad \begin{array}{l}
		\theta^Tx^{(i)} \ge 1 & \textrm{if } y^{(i)}=1\\
		\theta^Tx^{(i)} \le -1 & \textrm{if } y^{(i)}=0
	\end{array}
\end{array}
$$
We will get a very intersting decision boundary. The Support Vector Machines will choose a decision boundary that does a great job of separating the positive and negative examples (the black line below install of others).

![image-20191029171503318](https://tva1.sinaimg.cn/large/006y8mN6gy1g8f6tz8op1j30q60kon78.jpg)

we see that the black decision boundary has some larger minimum distance from any of my training examples, whereas the magenta and the green lines come awfully close to the training examples.

And mathematically, what that does is, this black decision boundary has a larger distance (the blue lines).That distance is called the *margin* of the support vector machine and this gives the SVM a certain robustness, because it tries to separate the data with as a large a margin as possible. So the support vector machine is sometimes also called a large margin classifier.

If $C$ is very large than the SVM will be sensitive to **outliers**. For example, we a very large $C$, $100000$ maybe, with a outliers at the left bottom, the learning algorithm will get the magenta decision boundary. However, if $C$ is not too large, we are going to get the black one as wanted:

![image-20191029173209265](https://tva1.sinaimg.cn/large/006y8mN6gy1g8f7bsn392j30zm0iqwmu.jpg)

### Mathematics Behind Large Margin Classification

#### Vector Inner Product

Let's say we have two vectors:
$$
u=\left[\begin{array}{l}u1 \\ u2\end{array}\right],\qquad v=\left[\begin{array}{l}v1 \\ v2\end{array}\right]
$$
We define their *Vector Inner Product* as:
$$
\textrm{Inner Product} =
u^Tv=v^Tu
$$
And we can also get the inner product by getting:
$$
\begin{array}{ccl}
||u|| &=& \textrm{length of vector } u= \sqrt{u_1^2+u_2^2}\\
p &=& \textrm{length of projection of } v \textrm{ onto } u \textrm{ (signed)} \\ \\
u^Tv &=& p \cdot ||u||
\end{array}
$$
![image-20191031111759471](https://tva1.sinaimg.cn/large/006y8mN6ly1g8h7ruhj8kj31em0s0nfd.jpg)

#### SVM Decision Boundary

When the $C$ is very large, we can get this:
$$
\begin{array}{l}
	\min_\theta \frac{1}{2}\sum_{j=1}^{n}\theta_j^2
	=\frac{1}{2}\Big(\sqrt{\sum_{j=1}^n\theta_j^2}\Big)^2
	=\frac{1}{2}||\theta||^2 \\\\
	s.t. \quad \begin{array}{l}
		\theta^Tx^{(i)} \ge 1 & \textrm{if } y^{(i)}=1\\
		\theta^Tx^{(i)} \le -1 & \textrm{if } y^{(i)}=0
	\end{array}
\end{array}
$$
If we make a simplification as $\theta_0=0, n=2$, so that $\theta=[\theta_1,\theta_2]^T$, then our $\theta^Tx^{(i)}=p^{(i)}\cdot ||\theta||=\theta_1x_1^{(i)}+\theta_2x_2^{(i)}$.

![image-20191031123156678](https://tva1.sinaimg.cn/large/006y8mN6ly1g8h9w173flj309l06t3zr.jpg)

So, our description can be:
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
In the condition of $y=1$, to min the $\theta$, we should promise $||\theta||$ is small as well as make $p^{(i)}\cdot ||\theta|| \ge 1$ as possible. So, we get a large $p^{(i)}$.

For the negative example, similarly, we will get a $p^{(i)}$ whos absolute value is large.

![屏幕快照 2019-10-31 12.58.43](https://tva1.sinaimg.cn/large/006y8mN6ly1g8harwzv9cj324i0nu4qp.jpg)

As we seen, a large $p^{(i)}$ gives us a large margin.

## kernels

### Kernels and Similarity

We can develop complex nonlinear classifiers by adapting support vector machines. The main technique for this is something called *kernels*.

Let's say if we a training set that looks this:

![image-20191102114127170](https://tva1.sinaimg.cn/large/006y8mN6ly1g8jjopayn9j30c5083jui.jpg)

Recall the past, we will work with lots of polynomial features to hypothesis $y=1$ if $\theta_0+\theta_1x_1+\theta_2x_2+\theta_3x_1x_2+\theta_4x_1^2+\theta_5x_2^2+\cdots\ge 0$ and predict $0$ otherwise.

Another way of that is:
$$
\begin{array}{lcl}
\textrm{Predict } y=1 &\textrm{if}&\theta_0+\theta_1f_1+\theta_2f_2+\theta_3f_3+\cdots\ge 0
\end{array}
$$
Where $f_1=x_1,f_2=x_2,f_3=x_1x_2,f_4=x_1^2,...$

If we have a lot of features, then there will be too many polynomial terms, which can become very computationally expensive. So is there a different or a better choice of the features that we can use to plug into this sort of hypothesis form, or in another words, how to define a set of new $f_1,f_2,f_3$ avoiding high polynomial calculations?

Here is one idea of how to define our new $f_i$:

![image-20191102124615797](https://tva1.sinaimg.cn/large/006y8mN6ly1g8jljliww8j30o90dmwjt.jpg)

To simplify the description and make it more intuitional, let's say we have only $x_0,x_1,x_2$ and we are going to define only three new features ($f_1,f_2,f_3$). 

Leave $x_0$ alone, we manually pick a few points $(x_1^{(i)},x_2^{(i)})$ from a plot of $x_1$-$x_2$, in this example they are notated as $l^{(1)},l^{(2)},l^{(3)}$. We call this points `landmarks`.

And then, given a $x$, we can compute new feature depending on proximity to landmarks $l^{(1)},l^{(2)},l^{(3)}$ as follow:
$$
f_i = \mathop{\textrm{similarity}}(x,l^{(i)}) = \exp(-\frac{||x-l^{(i)}||^2}{2\sigma^2}) = \exp(-\frac{\sum_{j=1}^n(x_j-l_j^{(i)})^2}{2\sigma^2})
$$
The mathematical term for the simiarity function is `kernel function`. There are many formula of kernel functions can be chosen. And the specific kernel we're using here is actually called a *Gaussian Kernel*.

Note. $||w||$ means the length of the vector $w$.

Given  $x$, for each $l^{(i)}$ we can get a $f_i$:

* If x is near $l^{(i)}$:

$$
f_i \approx \lim_{x\to l^{(i)}}\exp(-\frac{||x-l^{(i)}||^2}{2\sigma^2}) = \exp(-\frac{0^2}{2\sigma^2}) = 1
$$

* If $x$ far from $l^{(i)}$:

$$
f_i \approx \lim_{||x-l^{(i)}||\to +\infin}\exp(-\frac{||x-l^{(i)}||^2}{2\sigma^2}) = \exp(-\frac{\infin^2}{2\sigma^2}) = 0
$$

![image-20191102132852867](https://tva1.sinaimg.cn/large/006y8mN6ly1g8jmrwo86pj30ph0dwwm1.jpg)

We can see that: If sigma squared is large, as we move away from $l^{(1)}$, the value of $f_1$ falls away much more slowly.

So, given this definition of the features, let's see what source of hypothesis we can learn:

![image-20191102133600603](https://tva1.sinaimg.cn/large/006y8mN6ly1g8jmzc2qq4j30ot0ditej.jpg)

We can see that, in this example, only given the $x$ near $l^{(1)}$ or $l^{(2)}$ will it predict "1", if the $x$ if far from this two landmarks, it will predict "0".

