# Импортируем необходимые библиотеки
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

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
        
        # Сохранение результатов
        if chi2_result == 'Не отклоняется от гипотезы нормальности' or anamorph_result == 'Тест Шапиро-Уилка: данные нормальны':
            distribution = 'Нормальное распределение'
        else:
            distribution = 'Показательное распределение'
        
        results[file] = {
            'distribution': distribution,
            'chi2_test': chi2_result,
            'anamorph_test': anamorph_result
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
    print('-' * 50)

# Визуализация данных
for file, df in data.items():
    sns.histplot(df['values'], kde=True)
    plt.title(f'Гистограмма для данных из {file}')
    plt.xlabel('Значение')
    plt.ylabel('Частота')
    plt.show()
