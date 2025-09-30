import pandas as pd

def mortgage(summa, years, rate):
    n = years*12
    r = rate/12/100
    ann = summa * (r*(1+r)**n)/((1+r)**n-1)
    data = []
    debt = summa
    for i in range(1, n+1):
        debt = debt*(1+r) - ann
        data.append((i, debt+ann, ann, debt))
    return pd.DataFrame(data, columns=["Месяц","Долг на начало","Платёж","Остаток"])

df = mortgage(3_000_000, 20, 12)
print(df.head())
