#!/usr/bin/env python

__author__ = 'Fred Flores'
__version__ = '0.0.1'
__date__ = '2020-05-21'
__email__ = 'fredflorescfa@gmail.com'

import pandas as pd
from datetime import datetime


class SP500(object):

    def __init__(self):
        data = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')

        self.current_list = data[0]
        self.current_list['current_member'] = 1
        self.changes = data[1]
        self.changes[('Date', 'Date')] = pd.to_datetime(self.changes[('Date', 'Date')], format='%B %d, %Y')

    def get_constituents(self, as_of_datetime):
        """ Get the constituents as of a specified date. Get current list and work backwards through changes.
            Get current list, subtract any additions between specified date and current date, add back
            any deletions that occurred between specified date and current date."""

        assert isinstance(as_of_datetime, datetime), 'Invalid datetime type.'

        # Get current list of constituents
        C = self.current_list[['Symbol', 'current_member']].set_index('Symbol')

        # Get list of historical changes to index since the as of date
        these_chgs = self.changes.loc[self.changes[('Date', 'Date')] >= as_of_datetime]

        # Count the number of times each ticker was added to index
        adds = these_chgs[[('Date', 'Date'), ('Added', 'Ticker')]].dropna().droplevel(level=0, axis=1)
        adds['action'] = -1
        A = adds.pivot(index='Ticker', columns='Date', values='action').fillna(0).sum(axis=1).to_frame(name='undo_adds')

        # Count the number of times each ticker was deleted from index
        deletes = these_chgs[[('Date', 'Date'), ('Removed', 'Ticker')]].dropna().droplevel(level=0, axis=1)
        deletes['action'] = 1
        D = deletes.pivot(index='Ticker', columns='Date', values='action').fillna(0).sum(axis=1).to_frame(name='undo_deletes')

        # Merge the current list, adds, and deletes
        as_of_constituents = pd.concat([C, A, D], axis=1).fillna(0)
        as_of_constituents['as_of_member'] = as_of_constituents.sum(axis=1)

        return list(as_of_constituents[as_of_constituents['as_of_member'] == 1].index)
