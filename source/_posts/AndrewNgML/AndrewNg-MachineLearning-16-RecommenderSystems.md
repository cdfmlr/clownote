---
categories:
- Machine Learning
- AndrewNg
date: 2019-12-05 21:21:26
tags: Machine Learning
title: 推荐系统
---


# Notes of Andrew Ng’s Machine Learning —— (16) Recommender Systems

## Predicting Movie Ratings

### Problem Formulation

Example: Predicting movies using zero to five stars.

Here we got some ratings for some movies given by  different users, where a `?` means this use not rated that movie:

| Movie                | Alice(1) | Bob(2) | Carol(3) | Dave(4) |
| -------------------- | -------- | ------ | -------- | ------- |
| Love at last         | 5        | 5      | 0        | 0       |
| Romance forever      | 5        | ?      | ?        | 0       |
| Cute puppies of love | ?        | 4      | 0        | ?       |
| Nonstop car chases   | 0        | 0      | 5        | 4       |
| Swords vs. karate    | 0        | 0      | 5        | ?       |

Notation:

- $n_u$ = number of users
- $n_m$ = number of movies
- $r(i,j)=1$ if user $j$ has rated movie $i$
- $y^{(i,j)}$ = rating given by user $j$ to movie $i$ (defined only if $r(i,j)=1$)

In this example,  $n_u=4$ and $n_m=5$.We can see that the first three movies is somewhat romantic where the last two is action movies. And we know that our Alice and Bob is more interested in romance  movies so they may give a higher (say, 4 or 5) rate to they  no watched *Cute pupies of love* and *Romance forever*, but they may give 0 to *Nonstop car chases* and *Sword vs. karate*. And Carol and Dave will behave  on the contrary.

### Content Based Recommendations

We can asume we have a set of $x$ measures the degree to the kind of the movie.

