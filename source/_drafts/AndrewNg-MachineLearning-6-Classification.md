---
title: AndrewNg-MachineLearning-6-Classification
tags: Machine Learning
categories:
  - Machine Learning
  - AndrewNg
---

# Notes of Andrew Ng’s Machine Learning —— (6) Classification and Representation

## Intro of Classification

Classification problems are something like giving a patient with a tumor, we have to predict whether the tumor is malignant or benign. It's expected to output **discrete** values.

The classification problem is just like the regression problem, except that the values we want to predict take on only a small number of discrete values. For now, we will focus on the **binary classification problem** in which `y` can take only two values, `0` and `1`. 

For instance, if we are trying to build a spam classifier for email, then $x^{(i)}$ may be some features of a piece of email, and $y$ may be `1` if it is a piece of spam mail, and `0` otherwise. Hence, $y \in \{0,1\}$. `0` is also called the *negative class*, and `1` the *positive class*, and they are sometimes also denoted by the symbols `-` and `+`. Given $x^{(i)}$, the corresponding $y^{(i)}$ is also called *the label for the training example*.

To attempt classification, one method is to use linear refression and map all predictions greater than `0.5` as a `1` and all less than `0.5` as a `0`. However, this method doesn't work because classification is not actually a linear function. So what we actually do to solve classification problems is an algorithm named **logistic regression**. Note that even be called *regression*, it is actually to do classification.

## Logistic Regression

### Hypothesis Representation

We could approach the classification problem ignoring the fact that `y` is discrete-valued, and use our old linear regression algorithm to try to predict `y` given `x`. However it is easy to construct examples where this method performs very poorly.

Intuitively, it also doesn't make sense for $h_\theta(x)$ to take values larger than `1` or smaller then `0` when we know that $y\in\{0,1\}$. To fix this, let's change our hypotheses $h_\theta(x)$ to satisfy $0 \le h_\theta(x) \le 1$. This accomplished by plugging $\theta^Tx$ into the **Logistic Function**.

The the **Simoid Function**, also called the **Logistic Function** is this:
$$
y = \frac{1}{1+e^{-x}}
$$
It looks like the following image:

