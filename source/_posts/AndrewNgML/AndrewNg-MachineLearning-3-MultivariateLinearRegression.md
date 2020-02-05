---
title: 多变量线性回归
tags: Machine Learning
categories:
  - Machine Learning
  - AndrewNg
date: 2019-09-05 17:11:21
---


# Notes of Andrew Ng’s Machine Learning —— (3) Multivariate Linear Regression

## Multiple Features

Linear regression with multiple variables is alse known as "**multivariate linear regression**".

### Notations

We now introduce notation for equations where we can have any number of input variables (Multiple Features, i.e. Multivariate):

- $m$: the number of training examples.
- $n$: the number of features.
- $x^{(i)}$: the input (features) of the $i^{th}$ training example, a n-dimensional vector.
- $x^{(i)}_j$: the value of feature $j$ in the $i^{th}$ training example.  

### Hypothesis

The multivariable form of the hypothesis function accommodating these multiple features is as follows:
$$
h_\theta(x)=\theta_0+\theta_1x_1+\theta_2x_2+\theta_3x_3+ ... + \theta_nx_n
$$

> In order to develop intuition about this function, we can think about $\theta_0$ as the basic price of a house, $\theta_1$ as the price per square meter, $\theta_2$ as the price per floor, etc. $x_1$ will be the number of square meters in the house, $x_2$ the number of floors, etc.

Using the definition of matrix muyltiplication, our multivariable hypothesis function can be concisely represented as:
$$
h_\theta(x)=
\left[\begin{array}{c}\theta_0 & \theta_1 & \ldots & \theta_n\end{array}\right]
\left[\begin{array}{c}x_0 \\ x_1 \\ \vdots \\ x_n \end{array}\right]
=
\theta^Tx
$$
This is a vectorization of our hypothesis function for one training example.

Remark: Note that for convenience reasons, we assume **$x^{(i)}_0=1 \quad \textrm{for(}i \in 1, ...,m \textrm{)}$**. This allows us to do matrix operations with $\theta$ and $x$. Hence making two vector $\theta$ and $x^{(i)}$ match each other element-wise (that is, have the same number of elements: n+1).

## Gradient Descent For Multiple Variables

Let's say the condition about the multiple variables:

> Hypothesis: $h_\theta(x)=\sum_{i=0}^m \theta_ix_i$.
>
> Parameters: $\theta_0, \theta_1, ...,\theta_n$.
>
> Cost Function: $J(\theta_0, \theta_1, ..., \theta_n)=\frac{1}{2m}\sum_{i=1}^m(h_\theta(x^{(i)})-y^{(i)})^2$.

Or vectorizedly:

> Hypothesis: $h_\theta(x)=\theta^Tx$.
>
> Parameters: $\theta$.
>
> Cost Function: $J(\theta)=\frac{1}{2m}\sum_{i=1}^m(\theta^Tx^{(i)}-y^{(i)})^2$.

The Gradient Descent will be like this:

> repeat until convergence {
>
> $\qquad \theta_j := \theta_j - \alpha \frac{1}{m} \sum^m_{i=1}[h_\theta(x^{(i)})-y^{(i)}] \cdot x_j^{(i)}\qquad \textrm{for }j:=0, ..., n$
>
> }

The following image compares gradient descent with one variable to gradient descent with multiple variables:

