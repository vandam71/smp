import uuid
import pandas as pd
import matplotlib.pyplot as plt
from data.reader import read_from_csv, get_ticker
from plot.graphs import pandas_candlestick
from data.statistics import Statistics
import pickle
import numpy as np
from scipy.stats import norm


class Stock(object):
    def __init__(self, ticker: str, data: pd.DataFrame):
        self.ticker = ticker
        self.data = pd.DataFrame(data)
        self.time_window = [self.data.index[0], self.data.index[-1]]
        self.statistics = Statistics(self.data)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{str(self.__class__)}: {str(self.ticker)}, id: {id(self)}'

    @classmethod
    def from_csv(cls, ticker):
        data = read_from_csv(ticker)
        return cls(ticker=ticker, data=data)

    @classmethod
    def from_remote(cls, ticker: str, start=None):
        data = get_ticker(ticker=ticker, start=start)
        return cls(ticker=ticker, data=data)

    @staticmethod
    def from_pickle(ticker):
        return pickle.load(open(ticker + ".smp", "rb"))

    def plot(self, fields='all'):
        if fields == 'all':
            plots = self.data[['Open', 'High', 'Low', 'Close']]
        else:
            plots = self.data[fields]
        plots.plot(grid=True)
        plt.title(self.ticker)

    def log_returns(self):
        return np.diff(np.log(self.close.copy()))

    def daily_drops(self, drops=None):
        if drops is None:
            drops = [-0.01, -0.05, -0.10, -0.15, -0.20, -0.25, -0.30, -0.35, -0.40, -0.45, -0.50]
        returns = self.log_returns()
        mean = returns.mean()
        sigma = returns.std(ddof=1)
        prob = []
        for i in range(len(drops)):
            prob.append(norm.cdf(drops[i], mean, sigma))
        return prob

    def yearly_drops(self, drops=None):     # Change to actual days and not a 225 value
        if drops is None:
            drops = [-0.01, -0.05, -0.10, -0.15, -0.20, -0.25, -0.30, -0.35, -0.40, -0.45, -0.50]
        returns = self.log_returns()
        mean225 = 225 * returns.mean()
        sigma225 = (225 ** 0.5) * returns.std(ddof=1)
        prob = []
        for i in range(len(drops)):
            prob.append(norm.cdf(drops[i], mean225, sigma225))
        return prob

    def quantile(self):
        returns = self.log_returns()
        mean = returns.mean()
        sigma = returns.std(ddof=1)
        quantile = [0.05, 0.25, 0.75, 0.95]
        for i in range(len(quantile)):
            quantile[i] = norm.ppf(quantile[i], mean, sigma)
        return quantile

    def z_scores(self):
        """Standardized test statistic for Z-Scores"""
        returns = self.log_returns()
        mean = returns.mean()       # mean = 0 under the null hypothesis
        sigma = returns.std(ddof=1)
        return (mean - 0)/(sigma/len(returns) ** 0.5)

    def draw_candlestick(self, window=2):
        pandas_candlestick(self.data, self.ticker, window=window)

    def dump(self):
        pickle.dump(self, open(self.ticker + ".smp", "wb"))
