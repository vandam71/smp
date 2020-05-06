from requests import get
from bs4 import BeautifulSoup
import pandas_datareader as pdr
import pandas as pd
from datetime import datetime
from constants import *
import pickle
from progressbar import ProgressBar
import sys


class Reader(object):
    """Stock market collector class"""
    def __init__(self):
        self._tickers = []
        self._stocks = []

    def fetch_tickers(self):
        """
        Downloads a list of tickers and saves them into a pickle
        :return: []
        """
        # TODO find a better source with more value
        resp = get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
        soup = BeautifulSoup(resp.text, features='lxml')
        table = soup.find('tbody')
        for row in table.findAll('tr')[1:]:
            ticker = str(row.findAll('td')[0].text)
            ticker = ticker.replace("\n", "")
            self._tickers.append(ticker)
        self._tickers.append('TSLA')
        with open(f"{FILE_PATH}/ticker_list.pickle", "wb") as f:
            pickle.dump(self._tickers, f)
        return self._tickers

    def fetch_data(self, reload_tickers: bool = False, reload_data: bool = False, start: datetime = datetime(2010, 1, 1)):
        """
        Fetch data using the pandas datareader utilities
        :param reload_tickers: bool
        :param reload_data: bool
        :param start: datetime
        :return: None
        """
        if reload_tickers:                  # check if tickers need to be reloaded
            self.fetch_tickers()
        elif not self._tickers:              # if list is empty check if there is a pickle file
            try:                            # tries to open pickle file
                with open(f"{FILE_PATH}/ticker_list.pickle", "rb") as f:
                    self._tickers = pickle.load(f)
            except FileNotFoundError:       # if there is no file download the data
                self.fetch_tickers()
        print('[READER] Downloading {} tickers'.format(len(self._tickers)))
        bar = ProgressBar(start=0, maxval=len(self._tickers), fd=sys.stdout)
        i = 0
        for ticker in self._tickers[:]:      # iterates over the tickers list and downloads data for each
            if not reload_data:
                if not os.path.exists(f'{TICKER_PATH}/{ticker}.csv'):   # if there is no file download it
                    try:
                        df = pdr.DataReader(name=ticker, data_source='yahoo', start=start, end=datetime.today())
                        self._stocks.append((ticker, df))
                    except KeyError:
                        pass
                else:                   # if the CSV file for the ticker exists simply load it
                    df = self.read_from_csv(ticker)
                    if df is not None:
                        self._stocks.append((ticker, df))
            else:                       # download all the data
                try:
                    df = pdr.DataReader(name=ticker, data_source='yahoo', start=start, end=datetime.today())
                    self._stocks.append((ticker, df))
                except KeyError:
                    pass
            i += 1
            bar.update(i)
        bar.finish()
        del bar
        return self

    def dump_to_csv(self):
        """
        Dumps all the stocks into separate CSV files
        :return: None
        """
        print('[READER] Dumping {} tickers to CSV'.format(len(self._stocks)))
        bar = ProgressBar(start=0, maxval=len(self._stocks), fd=sys.stdout)
        i = 0
        for ticker, stock in self._stocks:
            stock.to_csv(f'{TICKER_PATH}/{ticker}.csv')
            i += 1
            bar.update(i)
        bar.finish()
        del bar

    def get_ticker(self, search: str):
        """
        Finds a specific ticker in the list and returns it
        :param search: str
        :return: pd.Dataframe
        """
        for ticker, stock in self._stocks:
            if ticker is search:
                return stock

    def compile_data(self):
        """
        Compiles every Adj Close column into a file for every ticker in the reader already
        :return: None
        """
        main_df = pd.DataFrame()
        print('[READER] Compiling {} tickers'.format(len(self._stocks)))
        bar = ProgressBar(start=0, maxval=len(self._stocks), fd=sys.stdout)
        i = 0
        for ticker, stock in self._stocks:
            df = stock.copy()
            df.rename(columns={'Adj Close': ticker}, inplace=True)
            df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)
            if main_df.empty:
                main_df = df
            else:
                main_df = main_df.join(df, how='outer')
            i += 1
            bar.update(i)
        main_df.to_csv(f'{FILE_PATH}/compiled_closes.csv')
        bar.finish()
        del bar

    @staticmethod
    def fetch_single_data(ticker: str, start: datetime = datetime(2020, 1, 1), save: bool = False):
        """
        Downloads data for a single given ticker
        :param ticker: str
        :param start: datetime
        :param save: bool
        :return: pd.Dataframe
        """
        try:
            df = pdr.DataReader(name=ticker, data_source='yahoo', start=start, end=datetime.today())
            if save:
                df.to_csv(f'{TICKER_PATH}/{ticker}.csv')
            return df
        except KeyError:
            return None

    @staticmethod
    def read_from_csv(ticker: str, date: bool = True):
        """
        Reads a ticker from a CSV file
        :param ticker: str
        :param date: bool
        :return: pd.Dataframe or None
        """
        if not os.path.exists(f"{TICKER_PATH}/{ticker}.csv"):
            return None
        try:
            if date:
                return pd.read_csv(f"{TICKER_PATH}/{ticker}.csv", parse_dates=True, index_col='Date')
            return pd.read_csv(f"{TICKER_PATH}/{ticker}.csv")
        except pd.errors.EmptyDataError:
            return None
