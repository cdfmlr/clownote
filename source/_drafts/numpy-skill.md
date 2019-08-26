---
title: numpy-skill
tags:
	- Python
	- Mathematical Modeling
---

# `numpy`

推荐 numpy 中文文档：[https://www.numpy.org.cn/index.html](https://www.numpy.org.cn/index.html).

## `array`

### 创建 向量/矩阵

用 `np.array()`

```python
>>> import numpy as np
>>> np.array([1, 2, 3])
array([1, 2, 3])
>>> np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
array([[1, 2, 3],
       [4, 5, 6],
       [7, 8, 9]])
```

### 矩阵的拼接

- 列合并/扩展：`np.column_stack()`
- 行合并/扩展：`np.row_stack()`

```python
>>> import numpy as np
>>> A = np.array([[1,1], [2,2]])
>>> B = np.array([[3, 3], [4, 4]])
>>> A
array([[1, 1],
       [2, 2]])
>>> B
array([[3, 3],
       [4, 4]])
>>> np.column_stack((A, B))		# 行
array([[1, 1, 3, 3],
       [2, 2, 4, 4]])
>>> np.row_stack((A, B))			# 列
array([[1, 1],
       [2, 2],
       [3, 3],
       [4, 4]])
```

### 对角线元素赋值

比如说我们有一个 `np.array X`，我想对角线的所有值设置为0，可以用 `np.fill_diagonal(X, [0, 0, 0, ...])`。

```
>>> D = np.zeros([3, 3])
>>> np.fill_diagonal(D, [1, 2, 3])
>>> D
array([[1., 0., 0.],
       [0., 2., 0.],
       [0., 0., 3.]])
```

