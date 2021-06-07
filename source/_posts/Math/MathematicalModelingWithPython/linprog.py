import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt

'''
f = [0.5, 0.6, 0.7, 0.75, 0.8]
Aeq =[[1, 1, 1, 1, 1]]
beq = [4500]
bounds = ((0, 1600), (0, 1400), (0, 800), (0, 650), (0, 1000))
A = [[0.76, 0, 0, 0, 0], [0, 0.78, 0, 0, 0], [0, 0, 0.8, 0, 0], [0, 0, 0, 0.82, 0], [0, 0, 0, 0, 0.85]]
b = [1000, 1200, 900, 800, 1200]
res = optimize.linprog(f, A_ub=A, b_ub=b, A_eq = Aeq, b_eq = beq, bounds=bounds, options={"disp": True})
print(res)
'''

'''
c = [-2, -3, 5]
a = [[-2, 5, -1], [1, 3, 1]]
b = [-10, 12]
aeq = [[1, 1, 1]]
beq = [7]
bounds = [[0, None], [0, None], [0, None]]
result = optimize.linprog(c, a, b, aeq, beq, bounds)
print(result)
'''

'''
c = [2, 3, 1]
a = [[-1, -4, -2], [-3, -2, -0]]
b = [-8, -6]
print(optimize.linprog(c, a, b))
'''

'''
c = [1, 2, 3, 4] * 2
A = np.array([[1, -1, -1, 1], [1, -1, 1, -3], [1, -1, -2, 3]])
a = np.column_stack((A, -A))
b = [-2, -1, -0.5]
res = optimize.linprog(c, a, b)
print(res)
'''

'''
a = 0
c = [-0.05, -0.27, -0.19, -0.185, -0.185]
Aeq = [[1, 1.01, 1.02, 1.045, 1.065]]
beq = [1]
rp = []
while a < 0.05:
    A = np.zeros((4, 4))
    np.fill_diagonal(A, (0.025, 0.015, 0.055, 0.026))
    A = np.column_stack((np.zeros((4, 1)), A))
    b = a * np.ones((4,1))
    res = optimize.linprog(c, A, b, Aeq, beq)
    rp.append((a, -res.fun))
    a += 0.001

# print(rp)
rp = np.array(rp)
plt.plot(rp[:,0], rp[:,1], 'o')
plt.grid(True)
plt.xlabel('a')
plt.ylabel('Q')
plt.show()
'''

'''
c = [-3, 1, 1]
a = [[1, -2, 1], [4, -1, -2]]
b = [11, -3]
aeq = [[-2, 0, 1]]
beq = [1]
print(optimize.linprog(c, a, b, aeq, beq))
'''

