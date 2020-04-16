import pandas as pd
import matplotlib.pyplot as plt
from data.reader import read_from_csv, get_ticker
from plot.graphs import pandas_candlestick
from analysis.text import exploratory
from analysis.calculate import returns_histogram, returns_plot


class Stock:
    DATA: pd.DataFrame()
    TICKER: str

    def __init__(self, ticker, data=None, force=False):
        if ticker is None:
            return
        self.TICKER = ticker
        if data is None:
            if force is False:
                self.DATA = read_from_csv(self.TICKER)
            else:
                self.DATA = get_ticker(ticker=self.TICKER)

    def plot(self, fields='all'):
        if fields == 'all':
            plots = self.DATA[['Open', 'High', 'Low', 'Close']]
        else:
            plots = self.DATA[fields]
        plots.plot(grid=True)
        plt.show()

    def stock_returns(self):
        temp = pd.DataFrame({'Adj Close': self.DATA['Adj Close']})
        returns_histogram(temp)
        returns_plot(temp)
        plt.show()

    def draw_candlestick(self, window=2):
        pandas_candlestick(self.DATA, self.TICKER, window=window)
