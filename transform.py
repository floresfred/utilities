#!/usr/bin/env python

__author__ = 'Fred Flores'
__version__ = '0.0.1'
__date__ = '2020-04-05'
__email__ = 'fredflorescfa@gmail.com'

import numpy as np
import pandas as pd


def normalize(s, lo_pctl=0.01, hi_pctl=.99):
    """ Compute z-score = (x - mean) / standard_deviation
        Where mean and standard deviation are computed using only values within [lo_pctl, hi_pctl]
        range.
        Return array with same shape."""

    data_types = {pd.core.series.Series: (lambda x: x.values),
                  np.ndarray: (lambda x: x), 
                  list: (lambda x: np.array(x))}

    this_type = type(s)
    assert this_type in data_types.keys(), 'invalid data type. Enter numpy array, pandas series , or list of float.'
    
    for b in [lo_pctl, hi_pctl]:
        assert (b >= 0) & (b <= 1), 'invalid winsor bound. Value must be fraction: > 0 and < 1.'
    assert lo_pctl < hi_pctl, 'invalid winsor bound. First item '

    y = data_types[type(s)](s)
    z = np.empty(y.shape)
    z[:] = np.nan

    # Compute mean and stdev excluding outliers defined by lo and hi_pctl
    if len(y) > 1:
        upper_bound = np.nanquantile(y, hi_pctl)
        lower_bound = np.nanquantile(y, lo_pctl)
        with np.errstate(invalid='ignore'):  # ignore stupid warning about 'invalid value encountered in less than'
            mu = np.nanmean(y[(y >= lower_bound) & (y <= upper_bound)])
            sigma = np.nanstd(y[(y >= lower_bound) & (y <= upper_bound)])

        if sigma == 0:
            sigma = np.nan

        # Compute normalized variable
        with np.errstate(invalid='ignore'):
            y[y < lower_bound] = lower_bound
            y[y > upper_bound] = upper_bound
            z = (y - mu) / sigma

    return z

