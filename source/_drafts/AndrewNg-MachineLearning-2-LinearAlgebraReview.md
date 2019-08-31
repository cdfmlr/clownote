---
title: AndrewNg-MachineLearning-2-LinearAlgebraReview
tags:tags: Machine Learning
categories:	
	- Machine Learning
	- AndrewNg
---

# Notes of Andrew Ng’s Machine Learning —— (2) Linear Algebra Review



## Matrices and Vectors

- **Matrices** are 2-dimensional arrays:

$$
\left[\begin{array}{ll}
a & b & c \\
d & e & f \\
g & h & i \\
j & k & l \\
\end{array}\right]
$$

The above matrix has four rows and three columns, so it is a `4 x 3 matrix`.

- **Vector** are matrices with one column and many rows:

$$
\left[\begin{array}{ll}
w \\
x \\
y \\
z \\
\end{array}\right]
$$

The above vector is a `4 x 1 matrix`.

### Notation and terms

- $A_{ij}$ refers to the element in the *ith row* and *jth column* of matrix A.
- A vector with 'n' rows is referred to as a `'n'-dimensional vector`.
- $v_i$ refers to the element in the *ith row* of the vector.
- In general, all our vectors and matrices will be `1-indexed`, which refers that it's beginning from `1`. Note that this is different to lots of programming languages.
- Matrices are usualy denoted by uppercase names while vectors are lowercase.
- `Scalar` means that an object is a single value, not a vector or matrix.
- $\R$ referss to the set of scalar real numbers.
- $R^n$ refers to the set of n-dimensional vectors of real numbers.

### Create matrices and vectors in Octive/Matlab

```octave
% The ; denotes we are going back to a new row.
A = [1, 2, 3; 4, 5, 6; 7, 8, 9; 10, 11, 12]

% Initialize a vector 
v = [1;2;3] 

% Get the dimension of the matrix A where m = rows and n = columns
[m,n] = size(A)

% You could also store it this way
dim_A = size(A)

% Get the dimension of the vector v 
dim_v = size(v)

% Now let's index into the 2nd row 3rd column of matrix A
A_23 = A(2,3)

```

Output:

```octave
A =

    1    2    3
    4    5    6
    7    8    9
   10   11   12

v =

   1
   2
   3

m =  4
n =  3
dim_A =

   4   3

dim_v =

   3   1

A_23 =  6
```

