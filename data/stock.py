import pandas as pd
import matplotlib.pyplot as plt
from data.reader import read_from_csv, get_ticker
from plot.graphs import pandas_candlestick
import pickle
import numpy as np


class Stock:
    def __init__(self, ticker, data=None):
        self.ticker = ticker
        self.data = pd.DataFrame(data)

    @classmethod
    def fromCSV(cls, ticker):
        data = read_from_csv(ticker)
        return cls(ticker=ticker, data=data)

    @classmethod
    def fromRemote(cls, ticker, start=None):
        data = get_ticker(ticker=ticker, start=start)
        return cls(ticker=ticker, data=data)

    @staticmethod
    def fromPickle(ticker):
        return pickle.load(open(ticker + ".smp", "rb"))

    def plot(self, fields='all'):
        if fields == 'all':
            plots = self.data[['Open', 'High', 'Low', 'Close']]
        else:
            plots = self.data[fields]
        plots.plot(grid=True)
        plt.title(self.ticker)
        plt.show()

    def draw_candlestick(self, window=2):
        pandas_candlestick(self.data, self.ticker, window=window)

    def dump(self):
        pickle.dump(self, open(self.ticker + ".smp", "wb"))