![image-20190917162504420](https://tva1.sinaimg.cn/large/006y8mN6ly1g72ld52460j30ur0g8ta7.jpg)

Our new form uses the Simoid Function:
$$
\begin{array}{l}h_\theta(X) = g(\theta^TX)\\z = \theta^TX\\g(z) = \frac{1}{1+e^{-z}}\end{array}
$$
The logistic function $g(z)$ maps any real numbers to the $(0,1)$ interval, making it useful for transforming a arbitrary-valued function into a function better suited for classfication.

We can also simply write $h_\theta(x)$ like this:
$$
h_\theta(X) = \frac{1}{1+e^{-\theta^TX}}
$$
**$h_\theta(x)$ will output the probalility that our output is `1`.** For example, $h_\theta(x)=0.7$ gives us a probability of $70\%$ that our output is $1$ (then the probability that it is 0 is 30%):
$$
\begin{array}{l}
h_\theta(x)=P(y=1 \mid x;\theta)=1-P(y=0 \mid x; \theta)\\
P(y=0 \mid x;\theta) + P(y=1 \mid x;\theta) = 1
\end{array}
$$

### Decision Boundary

In order to get our discrete `0` or `1` classification, we can translate the output of the hyporithesis function as follows:
$$
\begin{array}{rcl}
h_\theta(x) \ge 0.5 &\Rightarrow& y=1\\
h_\theta(x) < 0.5 &\Rightarrow& y=0
\end{array}
$$
The way our logistic function $g$ behaves is that when its input is $\ge 0$, its output is $\ge 0.5$:
$$
g(z) \ge 0.5 \quad when \quad z \ge 0
$$
In fact, we know that:
$$
\begin{array}{ccccl}
z \to -\infin &,& e^{\infin} \to \infin & \Rightarrow & g(z) \to 0\\
z \to 0 &,& e^{0} \to 1 & \Rightarrow & g(z) \to 0.5\\
z \to +\infin &,& e^{-\infin} \to 0 & \Rightarrow & g(z) \to 1
\end{array}
$$
So if our input to $g$ is $\theta^TX$, then that means:
$$
h_\theta(X) = g(\theta^TX) \ge 0.5 \quad when \quad \theta^TX \ge 0
$$
From these statements we can now say:
$$
\begin{array}{rcl}
\theta^TX \ge 0 &\Rightarrow& y=1\\
\theta^TX \le 0 &\Rightarrow& y=0\\
\end{array}
$$
The **decision boundary** is the line that separates the area where $y=0$ and where $y=1$. It is created by our hypothesis function.

Example:
$$
\theta=\left[ \begin{array}{c}
5\\
-1\\
0
\end{array} \right]
$$
In this case, $y=1$ if $5+(-1)x_1+0x_2 \ge 0$ , i.e. $x_1 \le 5$. Our boundary is a straight vertical line placed on the graph where $x_1=5$, and everything to the left of that denotes $y=1$, while everything to the right denotes $y=0$:

![image-20190917173722734](https://tva1.sinaimg.cn/large/006y8mN6ly1g72ng9ovwsj306e04u74d.jpg)

Another example:

![image-20190917173931467](https://tva1.sinaimg.cn/large/006y8mN6ly1g72niix9vaj30m20cin2i.jpg)

Non-linear decision boundaries:

The input to the sigmoid function g(z) (e.g. $\theta^TX$) doesn't need to be linear, and could be a function that describes a circle (e.g. $z=\theta_0+\theta_1x_1^2+\theta_2x_2^2$) or any shape to fit our data.

Example:

![image-20190917174144868](https://tva1.sinaimg.cn/large/006y8mN6ly1g72nku2lrxj30mv08xtcy.jpg)

### Logistic Regression Model

In this part, we will implement the logistic regression model.
$$
\begin{array}{rcl}
\textrm{Training set} &:& \{(x^{(1)},y^{(1)}), (x^{(2)},y^{(2)}), \ldots, (x^{(m)},y^{(m)})\}\\
\textrm{m examples} &:&
x \in \left[\begin{array}{c}
x_0\\x_1\\ \vdots \\ x_n
\end{array}\right] \textrm{where }(x_0=1)
,\quad y \in \{0,1\}\\
\textrm{Hypothesis} &:& h_\theta(x)=\frac{1}{1+e^{-\theta^Tx}}
\end{array}
$$

#### Cost Function

If we use the same cost function that we use for *linear regression* ($J(\theta)=\frac{1}{m}\sum_{i=1}^m\frac{1}{2}(h_\theta(x^{(i)})-y^{(i)})^2$) for logistic regression, it will be **non-convex** (that looks wavy), which is causing many local optima and hard to find the global minimum.

![屏幕快照 2019-09-19 22.49.53](https://tva1.sinaimg.cn/large/006y8mN6ly1g757sf5lm8j30f504w3zi.jpg)

So, what we actually need is our new **Logistic Regression Cost Function**, which guarantees that $J(\theta)$ is convex for logistic regression.
$$
\begin{array}{l}
J(\theta)=\frac{1}{m}\sum_{i=1}^{m}Cost(h_\theta(x^{(i)},y^{(i)}))\\
\\
Cost(h_\theta(x),y)=\left\{\begin{array}{rl}
-log(h_\theta(x)) & \textrm{ if}\quad y=1\\
-log(1-h_\theta(x)) & \textrm{ if}\quad y=0
\end{array}\right.
\end{array}
$$
The “$J(\theta)$-$h_\theta(x)$” plots is like this:

![屏幕快照 2019-09-19 23.23.39](https://tva1.sinaimg.cn/large/006y8mN6ly1g758q7xincj31lc0mq76b.jpg)

Let's take a look at the $Cost(h_\theta(x),y)$ : 
$$
\begin{array}{lcl}Cost(h_\theta(x),y) = 0 &\textrm{if}& h_\theta(x)=y\\Cost(h_\theta(x),y) \to \infin &\textrm{if}& y=0 \quad\&\quad h_\theta(x) \to 1\\Cost(h_\theta(x),y) \to \infin &\textrm{if}& y=1 \quad\&\quad h_\theta(x) \to 0\\\end{array}
$$

>  If our correct answer 'y' is 0, then the cost function will be 0 if our hypothesis function also outputs 0. If our hypothesis approaches 1, then the cost function will approach infinity.
>
> If our correct answer 'y' is 1, then the cost function will be 0 if our hypothesis function outputs 1. If our hypothesis approaches 0, then the cost function will approach infinity.

