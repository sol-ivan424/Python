# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#данные случайных чисел
data_random_numbers = [4, 7, 3, 6, 3, 4]

variation_series = pd.Series(data_random_numbers).value_counts().sort_index()

#абсолютные частоты
absolute_frequencies = variation_series
#относительные частоты
relative_frequencies = variation_series / len(data_random_numbers)

#построение полигона относительных частот
plt.plot(relative_frequencies.index, relative_frequencies.values, marker='o')
plt.title('Полигон относительных частот случайных чисел')
plt.xlabel('Значение')
plt.ylabel('Относительная частота')
plt.show()

#вычисление статистических показателей
sample_mean = np.mean(data_random_numbers)  #выборочное среднее
sample_variance = np.var(data_random_numbers, ddof=1)  #выборочная дисперсия
sample_std = np.std(data_random_numbers, ddof=1)  #стандартное отклонение
sample_median = np.median(data_random_numbers)  #медиана
variation_coefficient = sample_std / sample_mean * 100  #коэффициент вариации

print(f"Выборочное среднее: {sample_mean}")
print(f"Выборочная дисперсия: {sample_variance}")
print(f"Выборочное стандартное отклонение: {sample_std}")
print(f"Выборочная медиана: {sample_median}")
print(f"Коэффициент вариации: {variation_coefficient:.2f}%")


data_discrete = [3, 11, 4, 2, 2, 4]

#создание вариационного ряда для дискретных данных
variation_series = pd.Series(data_discrete).value_counts().sort_index()

#абсолютные и относительные частоты для дискретных данных
absolute_frequencies = variation_series
relative_frequencies = variation_series / len(data_discrete)

#построение полигона относительных частот для дискретных данных
plt.plot(relative_frequencies.index, relative_frequencies.values, marker='o')
plt.title('Полигон относительных частот')
plt.xlabel('Значение')
plt.ylabel('Относительная частота')
plt.show()

#вычисление статистических показателей для дискретных данных
sample_mean = np.mean(data_discrete)  #выборочное среднее
sample_variance = np.var(data_discrete, ddof=1)  #выборочная дисперсия
sample_std = np.std(data_discrete, ddof=1)  #стандартное отклонение
sample_median = np.median(data_discrete)  #медиана
variation_coefficient = sample_std / sample_mean * 100  #коэффициент вариации

#вывод результатов для дискретных данных
print(f"Выборочное среднее: {sample_mean}")
print(f"Выборочная дисперсия: {sample_variance}")
print(f"Выборочное стандартное отклонение: {sample_std}")
print(f"Выборочная медиана: {sample_median}")
print(f"Коэффициент вариации: {variation_coefficient:.2f}%")


data_continuous = [1.78, 1.89, 1.91, 1.89, 1.75, 1.71]

#определяем количество интервалов для гистограммы по формуле Стерджесса
m = int(1 + 3.322 * np.log10(len(data_continuous)))

#определение интервалов для гистограммы
intervals = np.linspace(min(data_continuous), max(data_continuous), m+1)
#построение гистограммы с нормализацией (density=True)
hist, bins = np.histogram(data_continuous, bins=intervals, density=True)
#определяем центры интервалов для построения столбцов
bin_centers = 0.5 * (bins[1:] + bins[:-1])
#определение ширины столбцов (уменьшаем на 80%)
bar_width = (bins[1] - bins[0]) * 0.8

#построение гистограммы
plt.bar(bin_centers, hist, width=bar_width, edgecolor='black', linewidth=1.2, alpha=0.75)
plt.title('Гистограмма распределения частот')
plt.xlabel('Рост (см)')
plt.ylabel('Относительная частота')
plt.show()

#вычисление статистических показателей для непрерывных данных
sample_mean = np.mean(data_continuous)  #выборочное среднее
sample_variance = np.var(data_continuous, ddof=1)  #выборочная дисперсия
sample_std = np.std(data_continuous, ddof=1)  #стандартное отклонение
sample_median = np.median(data_continuous)  #медиана
variation_coefficient = sample_std / sample_mean * 100  #коэффициент вариации

#вывод результатов для непрерывных данных
print(f"Выборочное среднее: {sample_mean}")
print(f"Выборочная дисперсия: {sample_variance}")
print(f"Выборочное стандартное отклонение: {sample_std}")
print(f"Выборочная медиана: {sample_median}")
print(f"Коэффициент вариации: {variation_coefficient:.2f}%")
