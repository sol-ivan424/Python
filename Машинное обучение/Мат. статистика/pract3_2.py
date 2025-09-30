# Импортируем необходимые библиотеки
import numpy as np
import pandas as pd
import scipy.stats as stats #нельзя использовать дальше
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Загружаем данные из файлов
data_files = ['1.txt', '3.txt', '4.txt', '6.txt']

# Чтение данных в DataFrame
data = {}
for file in data_files:
    data[file] = pd.read_csv(file, header=None, names=['values'])

# Определение распределений двумя способами
def identify_distributions(data):
    results = {}
    for file, df in data.items():
        values = df['values']
        
        # 1. Критерий согласия Пирсона (хи-квадрат тест)
        k2, p = stats.normaltest(values)
        chi2_result = 'Не отклоняется от гипотезы нормальности' if p > 0.05 else 'Отклоняется от гипотезы нормальности'
        
        # 2. Метод анаморфоза (нормализация и проверка на нормальность)
        transformed_values = np.log1p(values - values.min() + 1)  # Логарифмическое преобразование для нормализации
        stat, p_value = stats.shapiro(values)  # Тест Шапиро-Уилка для проверки нормальности
        anamorph_result = 'Тест Шапиро-Уилка: данные нормальны' if p_value > 0.05 else 'Тест Шапиро-Уилка: данные не нормальны'
        
        # Построение графиков анаморфозы и линейного тренда
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Логарифмическая анаморфоза
        x_log = np.log1p(values - values.min() + 1).values.reshape(-1, 1)
        y_log = np.arange(len(values)).reshape(-1, 1)
        reg_log = LinearRegression().fit(x_log, y_log)
        y_log_pred = reg_log.predict(x_log)
        r2_log = r2_score(y_log, y_log_pred)
        
        axes[0].scatter(x_log, y_log, color='blue', label='Данные')
        axes[0].plot(x_log, y_log_pred, color='red', label=f'Линейный тренд (R^2={r2_log:.2f})')
        axes[0].set_title(f'Логарифмическая анаморфоза для {file}')
        axes[0].set_xlabel('Log значений')
        axes[0].set_ylabel('Порядок значений')
        axes[0].legend()
        
        # Квадратный корень анаморфоза
        x_sqrt = np.sqrt(values - values.min() + 1).values.reshape(-1, 1)
        y_sqrt = np.arange(len(values)).reshape(-1, 1)
        reg_sqrt = LinearRegression().fit(x_sqrt, y_sqrt)
        y_sqrt_pred = reg_sqrt.predict(x_sqrt)
        r2_sqrt = r2_score(y_sqrt, y_sqrt_pred)
        
        axes[1].scatter(x_sqrt, y_sqrt, color='blue', label='Данные')
        axes[1].plot(x_sqrt, y_sqrt_pred, color='red', label=f'Линейный тренд (R^2={r2_sqrt:.2f})')
        axes[1].set_title(f'Квадратный корень анаморфоза для {file}')
        axes[1].set_xlabel('Квадратный корень значений')
        axes[1].set_ylabel('Порядок значений')
        axes[1].legend()
        
        plt.tight_layout()
        plt.show()
        
        # Сохранение результатов
        if chi2_result == 'Не отклоняется от гипотезы нормальности' or anamorph_result == 'Тест Шапиро-Уилка: данные нормальны':
            distribution = 'Нормальное распределение'
        else:
            distribution = 'Показательное распределение'
        
        results[file] = {
            'distribution': distribution,
            'chi2_test': chi2_result,
            'anamorph_test': anamorph_result,
            'r2_log': r2_log,
            'r2_sqrt': r2_sqrt
        }
    return results

# Идентификация распределений
results = identify_distributions(data)

# Вывод результатов для каждого файла
for file, result in results.items():
    print(f'Файл: {file}')
    print(f"Распределение: {result['distribution']}")
    print(f"Результат критерия Пирсона: {result['chi2_test']}")
    print(f"Результат метода анаморфоза: {result['anamorph_test']}")
    print(f"Коэффициент детерминации (логарифм): R^2 = {result['r2_log']:.2f}")
    print(f"Коэффициент детерминации (квадратный корень): R^2 = {result['r2_sqrt']:.2f}")
    print('-' * 50)

# Визуализация данных
for file, df in data.items():
    sns.histplot(df['values'], kde=True)
    plt.title(f'Гистограмма для данных из {file}')
    plt.xlabel('Значение')
    plt.ylabel('Частота')
    plt.show()
