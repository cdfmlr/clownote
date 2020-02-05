---
title: 维数约减
tags: Machine Learning
categories:
  - Machine Learning
  - AndrewNg
date: 2019-11-13 16:50:27
---


# Notes of Andrew Ng’s Machine Learning —— (14) Dimensionality Reduction

## Motivation

### Data Compression

*Dimensionality reduction* is another type of unsupervised learning problem.

There are a couple of different reasons why one might want to do dimensionality reduction. One is **data compression** which  not only allows us to compress the data and have it therefore use up less computer memory or disk space, but it will also allow us to speed up our learning algorithms.

What we will do in data compression is reduce data from a high dimensionality to a lower one.

For example:

![image-20191107112251112](https://tva1.sinaimg.cn/large/006y8mN6ly1g8pbajmgl3j30mt0byq68.jpg)

![屏幕快照 2019-11-07 11.24.44](https://tva1.sinaimg.cn/large/006y8mN6gy1g8pbaeml8oj30p30brgt7.jpg)

As we see, to make dimensionality reduce, intuitionally , we projects the high-D on a lower-D.

In the more typical example of dimensionality reduction we might have a thousand dimensional data that we might want to reduce to let's say a hundred dimensional.

Generally, suppose we apply `dimensionality reduction` to a dataset of $m$ examples $\{x^{(1)},x^{(2)},\cdots,x^{(m)}\}$, where $x^{(i)}\in\R^n$. As a result of this, we will get out a lower dimensional dataset $\{z^{(1)},z^{(2)},\cdots,z^{(m)}\}$ of $m$ examples where $z^{(i)}\in\R^k$ for some value of $k$ and $k\le n$.

### Data Visualization

We can also utilize dimensionality reduction for data visualization.

For a lot of machine learning applications, it really helps us to develop effective learning algorithms, if we can understand our data better. And visualizing the data is a useful in this.

Let's say we have collected a large data set, which means we have a set of $x^{(i)}\in\R^n$ where $n$ is very large, and we can hardly visualize it because, you know, actually we can only draw a plot in or less than 3 dimension. In this case, what we need to do is dimensionality reduction.

For example, we've collected a large data set of many statistics about different countries. we may have a huge data set like this:

![屏幕快照 2019-11-07 12.32.30](https://tva1.sinaimg.cn/large/006y8mN6ly1g8pd8wo33nj30po0dbn3e.jpg)

To visualize this data, what we can do is reduce the dimensionality from 50-D to 2-D, and then we can plot a 2-D plot to understand our data better.

![屏幕快照 2019-11-07 12.31.49](https://tva1.sinaimg.cn/large/006y8mN6ly1g8pdanhskoj30nq0c0did.jpg)

![image-20191107123745407](https://tva1.sinaimg.cn/large/006y8mN6ly1g8pde507hrj30ox0bhdiw.jpg)

To wrap up, suppose you have a dataset $\{x^{(1)},x^{(2)},\cdots,x^{(m)}\}$ where $x^{(i)}\in\R^n$. In order to visualize it, we apply dimensionality reduction and get $\{z^{(1)},z^{(2)},\cdots,z^{(m)}\}$ where $z^{(i)}\in\R^k$. And we usual make $k = 2$ or $k = 3$ (since we can plot 2D or 3D data but don’t have ways to visualize higher dimensional data).

## Principal Component Analysis

For the problem of dimensionality reduction, the most commonly used algorithm is something called *principal component analysis* (PCA).

#### PCA problem formulation

![image-20191107165349198](https://tva1.sinaimg.cn/large/006y8mN6gy1g8pksu0z5nj30nu07mn1t.jpg)

* Reduce form 2-dimension to 1-dimension: 

  Find a direction (a vector $u^{(1)}\in\R^n$) onto which to project the data so as to minimize the projection error.

* Reduce form n-dimension to k-dimension:

  Find $k$ vectors $u^{(1)},u^{(2)},\cdots,u^{(k)}$ onto which to project the data, so as to minimize the projection error.

Notice that PCA is not linear regression! In the linear regression, we minimize the vertical length  between the data point and our hypothesis line, while in the PCA, we minimize the distance between the data point and its projected point:

![image-20191107171638816](https://tva1.sinaimg.cn/large/006y8mN6ly1g8plgct2i6j31iy0oywjp.jpg)

#### PCA Algorithm

##### Data preprocessing

Training set: $x^{(1)},x^{(2)},\cdots,x^{(m)}$

Preprocessing (feature scaling & mean normalization):

- $$
  \mu_j=\frac{1}{m}\sum_{i=1}^m x_j^{(i)},\qquad s_j=\textrm{standard deviation of feature $j$}
  $$

- Replace each $x_j^{(i)}$ with $\frac{x_j-\mu_j}{s_j}$

##### Reduce data from $n$-dimensions to $k$-dimensions

1. Compute `convariance matrix` (notated a big Sigma, notice that it's different from a sum notation):
   $$
   \Sigma = \frac{1}{m}\sum_{i=1}^n(x^{(i)})(x^{(i)})^T
   $$

2. Compute `eigenvectors` of matrix $\Sigma$:

   ```octave
   [U, S, V] = svd(Sigma);
   ```

3. Get from `svd`:
   $$
   U = \left[\begin{array}{cccc}
   | & | &  & |\\
   u^{(1)} & u^{(2)} & \cdots & u^{(n)}\\
   | & | &  & |
   \end{array}\right]
   \in \R^{n\times n}
   \Rightarrow 
   U_{reduce}=\left[\begin{array}{cccc}
   | & | &  & |\\
   u^{(1)} & u^{(2)} & \cdots & u^{(k)}\\
   | & | &  & |
   \end{array}\right]
   $$

4. Make $x\in\R^n\to z\in\R^k$:
   $$
   z = U_{reduce}^Tx
   =\left[\begin{array}{ccc}
   -- & (u^{(1)})^T & --\\
    & \vdots & \\ 
   -- & (u^{(k)})^T & --\\
   \end{array}\right]x
   $$
   

This does do the right thing of minimizing this square projection error although the  mathematical proof of that is beyond the scope of this course.

Summary:

After mean normalization (ensure every feature has zero mean) and optionally feature scaling:

```octave
Sigma = 1/m * X' * X;
[U, S, V] = svd(Sigma);

Ureduce = U(:, 1:K);
Z = X * Ureduce;
```

## Applying PCA

### Reconstruction from Compressed Representation

With PCA, we compressed data from n-dimension to a lower k-dimension. There should be a way to go back from the compressed representation to an approximation of our original high-dimensional data. We call this way *reconstruction*.

Recall that our PCA is working as $z= U_{reduce}^Tx$.

To reconstruction, what we will do is:
$$
x_{approx}=U_{reduce}z
$$
It makes $z\in\R^k \to x_{approx}\in\R^n$. The $x_{approx}$ will be close to $x$, but we can hardly expect $x=x_{approx}$.

![image-20191110215011122](https://tva1.sinaimg.cn/large/006y8mN6gy1g8ta88gafkj30oz0djaeo.jpg)

Previously, we said that PCA chooses a direction $u^{(1)},\cdots,u^{(k)}$ onto which to project the data so as to minimize the (squared) projection error. With our new defined $x_{approx}$, another way to say the same is that PCA tries to minimize:
$$
\frac{1}{m}\sum_{i=1}^{m}||x^{(i)}-x_{approx}^{(i)}||^2
$$

### Choosing the $k$ (number of principal components)

About PCA, we can see:

* Average squared projection error: $\frac{1}{m}\sum_{i=1}^m||x^{(i)}-x_{approx}^{(i)}||^2$
* Total variation in the data: $\frac{1}{m}\sum_{i=1}^{m}||x^{(i)}||^2$

Typically, choose $k$ to be smallest value so that:
$$
\frac{\frac{1}{m}\sum_{i=1}^m||x^{(i)}-x_{approx}^{(i)}||^2}{\frac{1}{m}\sum_{i=1}^{m}||x^{(i)}||^2}\le0.01
$$
We call it "99% of variance is retained".

We can also choose other numbers instead of the usual $0.01$, in practice, $0.01\sim0.05$ is all capable.

The algorithm utilized for $k$ choosing is that:

> Try PCA with $k=1,\cdots,n$:
>
> Compute $U_{reduce},z^{(1)},\cdots,z^{(m)},x_{approx}^{(1)},\cdots,x_{approx}^{m}$;
>
> Check if $\frac{\frac{1}{m}\sum_{i=1}^m||x^{(i)}-x_{approx}^{(i)}||^2}{\frac{1}{m}\sum_{i=1}^{m}||x^{(i)}||^2}\le0.01$?

In octave, we can implement it as:

1. `[U, S, V] = svd(Sigma)`, after running we can get a `S` that is useful here:

2. Pick smallest value of $k$ for which (99% of variance retained for example)
   $$
   \frac{\sum_{i=1}^k S_{ii}}{\sum_{i=1}^m S_{ii}}\ge0.99
   $$
   

### Advice for Applying PCA

####  Supervised Learning speedup

In supervised learning, we have data like this:
$$
(x^{(1)},y^{(1)}),(x^{(2)},y^{(2)}),\cdots,(x^{(m)},y^{(m)})
$$
We can **extract inputs** by:

- Unlabled dataset: $x^{(1)},x^{(2)},\cdots,x^{(m)}\in \R^n$
- Applying PCA: $z^{(1)},z^{(2)},\cdots,z^{(m)}\in \R^k$, where $k$ is lower than $n$

Then we get **new training set**:
$$
(z^{(1)},y^{(1)}),(z^{(2)},y^{(2)}),\cdots,(z^{(m)},y^{(m)})
$$
Note: Mapping $x^{(i)}\to z^{(i)}$ should be defined by running PCA only on the **training set** . This mapping can be applied as well to the examples $x_{cv}^{(i)}$ and $x_{test}^{(i)}$ in the cross validation and test sets.

#### Application of PCA

- Compression

  - Reduce memory/disk needed to store data
  - Speed up learning algorithm

  In this case, we should choose $k$ by `% of  variance retained`.

- Visualization

  In this case, $k=2$ or $k=3$

#### Bad use of PCA: To prevent overfitting

> Use $z^{(i)}$ instead of $x^{(i)}$ to reduce the number of features to $k<n$.
>
> Thus, fewer features, less likely to overfit.

👆 This is a BAD use of PCA.

This might work OK, but isn't a good way to address overfitting. Use regularization instead:

$$
\min_\theta\frac{1}{2m}\sum_{i=1}^m(h_\theta(x^{(i)})-y^{(i)})^2+\frac{\lambda}{2m}\sum_{j=1}^{n}\theta_j^2
$$

#### PCA or not

PCA is sometimes used where it shouldn't be, here is an example:

When designing a ML system, we wrote down this steps:

1. Get training set $\{(x^{(1)},y^{(1)}),\cdots,(x^{(m)},y^{(m)})\}$
2. Run PCA to reduce $x^{(i)}$ in dimension to get $z^{i}$
3. Train logistic regression on $\{(z^{(1)},y^{(1)}),\cdots,(z^{(m)},y^{(m)})\}$
4. Test on test set: Map $x_{test}^{(i)}$ to $z_{test}^{(i)}$. Run $h_\theta(z)$ on $\{(z_{test}^{(1)},y^{(1)}),\cdots,(z_{test}^{(m)},y^{(m)})\}$

But before doing this, we should think: How about the whole thing without using PCA?

Before implementing PCA, first try running whatever you want to do with the original/raw data $x^{(i)}$. Only if that doesn't do what you want, then implement PCA and consider using $z^{(i)}$.

