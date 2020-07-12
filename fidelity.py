#!/usr/bin/env python

__author__ = 'Fred Flores'
__version__ = '0.0.1'
__date__ = '2020-05-05'
__email__ = 'fredflorescfa@gmail.com'

"""Read and format data from Fidelity Active Trader Pro Account"""

import pandas as pd
import numpy as np
import re

numeric_data = ['Security-Price', 'P-E-Price-TTM-Earnings-', 'S-P-500-R-', 'P-E-Next-Year-s-Estimate-',
                'P-E-This-Year-s-Estimate-', 'Price-Book-Ratio', 'Shares-Outstanding',
                'Volume-30-Day-Average-', 'Institutional-Ownership',
                'Institutional-Ownership-Last-vs-Prior-Qtr-', 'Market-Capitalization',
                'Beta-1-Year-Annualized-', 'Beta-5-Yr-Annualized-', 'Gross-Profit-Margin-TTM-',
                'Return-on-Equity-TTM-', 'Return-on-Assets-TTM-',
                'Debt-to-Capital-Ratio-Most-Recent-Qtr-', 'Profit-Margin-TTM-',
                'Earnings-Yield-TTM-', 'Earnings-Announcements-Upcoming-',
                'Positive-Earnings-Surprises-90-Days-', 'Negative-Earnings-Surprises-90-Days-',
                'Total-Return-1-Yr-Annualized-', 'EBITD-Margin-TTM-', '-Revenue-to-RD-Last-FY-',
                'SG-A-Expense-Net-Sales', 'Total-Debt-Equity-TTM-', 'Operating-Margin-TTM-']


# Extrapolate capitalization in numeric form
def cap(s):

    if not isinstance(s, str):
        mcap = np.nan
    else:
        non_decimal = re.compile(r'[^\d.]+')
        unit = s[-1:]
        multiplier = {'B': 1, 'T': 1000, 'M': 1/1000}

        if unit not in multiplier.keys():
            mcap = np.nan
        else:
            value = float(non_decimal.sub('', s))
            mcap = value * multiplier[unit]

    return mcap


def get_data():
    csv_loc = r'C:\Users\fredf\OneDrive\data\fidelity\screener_results.xls'

    df = pd.read_excel(csv_loc, nrows=504)

    # Remove any special characters from columns names
    df = df.rename(columns={s: re.sub('[\W_]+', '-', s) for s in df.columns})
    df['Market-Capitalization'] = df['Market-Capitalization'].apply(lambda s: cap(s))

    df[numeric_data] = df[numeric_data].apply(pd.to_numeric, errors='coerce')

    return df

