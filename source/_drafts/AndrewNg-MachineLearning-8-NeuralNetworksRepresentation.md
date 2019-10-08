---
title: AndrewNg-MachineLearning-8-NeuralNetworksRepresentation
tags: Machine Learning
categories:
  - Machine Learning
  - AndrewNg
---

# Notes of Andrew Ng’s Machine Learning —— (8) Neural Networks: Representation

## Model Representation

Let's examine how we will represent a hypothesis function using neural networks.

At a very simple level, neurons are basically computational units that take inputs (**dendrites**) as electrical inputs (called "spikes") that are channeled to outputs (**axons**).

In our model, our dendrites are like the input features $x_1\cdots x_n$, and the output is the result of our hypothesis function.

In this model our $x_0$ input node is sometimes called the "bias unit." It is always equal to 1.

In neural networks, we use the same logistic function as in classification, $\frac{1}{1+e^{-\theta^Tx}}$, yet we sometimes call it a sigmoid (logistic) **activation** function. In this situation, our "theta" parameters are sometimes called "weights".

Visually, a simplistic representation looks like:
$$
\left[\begin{array}{c}
x_0\\x_1\\x_2
\end{array}\right]
\to [\quad] \to h_\theta(x)
$$
Our input nodes (layer 1), also known as the "input layer", go into another node (layer 2), which finally outputs the hypothesis function, known as the "output layer". We can have intermediate layers of nodes between the input and output layers called the "hidden layers."

In this example, we label these intermediate or "hidden" layer nodes $a^2_0 \cdots a^2_n$ and call them "activation units."

* $a_i^{(j)}$ = "activation" of unit $i$ in layer $j$
* $\Theta^{(j)}$ = matrix of weights controlling function mapping from layer $j$ to layer $j+1$

If we had one hidden layer, it would look like:
$$
\left[\begin{array}{c}x_0 \\ x_1 \\ x_2 \\ x_3\end{array}\right]\rightarrow\left[\begin{array}{c}a_1^{(2)} \\ a_2^{(2)} \\ a_3^{(2)} \\ \end{array}\right]\rightarrow h_\theta(x)
$$
The values for each of the "activation" nodes is obtained as follows:
$$
\begin{array}{r} a_1^{(2)} = g(\Theta_{10}^{(1)}x_0 + \Theta_{11}^{(1)}x_1 + \Theta_{12}^{(1)}x_2 + \Theta_{13}^{(1)}x_3) \\\\ a_2^{(2)} = g(\Theta_{20}^{(1)}x_0 + \Theta_{21}^{(1)}x_1 + \Theta_{22}^{(1)}x_2 + \Theta_{23}^{(1)}x_3) \\\\ a_3^{(2)} = g(\Theta_{30}^{(1)}x_0 + \Theta_{31}^{(1)}x_1 + \Theta_{32}^{(1)}x_2 + \Theta_{33}^{(1)}x_3) \\\\ h_\Theta(x) = a_1^{(3)} = g(\Theta_{10}^{(2)}a_0^{(2)} + \Theta_{11}^{(2)}a_1^{(2)} + \Theta_{12}^{(2)}a_2^{(2)} + \Theta_{13}^{(2)}a_3^{(2)}) \\\\ \end{array}
$$
To do a vectorized implementation of thew above functions, we're going to define a new variable $z_k^{(j)}$ that encompasses the parameters inside our $g$ function. In the previous example if we replaced by the vartizble $z$ for all the parameters we would get:
$$
\begin{array}{l}a_1^{(2)} = g(z_1^{(2)}) \\\\ a_2^{(2)} = g(z_2^{(2)}) \\\\ a_3^{(2)} = g(z_3^{(2)}) \\\\ \end{array}
$$
In other words, for layer $j=2$ and node $k$, the variable $z$ will be:
$$
z_k^{(2)} = \Theta_{k,0}^{(1)}x_0 + \Theta_{k,1}^{(1)}x_1 + \cdots + \Theta_{k,n}^{(1)}x_n
$$
The vector representation of $x$ and $z^{j}$ is:
$$
x = \begin{bmatrix}x_0 \\ x_1 \\ \vdots \\ x_n\end{bmatrix} \qquad z^{(j)} = \begin{bmatrix}z_1^{(j)} \\ z_2^{(j)} \\ \vdots \\ z_n^{(j)}\end{bmatrix}
$$
Setting $x = a^{(1)}$, we can rewrite the equation as:
$$
z^{(j)} = \Theta^{(j-1)}a^{(j-1)}
$$
We are multiplying our matrix $\Theta^{(j−1)}$ with dimensions $s_j\times (n+1)$ (where $s_j$ is the number of our activation nodes) by our vector $a^{(j-1)}$ with height $(n+1)$. This gives us our vector $z^{(j)}$ with height $s_j$. Now we can get a vector of our activation nodes for layer $j$ as follows:
$$
a^{(j)} = g(z^{(j)})
$$
Where our function g can be applied element-wise to our vector $z^{(j)}$.

We can then add a bias unit (equal to $1$) to layer $j$ after we have computed $a^{(j)}$. This will be element $a_0^{(j)}$ and will be equal to $1$. To compute our final hypothesis, let's first compute another $z$ vector:
$$
z^{(j+1)} = \Theta^{(j)}a^{(j)}
$$
We get this final $z$ vector by multiplying the next theta matrix after $\Theta^{(j−1)}$ with the values of all the activation nodes we just got. This last theta matrix $\Theta^{(j)}$ will have only **one row** which is multiplied by one column $a^{(j)}$ so that our result is a single number. We then get our final result with:
$$
h_\Theta(x)=a^{(j+1)}=g(z^{(j+1)})
$$
Notice that in this **last step**, between layer $j$ and layer $j+1$, we are doing **exactly the same thing** as we did in logistic regression. Adding all these intermediate layers in neural networks allows us to more elegantly produce interesting and more complex non-linear hypotheses.

##Examples and Intuitions

A simple example of applying neural networks is by predicting $x_1 \and x_2$, which is the logical 'and' operator and is only true if both $x_1$ and $x_2$ are $1$. The graph of our functions will look like: 
$$
\begin{align*}\begin{bmatrix}x_0 \newline x_1 \newline x_2\end{bmatrix} \rightarrow\begin{bmatrix}g(z^{(2)})\end{bmatrix} \rightarrow h_\Theta(x)\end{align*}
$$
