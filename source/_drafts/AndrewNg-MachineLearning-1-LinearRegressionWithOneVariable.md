---
title: AndrewNg-MachineLearning-1-LinearRegressionWithOneVariable
date: 2019-08-18 21:09:53
tags: MachineLearning
categories:	
	- MachineLearning
	- AndrewNg
---

# Notes of Andrew Ng’s Machine Learning —— (1) Linear Regression with One Variable

## Model Representation

### Notation

* [$x^{(i)}$][1] denote the *input* variables, called **input features**
* $y^{(i)}$ denote the *output* variables, called **target variable**
* $(x^{(i)}, y^{(i)})$ is called a **training example**
* $(x^{(i)}, y^{(i)}); i=1, ..., m$ —— is called a **training set**

⚠️【Note】The superscript "$^{(i)}$" in the notations is simply an **index** into the train set.

- $X$ denote the **space** of *input values*
- $Y$ denote the **space** of *output values*

In many examples, $X = Y =\R$.

### A more formal description of supervised learning

Given a training set, to learn a **function** $h: X \to Y$ so that $h(x)$ is a "good" predictor for the corresponding value of $y$.

For historical reasons, this function $h$ is called a **`hypothesis`**.

Pictorially:

![page1image20344816.png](http://ww4.sinaimg.cn/large/006tNc79gy1g652fmlvx6j30az078glq.jpg) 

With our new notations, the categories of supervised learning problems can be this:

* `regression problem`: when the **target variable** is continuous.
* `classification problem`: $y$ can take on only a small number of discrete values

### Hypothesis & Model Regression

To represent the hypothesis $h$, for example, if we want to fit a data set like this:

![image-20190819214710193](http://ww4.sinaimg.cn/large/006tNc79gy1g65bp99j97j307o05gq2z.jpg)

Simply, we may make the $h_\theta(x)=\theta_0+\theta_1x$. This is means that we are going to predict that $y$ is a linear function of $x$. 

Plotting this in the picture, it will be something like this:

![006tNc79gy1g65bp99j97j307o05gq2z](http://ww3.sinaimg.cn/large/006tNc79gy1g65byqwhjxj307o05gwee.jpg)

And what this function is doing is predicting that $y$ is some straight line function of $x$.

In this case, this **model** is called **`linear regression with one variable`**(or `Univariate linear regression`).

P.S. we can also fit a more complicated (perhaps non-linear) functions, but this linear case is the simplest.


## Cost Function

Well, now we have got this:

![image-20190819221840291](http://ww4.sinaimg.cn/large/006tNc79gy1g65cm1aucyj30js0a60v0.jpg)

To get a "good" hypothesis function, we need to choose $\theta_0$, $\theta_1$ so that $h_\theta(x)$ is close to $y$ for our training exmaples $(x, y)$.  A cost function is of great help with this goal.

### Cost function

A **`cost function`** can help us to measure the accuracy of our hypothesis function.

This takes an **average difference** of all the results of the hypothesis with inputs from x's and the actual output y's:
$$
J(\theta_0, \theta_1) = \frac{1}{2m}\sum^m_{i=1}[h_\theta(x^{(i)})-y^{(i)}]^2 \tag{1}
$$
The function $(1)$ is our *cost function* exactly. Take a look at it:

* $h_\theta(x^{(i)})-y^{(i)}$ shows the difference between the predicted value and the actual value.

* $\frac{1}{m}\sum^{m}_{i=1}...$ offers the mean of the squares of $h_\theta(x^{(i)})-y^{(i)}$
* The mean is halved ($\frac{1}{2}$) as a convenience for the computation of the **gradient descent**, as the $\frac{1}{2}f^2 = f$.

P.S. This function is otherwise called the "*Squared error function*", or "*Mean squared error*".

### Goal

To make $h_\theta(x)$ closing to $y$, we are just expected to minimize our cost function by adjusting the value of $\theta_0$, $\theta_1$.

We describe this **goal** like this:
$$
\mathop{minimize}\limits_{\theta_0, \theta_1} J(\theta_0, \theta_1) \tag{2}
$$
Or, more directly:
$$
\mathop{minimize}\limits_{\theta_0, \theta_1}
\frac{1}{2m}\sum^m_{i=1}[h_\theta(x^{(i)})-y^{(i)}]^2
\tag{3}
$$

And if we are working with a linear regression with one variable, the $h_\theta(x)=\theta_0+\theta_1x$.

⚠️【Note】Hypothesis Function & Cost Function

- $h_\theta(x)$ for fixed $\theta_i$, is a function of $x$.
- $J(\theta_0, \theta_1)$ is a function of the parameter $\theta_i$ .

## Cost Function - Intuition I

To getting start, we are going to work with a simplified hypothesis function:

![屏幕快照 2019-08-19 22.44.10](http://ww2.sinaimg.cn/large/006tNc79ly1g65ddr26d9j30ja0a4778.jpg)

Our training data set is scattered on the x-y plane. We are trying to make a straight line (defined by $h_\theta(x)$) which passes through these scattered data points.

Our objective is to get the best possible line. The best possible line will be such:

> So that the *average squared vertical distances of the scattered points from the line* ($\frac{1}{m}\sum^m_{i=1}[h_\theta(x^{(i)})-y^{(i)}]^2$) will be the least.

Ideally, the line should pass through all the points of our training data set. In such a case, the value of cost function $J(\theta_0, \theta_1)$ will be `0`. 

E.g. A ideal situation where $J=0$:

Let this be our training set: Only three points `(1, 1)`, `(2, 2)` & `(3, 3)`

![屏幕快照 2019-08-19 22.54.07](http://ww2.sinaimg.cn/large/006tNc79ly1g65dnu9hj7j309606iwen.jpg)

Now, we try setting $\theta_1$ to different values: `-0.5`,  `0`, `0.5`, `1`, `1.5`......

When $\theta_1=1$, we get a slope of 1 which goes through every single data point in our model. Conversely, when $\theta_1=0.5$, we see the vertical distance from our fit to the data points increase:

![新建项目](http://ww4.sinaimg.cn/large/006tNc79ly1g65ejfyhsbj30rs08cmzd.jpg)

By doing this, we got a series of graph of $h_\theta(x)$ in x-y plane as well as yield to the following $\theta_1$-$J(\theta_1)$ graph:

![image-20190819230628708](http://ww1.sinaimg.cn/large/006tNc79ly1g65dzrkce0j30b209ydh6.jpg)

Thus as a goal, we should try to **minimize the cost function**. In this case, $\theta_1=1$ is our global minimum.

## Cost Function - Intuition II

Unlike before, this time, we won't continue with the simplified hypothesis, we are going to keep both of parameters $\theta_0$ and $\theta_1$. So the hypithesis function will be $h_\theta(x)=\theta_0+\theta_1x$.

Here's our problem formulation as usual:
$$
\begin{array}{ll}
 \textrm{Hypothesis: } & h_\theta(x)=\theta_0+\theta_1x\\\\
 \textrm{Parameters: } & \theta_0, \theta_1\\\\
 \textrm{Cost Function: } & J(\theta_0, \theta_1) = \frac{1}{2m}\sum^m_{i=1}[h_\theta(x^{(i)})-y^{(i)}]^2\\\\
 \textrm{Goal: } & \mathop{minimize}\limits_{\theta_0, \theta_1} J(\theta_0, \theta_1)\\
\end{array}
$$
Same as last time, we want to unserstand the hypothesis $h$ and the cost function $J$ via a series of graph. However, we'd like to use a *`contour plot`* to describe our $J(\theta_0, \theta_1)$.

> A *contour plot* is a graph that contains many contour lines.
>
> A *contour line* of a two variable function has a constant value at all points of the same line. 

An example:

![image-20190820205719025](../../../Library/Application Support/typora-user-images/image-20190820205719025.png)

Taking any color and going along the 'circle', one would expect to get the same value of the cost function. 

To touch our optimization objective, we can try to setting the parameters $\theta_i$ to different values.

When $\theta_0 = 360$ and $\theta_1 = 0$, the value of $J(\theta_0, \theta_1)$ in the contour plot **gets closer to the center thus reducing the cost function error**. Now we get a result in a better fit of the data:

![屏幕快照 2019-08-21 09.29.48](../../../Desktop/屏幕快照 2019-08-21 09.29.48.png)

Minimizing the cost function as much as possible and consequently, the result of $\theta_1$ and $\theta_0$ tend to be around 0.12 and 250 respectively. Plotting those values on our graph to the right seems to put our point in the center of the inner most 'circle'.

Obviously, we dislike to write a software to just plot out a contour plot and then try to manually read off the numbers to reach our goal. We want **an efficient algorithm for automatically finding the value of $\theta_0$ and $\theta_1$ that minimizes the cost function $J$**.



TODO: Upload the pictures above.



[1]: http://clownote.github.io/about/index.html#数学公式