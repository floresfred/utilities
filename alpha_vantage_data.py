#!/usr/bin/env python

__author__ = 'Fred Flores'
__version__ = '0.0.1'
__date__ = '2020-04-19'
__email__ = 'fredflorescfa@gmail.com'

from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt

# Your key here
key = 'C1MLXDST5B1WH97M'  # created 2020-04-19 fredflorescfa@gmail.com

# Chose your output format, or default to JSON (python dict)
ts = TimeSeries(key, output_format='pandas')
ti = TechIndicators(key)