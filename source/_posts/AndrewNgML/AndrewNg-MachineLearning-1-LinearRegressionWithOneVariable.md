---
categories:
- Machine Learning
- AndrewNg
date: 2019-08-18 21:09:53
tags: Machine Learning
title: 单变量线性回归
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
* The mean is halved ($\frac{1}{2}$) as a convenience for the computati::on of the **gradient descent**, as the $\frac{1}{2}f^2 = f$.

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

Let's draw some pictures for better understanding of what the values of the cost function.

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
\begin{array}{rl}
 \textrm{Hypothesis: } & h_\theta(x)=\theta_0+\theta_1x\\
  & \\
 \textrm{Parameters: } & \theta_0, \theta_1\\
   & \\
 \textrm{Cost Function: } & J(\theta_0, \theta_1) = \frac{1}{2m}\sum^m_{i=1}[h_\theta(x^{(i)})-y^{(i)}]^2\\
   & \\
 \textrm{Goal: } & \mathop{minimize}\limits_{\theta_0, \theta_1} J(\theta_0, \theta_1)
\end{array}
$$
Same as last time, we want to unserstand the hypothesis $h$ and the cost function $J$ via a series of graph. However, we'd like to use a *`contour plot`* to describe our $J(\theta_0, \theta_1)$.

> A *contour plot* is a graph that contains many contour lines.
>
> A *contour line* of a two variable function has a constant value at all points of the same line. 

An example:

