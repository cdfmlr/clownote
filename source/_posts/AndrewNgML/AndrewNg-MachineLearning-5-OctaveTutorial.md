---
categories:
- Machine Learning
- AndrewNg
date: 2019-09-10 21:49:09
tags: Machine Learning
title: Octave 入门
---


# Notes of Andrew Ng’s Machine Learning —— (5) Octave Tutorial

## Basic Operations

### Elementary Operations

`+`, `-`, `*`, `/`, `^`.

```octave
>> 5 + 6
ans =  11
>> 20 - 1
ans =  19
>> 3 * 4
ans =  12
>> 8 / 2
ans =  4
>> 2 ^ 8
ans =  256
```

### Logical Operations

`==`, `~=`, `&&`, `||`, `xor()`.

Note that a **not equal sign** is **`~=`**, and not `!=`.

```octave
>> 1 == 0
ans = 0
>> 1 ~= 0
ans = 1
>> 1 && 0
ans = 0
>> 1 || 0
ans = 1
>> xor(1, 0)
ans = 1
```

### Change the Prompt

We can change the prompt via `PS1()`:

```octave
>> PS1("octave: > ")
octave: > PS1(">> ")
>> PS1("octave: > ")
octave: > PS1("SOMETHING > ")
SOMETHING > PS1(">> ")
>> % Prompt changed
```

### Variables

```
>> a = 3
a =  3
>> a = 3;    % semicolon supressing output
>> c = (3 >= 1);
>> c
c = 1
```

### Display variables

```
>> a = pi;
>> a
a =  3.1416
>> disp(a)
 3.1416
>> disp(sprintf('2 decimals: %0.2f', a))
2 decimals: 3.14
```

We can also set the default length of decimal places by entering `format short/long`:

```octave
>> a
a =  3.1416
>> format long
>> a
a =  3.141592653589793
>> format short
>> a
a =  3.1416
```

### Create Matrices

```octave
>> A = [1, 2, 3; 4, 5, 6]
A =

   1   2   3
   4   5   6

>> B = [1 3 5; 7 9 11]
B =

    1    3    5
    7    9   11

>> B = [1, 2, 3;
> 4, 5, 6;
> 7, 8, 9]
B =

   1   2   3
   4   5   6
   7   8   9

>> C = [1, 2, 4, 8]
C =

   1   2   4   8

>> D = [1; 2; 3; 4]
D =

   1
   2
   3
   4

```

There are some useful methods to generate matrices:

- Generate vector of a range

```octave
>> v = 1:10    % start:end
v =

    1    2    3    4    5    6    7    8    9   10

>> v = 1:0.1:2    % start:step:end
v =

 Columns 1 through 8:

    1.0000    1.1000    1.2000    1.3000    1.4000    1.5000    1.6000    1.7000

 Columns 9 through 11:

    1.8000    1.9000 
```

- Generate matrices of all ones/zeros

```octave
>> ones(2, 3)
ans =

   1   1   1
   1   1   1

>> zeros(3, 2)
ans =

   0   0
   0   0
   0   0

>> C = 2 * ones(4, 5)
C =

   2   2   2   2   2
   2   2   2   2   2
   2   2   2   2   2
   2   2   2   2   2

```

- Generate identity matrices

```octave
>> eye(3)
ans =

Diagonal Matrix

   1   0   0
   0   1   0
   0   0   1

```

- Generate matrices of random values

Uniform distribution between 0 and 1:

```octave
>> D = rand(1, 3)
D =

   0.14117   0.81424   0.83745

```

Gaussian random:

```octave
>> D = randn(1, 3)
D =

   0.22133  -2.00002   1.61025


```

We can generate a gaussian random vector with 10000 elements, and plot a histogram:

```octave
>> randn(1, 10000);
>> hist(w)
```

Output figure:

