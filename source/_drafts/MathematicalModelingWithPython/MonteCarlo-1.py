import numpy as np
import random

# 现在未注释的代码是最快的

x = [random.random() * 12 for i in range(0, 10000000)]
y = [random.random() * 9 for i in range(0, 10000000)]

# x = np.random.uniform(0, 12, [1, 10000000])[0]
# y = np.random.uniform(0, 9, [1, 10000000])[0]

p = 0
for i in range(0, 10000000):
    if x[i] <= 3 and y[i] < x[i] ** 2:
            p += 1
    elif x[i] > 3 and y[i] < 12 - x[i]:
            p += 1
 
a = 12 * 9 * p / 10 ** 7
print(a)


'''
l = [(random.random() * 12, random.random() * 9) for i in range(0, 10000000)]
def in_area(t: tuple) -> bool:
    if t[0] <= 3 and t[1] < t[0] ** 2:
            return True
    elif t[0] > 3 and t[1] < 12 - t[0]:
            return True
    return False

ll = list(filter(in_area, l))
a = 12 * 9 * len(ll) / 10 ** 7
print(a)
'''