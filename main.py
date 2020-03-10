import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale
from keras import models
import pandas_datareader as pdr

pdr.get_data_yahoo("AMZN")

model = models.Sequential()
