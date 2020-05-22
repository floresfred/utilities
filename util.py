#!/usr/bin/env python

__author__ = 'Fred Flores'
__version__ = '0.0.1'
__date__ = '2020-05-21'
__email__ = 'fredflorescfa@gmail.com'

import pickle


def pickle_save(obj, file_path):
    outfile = open(file_path, 'wb')
    pickle.dump(obj, outfile)
    outfile.close()


def pickle_load(file_path):
    infile = open(file_path, 'rb')
    obj = pickle.load(infile)
    infile.close()

    return obj


def grouped(iterable, n):
    """From an existing iterable, create new iterable in N chunks
        s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), (s2n,s2n+1,s2n+2,...s3n-1), ..."""
    return zip(*[iter(iterable)]*n)
