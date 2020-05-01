from mplfinance.original_flavor import candlestick_ohlc
from matplotlib.dates import date2num, DateFormatter
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd
from utilities.dates import get_business_days


def pandas_dataframe(data: pd.DataFrame, ticker: str, days: int = 0):
    if days == 0:
        days = data.shape[0]
    data = data[-days:]
    data.plot(grid=True)
    plt.title(ticker)
    plt.xlabel('Dates')
    plt.ylabel('Share Value ($)')
    plt.show(block=False)


def pandas_candlestick(data: pd.DataFrame, ticker: str, days: int = 0, window: int = 10):
    """
    Plots a candlestick graph for the data coming. Plots _days_ in the past with a _window_ for values
    :param data: pd.DataFrame
    :param ticker: str
    :param days: int
    :param window: INT
    :return: None
    """
    if days == 0:
        days = data.shape[0]
    df = data[-days:].copy()
    df = df['Adj Close'].resample(f'{window}D').ohlc()
    df.reset_index(inplace=True)
    diff = get_business_days(df['Date'][-1:].values.astype('datetime64[D]'), dt.datetime(2020, 1, 1).date())
    df['Date'] = df['Date'].map(date2num)
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    ax.grid(True)
    ax.xaxis_date()
    ax.autoscale_view()
    candlestick_ohlc(ax, df.values, width=1, colorup='green', colordown='red')
    if days < diff:
        ax.xaxis.set_major_formatter(DateFormatter('%b %d'))
    else:
        ax.xaxis.set_major_formatter(DateFormatter('%b %Y'))
    plt.title(f'{ticker} Candle Stick')
    plt.xlabel('Dates')
    plt.ylabel('Share Value ($)')
    plt.show(block=False)
