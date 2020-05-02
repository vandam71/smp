import numpy as np
from scipy.stats import norm
from utilities.dates import get_business_days, today, subtract_years


class Statistics(object):
    DROPS = [-0.01, -0.05, -0.10, -0.15, -0.20, -0.25, -0.30, -0.35, -0.40, -0.45, -0.50]
    QUANTILE = [0.05, 0.25, 0.75, 0.95]

    def __init__(self, data: []) -> None:
        """
        Initializes the Statistic class
        :param data: numpy array
        """
        self._close = data
        self._returns = np.array(np.diff(np.log(self._close)))
        self._mean = np.array(self._returns.mean())
        self._sigma = np.array(self._returns.std(ddof=1))

    def daily_drops(self) -> []:
        """
        Probability of drops under a certain percentage in a day
        :return: []
        """
        return norm.cdf(self.DROPS, self._mean, self._sigma)

    def yearly_drops(self) -> []:
        """
        Probability of drops under a certain percentage in a year
        Sometimes there aren't values in a data set to fill a year, these results
        will get more accurate with more values
        :return: []
        """
        days = get_business_days(today().date(), subtract_years(today(), 1).date())
        return norm.cdf(self.DROPS, days * self._mean, (days**0.5) * self._sigma)
    
    def quantile(self) -> []:
        """
        Quantile values for the percentages defined in self.QUANTILE
        :return: []
        """
        return norm.ppf(self.QUANTILE, self._mean, self._sigma)

    def z_scores(self) -> float:
        """
        Standardized test statistic for Z-Scores
        :return: float
        """
        return self._mean / (self._sigma / (len(self._returns)**0.5))
