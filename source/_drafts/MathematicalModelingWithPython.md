---
title: Mathematical Modeling With Python
tags: Mathematical Modeling
---

# 用 Python 做数学建模

## 线性规划

> 第三方依赖库：`scipy`。

用 `scipy.optimize.linprog` 可以解线性规划问题：

```python
linprog(c, A_ub=None, b_ub=None, A_eq=None, b_eq=None, bounds=None, method='simplex', callback=None, options=None)
```

其规定的问题标准型式为：

```
        Minimize:     c^T * x
    
        Subject to:   A_ub * x <= b_ub
                      A_eq * x == b_eq
```

e.g. 求接下列线性规划问题：
$$
\textrm{max } z=2x_1+3x_2-5x_3,\\
\textrm{s.t. } \left \{ \begin{array}{ll}
x_1+x_2+x_3=7\\
2x_1-5x_2+x_3\ge10\\
x_1+3x_2+x_3\le12\\
x_1,x_2,x_3\ge0
\end{array}\right.
$$
**解**：

```python
#! /usr/bin/python3

import numpy as np
from scipy import optimize


c = [-2, -3, 5]
a = [[-2, 5, -1], [1, 3, 1]]
b = [-10, 12]
aeq = [[1, 1, 1]]
beq = [7]
bounds = [[0, None], [0, None], [0, None]]	# (0, None) means non-negative, this is a default value
result = optimize.linprog(c, a, b, aeq, beq, bounds)
print(result)
```

> ⚠️【注意】这里题目是求max，标准型是min，所以在写`c`矩阵的时候把值都写成了题目中的负；类似地， `>=` 的项对应的a、b中值要取之负。然后最终结果也要取`fun`的负。

输出：

```
     fun: -14.571428571428571
 message: 'Optimization terminated successfully.'
     nit: 2
   slack: array([3.85714286, 0.        ])
  status: 0
 success: True
       x: array([6.42857143, 0.57142857, 0.        ])
```

最优解为$x_1=6.42857143, x_2=0.57142857, x_3=0$, 对应的最优值$z=14.571428571428571$.

若要取 fun、x的值，可以直接用 `result.fun` 和 `result.x`。

## 整数规划

线性整数规划问题可以转换为线性规划问题求解。

对于非线性的整数规划，在穷举不可为时，在一定计算量下可以考虑用 *蒙特卡洛法* 得到一个满意解。

### 蒙特卡洛法（随机取样法）

e.g. $y=x^2$、$y=12-x$ 与 $x$ 轴 在第一象限围成一个曲边三角形。设计一个随机试验，求该图像面积的近似值。

**解**：	设计的随机试验思想如下：在矩形区域 `[0, 12] * [0, 9]` 上产生服从均匀分布的 `10^7` 个随机点，统计随机点落在曲边三角形的频数，则曲边三角形的面积近似为上述矩形面积乘于频率。

```python
import random


x = [random.random() * 12 for i in range(0, 10000000)]
y = [random.random() * 9 for i in range(0, 10000000)]

p = 0
for i in range(0, 10000000):
    if x[i] <= 3 and y[i] < x[i] ** 2:
            p += 1
    elif x[i] > 3 and y[i] < 12 - x[i]:
            p += 1
 
area_appr = 12 * 9 * p / 10 ** 7
print(area_appr)
```

结果在 `49.5` 附近。

e.g. 已知非线性整数规划为：
$$
\textrm{max } z=x_1^2+x_2^2+3x_3^2+4x_4^2+2x_5^2-8x_1-2x_2-3x_3-x_4-2x_5\\
\textrm{s.t. } \left \{ \begin{array}{ll}
0 \le x_i \le 99, i=1,...,5,\\
x_1+x_2+x_3+x_4+x_5 \le 400\\
x_1+2x_2+2x_3+x_4+6x_5 \le 800\\
2x_1+x_2+6x_3 \le 200\\
x_3+x_4+5x_5 \le 200
\end{array}\right.
$$
如果用枚举法，要计算 `100^5 = 10^10` 个点，计算量太大。所以考虑用蒙特卡洛法去随机计算  `10^6` 个点，得到比较满意的点：

```python
import time
import random

# 目标函数
def f(x: list) -> int:
    return x[0] ** 2 + x[1] ** 2 + 3 * x[2] ** 2 + 4 * x[3] ** 2 + 2 * x[4] ** 2 - 8 * x[0] - 2 * x[1] - 3 * x[2] - x[3] -2 * x[4]

# 约束向量函数
def g(x: list) -> list:
    res = []
    res.append(sum(x) - 400)
    res.append(x[0] + 2 * x[1] + 2 * x[2] + x[3] + 6 * x[4] - 800)
    res.append(2 * x[0] + x[1] + 6 * x[2] - 200)
    res.append(x[2] + x[3] + 5 * x[4] - 200)
    return res

random.seed(time.time)

pb = 0
xb = []

for i in range(10 ** 6):
    x = [random.randint(0, 99) for i in range(5)]		# 产生一行五列的区间[0, 99] 上的随机整数
    rf = f(x)
    rg = g(x)
    if all((a < 0 for a in rg)):		# 若 rg 中所有元素都小于 0
        if pb < rf:
            xb = x
            pb = rf
            
print(xb, pb)
```

### 指派问题

> 第三方依赖库：`numpy` , `scipy`。

用 `scipy.optimize.linear_sum_assignment` 可以解指派问题(the linear sum assignment problem)：

```python
linear_sum_assignment(cost_matrix)
```

注意指派矩阵 `cost_matrix` 里的元素 `C[i, j]` 的 `i` 为 *worker*，`j` 为 *job*.

> Formally, let X be a boolean matrix where $X[i,j] = 1$ iff row i is assigned to column j. Then the optimal assignment has cost
> $$
> \min \sum_i \sum_j C_{i,j} X_{i,j}
> $$
> s.t. each row is assignment to at most one column, and each column to at most one row.

e.g. 求解下列指派问题，已知指派矩阵为
$$
\left[ \begin{array}{cc}
3 & 8 & 2 & 10 & 3\\
8 & 7 & 2 & 9 & 7\\
6 & 4 & 2 & 7 & 5\\
8 & 4 & 2 & 3 & 5\\
9 & 10 & 6 & 9 & 10\\
\end{array} \right].
$$
**解**：

```python
>>> import numpy as np
>>> from scipy import optimize
>>> c = [[3,8,2,10,3], [8,7,2,9,7], [6,4,2,7,5], [8,4,2,3,5], [9,10,6,9,10]]
>>> c = np.array(c)
>>> optimize.linear_sum_assignment(c)
(array([0, 1, 2, 3, 4]), array([4, 2, 1, 3, 0]))	# 对应 x15、x23、x32、x44、x51
>>> c[[0, 1, 2, 3, 4], [4, 2, 1, 3, 0]].sum()		# 结果代入 cost_matrix，求得最优值
21
```

## 非线性规划

### 非线性规划模型

> 第三方依赖库：`numpy` , `scipy`。

我们之前多次使用的 `scipy.optimize` 中集成了一系列用来求规划的函数，其中当然不乏解决非线性规划的方法。例如用其中的 `minimize` 函数就可以解决很多在 Matlab 中用 `fmincon` 解的非线性规划问题。

```
minimize(fun, x0, args=(), method=None, jac=None, hess=None, hessp=None, bounds=None, constraints=(), tol=None, callback=None, options=None)
```

常用的参数：

* `fun`:：待求 *最小值* 的目标函数，`fun(x, *args) -> float`， x 是 `shape (n,)`的 1-D array  
* `x0`：初始猜测值， `shape (n,)`的 1-D array 
* `bounds`：设置参数范围/约束条件，tuple，形如 `((0, None), (0, None))`
* `constraints`：*约束条件*，放一系列 dict 的 tuple，`({'type': TYPE, 'fun': FUN}, ...)`
  * `TYPE`：`'eq'`表示 函数结果等于0 ； `'ineq'` 表示 表达式大于等于0
  * `FUN`： 约束函数

e.g. 求下列非线性规划：
$$
\textrm{min } f(x)=x_1^2+x_2^2+x_3^2+8,\\
\textrm{s.t. } \left \{ \begin{array}{ll}
x_1^2+x_2^2+x_3^2 \ge 0,\\
x_1+x_2^2+x_3^2 \le 20,\\
-x_1-x_2^2+2=0,\\
x_2+2x_3^2=3,\\
x_1,x_2,x_3 \ge 0.
\end{array}\right.
$$

```python
import numpy as np
from scipy import optimize

f = lambda x: x[0] ** 2 + x[1] **2 + x[2] ** 2 + 8

cons = ({'type': 'ineq', 'fun': lambda x: x[0]**2 - x[1] + x[2]**2},
        {'type': 'ineq', 'fun': lambda x: -x[0] - x[1] - x[2]**3 + 20},
        {'type': 'eq', 'fun': lambda x: -x[0] - x[1]**2 + 2},
        {'type': 'eq', 'fun': lambda x: x[1] + 2 * x[2]**2 - 3})

res = optimize.minimize(f, (0, 0, 0), constraints=cons)

print(res)
```

输出：

```
     fun: 10.651091840572583
     jac: array([1.10433471, 2.40651834, 1.89564812])
 message: 'Optimization terminated successfully.'
    nfev: 86
     nit: 15
    njev: 15
  status: 0
 success: True
       x: array([0.55216734, 1.20325918, 0.94782404])
```

即，求得当 $(x_1,x_2,x_3)=(0.55216734, 1.20325918, 0.94782404)$ 时，最小值$y=10.651091840572583$.

### 无约束问题的 Python 解法

#### 符号解



#### 数值解

