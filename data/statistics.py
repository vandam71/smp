# TODO statistics class


class Statistics(object):
    def __init__(self, data):
        self.close = data['Adj Close'].to_numpy()
