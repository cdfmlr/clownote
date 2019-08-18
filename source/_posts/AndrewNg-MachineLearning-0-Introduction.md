---
title: AndrewNg-MachineLearning-0-Introduction
date: 2019-08-18 16:37:53
tags: MachineLearning
categories:	
	- MachineLearning
	- AndrewNg
---

# Notes of Andrew Ng’s Machine Learning —— (0) Introduction

## Welcome

Machine Learning 

- Grew out of work in AI
- New capability for computers

Examples:

- Database mining
  Large datasets from growth of automation / web.
    E.g. Web click data, medical records, biology, engineering

- Applications can’t program by hand.
    E.g. Autonomous helicopter, handwriting recognition, most of Natural Language Progressing (NLP), Computer Vision.

- Self-customizing programs
    E.g. Amazon, Netflix product recommendations

- Understanding human learning (brain, real AI)

## What is machine learning

### Machine Learning definition

* *Arthur Samuel (1959)* : Machine Learning: Field of study that gives computers the ability to learn without being explicitly programmed.
* *Tom Mitchell (1998)*, *a more modern definition* : Well-posed Learning Problem: A computer program is said to learn from experience `E` with respect to some task `T` and some prformance measure `P`, if its performance on T, as measured by P, improves with experience E.

Example:

* Playing checkers.

  `E` = the experience of playing many games of checkers
  `T` = the task of playing checkers.
  `P` = the probability that the program will win the next game.
	
* Spam Filter

  `E` = Watching you label emails as spam or not spam
  `T` = Classifying emails as spam or not spam
  `P` = The number (or fraction) of emails correctly classified as spam / not spam.

### Machine Learning algorithms

- Supervised learning
- Unsupervised learning

Others: Reinforcement learning, recommender system

## Supervised Learning

In supervised learning, we are:

* given a data set
* given "right answers" (already know what our correct output should look like)
* having the idea that there is a relationship between the input and the output.

#### Categories of supervised learning problems

1. `Regression`: Predict continuous valued output

   Trying to map input variables to some continuous function.

   *[To predict how much]*

   E.g.

   * You have a large inventory of identical items. You want to predict how many of these items will sell over the next 3 months.
   * Given a picture of a person, we have to predict their age on the basis of the given picture

2. `Classification`: Discrete valued output (0/1 or 0/1/2/3...)

   Trying to map input variables into discrete categories.

   *[To predict whether/which]*

   E.g.

   * Given a patient with a tumor, we have to predict whether the tumor is malignant or benign.
   * You'd like software to examine individual customer accounts, and for each accout decide if it has been hacked/compromised.

## Unsupervised Learning

In unsupervised learning we can:

* approach problems with little or no idea what our results should look like
* derive structure from data where we don't necessarily know the effect of the variables.
* derive this structure by **clustering the data** based on relationships among the variables in the data.

With unsupervised learning there is **no feedback based on the prediction results**.

E.g.

1. `Clustering`: 

   * Google news looks for tens of thousands of news stories and automatically cluster them together. So, the news stories that are all about the same topic get displayed together.

   * Take a collection of 1,000,000 different genes, and find a way to automatically group these genes into groups that are somehow similar or related by different variables, such as lifespan, location, roles, and so on.

2. `Non-clustering`:

   The "Cocktail Party Algorithm", allows you to find structure in a chaotic environment. (i.e. identifying individual voices and music from a mesh of sounds at a cocktail party).