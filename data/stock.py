import pandas as pd
from datetime import datetime
from data.reader import Reader
from plot.graphs import pandas_candlestick, pandas_dataframe
from data.statistics import Statistics
import pickle


class Stock(object):
    """Stock class, contains all the information regarding a specific ticker"""
    def __init__(self, ticker: str, data: pd.DataFrame) -> None:
        """
        Initializes the Stock object
        :param ticker: str
        :param data: pd.DataFrame
        """
        self._ticker = ticker
        self._data = pd.DataFrame(data)
        self._time_window = [self._data.index[0], self._data.index[-1]]
        self.statistics = Statistics(self._data['Adj Close'].to_numpy())

    def __repr__(self) -> str:
        """
        Returns the class representation
        :return: None
        """
        return str(self)

    def __str__(self) -> str:
        """
        Returns the readable string of the class
        :return:
        """
        return f'{str(self.__class__)}: {str(self._ticker)}, id: {id(self)}'

    @classmethod
    def from_csv(cls, ticker: str):
        """
        Loads the ticker from a .csv file
        :param ticker: str
        :return: Stock object
        """
        data = Reader.read_from_csv(ticker)
        return cls(ticker=ticker, data=data)

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

    @staticmethod
    def from_pickle(ticker: str):
        """
        Loads the ticker from a pickle file
        :param ticker: str
        :return: Stock object
        """
        return pickle.load(open(ticker + ".smp", "rb"))

    def draw_candlestick(self, window: int = 2, days: int = 0) -> None:
        """
        Draw the Candlestick graph for the Stock object
        :param window: int
        :param days: int
        :return: None
        """
        return pandas_candlestick(self._data, self._ticker, window=window, days=days)

    def draw_plot(self, fields: str = 'all', days: int = 0):
        """
        Plots the specific fields
        :param fields: str or [str]
        :param days: int
        :return: None
        """
        if fields == 'all':
            return pandas_dataframe(self._data[['Open', 'High', 'Low', 'Close']], self._ticker, days=days)
        else:
            for field in fields:
                if field not in self._data.columns:
                    raise Exception('Field not found in dataframe')
            return pandas_dataframe(self._data[fields], self._ticker, days=days)

    def dump(self) -> None:
        """
        Dumps the object in a pickle file
        :return: None
        """
        pickle.dump(self, open(self._ticker + ".smp", "wb"))

    def get_ticker(self) -> str:
        return str(self._ticker)
