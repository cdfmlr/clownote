---
date: 2020-11-28 22:00:27.588389
title: 数值分析算法总结
---
# 数值分析算法总结

数值分析的算法总结，用 Python 简要描述各种方法。考前复（yu）习向。

本文给出的代码主要是针对闭卷考试背算法写的。我 jo 得记数学公式和写 LaTeX 一样，是件比写代码更可怕的事。所以，把一些主要的算法用程序写了出来，方便记忆。

（其中一部分是考试前复习时写的，经过考场的抽样检验，比较靠谱。但那时写的不太完整，后面又补充写了点，这时成绩都出了，学的也都忘了，所以可能不太对，总之别报太大期望啦）

如果你需要的是更全的各种算法完整的代码实现与描述，请移步：

- https://github.com/cdfmlr/NumericalAnalysis
- or https://gitee.com/cdfmlr/NumericalAnalysis

All right, talk is cheap, let me show you the code!

## 非线性方程求根

### 二分法

```python
x = (a + b) / 2
while True:
    if f(x) * f(a) < 0:
        b = x
    else:
		a = x
	x = (a + b) / 2
```

### 不动点迭代

```python
x = x_0
while True:
    x = phi(x)
```

收敛：`diff(phi, x)`存在且连续 && `abs(diff(phi, x)(x_0)) < 1`。

or: 设 $x^*$ 为 $f(x)=0$ 的根，可以得到 $x^*=...(x^*)$，所以 $x^*$ 为 `x = phi(x)` 的不动点，对 $x^*$ 领域的 x：`abs(diff(phi, x)) < 1`

### 牛顿迭代

```python
x = x_0
while True:
    x -= f(x) / df(x)
```

## 插值

### Lagrange 插值

```python
def lagrange_interpolate(points):
	L = 0  # 插值多项式
    for i, (xi, yi) in enumerate(points):
        li = 1
        for j, (xj, yj) in enumerate(points):
            if j == i:
                continue
            li *= (x - xj) / (xi - xj)
        L += yi * li
    return L
```

这个程序不太好懂，还是看公式：

$$
L(x)=\sum _{j=0}^{k}y_{j}\ell _{j}(x)
$$

