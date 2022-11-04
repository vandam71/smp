import pandas_market_calendars as cal
import numpy as np
import datetime as dt


def get_business_days(start, end):
    """
    Calculates de business day difference between two dates (according to NYSE market)
    :param start: dt.datetime.date()
    :param end: dt.datetime.date()
    :return: int
    """
    nyse = cal.get_calendar('NYSE')
    holidays = nyse.holidays()
    holidays = list(holidays.holidays)
    return np.busday_count(end, start, holidays=holidays)


def subtract_years(date: dt.datetime, years):
    """
    Subtract two years, if the year is leap calculate the difference to day
    :param date: dt.datetime
    :param years: int
    :return: dt.datetime
    """
    try:
        return date.replace(year=date.year-years)
    except ValueError:
        return date.replace(year=date.year - years, day=date.day - 1)


def today():
    """
    Returns the today date as datetime
    :return: dt.datetime
    """
    return dt.datetime.now()
