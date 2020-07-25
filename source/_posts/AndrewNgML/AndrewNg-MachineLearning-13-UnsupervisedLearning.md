---
categories:
- Machine Learning
- AndrewNg
date: 2019-11-07 10:51:48
tags: Machine Learning
title: 无监督学习
---


# Notes of Andrew Ng’s Machine Learning —— (13) Unsupervised Learning

## Clustering

### Unsupervised Learning: Introduction

In supervised learning, we are given a set of labeled training set ( ($(x,y)$ given)) to fit a hypothesis to it:

![image-20191105144318970](https://tva1.sinaimg.cn/large/006y8mN6gy1g8n5s7zmffj30lv0ca40u.jpg)

In contrast, in the unsupervised learning problems, we are given data that does not have any labels associated with it ($x$ only, no $y$):

 ![屏幕快照 2019-11-05 14.49.05](https://tva1.sinaimg.cn/large/006y8mN6gy1g8n62mi54pj30lw0catay.jpg)

The slide above shows that here's a set of points add in no labels. So, in unsupervised learning what we do is we give this sort of unlabeled training set to an algorithm and we just ask the algorithm find some structure in the data for us. 

Given this data set one type of structure we might have an algorithm find is that it looks like this data set has points grouped into two separate clusters (drawn in green) and so an algorithm that finds **clusters** like the ones I've just circled is called a *clustering algorithm*.

![image-20191105150106356](https://tva1.sinaimg.cn/large/006y8mN6gy1g8n6ap2y9bj30lq0d7135.jpg)



### K-Means Algorithm

> In the clustering problem we are given an unlabeled data set and we would like to have an algorithm automatically group the data into coherent subsets or into coherent clusters for us.

The *K-Means Algorithm* is  by far the most popular and widely used clustering algorithm.

Given an unlabeled data set to group (cluster) them into K (let's say two, for example) clusters, what the `K-Means Algorithm` do is:

1. Randomly initialize two points, called the cluster centroids.
2. Cluster assignment step: going through each of the examples, for each of data dots depending on which cluster centroid it's closer to, one point is going to be assigned to one of the K cluster centroids (color them into the same color, illustratingly).
3. Move centroid step:  take the K cluster centroids, and we are going to move them to the average of the points colored the same colour.

We keep on move centroid then redo a cluster assignment. Doing this looply until the cluster centroids not change any further (i.e. the K-Means has converged). And, it's done a good job finding the clusters in the data.

![1572942743912](https://tva1.sinaimg.cn/large/006y8mN6ly1g8n8yx2xiwg30hy0cadi8.gif)

![屏幕快照 2019-11-05 16.23.33](https://tva1.sinaimg.cn/large/006y8mN6ly1g8n98yihsoj30us0c8go8.jpg)

#### K-means algoithm

Input: 

- $K$ (number of clusters)

- $\{x^{(1)},x^{(2)},\cdots,x^{(m)}\}$ (training set)

  $x^{(i)}\in\R^n$ (drop $x_0=1$ convention)

Output:

- $K$ subsets

Algorithm:
$$
\begin{array}{l}

\textrm{Randomly initialize $K$ cluster centroids $\mu_1, \mu_2,...\mu_k \in \R^n$}\\
\textrm{Repeat }\{\\
\qquad \textrm{for $i=1$ to $m$:}\qquad\textrm{// Cluster assignment step}\\
\qquad\qquad c^{(i)} := k \ \textrm{ s.t. } \min_k||x^{(i)}-\mu_k||^2 \\
\qquad\qquad \textrm{/* set $ c^{(i)}$ the index (from $1$ to $K$) of cluster centroid closest to $x^{(i)}$ */}\\
\qquad \textrm{for $k=1$ to $K$:}\qquad\textrm{// Move centroid step}\\
\qquad\qquad \textrm{if cluster centroid $\mu_i$ has 0 points assigned to it}:\\
\qquad\qquad\qquad \textrm{eliminate that cluster centroid, continue}\\
\qquad\qquad\qquad \textrm{// end up with $K-1$ clusters}\\
\qquad\qquad \mu_k:= \textrm{average (mean) of points assigned to cluster $k$}\\
\}\\

\end{array}
$$

#### K-Means for non-separated clusters

K-Means can do well in both well-separated cluster and non-separated clusters:

![image-20191105163643613](https://tva1.sinaimg.cn/large/006y8mN6ly1g8n930vsnrj30mv09swhe.jpg)

### K-means Optimization Objective

Notations:

* $c^{(i)}$ = index of cluster ($1,2,\cdots,K$) to which example $x^{(i)}$ is currently assigned.
* $\mu_k$ = cluster centroid $k$ ($\mu_k\in\R^n$).
* $\mu_{c^{(i)}}$ = cluster centroid of cluster to which example $x^{(i)}$ has been assigned.

For example, let's say we have a $x^{(1)}$ that is currently assigned to cluster $5$, so in this case, our $c^{(1)}=5$ and $\mu_{c^{(1)}}=\mu_5$, where cluster centroid of cluster $5$ is notated as $\mu_5$. 

Optimization objective:
$$
J(c^{(1)},\cdots,c^{(m)},\mu_1,\cdots,\mu_K)=\frac{1}{m}\sum_{i=1}^{m}||x^{(i)}-\mu_{c^{(i)}}||^2
$$

$$
\min_{
\begin{array}
	{1}c^{(1)},\cdots,c^{(m)},\\
	\mu_1,\cdots,\mu_K
\end{array}}
J(c^{(1)},\cdots,c^{(m)},\mu_1,\cdots,\mu_K)
$$

Our cost function $J$  is also called **distortion**.

In the K-means algorithm, what it doing in our cluster assignment step is minimize $J$ wit $c^{(1)},\cdots,c^{(m)}$ (holding $\mu_1,\cdots,\mu_k$ fixed), and the move centroid step is minimizing the $J$ wit $\mu_1,...,\mu_k$.

### Random initialization

There is a way to random initialization our $K$ cluster centroids:

1. Should have $K<m$
2. Randomly pick $K$ training examples.
3. Set $\mu_1,\cdots,\mu_k$ equal to these $K$ examples.

i.e. we pick $k$ distinct random integers $i_1,\cdots,i_k$ from $\{1,\cdots,m\}$, set $\mu_1=x^{(i_1)},\mu_2=x^{(i_2)},\cdots,\mu_k=x^{(i_k)}$.

#### Local optima

![image-20191106161508966](https://tva1.sinaimg.cn/large/006y8mN6ly1g8oe2i8gz8j30oo0d8tb5.jpg)

Beacuse of the random initialization, we sometimes get a good cluster (get a *global optima*, like the one at the right top of the picture) and we may also get a bad one (get a *local optima*, like the two at the right bottom of the picture).

To avoid the K-means algorithm stop at a loacal optima, we can try this:
$$
\begin{array}{l}
\textrm{For $i=1$ to $100$ <or 50~1000> \{}\\
\qquad\textrm{Randomly initialize K-means.}\\
\qquad\textrm{Run K-means. Get $c^{(1)},\cdots,c^{(m)},\mu_1,\cdots,\mu_k$}\\
\qquad\textrm{Compute cost function (distortion):}\\
\qquad\qquad J(c^{(1)},\cdots,c^{(m)},\mu_1,\cdots,\mu_K)\\
\textrm{\}}\\
\textrm{pick clustering that gave lowest $J$.}
\end{array}
$$

### Choosing the Number of Clusters

The most common way to choose the number of clusters $K$ is actually to choose it by hand.

Choosing the *Elbow* number is a capable way to choose the value of $K$:

![image-20191106171612460](https://tva1.sinaimg.cn/large/006y8mN6gy1g8oftu824rj30cb0c3407.jpg)

However the elbow method is not always make sense for a condition like this:

![image-20191106171906665](https://tva1.sinaimg.cn/large/006y8mN6gy1g8ofwmrgy0j30bb08fwf9.jpg)

We can hardly find a elbow of it.

So, there is another thought to make it:

> Sometimes, you are running K-means to get clusters to use for some later/downstream purpose. Elaluate K-means based on a metric for how well it performs for that later purpose.

T-shirt sizing for example:

![image-20191106172431180](https://tva1.sinaimg.cn/large/006y8mN6gy1g8og2ak66wj30o709l0wr.jpg)

In particular, what we can do is, think about this from the perspective of the T-shirt business and ask: "Well if I have five segments, then how well will my T-shirts fit my  customers and so, how many T-shirts can I sell? How happy will my customers be?" What really makes sense, from the perspective of the T-shirt business, in terms of whether, I want to have Goer T-shirt sizes so that my T-shirts fit my customers better. Or do I want to have fewer T-shirt sizes so that I make fewer sizes of T-shirts. And I can sell them to the customers more cheaply. And so, the t-shirt selling business, that might give you a way to decide, between three clusters versus five clusters.