![截屏2020-12-31 16.48.44](https://tva1.sinaimg.cn/large/0081Kckwly1gm74xhj8pcj31fk06eta3.jpg)

P.S. 这个公式是直接 Wikipedia 上复制的，KaTeX 渲染不出来，就放图片了。下面是它的源码：

```latex
$$
\ell _{j}(x)=\prod _{{i=0,\,i\neq j}}^{{k}}{\frac {x-x_{i}}{x_{j}-x_{i}}}={\frac {(x-x_{0})}{(x_{j}-x_{0})}}\cdots {\frac {(x-x_{{j-1}})}{(x_{j}-x_{{j-1}})}}{\frac {(x-x_{{j+1}})}{(x_{j}-x_{{j+1}})}}\cdots {\frac {(x-x_{{k}})}{(x_{j}-x_{{k}})}}
$$
```

### Newton 插值

差商：

```python
def dq(f, xs):
    if len(xs) == 1:  # 0阶
        return f(xs[0])
    # n 阶
    return (dq(f, xs[1:]) - dq(f, xs[:-1])) / (xs[-1] - xs[0]) 
```

手算用表：

![截屏2020-11-29 20.25.29](https://tva1.sinaimg.cn/large/0081Kckwly1gl6bgm6utbj31540igtek.jpg)

Newton 插值：

```python
def newton_interpolate(points):
    N = 0
    xs = []
    for (x, y) in points:
        xs.append(x)
        N += dq(f, xs) * prod( [('x' - xi) for xi in xs[:-1]] )
    return N
```

## 最小二乘拟合

```python
x = [0, 1, 2, 3].T
y = [1, 2, 4, 8].T

X = [1, x, x**2]
# (X.T @ X) @ theta = X.T @ y
theta = pinv(X.T @ X) @ X.T @ y
```

`@` 是矩阵乘法（这是标准的 Python 运算符哦：https://docs.python.org/3/library/operator.html#operator.matmul）

## 数值积分

### 梯形求积公式

```python
df = (b - a) * (f(a) + f(b)) / 2
```

### 辛普森求积公式

```python
df = (b - a) * (f(a) + 4 * f((a + b) / 2) + f(b)) / 6
```

### Newton-Cotes

求柯特斯系数 $C_k^{(n)}$:

```python
def costes_coefficient(n, k):
    ckn = ((-1) ** (n - k)) / n * factorial(k) * factorial(n - k)

    h = 1
    t = Symbol('t')
    for j in range(n+1):
        if j != k:
            h *= (t - j)

    ckn *= integrate(h, (t, 0, n))

    return ckn
```

打张表方便手算：

![costes_coefficient_table](https://tva1.sinaimg.cn/large/0081Kckwly1gm74jwolc6j315s0fw40k.jpg)

牛顿-科特斯求积公式：

```python
def newton_cotes_integral(f, a, b, n):
    step = (b - a) / n
    xs = [a + i * step for i in range(n+1)]
    return (b - a) * sum([costes_coefficient(n, k) * f(xs[k]) for k in range(0, n+1)])
```

## 常微分方程初值问题

问题：
$$
\begin{cases}
y'(x)=f(x,y)\\
y(a)=y_0\\
\end{cases}
\qquad (a\le x \le b)
$$


### 改进 Euler

```python
def improved_euler(f, a, b, h, y0):    
    x = a
    y = y0

    while x <= b:
        yield (x, y)

        y_next_g = y + h * f(x, y)  # 预估
        y_next = y + h * ( f(x, y) + f(x+h, y_next_g) ) / 2  # 校正
        
        x = x + h
        y = y_next
```

### RK4

```python
def runge_kutta(f, a, b, h, y0):
    x = a
    y = y0

    while x <= b:
        yield (x, y)

        k1 = f(x, y)
        k2 = f(x + h / 2, y + h * k1 / 2)
        k3 = f(x + h / 2, y + h * k2 / 2)
        k4 = f(x + h, y + h * k3)
        
        x = x + h
        y = y + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
```

## 线性方程组直接解法

### 高斯消元

```python
A = np.c_[a, b]  # 增广矩阵

n = A.shape[0]
x = np.zeros(n)  # 解

# 消元
for k in range(n-1):
    # 列选主元，如果做顺序消元就不用做下面两行
    i_max = k + argmax(abs(A[k:n, k]))
    A[[i_max, k]] = A[[k, i_max]]
    
    # if A[k][k] == 0: 求解失败
    for i in range(k+1, n):
        m = A[i][k] / A[k][k];
        A[i][k] = 0;
        for j in range(k+1, n+1):
            A[i][j] -= A[k][j] * m

# 回代：解三角方程
x[n-1] = A[n-1][n] / A[n-1][n-1]
for k in range(n-2, -1, -1): # from n-2 (included) to 0 (included)
    for j in range(k+1, n):
        A[k][n] -= A[k][j] * x[j]
    x[k] = A[k][n] / A[k][k]
```

### LU 分解

系数矩阵 a：

```python
n = a.shape[0]
p = [0, 1, ..., n-1]  # 记录交换

for k in range(n-1):
    if 列选主元:
        i_max = k + argmax(abs(a[k:n, k]))
        if i_max != k:
            a[[i_max, k]] = a[[k, i_max]]  # swap rows
            p[[i_max, k]] = p[[k, i_max]]  # record

    assert a[k][k] != 0, "错误: 主元素为零"

    for i in range(k+1, n):
        a[i][k] /= a[k][k]  # L @ 严格下三角
        for j in range(k+1, n):
            a[i][j] -= a[i][k] * a[k][j]  # U @ 上三角
```

把右端常数 b 做相同的行交换（p 记录）：

```python
b = [b[v] for v in p]
```

然后就可以解方程了：

```python
解方程("L * y = b") => y
解方程("U * x = y") => x
```

附：解三角方程：

```python
x = np.zeros(n, dtype=np.float)
x[n-1] = y[n-1] / u[n-1][n-1]
for i in range(n-2, -1, -1): # from n-2 (included) to 0 (included)
    yi = y[i]
    for j in range(i+1, n):
        yi -= x[j] * u[i][j]
    x[i] = yi / u[i][i]
```

## 线性方程组迭代解法

### Jacobi 迭代

```python
# A =  D - L - U
D = diag(diag(A))
L = - tril(A, -1)
U = - triu(A, 1)

B = inv(D) @ (L + U)
f = inv(D) @ 

while True:
    x_prev = x
    x = B @ x + f
```

emmmm，这种去手算不太现实。我依稀记得直接写出方程来算更容易（我考完试好久了，已经忘了）。。。

### Gauss-Seidel 迭代

```python
B = inv(D - L) @ U
f = inv(D - L) @ b
```

## 特征值求法

### 正幂法

```python
A = array(shape=(n, n)) # A 是要求特征值的 n*n 矩阵

m = m0 = 1  # 主特征值
u = u0 = [1, 1, ..., 1]  # 对应的特征向量

while True:
	m_prev = m

	v = dot(A, u)
	m = v[argmax(abs(v))]
	u = v / m
```

### 反幂法

正幂法改一下：

```python
v = solve(A, u)
```

最后结果是 `1/m` 和 `u`。

---

> EOF
>
> By CDFMLR 2020.12.31

