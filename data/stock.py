import pandas as pd
from datetime import datetime
from .reader import Reader
from plot.graphs import pandas_candlestick, pandas_dataframe
from .statistics import Statistics
import pickle


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
        self.statistics = Statistics(self.data['Adj Close'].to_numpy()).initialize()

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
        if fields == 'all':
            pandas_dataframe(self.data[['Open', 'High', 'Low', 'Close']], self.ticker, days=days)
        else:
            for field in fields:
                if field not in self.data.columns:
                    raise Exception('Field not found in dataframe')
            pandas_dataframe(self.data[fields], self.ticker, days=days)

    def dump(self):
        """
        Dumps the object in a pickle file
        :return: None
        """
        pickle.dump(self, open(self.ticker + ".smp", "wb"))
