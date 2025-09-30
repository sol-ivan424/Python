import numpy as np
import time

def F(xy):
    x, y = xy
    return np.array([x**2+y**2-1, x-y])

def J(xy):
    x, y = xy
    return np.array([[2*x, 2*y],[1, -1]])

def newton(x0, eps):
    x = np.array(x0, dtype=float)
    for i in range(100):
        delta = np.linalg.solve(J(x), -F(x))
        x = x + delta
        if np.linalg.norm(delta) < eps:
            return x, i+1
    return x, 100

for eps in [1e-3, 1e-6]:
    start = time.time()
    sol, it = newton([1,0], eps)
    print(f"eps={eps}: решение={sol}, итераций={it}, время={time.time()-start:.6f}с")
