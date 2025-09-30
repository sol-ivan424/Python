import numpy as np
import pandas as pd

def f(x, y):
    return 4*x - 2*y

def exact(x):
    return 2*x - 1 + 2.5*np.exp(-2*x)

def euler_mod(x0, y0, h, n):
    x, y = x0, y0
    data = []
    for i in range(n):
        k1 = f(x, y)
        k2 = f(x+h, y+h*k1)
        y = y + (h/2)*(k1+k2)
        x += h
        data.append((x, y, exact(x), abs(y-exact(x))))
    return data

for h in [0.01, 0.001]:
    n = int(1/h)
    res = euler_mod(0, 1.5, h, n)
    df = pd.DataFrame(res, columns=["x", "y_числ", "y_точн", "ошибка"])
    print(f"\nШаг {h}:")
    print(df.head())
