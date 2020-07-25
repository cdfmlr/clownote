---
categories:
- Machine Learning
- AndrewNg
date: 2019-10-26 12:37:19
tags: Machine Learning
title: 机器学习的应用建议
---


# Notes of Andrew Ng’s Machine Learning —— (10) Advice for Applying Machine Learning

## Evaluating a Learning Algorithm

### Machine learning diagnostic

`Diagnostic`: A test that you can run to gain insight what is/isn't working with a learning algorithm, and gain guidance as to how best to improve its performance.

Diagnostics can take time to implement, but doing so can be a very good use of our time.

### Evaluating a Hypothesis

Once we have done some trouble shooting for errors in our predictions by: 

- Getting more training examples
- Trying smaller sets of features
- Trying additional features
- Trying polynomial features
- Increasing or decreasing λ

We can move on to evaluate our new hypothesis. 

A hypothesis may have a low error for the training examples but still be inaccurate (because of overfitting). Thus, to evaluate a hypothesis, given a dataset of training examples, we can split up the data into two sets: a **`training set`** and a **`test set`**. Typically, the training set consists of `70%` of your data and the test set is the remaining `30%`.

The new procedure using these two sets is then:

1. Learn $\Theta$ and minimize $J_{\textrm{train}}(\Theta)$ using the training set

2. Compute the test set error $J_{\textrm{test}}(\Theta)$

#### The test set error

1. For linear regression: $J_{test}(\Theta) = \dfrac{1}{2m_{test}} \sum_{i=1}^{m_{test}}(h_\Theta(x^{(i)}_{test}) - y^{(i)}_{test})^2$
2. For classification ~ Misclassification error (aka 0/1 misclassification error):

