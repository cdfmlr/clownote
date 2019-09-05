---
title: AndrewNg-MachineLearning-4-NormalEquation
tags: Machine Learning
categories:
  - Machine Learning
  - AndrewNg
---

# Notes of Andrew Ng’s Machine Learning —— (4) Normal Equation

## Normal Equation

Gradient dedcent gives one way of minimizing our cost function $J$. Let's discuss a second way of doing so -- **`Normal Equation`**.

Normal Equation minimize $J$ by explicitly taking its derivatives with resspect to the $\theta_j$s, and setting them to zero. This alllows us to find the optimum theta without resorting to an iteration.

The normal equation formula is given below:
$$
\theta = (X^TX)^{-1}X^Ty
$$


There is no need to do feature scaling with the normal equation.

### Example

![img](https://tva1.sinaimg.cn/large/006y8mN6ly1g6oul2lb93j30gq09dgn1.jpg)

### Normal Equation V.S. Gradient Descent

| Gradient Descent           | Normal Equation                                           |
| -------------------------- | --------------------------------------------------------- |
| Need to choose alpha       | No need to choose alpha                                   |
| Needs many iterations      | No need to iterate                                        |
| Time cost: $O(kn^2)$       | Need to calculate inverse of $X^TX$, which costs $O(n^3)$ |
| Works well when n is large | Slow if n is very large                                   |

In practice, when $n > 10,000$, we are tend to use gradient descent, otherwise, normal equation will perform better.

