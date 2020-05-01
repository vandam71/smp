from data.reader import Reader
from data.stock import Stock
from datetime import datetime
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (10, 5)
# TODO docstrings


def reload_data():
    reader = Reader()
    reader.fetch_data(reload_data=False, reload_tickers=False, start=datetime(2020, 1, 1)).dump_to_csv()
    reader.compile_data()


def main():
    ticker1 = Stock.from_pickle("AMZN")
    # CODE GOES HERE

    # ---------------
    plt.show()
    ticker1.dump()


if __name__ == "__main__":
    main()
