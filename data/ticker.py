import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class Ticker:
    data: pd.DataFrame()
    ticker: str
    adj_close: pd.DataFrame()

    def __init__(self, data, ticker):
        self.data = data
        self.ticker = ticker
        self.adj_close = pd.DataFrame({'Adj Close': data['Adj Close']})

    def plot(self, fields='all'):
        if fields == 'all':
            plots = self.data[['Open', 'High', 'Low', 'Close']]
        else:
            plots = self.data[fields]
        plots.plot(grid=True)
        plt.show()

    def stock_returns(self):
        temp = self.adj_close.copy()
        temp.rename(columns={'Adj Close': 'Returns'}, inplace=True)
        return temp.apply(lambda x: x/x[0])

    def stock_growth(self):
        temp = self.adj_close.copy()
        temp.rename(columns={'Adj Close': 'Growth'}, inplace=True)
        return temp.apply(lambda x: (x.shift(-1)-x)/x)

    def stock_increase(self):
        temp = self.adj_close.copy()
        temp.rename(columns={'Adj Close': 'Increase'}, inplace=True)
        return temp.apply(lambda x: (x - x.shift(1))/x)

    def stock_change(self):
        temp = self.adj_close.copy()
        temp.rename(columns={'Adj Close': 'Change'}, inplace=True)
        return temp.apply(lambda x: np.log(x) - np.log(x.shift(1)))
