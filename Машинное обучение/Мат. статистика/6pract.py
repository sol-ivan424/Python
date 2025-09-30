
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def simple_moving_average(series, window):
    return series.rolling(window=window, center=True).mean()

def weighted_moving_average(series, window, epsilon):
    weights = np.exp(-epsilon * np.arange(-(window // 2), (window // 2) + 1))
    weights /= weights.sum()
    return series.rolling(window=window, center=True).apply(lambda x: np.dot(x, weights), raw=True)

def exponential_moving_average(series, alpha):
    return series.ewm(alpha=alpha, adjust=False).mean()

def double_exponential_moving_average(series, alpha, gamma):
    ema1 = series.ewm(alpha=alpha, adjust=False).mean()
    ema2 = ema1.ewm(alpha=gamma, adjust=False).mean()
    return 2 * ema1 - ema2

# Load the data from the provided text files
file1_path = '1.txt'
file2_path = '2.txt'

data1 = np.loadtxt(file1_path)
data2 = np.loadtxt(file2_path)

# Convert to DataFrame with appropriate indexing for time series
df1 = pd.DataFrame(data1, columns=["Value"])
df2 = pd.DataFrame(data2, columns=["Value"])
df1.index = pd.date_range(start="2023-01-01", periods=len(df1), freq='D')
df2.index = pd.date_range(start="2023-01-01", periods=len(df2), freq='D')

# Define optimal parameters
optimal_params1 = {
    'SMA': {'window': 11},
    'WMA': {'window': 11, 'epsilon': 0.8},
    'EMA': {'alpha': 0.7},
    'DEMA': {'alpha': 0.2, 'gamma': 0.3}
}
optimal_params2 = optimal_params1

# Generate and display the plots for the actual time series
plt.figure(figsize=(14, 8))

# Plot optimal smoothing for each method for Time Series 1
for i, (method, params) in enumerate(optimal_params1.items(), 1):
    if method == 'SMA':
        smoothed = simple_moving_average(df1['Value'], params['window'])
    elif method == 'WMA':
        smoothed = weighted_moving_average(df1['Value'], params['window'], params['epsilon'])
    elif method == 'EMA':
        smoothed = exponential_moving_average(df1['Value'], params['alpha'])
    elif method == 'DEMA':
        smoothed = double_exponential_moving_average(df1['Value'], params['alpha'], params['gamma'])
    
    plt.subplot(2, 2, i)
    plt.plot(df1.index, df1['Value'], label='Original Series', color='blue', alpha=0.5)
    plt.plot(smoothed.index, smoothed, label=f'{method} Optimal', color='red')
    plt.title(f'{method} (Optimal Parameters) - Time Series 1')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.legend()

plt.tight_layout()
plt.show()

plt.figure(figsize=(14, 8))

# Plot optimal smoothing for each method for Time Series 2
for i, (method, params) in enumerate(optimal_params2.items(), 1):
    if method == 'SMA':
        smoothed = simple_moving_average(df2['Value'], params['window'])
    elif method == 'WMA':
        smoothed = weighted_moving_average(df2['Value'], params['window'], params['epsilon'])
    elif method == 'EMA':
        smoothed = exponential_moving_average(df2['Value'], params['alpha'])
    elif method == 'DEMA':
        smoothed = double_exponential_moving_average(df2['Value'], params['alpha'], params['gamma'])
    
    plt.subplot(2, 2, i)
    plt.plot(df2.index, df2['Value'], label='Original Series', color='green', alpha=0.5)
    plt.plot(smoothed.index, smoothed, label=f'{method} Optimal', color='red')
    plt.title(f'{method} (Optimal Parameters) - Time Series 2')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.legend()

plt.tight_layout()
plt.show()
