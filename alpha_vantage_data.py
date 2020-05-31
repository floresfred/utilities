#!/usr/bin/env python

__author__ = 'Fred Flores'
__version__ = '0.0.1'
__date__ = '2020-04-19'
__email__ = 'fredflorescfa@gmail.com'

from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import time
from utilities import util
import pandas as pd
import numpy as np
from datetime import datetime as dt

key = 'C1MLXDST5B1WH97M'  # created 2020-04-19 fredflorescfa@gmail.com

# Some AV APIs
ts = TimeSeries(key, output_format='pandas')
ti = TechIndicators(key)


def price_volume(ticker_list, frequency='daily'):
    """Retrieve daily prices, 5 tickers at a time with a minute lag from Alpha Vantage."""

    # This needs to be fixed. The grouped method is dropping companies that don't make a complete 5 member group
    # and not making a group at all for lists < 5.
    if len(ticker_list) > 5:
        tick_grp = list(set(util.grouped(ticker_list, 5)))
    else:
        tick_grp = list(set(ticker_list))

    df = pd.DataFrame()
    counter = 1

    for tckr in tick_grp:

        if counter > 1:
            time.sleep(60 + np.random.randint(2, 25))

        for t in tckr:

            try:  # Get daily prices and volumes
                get = {'daily': ts.get_daily(symbol=t),
                       'monthly': ts.get_monthly(symbol=t)}
                company, meta = get[frequency]

                # company, meta = ts.get_daily(symbol=t)
                company['ticker'] = t
                company['run_date'] = pd.to_datetime(dt.now(), unit='ns')

                # Compute daily returns
                company['d_ret'] = company['4. close'].sort_index(ascending=True).pct_change(periods=1)

                # Reset index and merge into main dataset
                company = company.reset_index()
                df = pd.concat((df, company))
                counter += 1

            except:
                print('Invalid ticker: ' + t)

    return df
