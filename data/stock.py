import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from .reader import Reader
from plot.graphs import pandas_candlestick
from data.statistics import Statistics
import pickle
import numpy as np
from scipy.stats import norm


# TODO migrate every calculation to the Statistics class

class Stock(object):
    """Stock class, contains all the information regarding a specific ticker"""
    def __init__(self, ticker: str, data: pd.DataFrame):
        """
        Initializes the Stock object
        :param ticker: str
        :param data: pd.DataFrame
        """
        self.ticker = ticker
        self.data = pd.DataFrame(data)
        self.time_window = [self.data.index[0], self.data.index[-1]]
        self.statistics = Statistics(self.data)

    def __repr__(self):
        """
        Returns the class representation
        :return: None
        """
        return str(self)

    def __str__(self):
        """
        Returns the readable string of the class
        :return:
        """
        return f'{str(self.__class__)}: {str(self.ticker)}, id: {id(self)}'

    @classmethod
    def from_csv(cls, ticker: str):
        """
        Loads the ticker from a .csv file
        :param ticker: str
        :return: Stock object
        """
        data = Reader.read_from_csv(ticker)
        return cls(ticker=ticker, data=data)
        pass

    @classmethod
    def from_remote(cls, ticker: str, start: datetime = None):
        """
        Loads the ticker from remote
        :param ticker: str
        :param start: datetime
        :return: Stock object
        """
        data = Reader.fetch_single_data(ticker, start)
        return cls(ticker=ticker, data=data)
        pass

    @staticmethod
    def from_pickle(ticker: str):
        """
        Loads the ticker from a pickle file
        :param ticker: str
        :return: Stock object
        """
        return pickle.load(open(ticker + ".smp", "rb"))

    def log_returns(self):
        return np.diff(np.log(self.close.copy()))

    def daily_drops(self, drops: [] = None):
        if drops is None:
            drops = [-0.01, -0.05, -0.10, -0.15, -0.20, -0.25, -0.30, -0.35, -0.40, -0.45, -0.50]
        returns = self.log_returns()
        mean = returns.mean()
        sigma = returns.std(ddof=1)
        prob = []
        for i in range(len(drops)):
            prob.append(norm.cdf(drops[i], mean, sigma))
        return prob

    def yearly_drops(self, drops: [] = None):     # TODO Change to actual days and not a 225 value
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

    def draw_candlestick(self, window: int = 2, days: int = 0):
        """
        Draw the Candlestick graph for the Stock object
        :param window: int
        :param days: int
        :return: None
        """
        pandas_candlestick(self.data, self.ticker, window=window, days=days)

    def draw_plot(self, fields: str = 'all', days: int = 0):
        """
        Plots the specific fields
        :param fields: str or [str]
        :param days: int
        :return: None
        """
        if days == 0:
            days = self.data.shape[0]
        if fields == 'all':
            plots = self.data[['Open', 'High', 'Low', 'Close']][:days]
        else:
            plots = self.data[fields]
        plots.plot(grid=True)
        plt.title(self.ticker)
        plt.xlabel('Dates')
        plt.ylabel('Share Value ($)')
        plt.show(block=False)

    def dump(self):
        """
        Dumps the object in a pickle file
        :return: None
        """
        pickle.dump(self, open(self.ticker + ".smp", "wb"))
