---
title: AndrewNg-MachineLearning-9-NeuralNetworksLearning
tags: Machine Learning
categories:
  - Machine Learning
  - AndrewNg
---

# Notes of Andrew Ng’s Machine Learning —— (9) Neural Networks: Learning

## Cost Functon & Backpropagation

### Cost Function

Firstly, define some needed variables:

| Notation | Represent                                             |
| -------- | ----------------------------------------------------- |
| $L$      | total number of layers in the network                 |
| $s_l$    | number of units (not counting bias unit) in layer $l$ |
| $K$      | number of output units/classes                        |

Recall that in neural networks, we may have many output nodes. 

We denote $H_\Theta(x)_k$ as being a hypothesis that results in the $K^{th}$ output. 

Our cost function for neural networks is going to be a generalization of the one we used for logistic regression. Recall that the cost function for regularized logistic regression was:

$J(\theta) = - \frac{1}{m} \sum_{i=1}^m \large[ y^{(i)}\ \log (h_\theta (x^{(i)})) + (1 - y^{(i)})\ \log (1 - h_\theta(x^{(i)}))\large] + \frac{\lambda}{2m}\sum_{j=1}^n \theta_j^2$

For neural networks, it is going to be slightly more complicated:
$$
J(\Theta)=-\frac{1}{m}\sum_{i=1}^{m}\sum_{k=1}^{K}\Big[
y_k^{(i)}log\Big(\big(h_\Theta(x^{(i)})\big)_k\Big)+
(1-y_k^{(i)})log\Big(1-\big(h_\Theta(x^{(i)})\big)_k\Big)
\Big]+
\frac{\lambda}{2m}\sum_{l=1}^{L-1}\sum_{i=1}^{s_l}\sum_{j=1}^{s_{l+1}}\Big(\Theta_{j,i}^{(l)}\Big)^2
$$
We have added a few nested summations to account for our multiple output nodes. In the first part of the equation, before the square brackets, we have an additional nested summation that loops through the number of output nodes.

In the regularization part, after the square brackets, we must account for multiple theta matrices. The number of columns in our current theta matrix is equal to the number of nodes in our current layer (including the bias unit). The number of rows in our current theta matrix is equal to the number of nodes in the next layer (excluding the bias unit). As before with logistic regression, we square every term.

Note:

- the double sum simply adds up the logistic regression costs calculated for each cell in the output layer
- the triple sum simply adds up the squares of all the individual Θs in the entire network.
- the i in the triple sum does **not** refer to training example i

## Backpropagation Algorithm

`Backpropagation` is neural-network terminology for minimizing our cost function, just like what we were doing with gradient descent in logistic and linear regression. Our goal is to compute:

$\mathop{\textrm{min}}_\Theta J(\Theta)$

That is, we want to minimize our cost function $J$ using an optimal set of parameters in theta. In this section we'll look at the equations we use to compute the partial derivative of $J(\Theta)$:

$\frac{\partial}{\partial\Theta_{i,j}^{(l)}}J(\Theta)$

To do so, we use the following algorithm:

![img](https://tva1.sinaimg.cn/large/006y8mN6gy1g7y3ekmyjmj30om0d9gs6.jpg)

### Backpropagation Algorithm

Given training set ${(x^{(1)},y^{(1)}),...,(x^{(m)},y^{(m)})}$

* Set $\Delta_{i,j}^{(l)}:=0$ for all $l,i,j$, (hence you end up having a matrix full of zeros)

(@ For loop: @)

**For** training example $t=1\textrm{ to } m$:

1. Set $a^{(1)}:=x^{(t)}$
2. Preform forward propagation to compute $a^{(l)}$ for $l=2,3,...,L$

![img](https://tva1.sinaimg.cn/large/006y8mN6gy1g7y3n2yqdkj30d8074q53.jpg)

3. Using $y^{(t)}$, compute $\delta^{(L)}=a^{(L)}-y^{(t)}$

Where $L$ is our total number of layers and $a^{(L)}$ is the vector of outputs of the activation units for the last layer.

So, our `error values` for the last layer are simply the differences of our actual results in the last layer and the correct outputs in $y$.

To get the delta values of the layers before the last layer, we can use an equation that steps us back from right to left:

4. Compute $\delta^{(L-1)},\delta^{(L-2)},...,\delta^{(2)}$ using $\delta^{(l)}=\big((\Theta^{(l)})^T\delta^{(l+1)}\big).*a^{(l)}.*(1-a^{(l)})$

*【Note】: "$.*$" above are the element-wise multiplications in Octave/MATLAB.*

The delta values of layer $l$ are calculated by multiplying the delta values in the next layer with the theta matrix of layer $l$.

We then element-wise multiply that with a function called $g'$, or g-prime, which is the derivative of the activation function $g$ evaluated with the input values given by $z^{(l)}$.

The g-prime derivative terms can also be written out as: $g'(z^{(l)})=a^{(l)}.*(1-a^{(l)})$

5. $\Delta_{i,j}^{(l)}:=\Delta_{i,j}^{l}+a_j^{(l)}\delta^{(l+1)}$ or with vectorization, $\Delta^{(l)}:=\Delta^{(l)}+\delta^{(l+1)}(a^{(l)})^T$

(@ End For @)

Hence we update our new $\Delta$ matrix.

* $D_{i,j}^{(l)}:=\frac{1}{m}\big(\Delta_{i,j}^{(l)}+\lambda\Theta_{i,j}^{(l)}\big)$, if $j\not=0$;

* $D_{i,j}^{(l)}:=\frac{1}{m}\Delta_{i,j}^{(l)}$ if $j=0$.

The capital-delta matrix $D$ is used as an `accumulator` to add up our values as we go along and eventually compute our partial derivate.

Thus we get $\frac{\partial}{\partial\Theta_{i,j}^{(l)}}J(\Theta)=D_{i,j}^{(l)}$.

