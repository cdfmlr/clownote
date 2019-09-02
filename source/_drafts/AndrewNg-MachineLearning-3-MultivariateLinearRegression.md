---
title: AndrewNg-MachineLearning-3-MultivariateLinearRegression
tags: Machine Learning
categories:
  - Machine Learning
  - AndrewNg
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
\left[\begin{array}{c}x_0 \\ x_1 \\ \vdots \\ x_n\end{array}\right]
=
\theta^Tx
$$
This is a vectorization of our hypothesis function for one training example.

Remark: Note that for convenience reasons, we assume $x^{(i)}_0=1 \quad \textrm{for($i \in 1, ...,m$)}$. This allows us to do matrix operations with $\theta$ and $x$. Hence making two vector $\theta$ and $x^{(i)}$ match each other element-wise (that is, have the same number of elements: n+1)