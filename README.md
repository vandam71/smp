# smp
SMP - Stock Market Predictor based on TensorFlow neural networks pattern analysis and aims to predict stock market values for the given company.

# reload_data()
```python
def reload_data():
    reader = Reader()
    reader.fetch_data(reload_data=True, reload_tickers=True, start=datetime(2020, 1, 1)).dump_to_csv()
    reader.compile_data()
```
In this function `Reader()` uses Wikipedia's S&P 500 companies to fetch and store all the tickers available to process, using `reader.fetch_data(...)` to read and store a .csv file for each and everyone of the tickers, using Pandas capabilities to retrieve this information from Yahoo. `reader.compile_data()` compiler every Adj Close column in these files into a single one for every ticker in the reader.

# Main function
```python
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
```
In this example, the program reads a single ticker and computes a graph of it into a window.


# TO-DO
[ ] In progress...
