import requests
import bs4
import pickle
import os
from datetime import datetime
import pandas_datareader as pdr
import pandas as pd
import Constants


def save_sp500_tickers():
    # Wikipedia page that has the full list of tickers
    resp = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = bs4.BeautifulSoup(resp.text, features='lxml')
    table = soup.find('tbody')
    tickers = []
    if not os.path.exists(Constants.FILE_PATH):
        os.makedirs(Constants.FILE_PATH)
    # tickers table
    for row in table.findAll('tr')[1:]:
        # first column of the table for each line that has the ticker name
        ticker = row.findAll('td')[0].text
        # Avoid line-end after ticker name
        ticker = ticker.replace("\n", "")
        tickers.append(ticker)
    # Extra add Tesla or other tickers to the list
    tickers.append('TSLA')
    # save to a file
    with open(f"{Constants.FILE_PATH}/sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
    print(tickers)
    return tickers


def get_data(reload_sp500=False, reload_data=False, start=None):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        try:
            with open(f"{Constants.FILE_PATH}/sp500tickers.pickle", "rb") as f:
                tickers = pickle.load(f)
        except FileNotFoundError:
            print("File Not Found")
            return
    if not os.path.exists(Constants.TICKER_PATH):
        os.makedirs(Constants.TICKER_PATH)
    # if start is specified, else take a default value
    start = datetime(2010, 1, 1) if start is None else start
    for ticker in tickers[:]:
        if not reload_data:
            if not os.path.exists(f''):
                while True:
                    try:
                        df = pdr.DataReader(name=ticker, data_source='yahoo', start=start, end=datetime.today())
                        df.to_csv(f'{Constants.TICKER_PATH}/{ticker}.csv')
                        print(f'Detected {ticker}. Saving as {ticker}.csv')
                    except FileNotFoundError or KeyError:
                        print(f"Couldn't read {ticker}")
                    except requests.exceptions.ConnectionError:
                        continue
                    break
            else:
                print("Already have ticker saved")
        else:
            try:
                df = pdr.DataReader(name=ticker, data_source='yahoo', start=start, end=datetime.today())
                df.to_csv(f'{Constants.TICKER_PATH}/{ticker}.csv')
                print(f'Detected {ticker}. Saving as {ticker}.csv')
            except FileNotFoundError:
                print(f"Couldn't read {ticker}")
            except KeyError:
                pass


def get_ticker(ticker, start=None):
    if ticker is None:
        return
    if not os.path.exists(Constants.TICKER_PATH):
        os.makedirs(Constants.TICKER_PATH)
    start = datetime(2020, 1, 1) if start is None else start
    try:
        df = pdr.DataReader(name=ticker, data_source='yahoo', start=start, end=datetime.today())
        df.to_csv(f'{Constants.TICKER_PATH}/{ticker}.csv')
        print(f'Detected {ticker}. Saving as {ticker}.csv')
        return df
    except FileNotFoundError:
        print(f"Couldn't read {ticker}")


def compile_data():
    try:
        with open(f"{Constants.FILE_PATH}/sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    except FileNotFoundError:
        print("File Not Found")
        return
    main_df = pd.DataFrame()
    c = 0
    for count, ticker in enumerate(tickers):
        try:
            df = pd.read_csv(f'{Constants.TICKER_PATH}/{ticker}.csv')
            df.set_index('Date', inplace=True)
            df.rename(columns={'Adj Close': ticker}, inplace=True)
            df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)
            if main_df.empty:
                main_df = df
            else:
                main_df = main_df.join(df, how='outer')
            print(f"Compiling {c}/{len(tickers)}")
        except FileNotFoundError:
            print("Ticker file not found")
        c += 1
    main_df.to_csv(f'{Constants.FILE_PATH}/sp500_closes.csv')


def read_from_csv(ticker, date=True):
    if date:
        df = pd.read_csv(f"{Constants.TICKER_PATH}/{ticker}.csv", parse_dates=True, index_col='Date')
    else:
        df = pd.read_csv(f"{Constants.TICKER_PATH}/{ticker}.csv")
    return df