![屏幕快照 2019-11-26 16.04.26](https://tva1.sinaimg.cn/large/006y8mN6gy1g9bi5bv4etj30nz06lac1.jpg)

We can bulid a model like this: for each user $j$, learn a parameter $\theta^{(j)}\in\R^3$. Predict user $j$ as rating movie $i$ with $(\theta^{(j)})^Tx^{(i)}$ stars.

Here is what we will do:

- $r(i,j)=1$ if user $j$ has rated movie $i$ ($0$ otherwise)
- $y^{(i,j)}$ = rating given by user $j$ to movie $i$ (if defined)

- $\theta^{(j)}$ = parameter vector for user $j$
- $x^{(i)}$ = feature vector for movie $i$

For User $j$, movie $i$, predicted rating: $(\theta^{(j)})^T(x^{(i)})$

So our **optimization objective** is:

To learn $\theta^{(j)}$ (parameter for a single user $j$):
$$
\min_{\theta^{(j)}}\sum_{i:r(i,j)=1}\left((\theta^{(j)})^Tx^{(i)}-y^{(i,j)}\right)^2+\frac{\lambda}{2}\sum_{k=1}^n \left(\theta_k^{(j)}\right)^2
$$
To learn $\theta^{(1)},\theta^{(2)},\cdots,\theta^{(n_u)}$ (for all users):
$$
\min_{\theta^{(1)},\cdots,\theta^{(n_u)}}
\sum_{j=1}^{n_u}\sum_{i:r(i,j)=1}\left((\theta^{(j)})^Tx^{(i)}-y^{(i,j)}\right)^2 +
\frac{\lambda}{2}\sum_{j=1}^{n_u}\sum_{k=1}^n \left(\theta_k^{(j)}\right)^2
$$
We can use a gradient descent to solve it
$$
\begin{array}{l}
Repeat\quad\{\\
\qquad \theta_0^{(j)}:=\theta_0^{(j)}-\alpha\sum_{i:r(i,j)=1} \big((\theta^{(j)})^T(x^{(i)})-y^{(i,j)}\big)x_0^{(i)}\\
\qquad \theta_k^{(j)}:=\theta_k^{(j)}-\alpha\Big[\Big(\sum_{i:r(i,j)=1}\big((\theta^{(j)})^T(x^{(i)})-y^{(i)}\big)x_k^{(i)}\Big)+\lambda\theta_k^{(j)}\Big]\qquad (\textrm{for } k \neq 0)\\
\}
\end{array}
$$

## Collaborative Filtering

### Collaborative Filtering

In many conditions, we have no idea of what features to use, so we need this algtorithm that is called *Collaborative Filtering* to help us **learn the features**.

Here is a example:

![屏幕快照 2019-11-28 14.55.32](https://tva1.sinaimg.cn/large/006y8mN6ly1g9drfoeqaoj30lo0avacu.jpg)

Given rates of movies by people and how this people like different kinds of movies ($\theta$), we try to get what kind of a movie is likely to be ($x$).

**Optimization algorithm**

Given $\theta^{(1)},\theta^{(2)},\cdots,\theta^{(n_u)}$, to learn $x^{(i)}$:
$$
\min_{x^{(i)}}\frac{1}{2}\sum_{i:r(i,j)=1}\left((\theta^{(j)})^Tx^{(i)}-y^{(i,j)}\right)^2+\frac{\lambda}{2}\sum_{k=1}^n \left(x_k^{(i)}\right)^2
$$
Given $\theta^{(1)},\theta^{(2)},\cdots,\theta^{(n_u)}$, to learn $x^{(1)},\cdots,x^{(n_m)}$:
$$
\min_{x^{(1)},\cdots,x^{(n_m)}}\frac{1}{2}
\sum_{i=1}^{n_m}\sum_{i:r(i,j)=1}\left((\theta^{(j)})^Tx^{(i)}-y^{(i,j)}\right)^2 +
\frac{\lambda}{2}\sum_{i=1}^{n_m}\sum_{k=1}^n \left(x_k^{(i)}\right)^2
$$
**Collaborative filtering**

So if we knew the features, we can learn the parameters theta for different users. If our users are willing to give us parameters, then we can estimate features for the different movies. 

So this is kind of a chicken and egg problem. Which comes first? If we can get the thetas, we can know the xs. If we have the xs, we can learn the thetas.

What we can do is in fact **randomly guess** some value of the thetas. Now based on the initial random guess for the thetas, we can then go ahead and use the procedure that we just talked about in order to learn features for different movies. Then we get better thetas by using the new xs. Then another set of better xs, ... Keep on doing this, it can finally coverage.

![屏幕快照 2019-11-28 15.20.59](https://tva1.sinaimg.cn/large/006y8mN6ly1g9ds8xkjatj30ob0bd0w0.jpg)

### Collaborative Filtering Algorithm

Here is what we do in the previous content:

> Given $x^{(1)},\cdots,x^{(n_m)}$, estimate $\theta^{(1)},\cdots,\theta^{(n_u)}$:
> $$
> \min_{\theta^{(1)},\cdots,\theta^{(n_u)}}
> \sum_{j=1}^{n_u}\sum_{i:r(i,j)=1}\left((\theta^{(j)})^Tx^{(i)}-y^{(i,j)}\right)^2 +
> \frac{\lambda}{2}\sum_{j=1}^{n_u}\sum_{k=1}^n \left(\theta_k^{(j)}\right)^2
> $$
> Given $\theta^{(1)},\cdots,\theta^{(n_u)}$, estimate $x^{(1)},\cdots,x^{(n_m)}$:
> $$
> \min_{x^{(1)},\cdots,x^{(n_m)}}\frac{1}{2}
> \sum_{i=1}^{n_m}\sum_{i:r(i,j)=1}\left((\theta^{(j)})^Tx^{(i)}-y^{(i,j)}\right)^2 +
> \frac{\lambda}{2}\sum_{i=1}^{n_m}\sum_{k=1}^n \left(x_k^{(i)}\right)^2
> $$
> We randomly initialize the parameters and go back and forth between the x's and the thetas, to get the objective.

There is a more efficient way to do so:

Minimizing $x^{(1)},\cdots,x^{(n_m)}$ and $\theta^{(1)},\cdots,\theta^{(n_u)}$ simultaneously:
$$
J(x^{(1)},\cdots,x^{(n_m)},\theta^{(1)},\cdots,\theta^{(n_u)})=
\frac{1}{2}
\sum_{(i,j):r(i,j)=1}\left((\theta^{(j)})^Tx^{(i)}-y^{(i,j)}\right)^2+
\frac{\lambda}{2}\sum_{i=1}^{n_m}\sum_{k=1}^n \left(x_k^{(i)}\right)^2+
\frac{\lambda}{2}\sum_{i=1}^{n_m}\sum_{k=1}^n \left(x_k^{(i)}\right)^2
$$

$$
\min_{\begin{array}{c}x^{(1)},\cdots,x^{(n_m)}\\\theta^{(1)},\cdots,\theta^{(n_u)}\end{array}}
J(x^{(1)},\cdots,x^{(n_m)},\theta^{(1)},\cdots,\theta^{(n_u)})
$$

Put everything together, we get the **collaborative filtering algorithm**:

1. Initialize $x^{(1)},\cdots,x^{(n_m)},\theta^{(1)},\cdots,\theta^{(n_u)}$ to small random values

2. Minimize $J(x^{(1)},\cdots,x^{(n_m)},\theta^{(1)},\cdots,\theta^{(n_u)})$ using gradient descent (or an advanced optimization algorithm).

   E.g. for every $j=1,...,n_u,i=1,...,n_m$:
   $$
   x_k^{(i)}:=x_k^{(i)}-\alpha\Big[\Big(\sum_{j:r(i,j)=1}\big((\theta^{(j)})^T(x^{(i)})-y^{(i)}\big)\theta_k^{(j)}\Big)+\lambda x_k^{(i)}\Big]
   $$
   
   $$
   \theta_k^{(j)}:=\theta_k^{(j)}-\alpha\Big[\Big(\sum_{i:r(i,j)=1}\big((\theta^{(j)})^T(x^{(i)})-y^{(i)}\big)x_k^{(i)}\Big)+\lambda\theta_k^{(j)}\Big]
   $$

3. For a user with parameters $\theta$ and a movie with (learned) features $x$, predict a star rating of $\theta^Tx$.

## Low Rank Matrix Factorization

### Vectorization: Low Rank Matrix Factorization

To vectorize the collaborative filtering algorithm, we are going to put xs/thetas together:

So, let:
$$
X = \left[\begin{array}{ccc}
- & (x^{(1)})^T & - \\
  & \vdots & \\
- & (x^{(n_m)})^T & - \\
\end{array}\right],
\qquad
\Theta = \left[\begin{array}{ccc}
- & (\theta^{(1)})^T & - \\
  & \vdots & \\
- & (\theta^{(n_u)})^T & - \\
\end{array}\right]
$$
Then, we can get prediction by:
$$
X\Theta^T= \left[\begin{array}{ccccc} (x^{(1)})^T(\theta^{(1)}) & \ldots & (x^{(1)})^T(\theta^{(n_u)})\\ \vdots & \ddots & \vdots \\ (x^{(n_m)})^T(\theta^{(1)}) & \ldots & (x^{(n_m)})^T(\theta^{(n_u)})\end{array}\right]
$$
And this algorithm is called *Low Rank Matrix Factorization*.

#### Finding related movies

For each product (e.g. movie) $i$, we learn a feature vector $x^{(i)}\in\R^n$. We can find a movie $j$ that is most related to movie $i$ by finding a $j$ that has:
$$
\mathop{\textrm{smallest}} ||x^{(i)}-x^{(j)}||.
$$

### Implementational Detail: Mean Normalization

If we use what we talked about above, given a user who ranked no movies, than, our recommend system will output a all zeros result, so we can recommend nothing to this user. We never hope this, so we do a mean normalization:
$$
\mu_i=\mathop{\textrm{average}} y^{(i,:)}
$$

$$
Y_i = Y_i-\mu_i
$$

For user $j$, on movie $i$, we predict:
$$
\left(\Theta^{(j)}\right)^T\left(x^{(i)}\right)+\mu_i
$$
Then we can get a set of "average" recommendation  for a no-ranked user.

We talked about mean normalization. However, unlike some other applications of feature scaling, we did not scale the movie ratings by dividing by the range (max – min value). This is because all the movie ratings are already comparable (e.g., 0 to 5 stars), so they are already on similar scales.