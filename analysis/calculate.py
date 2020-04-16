import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm


def log_returns(data):
    data['Log Returns'] = np.log(data['Adj Close'].shift(-1)) - np.log(data['Adj Close'])
    data = pd.DataFrame({'Log Returns': data['Log Returns']})
    print('check')
    return data


def returns_histogram(data):
    if 'Log Returns' not in data.columns:
        data = log_returns(data)
    mu = data['Log Returns'].mean()
    sigma = data['Log Returns'].std(ddof=1)
    density = pd.DataFrame()
    density['x'] = np.arange(data['Log Returns'].min() - 0.01, data['Log Returns'].max() + 0.01, 0.001)
    density['pdf'] = norm.pdf(density['x'], mu, sigma)
    data['Log Returns'].hist(bins=50, figsize=(8, 4))
    plt.plot(density['x'], density['pdf'], color='red')


def returns_plot(data):
    if 'Log Returns' not in data.columns:
        data = log_returns(data)
    plt.figure(figsize=(8, 4))
    plt.plot(data['Log Returns'])
    plt.title('Stock Log Returns')
    plt.axhline(0, color='red')
    plt.ylabel('Log Returns')