![image-20190907224934733](https://tva1.sinaimg.cn/large/006y8mN6ly1g6rc9xza9dj30ff0blt8s.jpg)

We can also plot a histogram with more buckets, 50 bins for example:

```octave
>> hist(w, 50)
```

![image-20190907224859815](https://tva1.sinaimg.cn/large/006y8mN6ly1g6rc9cow1gj30fh0bjjri.jpg)

### Get Help

```octave
>> help

  For help with individual commands and functions type

    help NAME
    
......

>> help eye
'eye' is a built-in function from the file libinterp/corefcn/data.cc
 
......

>> help help

......

```

## Moving Data Around

### Size of matrix

`size()`: get the size of a matrix, return `[rows, columns]`.

```octave
>> A = [1, 2; 3, 4; 5, 6]
A =

   1   2
   3   4
   5   6

>> size(A)    % get the size of A
ans =

   3   2

>> sz = size(A);    % actually, size return a 1x2 matrix
>> size(sz)
ans =

   1   2

>> size(A, 1)    % get the first dimension of A (i.e. the number of rows)
ans =  3
>> size(A, 2)    % the number of columns
ans =  2
```

`length()`: return the size of the longest dimension.

```octave
>> length(A)    % get the size of the longest dimension. Confusing, not recommend
ans =  3
>> v = [1, 2, 3, 4];
>> length(v)    % We often length() to get the length of a vector
ans =  4
```

### Load data

We can use basic shell commands to find data that we want.

```octave
>> pwd
ans = /Users/c
>> cd MyProg/octave/
>> pwd
ans = /Users/c/MyProg/octave
>> ls
featureX.dat featureY.dat
>> ls -l
total 16
-rw-r--r--  1 c  staff  188 Sep  8 10:00 featureX.dat
-rw-r--r--  1 c  staff  135 Sep  8 10:00 featureY.dat
```

`load` command can load data from a file.

```octave
>> load featureX.dat
>> load('featureY.dat')
```

The data from file is now comed into matrices after load

```octave
>> featureX
featureX =

   2104      3
   1600      3
   2400      3
   1416      2
......

>> size(featureX)
ans =

   27    2

```

### Show variables

`who/whos`: show variables in memory currently.

```octave
>> who
Variables in the current scope:

A         ans       featureX  featureY  sz        v         w

>> whos    % for more details
Variables in the current scope:

   Attr Name          Size                     Bytes  Class
   ==== ====          ====                     =====  ===== 
        A             3x2                         48  double
        ans           1x2                         16  double
        featureX     27x2                        432  double
        featureY     27x1                        216  double
        sz            1x2                         16  double
        v             1x4                         32  double
        w             1x10000                  80000  double

Total is 10095 elements using 80760 bytes

```

### Clear variables

`clear` command can help us to clear variables that are no longer useful.

```octave
>> who
Variables in the current scope:

A         ans       featureX  featureY  sz        v         w

>> clear A    % clear a variable
>> clear sz v w    % clear variables
>> whos
Variables in the current scope:

   Attr Name          Size                     Bytes  Class
   ==== ====          ====                     =====  ===== 
        ans           1x2                         16  double
        featureX     27x2                        432  double
        featureY     27x1                        216  double

Total is 83 elements using 664 bytes
>> clear    % clear all variables
>> whos
>> 
```

### Save data

Take a part of a vector.

```octave
>> v = featureY(1:5)
v =

   3999
   3299
   3690
   2320
   5399
   
>> whos
Variables in the current scope:

   Attr Name          Size                     Bytes  Class
   ==== ====          ====                     =====  ===== 
        featureX     27x2                        432  double
        featureY     27x1                        216  double
        v             5x1                         40  double

Total is 86 elements using 688 bytes

```

Save data to disk: `save file_name variable [-ascii]`

```octave
>> save hello.mat v    % save as a binary format
>> ls
featureX.dat featureY.dat hello.mat
>> save hello.txt v -ascii;    % save as a ascii txt
>> 
```

Then we can clear it from memory and load v back from disk:

```octave
>> clear v
>> whos
Variables in the current scope:

   Attr Name          Size                     Bytes  Class
   ==== ====          ====                     =====  ===== 
        featureX     27x2                        432  double
        featureY     27x1                        216  double

Total is 81 elements using 648 bytes

>> load hello.mat 
>> whos
Variables in the current scope:

   Attr Name          Size                     Bytes  Class
   ==== ====          ====                     =====  ===== 
        featureX     27x2                        432  double
        featureY     27x1                        216  double
        v             5x1                         40  double

Total is 86 elements using 688 bytes

>> 
```

### Manipulate data

Get element from a matrix:

```octave
>> A = [1, 2; 3, 4; 5, 6]
A =

   1   2
   3   4
   5   6

>> A(3, 2)    % get a element of matrix
ans =  6
>> A(2, :)    % ":" means every element along that row/column
ans =

   3   4

>> A(:, 1)
ans =

   1
   3
   5

>> A([1, 3], :)    % get the elements along row 1 & 3
ans =

   1   2
   5   6

```

Change the elements of a matrix:

```octave
>> A = [1, 2; 3, 4; 5, 6]
A =

   1   2
   3   4
   5   6

>> A(:, 2) = [10, 11, 12]
A =

    1   10
    3   11
    5   12

>> A(1, 1) = 0
A =

    0   10
    3   11
    5   12

>> A = [A, [100; 101; 102]]    % append another column vector to right
A =

     0    10   100
     3    11   101
     5    12   102

>> A = [1, 2; 3, 4; 5, 6]
A =

   1   2
   3   4
   5   6

>> B = A + 10
B =

   11   12
   13   14
   15   16

>> C = [A, B]
C =

    1    2   11   12
    3    4   13   14
    5    6   15   16

>> D = [A; B];
>> size(D)
ans =

   6   2

```

Put all elements of a matrix into a single column vector:

```octave
>> A
A =

     0    10   100
     3    11   101
     5    12   102

>> A(:)    % put all elements of A into a single vector
ans =

     0
     3
     5
    10
    11
    12
   100
   101
   102
```

## Computing on Data

### Element-wise operations

Use `.<operator>` instead of `<operator>` for element-wise operations (i.e. operations between elements).

```octave
>> A = [1, 2; 3, 4; 5, 6];
>> B = [11, 12; 13, 14; 15, 16];
>> C = [1 1; 2 2];
>> v = [1, 2, 3];
>> A .* B    % element-wise multiplication (ans = [A(1,1)*B(1,1), A(1,2)*B(1,2); ...])
ans =

   11   24
   39   56
   75   96

>> A .^ 2    % squaring each element of A
ans =

    1    4
    9   16
   25   36

>> 1 ./ A
ans =

   1.00000   0.50000
   0.33333   0.25000
   0.20000   0.16667

>> v .+ 1    % equals to `v + 1` & `v + ones(1, length(v))`
ans =

   2   3   4

```

Element-wise comparison:

```octave
>> a
a =

    1.00000   15.00000    2.00000    0.50000

>> a < 3
ans =

  1  0  1  1
  
>> find(a < 3)    % to find the elements that are less then 3 in a, return their indices
ans =

   1   3   4
   
>> A
A =

   1   2
   3   4
   5   6

>> [r, c] = find(A < 3)
r =

   1
   1

c =

   1
   2

```

Functions are element-wise:

```octave
>> v = [1, 2, 3]
v =

   1   2   3

>> log(v)
ans =

   0.00000   0.69315   1.09861

>> exp(v)
ans =

    2.7183    7.3891   20.0855

>> abs([-1, 2, -3, 4])
ans =

   1   2   3   4

>> -v    % -1 * v
ans =

  -1  -2  -3

```

Floor and Ceil of elements:

```octave
>> a
a =

    1.00000   15.00000    2.00000    0.50000

>> floor(a)
ans =

    1   15    2    0

>> ceil(a)
ans =

    1   15    2    1

```

### Matrix operations

Matrix multiplication:

```octave
>> A = [1, 2; 3, 4; 5, 6];
>> C = [1 1; 2 2];
>> A * C    % matrix multiplication
ans =

    5    5
   11   11
   17   17
```

Transpose:

```octave
>> A = [1, 2; 3, 4; 5, 6];
>> A'    % transposed
ans =

   1   3   5
   2   4   6

```

Get the max element of a vector | matrix:

```octave
>> a = [1 15 2 0.5];
>> A = [1, 2; 3, 4; 5, 6];
>> max_val = max(a)
max_val =  15
>> [val, index] = max(a)
val =  15
index =  2
>> max(A)    % `max(<Matrix>)` does a column-wise maximum
ans =

   5   6
>> max(A, [], 1)    % max per column
ans =

   5   6

>> max(A, [], 2)    % max per row
ans =

   2
   4
   6

>> max(max(A))    % the max element of whole matrix
ans =  6
>> max(A(:))
ans =  6
```

Sum & prod of vector:

```octave
>> a
a =

    1.00000   15.00000    2.00000    0.50000
    
>> A
A =

   1   2
   3   4
   5   6

>> sum(a)
ans =  18.500
>> sum(A)
ans =

    9   12
    
>> sum(A, 1)
ans =

    9   12

>> sum(A, 2)
ans =

    3
    7
   11

>> prod(a)
ans =  15
>> prod(A)
ans =

   15   48

```

Get the diagonal elements:

```octave
>> A = magic(4)
A =

   16    2    3   13
    5   11   10    8
    9    7    6   12
    4   14   15    1

>> A .* eye(4)
ans =

   16    0    0    0
    0   11    0    0
    0    0    6    0
    0    0    0    1

>> sum(A .* eye(4))
ans =

   16   11    6    1

>> flipud(eye(4))    % flip up down
ans =

Permutation Matrix

   0   0   0   1
   0   0   1   0
   0   1   0   0
   1   0   0   0

>> sum(A .* flipud(eye(4)))
ans =

    4    7   10   13

```

Inverse:

```octave
>> A = magic(3)
A =

   8   1   6
   3   5   7
   4   9   2

>> pinv(A)
ans =

   0.147222  -0.144444   0.063889
  -0.061111   0.022222   0.105556
  -0.019444   0.188889  -0.102778

>> pinv(A) * A    % get identity matrix
ans =

   1.0000e+00   2.0817e-16  -3.1641e-15
  -6.1062e-15   1.0000e+00   6.2450e-15
   3.0531e-15   4.1633e-17   1.0000e+00

```

## Plotting Data

### Plotting a function

```octave
>> clear
>> t = [0:0.01:0.98];
>> size(t)
ans =

    1   99

>> y1 = sin(2*pi*4*t);
>> plot(t, y1);
```

It will show you a figure like this:

![image-20190908153422239](https://tva1.sinaimg.cn/large/006y8mN6ly1g6s5bn03vsj30dj0ao3yt.jpg)

```octave
>> y2 = cos(2*pi*4*t);
>> plot(t, y2);
```

👆 This will replace the sin figure with a new cos figure.

If we want to have both the sin and cos plots, the `hold on` command will help:

```octave
>> plot(t, y1);
>> hold on;
>> plot(t, y2, 'r');
```

We can set some text on thw figure:

```octave
>> xlabel("time");
>> ylabel("value");
>> legend('sin', 'cos');    % Show what the 2 lines are
>> title('my plot');
```

Now, we get this:

![myPlot](https://tva1.sinaimg.cn/large/006y8mN6ly1g6s5m92rbyj30dc0a0jsq.jpg)

Then, we save it and close the plotting window:

```octave
>> print -dpng 'myPlot.png'    % save it to $(pwd)
>> close
```

We can show two figures at the same time:

```octave
>> figure(1); plot(t, y1);
>> figure(2); plot(t, y2);
```

Then, we can also generate figures like this:

![image-20190908155218094](https://tva1.sinaimg.cn/large/006y8mN6ly1g6s5u82kobj30e20avwf2.jpg)

What we need to do is using a `subplot`:

```octave
>> subplot(1, 2, 1);    % Divides plot a 1x2 grid, access first element
>> plot(t, y1);
>> subplot(1, 2, 2);
>> plot(t, y2);
>> axis([0.5, 1, -1, 1])    % change the range of axis
```

Use `clf` to clear a figure:

```octave
>> clf;
```

### Showing a matrix

```octace
>> A = magic(5)
A =

   17   24    1    8   15
   23    5    7   14   16
    4    6   13   20   22
   10   12   19   21    3
   11   18   25    2    9

>> imagesc(A), colorbar
```

It gives us a figure like this:

![image-20190908160029068](https://tva1.sinaimg.cn/large/006y8mN6ly1g6s62mn3gwj30d60afwej.jpg)

The different colors correspond to the different values.

Another example:

```octave
>> B = magic(10);
>> imagesc(B), colorbar, colormap gray;
```

Output:

![image-20190908160540485](https://tva1.sinaimg.cn/large/006y8mN6ly1g6s680rvexj30dd0aidfw.jpg)

## Contriol Statements

### `for`

```octave
>> v = zeros(10, 1)
v =

   0
   0
   0
   0
   0
   0
   0
   0
   0
   0

>> for i = 1: 10,
>     v(i) = 2^i;
> end;
>> v'
ans =

      2      4      8     16     32     64    128    256    512   1024

```

### `while`

```octave
>> i = 1;
>> while i <= 5,
>     v(i) = 100;
>     i = i + 1;
> end;
>> v'
ans =

    100    100    100    100    100     64    128    256    512   1024

```

### `if`

```octave
>> for i = 1: 10,
>     if v(i) > 100,
>         disp(v(i));
>     end;
> end;
 128
 256
 512
 1024
```

Or, we can program like this,

```octave
x = 1;
if (x == 1)
    disp ("one");
elseif (x == 2)
    disp ("two");
else
    disp ("not one or two");
endif
```

### `break` & `continue`

```octave
i = 1;
while true,
    v(i) = 999;
    i = i + 1;
    if i == 6,
        break;
    end;
end;
```

Output:

```
v =

    999
    999
    999
    999
    999
     64
    128
    256
    512
   1024

```

## Function

### Create a Function

To create a function, type the function code in a text editor (e.g. gedit or notepad), and save the file as `functionName.m`

Example function:

```octave
function y = squareThisNumber(x)

y = x^2;

```

To call this function in Octave, do either:

1. `cd` to the directory of the functionName.m file and call the function:

```octave
% Navigate to directory:
cd /path/to/function

% Call the function:
functionName(args)
```

2. Add the directory of the function file to the load path:

```octave
% To add the path for the current session of Octave:
addpath('/path/to/function/')

% To remember the path for future sessions of Octave, after executing addpath above, also do:
    savepath
```

### Function with multiple return values

Octave's functions can return more than one value:

```octave
function [square, cube] = squareAndCubeThisNumber(x)

square = x^2;
cube = x^3;

```

```octave
>> [s, c] = squareAndCubeThisNumber(5)
s =  25
c =  125
```

### Practice

Let's say I have a data set that looks like this, with data points at `(1, 1)`,` (2, 2)`, `(3, 3)`. And what I'd like to do is to define an octave function to compute the cost function J of theta for different values of theta.

![image-20190908170150862](https://tva1.sinaimg.cn/large/006y8mN6ly1g6s7xhva3yj30em08baar.jpg)

First, put the data into octave:

```octave
X = [1, 1; 1, 2; 1, 3]    % Design matrix
y = [1; 2; 3]
theta = [0; 1]
```

Output:

```octave
X =

   1   1
   1   2
   1   3

y =

   1
   2
   3

theta =

   0
   1

```

Then define the cost function:

```octave
% costFunctionJ.m

function J = costFunctionJ(X, y, theta)

% X is the *design matrix* containing our training examples.
% y is the class labels

m = size(X, 1);    % number of training examples
predictions = X * theta;    % predictions of hypothesis on all m examples
sqrErrors = (predictions - y) .^ 2;    % squared erroes

J = 1 / (2*m) * sum(sqrErrors);

```

Now, use the costFunctionJ:

```octave
>> j = costFunctionJ(X, y, theta)
j = 0
```

Got `j = 0` because we set theta as `[0; 1]` which is fitting our data set perfectly.

## Vectorization

Vectorization is the process of taking code that relies on **loops** and converting it into **matrix operations**. It is more efficient, more elegant, and more concise.

As an example, let's compute our prediction from a hypothesis. Theta is the vector of fields for the hypothesis and x is a vector of variables.

With loops:

```octave
prediction = 0.0;
for j = 1:n+1,
  prediction += theta(j) * x(j);
end;
```

With vectorization:

```octave
prediction = theta' * x;
```

If you recall the definition multiplying vectors, you'll see that this one operation does the element-wise multiplication and overall sum in a very concise notation.

