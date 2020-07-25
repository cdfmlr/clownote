---
categories:
- Machine Learning
- AndrewNg
date: 2019-11-04 16:38:39
tags: Machine Learning
title: 支持向量机
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

If we have a lot of features, then there will be too many polynomial terms, which can become very computationally expensive. So is there a different or a better choice of the features that we can use to plug into this sort of hypothesis form, or in another words, how to define a set of new $f_1,f_2,f_3$ to avoid  high polynomial calculations?

Here is one idea:

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

### SVM with Kernels

We have talked about the process of picking a few landmarks. But how to choose our $l^{(i)}$s? Actually we will simply choose the location of our landmarks to be exactly near the locations of our m training examples. Here is what we are going to do:

---

#### The Support Vector Machine With Kernels Algorithm

Given a set of training data: $(x^{(1)},y^{(1)}),(x^{(2)},y^{(2)}),...,(x^{(m)},y^{(m)})$ 

Choose landmarks: $l^{(i)}=x^{(i)} \quad \textrm{for }i=1,2,\cdots,m$

For example $x$: $f_i=\mathop{\textrm{similarity}}(x,l^{(i)}) \quad \textrm{for }i=1,2,\cdots,m$

Group $f_i$s into a vector: $f=[f_0,f_1,f_2,\cdots,f_m]^T$, in which the $f_0 \equiv 1$ is a extra feature for convention.

Hypothesis: 

* Given $x$, compute features $f\in\R^{m+1}$
* Predict $y=1$ if $\theta^Tf=\theta_0f_0+\theta_1f_1+\cdots\ge 0$ (where $\theta\in\R^{m+1}$)

Training:
$$
\min_\theta 
C\sum_{i=1}^m \large[ y^{(i)} \mathop{\textrm{cost}_1}(\theta^Tf^{(i)})
+ (1 - y^{(i)})\ \mathop{\textrm{cost}_0}(\theta^Tf^{(i)})\large]
+ \frac{1}{2}\sum_{j=1}^n \theta_j^2
$$
Notice: instead of $\theta^Tx^{(i)}$ that we use before, now we use $\theta^Tf^{(i)}$. And here our $n$ is equal to $m$. 

Mathematical tricks in practice: Ignoring the $\theta_0$ (s.t. $\theta=[\theta_1,\cdots,\theta_m]^T$), we can get $\sum_j\theta_j^2=\theta^T\theta$. Moreover, for mathematical convenience when deal with a large training set, we gonna use **$\theta^T M \theta$** instead of $\theta^T\theta$.

---

#### SVM parameters

Here are parameters that we are going to choose when use the algorithm above:

* $C$ (=$\frac{1}{m}$)
  * Large $C$: Lower bias, high variance (small $\lambda$)
  * Small $C$: Higher bias, low variance (large $\lambda$)
* $\sigma^2$
  * Large $\sigma^2$: Features $f_i$ vary more smoothly. Higher bias, lower variance.![屏幕快照 2019-11-02 15.51.46](https://tva1.sinaimg.cn/large/006y8mN6ly1g8jukxlnxkj306u04laad.jpg)
  * Small $\sigma^2$: Features $f_i$ vary less smoothly. Lower bias, higher variance.![屏幕快照 2019-11-02 15.51.50](https://tva1.sinaimg.cn/large/006y8mN6ly1g8jul1utnaj306i04ezk4.jpg)

E.g. Suppose we train an SVM and find it overfits our training data. A reasonable next step is going to decrease $C$ or increase $\sigma^2$.

## SVM in Practice

### Using An SVM

We are not recommended writing our own software to solve for the parameters via a SVM. We should call some library functions to do that.

When using SVM software package (e.g. `liblinear`, `libsvm`) to solve for parameters $\theta$, we need to specify:

* Choice of parameter $C$;
* Choice of kernel (similarity function):
  * **No kernel** ("linear kernel", do our common logistic regression): Predict $y=1$ if $\theta^Tx\ge0$. For large $n$ and small $m$ case (no kernel can avoid overfitting).
  * **Gaussian kernel**: $f_i=\exp(-\frac{||x-l^{(i)}||^2}{2\sigma^2})$, where $l^{(i)}=x^{(i)}$.(Need to choose $\sigma^2$). For small $n$ and large $m$ case (Gaussian kernel can fit a more complex nonlinear decision boundary).

If we decide to use a Gaussian kernel, here is what we are going to do:

* Provide a kernel (similarity) function:
  $$
  \begin{array}{l}
  \textrm{function f = kernel(x1, x2)}\\
  \qquad \textrm{f} = \exp(-\frac{||\textrm{x1}-\textrm{x2}||^2}{2\sigma^2})\\
  \textrm{return}
  \end{array}
  $$
  Note: Do perform feature scaling before using the Gaussian kernel.

### Other choices of kernel

Not all similarity functions $\mathop{\textrm{similarity}}(x,l)$ make valid kernels. (Need to satisfy technical condiction called "Mercer's Theorem" to make sure SVM packages' optimizations run correctly, and do not diverge).

There are many off-the-shelf kernels available, for example:

- Polynomial kernel: $k(x,l)=(X^Tl+constant)^{degree}$, need to choose the $constant$ and $degree$. Usually performs worse than Gaussian kernel. Only for $X$ and $l$ are all strictly non negative.
- More esoteric: String kernel (for input is text string),  chi-square kernel, histogram intersection kernel, ...

### Multi-class classification

![image-20191102171432072](https://tva1.sinaimg.cn/large/006y8mN6ly1g8jul8myufj30mv0cz0xu.jpg)

### Logistic regression v.s. SVMs

$n$ = number of features ($x\in\R^{n+1}$);

$m$ = number of training examples;

* If $n$ is large (relative to $m$): ($n\ge m$, e.g. $n=10,000, m=10 \sim 1000$)
  * Use logistic regression, or SVM without a kernel ("linear kernel") 
* If $n$ is small, $m$ is intermediate: (e.g. $n=1\sim1000,m=50,000+$)
  * Use SVM with Gaussian kernel
* If $n$ is small, $m$ is large:
  * Create/add more features, then use logistic regression or SVM without a kernel

Note: Neural network likely to work well for most of these settings, but may be slower to train.

