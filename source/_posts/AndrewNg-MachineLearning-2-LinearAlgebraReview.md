---
title: 吴恩达机器学习2-线性代数复习
tags: Machine Learning
categories:
  - Machine Learning
  - AndrewNg
date: 2019-09-02 18:17:19
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

### in Octave/Matlab

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

## Addition and Scalar Multiplication

### Addition

**Addition** and **subtraction** are element-wise, so you simply add or subtract each corresponding element:
$$
\left[\begin{array}{ll}
a & b \\
c & d \\
\end{array}\right]
+
\left[\begin{array}{ll}
w & x\\
y & z\\
\end{array}\right]
=
\left[\begin{array}{ll}
a+w & b+x \\
c+y & d+z \\
\end{array}\right]
$$
To add or subtract two matrices, their *dimensions* must be **the same**.

### Scalar multiplication

In **scalar multiplication**, we simply multiply every element by the scalar value:
$$
\left[\begin{array}{ll}
a & b \\
c & d \\
\end{array}\right]
*x
=
\left[\begin{array}{ll}
ax & bx \\
cx & dx \\
\end{array}\right]
$$

### in Octave/Matlab

```octave
% Initialize matrix A and B 
A = [1, 2, 4; 5, 3, 2]
B = [1, 3, 4; 1, 1, 1]

% Initialize constant s 
s = 2

% See how element-wise addition works
add_AB = A + B 

% See how element-wise subtraction works
sub_AB = A - B

% See how scalar multiplication works
mult_As = A * s

% Divide A by s
div_As = A / s

% A Matrix + scalar will get Matrix + a new matrix that each element equals the scalar 
add_As = A + s
```

Output:

```octave
A =

   1   2   4
   5   3   2

B =

   1   3   4
   1   1   1

s =  2
add_AB =

   2   5   8
   6   4   3

sub_AB =

   0  -1   0
   4   2   1

mult_As =

    2    4    8
   10    6    4

div_As =

   0.50000   1.00000   2.00000
   2.50000   1.50000   1.00000

add_As =

   3   4   6
   7   5   4

```

## Matrix-Vector Multiplication

We map the column of the vector onto each row of the matrix, multiplying each element and summing the result.
$$
\left[\begin{array}{ll}
a & b\\
c & d\\
e & f\\
\end{array}\right]
*
\left[\begin{array}{ll}
x\\
y\\
\end{array}\right]
=
\left[\begin{array}{ll}
ax & by\\
cx & dy\\
ex & fy\\
\end{array}\right]
$$
The result is a **vector**. The number of **columns** of the matrix must equal the number of **rows** of the vector.

An `m x n matrix` multiplied by an `n x 1 vector` results in an `m x 1 vector`.

### in Octave/Matlab

```octave
% Initialize matrix A 
A = [1, 2, 3; 4, 5, 6;7, 8, 9] 

% Initialize vector v 
v = [1; 1; 1] 

% Multiply A * v
Av = A * v
```

Output:

```octave
A =

   1   2   3
   4   5   6
   7   8   9

v =

   1
   1
   1

Av =

    6
   15
   24
```

### Neat Trick

Say, we have a set of four sizes of houses, and we have a hypotheses for predictiong what the price of a house. We are going to compute $h(x)$ of each of our 4 houses:

> House sizes:
> $$
> \begin{array}{c}
> 2104\\
> 1416\\
> 1534\\
> 852\\
> \end{array}
> $$
> Hypothesis:
> $$
> h_\theta(x)=-40+0.25x
> $$
> 

It turns out there's neat way of posing this, applying this hypothesis to all of my houses at the same time via a Matrix-Vector multiplication.

- Construct a `DataMatrix`:

$$
\textrm{DataMatrix}=
\left[\begin{array}{ll}
1 & 2104\\
1 & 1416\\
1 & 1534\\
1 & 852\\
\end{array}\right]
$$

- Put `Parameters` to a vector:

$$
\textrm{Parameters}=
\left[\begin{array}{ll}
-40\\
0.25\\
\end{array}\right]
$$

- Then, the `Predictions` will be clear by calculate a Matrix-Vector Multiplication:

$$
\begin{array}{ll}
\textrm{Predictions} & = & \textrm{DataMatrix} & * & \textrm{Parameters}\\
 & = & \left[\begin{array}{c}
1 & 2104\\
1 & 1416\\
1 & 1534\\
1 & 852\\
\end{array}\right] & * & \left[\begin{array}{c}
-40\\
0.25\\
\end{array}\right]\\
\end{array}
$$

The reuslt will be something like this:
$$
\textrm{Predictions}=
\left[\begin{array}{c}
-40 \times 1 + 0.25 \times 2104\\
-40 \times 1 + 0.25 \times 1416\\
\vdots\\
\end{array}\right]
$$
Obviously, it's equal to the codes below:

```
for (i = 0; i < X.size(); i++) {
		Predictions[i] = h(X[i]);
}
```

However, our new trick simplifies the code, makes it more readable as well as driving it faster to be solved in most programming languages, we just construct two matrices and do a multiplication:

```
DataMatrix = [...]
Parameters = [...]
Predictions = DataMatrix * Parameters
```

## Matrix-Matrix Multiplication

