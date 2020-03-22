from mplfinance.original_flavor import candlestick_ohlc
from matplotlib.dates import date2num, DateFormatter
import pandas_market_calendars as cal
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np


def pandas_candlestick(data, ticker, days=0, window=10):
    if days == 0:
        days = data.shape[0]
    df = data[-days:].copy()
    df = df['Adj Close'].resample(f'{window}D').ohlc()
    df.reset_index(inplace=True)
    diff = get_business_days(df['Date'][-1:].values.astype('datetime64[D]'), dt.datetime(2020, 1, 1, 0, 0).date())
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
    plt.show()


def get_business_days(start, end):
    nyse = cal.get_calendar('NYSE')
    holidays = nyse.holidays()
    holidays = list(holidays.holidays)
    return np.busday_count(end, start, holidays=holidays)[0]
