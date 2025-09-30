import numpy as np
import scipy.stats as stats
import os

# Функция для чтения данных из файла
def read_data(file_path):
    with open(file_path, 'r') as file:
        data = [float(line.strip()) for line in file.readlines()]
    return np.array(data)

# Функция для расчёта выборочных статистик, доверительных интервалов
# по нормальному распределению, t-распределению и распределению хи-квадрат
def calculate_statistics(data, confidence=0.95):
    n = len(data)
    sample_mean = np.mean(data)
    # выборочное стандартное отклонение
    sample_std = np.std(data, ddof=1)

    # Доверительный интервал для среднего по нормальному распределению
    # 1−(1−0.95)/2=0.97 - уровень уверенности
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    # границы доверительного интервала
    ci_normal = (
        sample_mean - z * (sample_std / np.sqrt(n)),
        sample_mean + z * (sample_std / np.sqrt(n))
    )

    # Доверительный интервал для среднего по t-распределению Стьюдента
    t = stats.t.ppf(1 - (1 - confidence) / 2, df=n - 1)
    ci_t = (
        sample_mean - t * (sample_std / np.sqrt(n)),
        sample_mean + t * (sample_std / np.sqrt(n))
    )

    # Доверительный интервал для стандартного отклонения по хи-квадрат распределению
    chi2_lower = stats.chi2.ppf((1 - confidence) / 2, df=n - 1)
    chi2_upper = stats.chi2.ppf(1 - (1 - confidence) / 2, df=n - 1)
    ci_std = (
        sample_std * np.sqrt((n - 1) / chi2_upper),
        sample_std * np.sqrt((n - 1) / chi2_lower)
    )
    # ci_std содердит нижнюю и верхнюю границу доверительного интервала для выбор стандарт отклон

    return {
        'mean': sample_mean,
        'std': sample_std,
        'ci_normal': ci_normal,
        'ci_t': ci_t,
        'ci_std': ci_std
    }


def main():
    files = ['1.txt', '2.txt', '3.txt', '4.txt']

    for file_name in files:
        data = read_data(file_name)
        stats_result = calculate_statistics(data)

        print(f"\nРезультаты для файла {file_name}:")
        print(f"Выборочное среднее: {stats_result['mean']:.4f}")
        print(f"Выборочное стандартное отклонение: {stats_result['std']:.4f}")
        print(f"Доверительный интервал для среднего (нормальное распределение): {stats_result['ci_normal']}")
        print(f"Доверительный интервал для среднего (t-распределение): {stats_result['ci_t']}")
        print(f"Доверительный интервал для стандартного отклонения: {stats_result['ci_std']}")

if __name__ == "__main__":
    main()