![img](https://tva1.sinaimg.cn/large/006y8mN6ly1g6ljh8xnnuj30g508ttam.jpg)

##  Feature Scaling

We can speed up gradient descent by **having each of our input values in roughly the same range**. This is because $\theta$ will descend quickly on small ranges and slowly on large ranges, and so will oscillate inefficiently down to the optimum when the variables are very uneven.

The way to prevent this is to **modify the ranges of our input variables** so that they are all roughly the same. Ideally:
$$
\begin{array}{c}
-1 \le x_{i} \le 1\\
\textrm{or}\\
-0.5 \le x_{i} \le 0.5
\end{array}
$$
These aren't exact requirements; we are only trying to speed things up. The goal is to get all input variables into roughly one of these ranges, give or take a few.

In practice, we offen think it's ok for variables in range $[-3,-\frac{1}{3}) \cup (+\frac{1}{3}, +3]$.

Two techniques to help with this are `feature scaling` and `mean normalization`.

### Feature scaling

Feature scaling involves **dividing the input values by *the range*** (i.e. the maximum value minus the minimum value) of input variable, resulting in a new range of just 1.
$$
\begin{array}{rl}
\textrm{Range:} & s_i = max(x_i)-min(x_i)\\
\textrm{Scaling:} & x_i:=\frac{x_i}{s_i}
\end{array}
$$


### Mean normalization

Mean normalization involves subtracting the average value for an input variable from the values for that input variable resulting in a new average value for the input variable of just zero.
$$
\begin{array}{rl}
\textrm{Average:} & \mu_i = \frac{sum(x_i)}{m}\\
\textrm{Mean normalizing:} & x_i:=x_i-\mu_i
\end{array}
$$

### Implement

We always implement both of these techniques via adjusting our input values as shown in this formula: 
$$
x_i:=\frac{x_i-\mu_i}{s_i}
$$

* **$\mu_i$** is the **average of all the values for feature (i)**
* **$s_i$** is the **range of values (`max - min`)**, or $s_i$ could also be the **standard deviation**.

For example, if $x_i$ represents housing prices with a range of 100 to 2000 and a mean value of 1000, then, $x_i := \dfrac{price-1000}{1900}$.

#### In octave

In octave, the function `mean` can offer us the avaerage of values for feature (i), when the function `std` gives us the standard deviation of values for feature (i). So we can program like this:

```octave
function [X_norm, mu, sigma] = featureNormalize(X)
%FEATURENORMALIZE Normalizes the features in X 
%   FEATURENORMALIZE(X) returns a normalized version of X where
%   the mean value of each feature is 0 and the standard deviation
%   is 1. This is often a good preprocessing step to do when
%   working with learning algorithms.

X_norm = X;
mu = zeros(1, size(X, 2));
sigma = zeros(1, size(X, 2));

% Instructions: First, for each feature dimension, compute the mean
%               of the feature and subtract it from the dataset,
%               storing the mean value in mu. Next, compute the 
%               standard deviation of each feature and divide
%               each feature by it's standard deviation, storing
%               the standard deviation in sigma. 
%
%               Note that X is a matrix where each column is a 
%               feature and each row is an example. You need 
%               to perform the normalization separately for 
%               each feature. 
%

mu = mean(X);
sigma = std(X);
X_norm = (X - mu) ./ sigma;

end

```



## Learning Rate

### Debugging gradient descent

Make a plot with *number of iterations* on the x-axis. Now plot the cost functiong $J(\theta)$ over the number of iterations of  gradient descent. If $J(\theta)$ ever increases, then you probably need to decrease learning rate $\alpha$.

### Automatic convergence test

Declare convergence if $J(\theta)$ decreases by less than $\epsilon$, where $\epsilon$ is some small value such as $10^{-3}$. However in practice it's difficult to choose this threshold value.

### Making sure gradient descent is working correctly

![img](https://tva1.sinaimg.cn/large/006y8mN6ly1g6mi7c257sj30eg07wt9v.jpg)

It has been proven that if learning rate α is sufficiently small, then J(θ) will decrease on every iteration.

![img](https://tva1.sinaimg.cn/large/006y8mN6ly1g6mi84pb5bj30e807pjsd.jpg)

To summarize:

> If $\alpha$ is too small: slow convergence.
>
> If $\alpha$ is too large: ￼may not decrease on every iteration and thus may not converge.

### Implement

We should try different $\alpha$ to find a fit one by drawing #iterations-J(θ) plots.

E.g. To choose $\alpha$, try:


```
... , 0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1, ...
```

## Features and Polynomial Regression

### Combine Features

We can improve our features and the form of our hypothesis function in a couple different ways.

For example, we can **combine** multiple features into one, Such as combining $x_1$ and $x_2$ into a new feature $x_3$ by taking $x_1 \cdot x_2$.

### Polynomial Regression

To fit the data well, our hypothesis function may need to be non-linear. So we can **change the behavior or curve** of our hypothesis function by making it a quadratic, cubic or square root function (or any other form).

For example, if our hypothesis function is $h_\theta(x)=\theta_0+\theta_1x_1$ then we can create additional features based on $x_1$, to get the quadratic function $h_\theta(x)=\theta_0+\theta_1x_1+\theta_2x_1^2$ or the cubic function $h_\theta(x)=\theta_0+\theta_1x_1+\theta_2x_1^2+\theta_3x_1^3$, to make it a square root function, we could do: $h_\theta(x) = \theta_0 + \theta_1 x_1 + \theta_2 \sqrt{x_1}$.

In the cubic version, we can create new features $x_2$, $x_3$ where $x_2=x_1^2$ and $x_3=x_1^3$, then we can get a set of thetas via gradient descent for multiple variables.

⚠️Note. if you choose your features this way then **feature scaling** becomes very important.

e.g. if x has range 1 ~ 1000:

Then range of x^2 becomes 1 ~ 1000000;

And range of x^3 becomes 1 ~ 1000000000;

