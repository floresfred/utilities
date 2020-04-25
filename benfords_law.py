#!/usr/bin/env python

__author__ = 'Fred Flores'
__version__ = '0.0.1'
__date__ = '2020-04-24'
__email__ = 'fredflorescfa@gmail.com'

import re
import numpy as np
import pandas as pd
np.seterr(divide='ignore', invalid='ignore')


def significand(x):
    """Extract the significant digits from a number and return a string."""

    assert isinstance(x, (int, float)), 'Invalid number.'

    # Convert number to scientific notation
    sci_num = '%E' % x

    # Extract significand
    sig_digits = sci_num.split('E')[0].rstrip('0').rstrip('.')

    # Remove extraneous characters such as sign and decimal point
    sig_digits = re.sub("[^0-9]", "", str(sig_digits))

    return sig_digits


def digit_position(x, max_positions=10):
    """Locate the digits of a number in a position matrix where
            rows are the position number [0, max_positions)
            columns are the digits [0-9]."""
    digits = significand(x)  # convert number to a string of relevant digits

    if len(digits) > max_positions:
        digits = digits[:max_positions]  # reduce string if necessary to maximum length

    position_matrix = np.zeros((max_positions, 10))

    for p in np.arange(0, len(digits)):
        position_matrix[p, int(digits[p])] = 1

    return position_matrix


def digit_frequency(x, max_positions=10):
    """Compute the digit frequency from a series of numbers."""

    data_types = {pd.core.series.Series: (lambda x: x.values),
                  np.ndarray: (lambda x: x),
                  list: (lambda x: np.array(x))}

    assert type(x) in data_types.keys(), 'invalid data type. Enter numpy array, pandas series , or list of float.'

    # Convert data to a numpy array of valid numbers only
    y = data_types[type(x)](x)
    is_valid = ~np.isnan(y)
    y = y[is_valid]

    # Inspect string conversion
    digits = np.array([significand(yi) for yi in y])

    # Count occurrences of each digit in each position
    counts = np.zeros((max_positions, 10))
    for n in y:
        counts = counts + digit_position(n, max_positions=max_positions)

    frequency = np.divide(counts, counts.sum(axis=1).reshape(-1, 1))

    return frequency








