---
title: 神经网络的拟合
tags: Machine Learning
categories:
  - Machine Learning
  - AndrewNg
date: 2019-10-21 17:05:22
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

### Backpropagation Algorithm

`Backpropagation` is neural-network terminology for minimizing our cost function, just like what we were doing with gradient descent in logistic and linear regression. Our goal is to compute:

$\mathop{\textrm{min}}_\Theta J(\Theta)$

That is, we want to minimize our cost function $J$ using an optimal set of parameters in theta. In this section we'll look at the equations we use to compute the partial derivative of $J(\Theta)$:

$\frac{\partial}{\partial\Theta_{i,j}^{(l)}}J(\Theta)$

To do so, we use the following algorithm:

![img](https://tva1.sinaimg.cn/large/006y8mN6gy1g7y3ekmyjmj30om0d9gs6.jpg)

---

#### Backpropagation Algorithm

Given training set ${(x^{(1)},y^{(1)}),...,(x^{(m)},y^{(m)})}$

* Set $\Delta_{i,j}^{(l)}:=0$ for all $l,i,j$, (hence you end up having a matrix full of zeros)

(👇 Begin For loop: 👇)

**For** training example $t=1\textrm{ to } m$:

1. Set $a^{(1)}:=x^{(t)}$
2. Preform forward propagation to compute $a^{(l)}$ for $l=2,3,...,L$

![img](https://tva1.sinaimg.cn/large/006y8mN6gy1g7y3n2yqdkj30d8074q53.jpg)

3. Using $y^{(t)}$, compute $\delta^{(L)}=a^{(L)}-y^{(t)}$

Where $L$ is our total number of layers and $a^{(L)}$ is the vector of outputs of the activation units for the last layer.

So, our `error values` for the last layer are simply the differences of our actual results in the last layer and the correct outputs in $y$.

To get the delta values of the layers before the last layer, we can use an equation that steps us back from right to left:

4. Compute $\delta^{(L-1)},\delta^{(L-2)},...,\delta^{(2)}$ using $\delta^{(l)}=\big((\Theta^{(l)})^T\delta^{(l+1)}\big).*a^{(l)}.*(1-a^{(l)})$

【Note】: "$.* $" above are the element-wise multiplications in Octave/MATLAB.

The delta values of layer $l$ are calculated by multiplying the delta values in the next layer with the theta matrix of layer $l$.

We then element-wise multiply that with a function called $g'$, or g-prime, which is the derivative of the activation function $g$ evaluated with the input values given by $z^{(l)}$.

The g-prime derivative terms can also be written out as: $g'(z^{(l)})=a^{(l)}.*(1-a^{(l)})$

5. $\Delta_{i,j}^{(l)}:=\Delta_{i,j}^{l}+a_j^{(l)}\delta^{(l+1)}$ or with vectorization, $\Delta^{(l)}:=\Delta^{(l)}+\delta^{(l+1)}(a^{(l)})^T$

(👆 End For 👆)

Hence we update our new $\Delta$ matrix.

* $D_{i,j}^{(l)}:=\frac{1}{m}\big(\Delta_{i,j}^{(l)}+\lambda\Theta_{i,j}^{(l)}\big)$, if $j\not=0$;

* $D_{i,j}^{(l)}:=\frac{1}{m}\Delta_{i,j}^{(l)}$ if $j=0$.

The capital-delta matrix $D$ is used as an `accumulator` to add up our values as we go along and eventually compute our partial derivate.

Thus we get $\frac{\partial}{\partial\Theta_{i,j}^{(l)}}J(\Theta)=D_{i,j}^{(l)}$.

---

#### Backpropagation Intuition

Recall that the cost function for a neural network is:
$$
J(\Theta)=-\frac{1}{m}\sum_{i=1}^{m}\sum_{k=1}^{K}\Big[y_k^{(t)}\log\big(h_\Theta(x^{(t)})\big)_k+(1-y_k^{(t)})\log\big(1-h_\Theta(x^{(t)})\big)_k\Big]+\frac{\lambda}{m}\sum_{l=1}^{L-1}\sum_{i=1}^{s_l}\sum_{j=1}^{s_l+1}\Big(\Theta_{j,i}^{(l)}\Big)^2
$$
If we consider simple non-multiclass classification ($K=1$) and disregard regularization, the cost is copmputed with:
$$
cost(t) = y^{(t)}\log\big(h_\Theta(x^{(t)})\big)+(1-y^{(t)})\log\big(1-h_\Theta(x^{(t)})\big)
$$
Intuitively, $\delta_j^{(l)}$ is the "error" for $a_j^{(l)}$ (unit $j$ in layer $l$). More formally, the delta values are actually the derivative of the cost function:
$$
\delta_j^{(l)}=\frac{\partial}{\partial z_j^{(l)}}cost(t)
$$
Recall that our derivative is the slope of a line tangent to the cost function, so the steeper the slope the more incorrect we are. Let us consider the following neural network below and see how we could calculate some $\delta_j^{(l)}$:

![img](https://tva1.sinaimg.cn/large/006y8mN6gy1g8072ftfjzj30k00b9wi3.jpg)

In the image above, to calculate $\delta_2^{(2)}$ , we multiply the weights $\Theta_{12}^{(2)}$ and $\Theta_{22}^{(2)}$ by their respective $\delta$ values found to the right of each edge. So we get $\delta_2^{(2)}=\Theta_{12}^{(2)}\times\delta_1^{(3)}+\Theta_{22}^{(2)}\times\delta_2^{(3)}$. To calculate every single possible $\delta_j^{(l)}$, we could start from the right of our diagram. We can think of our edges as our $\Theta_{ij}$. Going from right to left, to calculate the value of $\delta_j^{(l)}$, you can just take the over all sum of each weight times the $\delta$ it is coming from. Hence, another example would be $\delta_2^{(3)}=\Theta_{12}^{(3)}\times\delta_1^{(4)}$.

## Backpropagation in Practice

### Unrolling Parameters

With neural networks, we are working with sets of matrices:
$$
\begin{array}{lll} \Theta^{(1)}, \Theta^{(2)}, \Theta^{(3)}, \dots \newline D^{(1)}, D^{(2)}, D^{(3)}, \dots \end{array}
$$
In order to use optimizing function such as `fminunc()`, we will want to *unroll* all the elements and put them into one long vector:

```octave
thetaVector = [ Theta1(:); Theta2(:); Theta3(:) ];
deltaVector = [ D1(:); D2(:); D3(:) ];
```

If the dimensions of Theta1 is 10x11, Theta2 is 10x11 and Theta3 is 1x11, then we can get back our original matrices from the "unrolled" versions as follows:

```octave
Theta1 = reshape(thetaVector(1:110),10,11)
Theta2 = reshape(thetaVector(111:220),10,11)
Theta3 = reshape(thetaVector(221:231),1,11)
```

To summarize:

![img](https://tva1.sinaimg.cn/large/006y8mN6gy1g80ervs2l4j30ey06aq57.jpg)

### Gradient Checking

Gradient checking will assure that our backpropagation works as intended. We can approximate the derivative of our cost function with:
$$
\frac{\partial}{\partial\Theta}J(\Theta) \approx \frac{J(\Theta+\epsilon)-J(\Theta-\epsilon)}{2\epsilon}
$$
A small value for $\epsilon$ such as $\epsilon=10^{-4}$, guarantees that the math works out properly. If the value for $\epsilon$, we can end up with numerical problems.

With multiple theta matrices, we can approximate the derivative with respect to $\Theta_j$ (where we get $j$ from 1 to n, for each one) as follows:
$$
\frac{\partial}{\partial\Theta_j}J(\Theta) \approx \frac{J(\Theta_1,...,\Theta_j+\epsilon,...,\Theta_n)-J(\Theta_1,...,\Theta_j-\epsilon,...,\Theta_n)}{2\epsilon}
$$
Hence, we are only adding or subtracting epsilon to the $\Theta_j$ matrix.

In octave we can do it as follows:

```octave
epsilon = 1e-4;
for i = 1 : n
	thetaPlus = theta;
	thetaPlus(i) += epsilon;
	thetaMinus = theta;
	thetaMinus(i) += epsilon;
	gradApprox(i) = (J(thetaPlus) - J(thetaMinus)) / (2*epsilon);
end
```

We previously saw how to calculate the deltaVector. So once we compute our `gradApprox` vector, we can check that `gradApprox ≈ deltaVector`. 

Once we have verified **once** that your backpropagation algorithm is correct, we don't need to compute gradApprox again. The code to compute gradApprox can be very slow. So we guess it's better to turn off or disable the codes for gradient checking.

### Randoom Initialization

Initializing all theta weights to zero does not work with neural networks. When we backpropagate, all nodes will update to the same value repeatedly. Instead we can randomly initialize our weights for our $\Theta$  matrices using the following method:

![img](https://tva1.sinaimg.cn/large/006y8mN6gy1g84m3eabzfj30fb07qjsk.jpg)

Hence, we initialize each $\Theta_{ij}^{(l)}$ to a random value between $[-\epsilon,\epsilon]$.  Using the above formula guarantees that we get the desired bound. The same procedure applies to all the $\Theta$'s. 

Below is some working code implement.

```octave
# If the dimensions of Theta1 is 10x11, Theta2 is 10x11 and Theta3 is 1x11.

Theta1 = rand(10,11) * (2 * INIT_EPSILON) - INIT_EPSILON;
Theta2 = rand(10,11) * (2 * INIT_EPSILON) - INIT_EPSILON;
Theta3 = rand(1,11) * (2 * INIT_EPSILON) - INIT_EPSILON;
```

`rand(x,y)` is just a function in octave that will initialize a matrix of random real numbers between 0 and 1. 

(Note: the epsilon used above is unrelated to the epsilon from Gradient Checking)

### Putting It Together

First, pick a network architecture; choose the layout of your neural network, including how many hidden units in each layer and how many layers in total you want to have.

- Number of input units = dimension of features $x^{(i)}$
- Number of output units = number of classes
- Number of hidden units per layer = usually more the better (must balance with cost of computation as it increases with more hidden units)
- Defaults: 1 hidden layer. If you have more than 1 hidden layer, then it is recommended that you have the same number of units in every hidden layer.

**Training a Neural Network**

1. Randomly initialize the weights
2. Implement forward propagation to get $h_\Theta(x^{(i)})$ for any $x^{(i)}$
3. Implement the cost function
4. Implement backpropagation to compute partial derivatives
5. Use gradient checking to confirm that your backpropagation works. Then disable gradient checking.
6. Use gradient descent or a built-in optimization function to minimize the cost function with the weights in theta.

When we perform forward and back propagation, we loop on every training example:

```
for i = 1:m,
   Perform forward propagation and backpropagation using example (x(i),y(i))
   (Get activations a(l) and delta terms d(l) for l = 2,...,L
```

The following image gives us an intuition of what is happening as we are implementing our neural network: 

![img](https://tva1.sinaimg.cn/large/006y8mN6gy1g84ozcnlokj30eu08aq5g.jpg)

Ideally, we want $h_\Theta(x^{(i)})\approx y^{(i)}$. This will minimize our cost function. However, keep in mind that $J(\Theta)$  is not convex and thus we can end up in a local minimum instead. 

