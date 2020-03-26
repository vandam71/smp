from data.stocks import get_data, compile_data
from data.ticker import Ticker
import Constants
import pandas as pd
import matplotlib.pyplot as plt


def reload_data():
    get_data(reload_data=True, reload_sp500=True)
    compile_data()


def main():
    ticker = 'AMZN'
    df = pd.read_csv(f"{Constants.TICKER_PATH}/{ticker}.csv", parse_dates=True, index_col='Date')
    df = df[-50:]
    ticker = Ticker(df, ticker)
    full = pd.DataFrame({'Growth': ticker.stock_growth()['Growth'],
                         'Increase': ticker.stock_increase()['Increase'],
                         'Change': ticker.stock_change()['Change']})
    full.plot(grid=True).axhline(y=0, color='black', lw=2)
    ticker.draw_candlestick()
    plt.show()


if __name__ == "__main__":
    main()