![屏幕快照 2019-08-21 09.29.48](http://ww3.sinaimg.cn/large/006y8mN6gy1g673ule5evj30p40cqafx.jpg)

Taking any color and going along the 'circle', one would expect to get the same value of the cost function. 

To touch our optimization objective, we can try to setting the parameters $\theta_i$ to different values.

When $\theta_0 = 360$ and $\theta_1 = 0$, the value of $J(\theta_0, \theta_1)$ in the contour plot **gets closer to the center thus reducing the cost function error**. Now we get a result in a better fit of the data:

![屏幕快照 2019-08-21 09.29.58](http://ww3.sinaimg.cn/large/006y8mN6gy1g673vbnti4j30o20bggqp.jpg)

Minimizing the cost function as much as possible and consequently, the result of $\theta_1$ and $\theta_0$ tend to be around 0.12 and 250 respectively. Plotting those values on our graph to the right seems to put our point in the center of the inner most 'circle'.

Obviously, we dislike to write a software to just plot out a contour plot and then try to manually read off the numbers to reach our goal. We want **an efficient algorithm for automatically finding the value of $\theta_0$ and $\theta_1$ that minimizes the cost function $J$**. Actually, the *gradient descent* algorithm that we will talk about works great on this question.

## Gradient Descent

There is a algorithm called **gradient descent** for **minimizing the cost function $J$**. And we can use it not only in linear regression as it's actually used all over the place in machine learning.

Let's talk about gradient descent for minimizing some arbitrary function $J$. So here's the problem setup:

![image-20190821172439919](http://ww2.sinaimg.cn/large/006y8mN6ly1g67fcs8k0mj30gs09gjsz.jpg)

We put $\theta_0$ on the `x` axis and $\theta_1$ on the `y` axis, with the **cost function** on the vertical `z` axis. The points on our graph will be the result of the cost function using our hypothesis with those specific theta parameters. The graph below depicts such a setup:

![image-20190821204112216](http://ww2.sinaimg.cn/large/006y8mN6gy1g67l1ajh02j30no0con68.jpg)

We will know that we have succeeded when our cost function is at the very bottom of the pits in our graph, i.e. when its value is the minimum. The red arrows show the minimum points in the graph.

Image that we are physically standing at a point on a hill, in gradient descent, what we're going to do is to spin 360 degrees around and just look all around us, and ask, "If I were to take a little step in some direction, and I want to go down the hill as quickly as possible, what direction should I take?" then you take a step in that direction. Repeat doing this until you converge to a local minimum. Like the black line in the picture above shows.

Notice that if we choose different points to grandient descent, we may reach different local optimums.

Mathematically, this is the definition of the gradient descent algorithm:

> **Gradient Descent Algorithm**
>
> repeat until convergence {
> 
>$\qquad\theta_j := \theta_j - \alpha\frac{\partial}{\partial\theta_j}J(\theta_0, \theta_1)\qquad \textrm{(for } j=0 \textrm{ and } j=1 \textrm{)}$
>
> }

The $\alpha$ is a number that is called the **`learning rate`**. It basically controls how big a step we take downhill with gradient descent.

At each iteration $j$, one should simultaneously update the parameters θ1,θ2,...,θn. Updating a specific parameter prior to calculating another one on the `j(th)` iteration would yield to a wrong implementation:

![屏幕快照 2019-08-21 21.24.15](http://ww3.sinaimg.cn/large/006y8mN6ly1g67magihpyj30wo0hu7iy.jpg)

## Gradient Descent Intuition

Let's explore the scenario where we used **one parameter $\theta_1$ ** and plotted its cost function to implement a gradient descent. Our formula for a single parameter was : Repeat until convergence:
$$
\theta_1:=\alpha\frac{d}{d\theta_1}J(\theta_1)
$$


Regardless of the slope's sign for $\frac{d}{d\theta_1}J(\theta_1)$ eventually converges to its minimum value. 

The following graph shows that when the slope is negative, the value of $\theta_1$ increases and when it is positive, the value of $\theta_1$ decreases:

![image-20190826211520863](https://tva1.sinaimg.cn/large/006y8mN6ly1g6de48b49qj30i50af0ui.jpg)



On a side note, we should adjust our parameter $\alpha$ to ensure that the gradient descent algorithm converges in a reasonable time. Failure to converge or too much time to obtain the minimum value imply that our step size is wrong.

![image-20190826211727240](https://tva1.sinaimg.cn/large/006y8mN6ly1g6de6eemuhj30im0astb9.jpg)



How does gradient descent converge with a fixed step size $\alpha$?
The intuition behind the convergence is that $\frac{d}{d\theta_1}J(\theta_1)$ approaches 0 as we approach the bottom of our convex function. At the minimum, the derivative will always be 0 and thus we get:

![image-20190826211936126](https://tva1.sinaimg.cn/large/006y8mN6ly1g6de8nmhaoj30ia0a4why.jpg)



## Gradient Descent for Linear Regression

Now, we have learnt the gradient descent, the linear regression model and the squared error cost function as well. This time, we are going to put together gradient descent with our cost function that will give us an algorithm for linear regression for fitting a straight line to our data.

This is what we worked out:

![image-20190826212442071](https://tva1.sinaimg.cn/large/006y8mN6ly1g6dedxiq58j30ej052aay.jpg)

We are going to apply gradient descent algorithm to minimize our squared error cost function.

The key term is the derivative term:

$$
\frac{\partial}{\partial\theta_j}J(\theta_0, \theta_1) = \frac{\partial}{\partial\theta_j}\frac{1}{2m}\sum^m_{i=1}[h_\theta(x^{(i)})-y^{(i)}]^2
=
\frac{\partial}{\partial\theta_j}\frac{1}{2m}\sum^m_{i=1}[\theta_0+\theta_1x^{(i)}-y^{(i)}]^2
$$

$$
\begin{array}{rl}
j=0: & \frac{\partial}{\partial\theta_0}J(\theta_0,\theta_1)=\frac{1}{m}\sum^m_{i=1}[h_\theta(x^{(i)})-y^{(i)}]\\
 & \\
j=1: & \frac{\partial}{\partial\theta_1}J(\theta_0,\theta_1)=\frac{1}{m}\sum^m_{i=1}[h_\theta(x^{(i)})-y^{(i)}] \cdot x^{(i)}
\end{array}
$$



Plug them back into our gradient descent algorithm:

> repeat until convergence {
>
> $\qquad\theta_0 := \theta_0 - \alpha\frac{1}{m}\sum^m_{i=1}[h_\theta(x^{(i)})-y^{(i)}]$
> 
>$\qquad\theta_1 := \theta_1 - \alpha\frac{1}{m}\sum^m_{i=1}[h_\theta(x^{(i)})-y^{(i)}] \cdot x^{(i)}$
>
> }

Notice: update $\theta_0$ and $\theta_1$ simultaneously.

The point of all this is that if we start with a guess for our hypothesis and then repeatedly apply these gradient descent equations, our hypothesis will become more and more accurate. So, this is simply gradient descent on the original cost function J. 

This method looks at every example in the entire training set on every step, and is called **batch gradient descent**. 

Note that, while gradient descent can be susceptible to local minima in general, the optimization problem we have	 posed here for linear regression has only one global, and no other local,optima; thus gradient descent always converges (assuming the learning rate α is not too large) to the global minimum. Indeed, J is a convex quadratic function. Here is an example of gradient descent as it is run to minimize a quadratic function.

![image-20190826231632514](https://tva1.sinaimg.cn/large/006y8mN6ly1g6dhmaf0chj308q06qgml.jpg)

The ellipses shown above are the contours of a quadratic function. Also shown is the trajectory taken by gradient descent, which was initialized at (48,30). The x’s in the figure (joined by straight lines) mark the successive values of θ that gradient descent went through as itconverged to its minimum.

---

## Experiment

A Wild Implement of Linear Regression with One Variable via Gradient Descent in Python Made by Myself:

```python
# 
# linregress.py
# Linear Regression with one variable via a Batch Gradient Descent
# 
# Created by CDFMLR on 2019/8/28.
# Copyright © CDFMLR. All right reserved.
#

import math
import random


class LinearRegressionWithOneVariable(object):
    '''
    # Linear regression with one variable
    
    > Given a training set, to find a set of parameters (theta_0, theta_1) of hypothesis function `h(x) = theta_0 + theta_1 * x` via gradient descent so that h(x) is a "good" predictor for the corresponding value of y.

    Properties
        
        - `training_set`
        - `theta`

    Methods

        - `regress`: to find a set of thetas to make hypothesis a "good" predictor
        - `hypothesis`: to get a predicted value

    Example

    ``python
    >>> model = LinearRegressionWithOneVariable([(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)])
    >>> model.regress(verbose=True, epsilon=0.0001)
    theta_0:        0.025486336182825836
    theta_1:        0.9940305813471573
    cost:           9.99815680487604e-05
    hypothesis:     h(x) = 0.025486336182825836 + 0.9940305813471573*x
    >>> model.hypothesis(10)
    9.9657921496544
		``
    '''
    def __init__(self, training_set):
        '''
        training_set: training set
        '''
        self.training_set = training_set    # [(x: int, y: int), ...]
        self.theta = [0, 0]
    
    def _hypothesis(self, x, theta):
        return theta[0] + theta[1] * x
    
    def _cost(self, dataset, theta):
        s = 0
        for i in dataset:
            s += (self._hypothesis(i[0], theta) - i[1]) ** 2
        return s / (2 * len(dataset))
    
    def _gradient_descent(self, dataset, starting_theta, learning_rate, epsilon, max_count=4294967296):
        theta = list.copy(starting_theta)
        last_theta = list.copy(starting_theta)
        cost = self._cost(dataset, theta)
        last_cost = cost * 2
        count = 0
        epsilon = abs(epsilon)
        diff = epsilon + 1
        while (diff > epsilon):
            count += 1
            if count >= max_count:
                raise RuntimeError("Failed in gradient descent: cannot convergence after {mc} iterations.".format(mc=max_count))
    
            try:
                t_sum= sum((self._hypothesis(i[0], theta) - i[1] for i in dataset))
                theta[0] = theta[0] - learning_rate * t_sum / len(dataset)
    
                t_sum = sum(
                    ((self._hypothesis(i[0], theta) - i[1]) * i[0] for i in dataset)
                    )
                theta[1] = theta[1] - learning_rate * t_sum / len(dataset)
    
                last_cost = cost
                cost = self._cost(dataset, theta)
    
                if not any((math.isnan(x) or math.isinf(x) for x in theta)) and abs(cost) <= abs(last_cost):
                    diff = max((abs(last_theta[i] - theta[i]) for i in range(len(theta))))
                    last_theta = list.copy(theta)
                    learning_rate += learning_rate * 4
                else:
                    theta = list.copy(last_theta)
                    learning_rate /= 10
                    if (learning_rate == 0):
                        learning_rate = self._get_learning_rate(self.training_set)
    
                # print('[DEBUG] (%s) theta: %s, diff=%s, learning_rate=%s, cost=%s' % (count, theta, diff, learning_rate, cost))
            except OverflowError:
                theta = list.copy(last_theta)
                learning_rate /= 10
                if (learning_rate == 0):
                    learning_rate = self._get_learning_rate(self.training_set)


        return theta, count
    
    def _get_learning_rate(self, dataset):
        return 1 / max((i[1] for i in dataset))
    
    def regress(self, epsilon=1, learning_rate=0, verbose=False):
        '''
        To find a set of thetas to make hypothesis a "good" predictor
    
        Parms:
            - epsilon: when the difference between new theta and last theta less then epsilon, finish regressing
            - learning_rate: about the "step length" of gtadient descent. Too small will take a long time to regress, and too big will raise a Overflow error. `0` to allow the algorithm to select an appropriate value automatically.
            - verbose: true to print the result of regression
        '''
        init_theta = [random.random(), random.random()]
    
        if learning_rate == 0:
            learning_rate = self._get_learning_rate(self.training_set)
        
        self.theta, count = self._gradient_descent(self.training_set, init_theta, learning_rate, epsilon)
        
        if verbose:
            print('Gradient descent finished after {count} iterations:\ntheta_0:\t{t0}\ntheta_1:\t{t1}\ncost:\t\t{cost}\nhypothesis:\th(x) = {t0} + {t1}*x'.format(
                    count=count, t0=self.theta[0], t1=self.theta[1], cost=self._cost(self.training_set, self.theta)))
    
    def hypothesis(self, x):
        '''
        To get a predicted y value of giving x
        
        Parms:
            - x: x value of the point you want to predict
        '''
        return self._hypothesis(x, self.theta)


if __name__ == '__main__':
    model = LinearRegressionWithOneVariable([(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)])
    model.regress(verbose=True, epsilon=0.0000000001)
    model.hypothesis(10)
```





[1]: http://clownote.github.io/about/index.html#数学公式

