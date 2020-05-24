from mplfinance.original_flavor import candlestick_ohlc
from matplotlib.dates import date2num, DateFormatter
from matplotlib.figure import Figure
import datetime as dt
import pandas as pd
from utilities.dates import get_business_days


def pandas_dataframe(data: pd.DataFrame, ticker: str, days: int = 0):
    """
    Plots a pandas dataframe for a ticker, in the time window of _days_
    :param data: pd.Dataframe
    :param ticker: str
    :param days: int
    :return: Figure
    """
    names = list(data.columns)
    if days == 0:
        days = data.shape[0]
    data = data[-days:]
    fig = Figure()
    a = fig.add_subplot(111, title=f'{ticker} Market Value', xlabel='Dates', ylabel='Share Value ($)')
    l1, l2, l3, l4 = a.plot(data)
    a.grid(True)
    a.legend((l1, l2, l3, l4), names)
    return fig


def pandas_candlestick(data: pd.DataFrame, ticker: str, days: int = 0, window: int = 10):
    """
    Plots a candlestick graph for the data coming. Plots _days_ in the past with a _window_ for values
    :param data: pd.DataFrame
    :param ticker: str
    :param days: int
    :param window: int
    :return: Figure
    """
    if days == 0:
        days = data.shape[0]
    df = data[-days:].copy()
    df = df['Adj Close'].resample(f'{window}D').ohlc()
    df.reset_index(inplace=True)
    diff = get_business_days(df['Date'][-1:].values.astype('datetime64[D]'), dt.datetime(2020, 1, 1).date())
    df['Date'] = df['Date'].map(date2num)
    fig = Figure()
    ax = fig.add_subplot(111, title=f'{ticker} Candle Stick', xlabel='Dates', ylabel='Share Value ($)')
    ax.grid(True)
    ax.xaxis_date()
    ax.autoscale_view()
    candlestick_ohlc(ax, df.values, width=1, colorup='green', colordown='red')
    if days < diff:
        ax.xaxis.set_major_formatter(DateFormatter('%b %d'))
    else:
        ax.xaxis.set_major_formatter(DateFormatter('%b %Y'))
    return fig
