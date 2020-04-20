from data.reader import get_data, compile_data
from data.stock import Stock
from datetime import datetime


def reload_data():
    start = datetime(2020, 1, 1).date()
    get_data(reload_data=True, reload_sp500=True, start=start)
    compile_data()


def main():
    ticker1 = Stock.from_csv('AMZN')
    print(ticker1)


if __name__ == "__main__":
    main()
