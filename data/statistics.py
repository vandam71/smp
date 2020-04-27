class Statistics:
    def __init__(self, data):
        self.close = data['Adj Close'].to_numpy()
