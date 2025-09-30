import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Параметры задачи
k = 20  # Количество случайных величин
n = 1000  # Количество реализаций
a, b = 0, 1  # Параметры равномерного распределения на отрезке [0, 1]

# Генерация выборки Y (сумма k равномерных случайных величин)
Y = np.array([np.sum(np.random.uniform(a, b, k)) for _ in range(n)])

# Несмещенные точечные оценки для среднего и стандартного отклонения
mu = np.mean(Y)
sigma = np.std(Y)

# Построение гистограммы выборки Y
plt.hist(Y, bins=30, density=True, alpha=0.6, color='g', label='Гистограмма выборки Y')

# Теоретическая плотность нормального распределения с оценками mu и sigma
x = np.linspace(min(Y), max(Y), 100)
p = norm.pdf(x, mu, sigma)
plt.plot(x, p, 'k', linewidth=2, label='Теоретическая плотность')

plt.title('Гистограмма выборки Y и теоретическая плотность нормального распределения')
plt.legend()
plt.show()

# Проверка нормальности с помощью критерия \(\chi^2\)-Пирсона
m = 10  # Количество интервалов для гистограммы
observed_freq, bins = np.histogram(Y, bins=m, density=True)

# Строим центры интервалов
bin_centers = (bins[:-1] + bins[1:]) / 2

# Теоретические частоты для нормального распределения
theoretical_freq = []
for i in range(m):
    p1 = norm.cdf(bins[i+1], loc=mu, scale=sigma)  # CDF для правой границы
    p2 = norm.cdf(bins[i], loc=mu, scale=sigma)    # CDF для левой границы
    theoretical_freq.append(p1 - p2)  # Вероятность попадания в этот интервал

# Переводим вероятности в частоты с учетом общего числа наблюдений
expected_freq = np.array(theoretical_freq) * len(Y)

# Вычисление статистики \(\chi^2\)
chi2_stat = np.sum((observed_freq - expected_freq) ** 2 / expected_freq)

# Степени свободы
df = m - 3  # Степени свободы для \(\chi^2\) - Пирсона

# Критическое значение \(\chi^2\) для уровня значимости 0.05
alpha = 0.05
critical_value = norm.ppf(1 - alpha) * np.sqrt(2 * df)

# Выводим статистику \(\chi^2\) и критическое значение
print(f'Chi2 Statistic: {chi2_stat:.4f}')
print(f'Критическое значение \(\chi^2\) для df={df} и уровня значимости 0.05: {critical_value:.4f}')

# Интерпретация результата
if chi2_stat > critical_value:
    print('Гипотеза о нормальности отклоняется.')
else:
    print('Гипотеза о нормальности не отклоняется.')

# Преобразование выборки методом анаморфоза
# Метод анаморфоза включает использование стандартного нормального распределения для преобразования.
# Рассчитываем нормированную выборку Z (анморфоз).
if sigma != 0:  # Проверка на нулевое стандартное отклонение
    Z = (Y - mu) / sigma
else:
    Z = Y

# Построим гистограмму преобразованных данных Z
plt.hist(Z, bins=30, density=True, alpha=0.6, color='b', label='Гистограмма преобразованной выборки')

# Плотность стандартного нормального распределения
x = np.linspace(min(Z), max(Z), 100)
p_z = norm.pdf(x, 0, 1)
plt.plot(x, p_z, 'r', linewidth=2, label='Стандартное нормальное распределение')

plt.title('Гистограмма преобразованной выборки и стандартное нормальное распределение')
plt.legend()
plt.show()

