from data.reader import get_data, compile_data
from data.stock import Stock
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from plot.graphs import get_business_days
import numpy as np
import pandas as pd


def reload_data():
    start = datetime(2020, 1, 1).date()
    get_data(reload_data=True, reload_sp500=True, start=start)
    compile_data()


def main():
    ticker = Stock('TSLA', force=True)
    ticker.stock_returns()


def func():
    table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies', header=0)[0]
    tickers = table.loc[table['Symbol'] == 'AMZN']
    print(tickers)


if __name__ == "__main__":
    func()