We multiply two matrices by breaking it into serveral vector multiplications and concatenating the result.
$$
\left[\begin{array}{ll}
a & b\\
c & d\\
e & f\\
\end{array}\right]
*
\left[\begin{array}{ll}
w & x\\
y & z\\
\end{array}\right]
=
\left[\begin{array}{ll}
aw+by & ax+bz\\
cw+dy & cx+dz\\
ew+fy & ex+fz\\
\end{array}\right]
$$
An `m x n matrix` multiplied by an `n x o matrix` result in an `m x o` matrix ($[m \times n]*[n \times o]=[m \times o]$). In the above example, a 3 x 2 matrix times a 2 x 2 matrix resulted in a 3 x 2 matrix.

To multiply two matrices, the number of **columns** of the first matrix must equal the number of **rows** of the second matrix.

### in Octave/Matlab

```octave
A = [1, 2; 3, 4; 5, 6]
B = [7, 8; 9, 10]
A*B
```

Output:

```octave
A =

   1   2
   3   4
   5   6

B =

    7    8
    9   10

ans =

    25    28
    57    64
    89   100
```

### Neat Trick

Let's say, as befor, that we have four houses, and we want to predict their prices. Ony now, we have three competing hypotheses. We want to apply all three competing hypotheses to all four Xs. It turns out we can do that very efficiently using a matrix-matrix multiplication.

![image-20190901154936492](https://tva1.sinaimg.cn/large/006y8mN6ly1g6k2f8f6tyj30hw09f40y.jpg)

## Matrix Multiplication Properties

### Non-commutative

Matrices are not commutative:
$$
A \times B \neq B \times A
$$

### Associative

Matrices are associative:
$$
(A \times B) \times C = A \times (B \times C)
$$

### Identity matrix

`Identity matrix`: a matrix that simply has `1`'s on the diagonal (upper left to lower right diagonal) and `0`'s elsewhere.
$$
I=\left[\begin{array}{ll}
1 & 0 & 0\\
0 & 1 & 0\\
0 & 0 & 1\\
\end{array}\right]
$$
The identity matrix, when multiplied by any matrix of the same dimensions, results in the original matrix. It's just like multiplying numbers by 1.
$$
A \times I = I \times A = A
$$
Notice that when doing `A*I`, the `I` should match the matrix's columns and when doing `I*A`, the `I` should match the matrix's rows:
$$
A_{m \times n} \times I_{n \times n}=I_{m \times m} \times A_{m \times n} = A_{m \times n}
$$

### in Octave/Matlab

```octave
% Initialize random matrices A and B 
A = [1,2;4,5]
B = [1,1;0,2]

% Initialize a 2 by 2 identity matrix
I = eye(2)

% The above notation is the same as I = [1,0;0,1]

% What happens when we multiply I*A ? 
IA = I*A 

% How about A*I ? 
AI = A*I 

% Compute A*B 
AB = A*B 

% Is it equal to B*A? 
BA = B*A 

% Note that IA = AI but AB != BA
```

Output:

```
A =

   1   2
   4   5

B =

   1   1
   0   2

I =

Diagonal Matrix

   1   0
   0   1

IA =

   1   2
   4   5

AI =

   1   2
   4   5

AB =

    1    5
    4   14

BA =

    5    7
    8   10

```

## Inverse and Transpose

### Inverse

The inverse of a matrix $A$ is denoted $A^{-1}$. Multiplying by the inverse results in the identity matrix:
$$
A_{m \times m} \times A^{-1}_{m \times m}=A^{-1}_{m \times m} \times A_{m \times m} = I_{m \times m}
$$
A non square matrix does not have an inverse matrix. We can compute inverses of matrices in octave with the `pinv(A)` function and in Matlab with the `inv(A)` function. Matrices that don't have an inverse are *singular* or *degenerate*.

In practice, when we are using normal equation with Octave, there are two functions to inverse a Matrix -- pinv and inv. For some mathematically reason, The `pinv(A)` will always offer us the value of data that we want, even if A is non-invertible.

### Transpose

The transposition of a matrix is like rotating the matrix 90º in clockwise direction and then reversing it.

In other words: Let $A$ be an $m \times n$ matrix, and let $B=A^T$. Then  $B$ is an $n \times m$ matrix, and $B_{ij}=A_{ji}$.
$$
A=
\left[\begin{array}{l}
a & b\\
c & d\\
e & f\\
\end{array}\right]
\qquad A^T=
\left[\begin{array}{l}
a & c & e\\
b & d & f\\
\end{array}\right]
$$
We can compute transposition of matrices in matlab with the `transpose(A)` function or `A'`

### in Octave/Matlab

```octave
% Initialize matrix A 
A = [1,2,0;0,5,6;7,0,9]

% Transpose A 
A_trans = A' 

% Take the inverse of A 
A_inv = inv(A)

% What is A^(-1)*A? 
A_invA = inv(A)*A
```

Output:

```octave
A =

   1   2   0
   0   5   6
   7   0   9

A_trans =

   1   0   7
   2   5   0
   0   6   9

A_inv =

   0.348837  -0.139535   0.093023
   0.325581   0.069767  -0.046512
  -0.271318   0.108527   0.038760

A_invA =

   1.00000  -0.00000   0.00000
   0.00000   1.00000  -0.00000
  -0.00000   0.00000   1.00000

```