$$
err(h_\Theta(x),y) = \left\{\begin{array}{lll} 1 & \textrm{if } h_\Theta(x) \geq 0.5\ and\ y = 0\ or\ h_\Theta(x) < 0.5\ and\ y = 1\\ 0 & \textrm{otherwise} \end{array}\right.
$$

This gives us a binary 0 or 1 error result based on a misclassification. The average test error for the test set is:
$$
\text{Test Error} = \dfrac{1}{m_{test}} \sum^{m_{test}}_{i=1} err(h_\Theta(x^{(i)}_{test}), y^{(i)}_{test})
$$
This gives us the proportion of the test data that was misclassified.

### Model Selection and Train/Validation/Test Sets

Just because a learning algorithm fits a training set well, that does not mean it is a good hypothesis. It could over fit and as a result your predictions on the test set would be poor. The error of your hypothesis as measured on the data set with which you trained the parameters will be lower than the error on any other data set. 

Given many models with different polynomial degrees, we can use a systematic approach to identify the 'best' function. In order to choose the model of your hypothesis, you can test each degree of polynomial and look at the error result.

One way to break down our dataset into the three sets is:

- Training set: 60%
- Cross validation set: 20%
- Test set: 20%

We can now calculate three separate error values for the three different sets using the following method:

1. Optimize the parameters in $\Theta$ using the training set for each polynomial degree.
2. Find the polynomial degree d with the least error using the cross validation set.
3. Estimate the generalization error using the test set with $J_{test}(\Theta(d))$, ($d$ = theta from polynomial with lower error);

This way, the degree of the polynomial d has not been trained using the test set.

## Bias v.s. Variance

### Diagnosing Bias v.s. Variance

We offen need to examine the relationship between the degree of the polynomial $d$ and the *underfitting* or *overfitting* of our hypothesis.

- We need to distinguish whether **bias** or **variance** is the problem contributing to bad predictions.
- High bias is underfitting and high variance is overfitting. Ideally, we need to find a golden mean between these two.

The training error will tend to **decrease** as we increase the degree d of the polynomial.

At the same time, the cross validation error will tend to **decrease** as we increase d up to a point, and then it will **increase** as $d$ is increased, forming a convex curve.

* **High bias (underfitting)**: both $J_{\textrm{train}}(\Theta)$ and $J_{\textrm{CV}}(\Theta)$ will be high. Also, $J_{\textrm{CV}}(\Theta) \approx J_{\textrm{train}}(\Theta)$.
* **High variance (overfitting)**: $J_{\textrm{train}}(\Theta)$ will be low and $J_{\textrm{CV}}(\Theta) \gg J_{\textrm{train}}(\Theta)$.

![img](https://tva1.sinaimg.cn/large/006y8mN6gy1g8ajhooasfj308c073q3l.jpg)

### Regularization and Bias/Variance

![img](https://tva1.sinaimg.cn/large/006y8mN6gy1g8al43zgpwj30jj0akq4m.jpg)

In the figure above, we see that as $\lambda$ increases, our fit becomes more rigid. On the other hand, as $\lambda$ approaches $0$, we tend to over overfit the data. So how do we choose our parameter $\lambda$ to get it 'just right' ? In order to choose the model and the regularization term $\lambda$,  we need to:

1. Create a list of lambdas (i.e. $\lambda∈{0,0.01,0.02,0.04,0.08,0.16,0.32,0.64,1.28,2.56,5.12,10.24}$);
2. Create a set of models with different degrees or any other variants.
3. Iterate through the$\lambda$s and for each $\lambda$ go through all the models to learn some $\Theta$.
4. Compute the cross validation error using the learned $\Theta$ (computed with $\lambda$) on the $J_{\textrm{CV}}(\Theta)$ **without** regularization or $\lambda = 0$.
5. Select the best combo that produces the lowest error on the cross validation set.
6. Using the best combo $\Theta$ and $\lambda$, apply it on $J_{\textrm{test}}(\Theta)$ to see if it has a good generalization of the problem.

![image-20191025191458736](https://tva1.sinaimg.cn/large/006y8mN6gy1g8antxbcmwj30pu0eiq8l.jpg)

### Learning Curves

Training an algorithm on a very few number of data points (such as 1, 2 or 3) will easily have 0 errors because we can always find a quadratic curve that touches exactly those number of points. Hence:

- As the training set gets larger, the error for a quadratic function increases.
- The error value will plateau out after a certain m, or training set size.

*Learning curves* is often a very useful thing to plot if either we wanted to sanity check that our algorithm is working correctly, or if we want to improve the performance of the algorithm.

![image-20191025191643371](https://tva1.sinaimg.cn/large/006y8mN6gy1g8anv9sdhvj30pq0ef0xi.jpg)

#### Experiencing high bias

**Low training set size**: cases $J_{\textrm{train}}(\Theta)$ to be low and $J_{\textrm{CV}}(\Theta)$ to be high.

**Large training set size**: cases both $J_{\textrm{train}}(\Theta)$ and $J_{\textrm{CV}}(\Theta)$ to be high with $J_{\textrm{train}}(\Theta) \approx J_{\textrm{CV}}(\Theta)$.

If a learning algorithm is suffering from **high bias**, getting more training data will not **(by itself)** help much.

![img](https://tva1.sinaimg.cn/large/006y8mN6gy1g8annycdk8j308c056q3e.jpg)

#### Experiencing high variance

**Low training set size**: $J_{\textrm{train}}(\Theta)$ will be low and $J_{\textrm{CV}}(\Theta)$ will be high.

**Large training set size**: $J_{\textrm{train}}(\Theta)$ increases with training set size and $J_{\textrm{CV}}(\Theta)$ continues to decrease without leveling off. Also, $J_{\textrm{train}}(\Theta) < J_{\textrm{CV}}(\Theta)$ but the difference between them remains significant.

If a learning algorithm is suffering from **high variance**, getting more training data is likely to help.

![img](https://tva1.sinaimg.cn/large/006y8mN6gy1g8anrlbbfkj308c04rdgb.jpg)

### Deciding What to Do Next Revisited

Our decision process can be broken down as follows:

- **Getting more training examples:** Fixes high variance

- **Trying smaller sets of features:** Fixes high variance

- **Adding features:** Fixes high bias

- **Adding polynomial features:** Fixes high bias

- **Decreasing λ:** Fixes high bias

- **Increasing λ:** Fixes high variance.

#### Diagnosing Neural Networks

- A neural network with fewer parameters is **prone to underfitting**. It is also **computationally cheaper**.
- A large neural network with more parameters is **prone to overfitting**. It is also **computationally expensive**. In this case you can use regularization (increase λ) to address the overfitting.

Using a single hidden layer is a good starting default. You can train your neural network on a number of hidden layers using your cross validation set. You can then select the one that performs best.

#### Model Complexity Effects:

- Lower-order polynomials (low model complexity) have high bias and low variance. In this case, the model fits poorly consistently.
- Higher-order polynomials (high model complexity) fit the training data extremely well and the test data extremely poorly. These have low bias on the training data, but very high variance.
- In reality, we would want to choose a model somewhere in between, that can generalize well but also fits the data reasonably well.

