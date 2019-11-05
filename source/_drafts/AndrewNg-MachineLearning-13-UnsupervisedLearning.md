---
title: AndrewNg-MachineLearning-13-UnsupervisedLearning
tags: Machine Learning
categories:
  - Machine Learning
  - AndrewNg
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
2. Cluster assignment: going through each of the examples, for each of data dots depending on which cluster centroid it's closer to, one point is going to be assigned to one of the K cluster centroids (color them into the same color, illustratingly).
3. Move centroid:  take the K cluster centroids, and we are going to move them to the average of the points colored the same colour.

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
\qquad \textrm{for $i=1$ to $m$:}\\
\qquad\qquad c^{(i)} := k \ \textrm{ s.t. } \min_k||x^{(i)}-\mu_k||^2 \\
\qquad\qquad \textrm{/* set $ c^{(i)}$ the index (from $1$ to $K$) of cluster centroid closest to $x^{(i)}$ */}\\
\qquad \textrm{for $k=1$ to $K$:}\\
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

