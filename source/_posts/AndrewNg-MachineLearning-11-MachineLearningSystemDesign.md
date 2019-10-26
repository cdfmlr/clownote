---
title: 机器学习系统设计
tags: Machine Learning
categories:
  - Machine Learning
  - AndrewNg
date: 2019-10-26 21:56:37
---


# Notes of Andrew Ng’s Machine Learning —— (11) Machine Learning System Design

## Prioritizing What to Work On

**System Design Example:**

Given a data set of emails, we could construct a vector for each email. Each entry in this vector represents a word. The vector normally contains 10,000 to 50,000 entries gathered by finding the most frequently used words in our data set. If a word is to be found in the email, we would assign its respective entry a 1, else if it is not found, that entry would be a 0. Once we have all our x vectors ready, we train our algorithm and finally, we could use it to classify if an email is a spam or not.

![img](https://tva1.sinaimg.cn/large/006y8mN6gy1g8bj9rx2urj30ki09mdk2.jpg)

So how could you spend your time to improve the accuracy of this classifier?

- Collect lots of data (for example "honeypot" project but doesn't always work)
- Develop sophisticated features (for example: using email header data in spam emails)
- Develop algorithms to process your input in different ways (recognizing misspellings in spam).

It is difficult to tell which of the options will be most helpful.

## Error Analysis

The recommended approach to solving machine learning problems is to:

- Start with a simple algorithm, implement it quickly, and test it early on your cross validation data.
- Plot learning curves to decide if more data, more features, etc. are likely to help.
- Manually examine the errors on examples in the cross validation set and try to spot a trend where most of the errors were made.

For example, assume that we have 500 emails and our algorithm misclassifies a 100 of them. We could manually analyze the 100 emails and categorize them based on what type of emails they are. We could then try to come up with new cues and features that would help us classify these 100 emails correctly. Hence, if most of our misclassified emails are those which try to steal passwords, then we could find some features that are particular to those emails and add them to our model. We could also see how classifying each word according to its root changes our error rate:

![img](https://tva1.sinaimg.cn/large/006y8mN6gy1g8bl9vwi9lj30jg0a143a.jpg)

It is very important to **get error results as a single, numerical value**. Otherwise it is difficult to assess your algorithm's performance.

For example if we use stemming, which is the process of treating the same word with different forms (fail/failing/failed) as one word (fail), and get a 3% error rate instead of 5%, then we should definitely add it to our model. However, if we try to distinguish between upper case and lower case letters and end up getting a 3.2% error rate instead of 3%, then we should avoid using this new feature. 

Hence, we should try new things, get a numerical value for our error rate, and based on our result decide whether we want to keep the new feature or not.

## Handling Skewed Data

### Error metrics for skewed classes

A *skewed class* is a case of that the ratio of positive to negative examples is very close to one of two extremes.

For example, consider the problem of cancer classification, when we say $y = 1$ if the patient has cancer and $y = 0$ if they do not. We have trained the progression classifier and let's say we test out classifier on a test set and find that we get 1% error. So, we are making 99% correct diagnosis. Seems like a really impressive result. 

But now, we find out that only 0.5% of patients in out training test sets actually have cancer (i.e. only half a percent of the patients that come though our screening process have cancer). This case is actually what we called a skewed class. In this case the 1% error no longert looks so impressive.

And in particular, here's a piece of code, which is actually even a non learning code like this:

```octave
function y = predictCancer(x)
	y = 0;	% just output 0 for whatever x.
return
```

It just sets $y=0$, and always predicts nobody has cancer. This algorithm would actually get 0.5% error.So this is even better then the 1% offered by our classifier. 

So, How can we know whether a implement (e.g. using the $y \equiv 0$ instead of our learning algorithm) is actually a improvement for a skewed class?

One of the evaluatin  metric are what's called *Precision/Recall*:

![image-20191026152903469](https://tva1.sinaimg.cn/large/006y8mN6ly1g8bmwqbebxj30po0dgahc.jpg)

If a classifier is high precision and high recall, then we can make sure that this algorithm preforms pretty well.

### Trading Off Precision and Recall

After training a logistic regression classifier, we plan to make predictions according to:

- Predict $y=1$ if $h_\theta(x)≥threshold$
- Predict $y=1$ if $h_\theta(x)<threshold$

For different values of the `threshold` parameter, we get different values of precision (P) and recall (R).

![image-20191026165452692](https://tva1.sinaimg.cn/large/006y8mN6gy1g8bpe4ywhyj30pr0edgth.jpg)

So, how to compare precision/recall numbers? We get what called *F score* (or *$F_1$ score*) for help:
$$
F_1 \textrm{ Score} = 2 \frac{PR}{P+R}
$$
![image-20191026171016268](https://tva1.sinaimg.cn/large/006y8mN6gy1g8bpu6kdx0j30pm0ec446.jpg)

In the worst case where our $P=R=0$, we will get $F_1$ score = 0. And in the best case where $P=R=1$, the F score will equals 1. So a $F_1$ Score will be a value between 0 and 1, the higher $F_1$ Score we get, the better implement it is.

A reasonable way to pick the value to use for the threshold is to measure precision (P) and recall (R) on the   **cross validation set** and choose the value of threshold which maximizes $2\frac{PR}{P+R}$.

## Data For Machine Learning

> It's not who has the best algorithm that wins. It's who has the most data.

### Large data rationale

We think a massive  training set will be able to help when we assume feature $x\in\R^{n+1}$ has sufficient information to predict $y$ accurately.

A useful test for this is: **Given the input $x$, can a human expert confidently predict $y$?**

Example: For breakfast I ate <u>{two, to, too}</u> eggs.

Counterexample: Predict housing price from only size and no other features.

---

To make $J_{\textrm{test}}(\Theta)$ be small, we should:

* Using a learning algorithm with many parameters (*low bias algorithm* e.g. logistic/linear regression regression with many features; neural network with many hidden units)

  -> $J_{\textrm{train}}(\Theta)$ will be small

* Using a very large training set (unlikely to overfit)

  -> $J_{\textrm{train}}(\Theta) \approx J_{\textrm{test}}(\Theta)$

