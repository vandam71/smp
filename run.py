from data.reader import Reader
from data.stock import Stock
from datetime import datetime
from interface.application import Application
from interface.tab import GraphWindow


def reload_data():
    reader = Reader()
    reader.fetch_data(reload_data=True, reload_tickers=True, start=datetime(2020, 1, 1)).dump_to_csv()
    reader.compile_data()


def main():
    ticker1 = Stock.from_csv("AMZN")
    # CODE GOES HERE
    fig = ticker1.draw_candlestick(window=4, days=200)
    app = Application()
    window = GraphWindow(ticker1.get_ticker())
    window.change_content(fig)
    app.add_tab(window)
    app.mainloop()
    # --------------
    ticker1.dump()


if __name__ == "__main__":
    main()
