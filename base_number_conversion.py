#!/usr/bin/env python

__author__ = 'Fred Flores'
__version__ = '0.0.1'
__date__ = '2020-04-11'
__email__ = 'fredflorescfa@gmail.com'

import numpy as np
import re


def split_number(x):
    """" Split float into its sign, integer part, and fractional part. """
    assert isinstance(x, (float, int)), 'Not a valid number.'

    if x < 0:
        sign = '-'
    else:
        sign = '+'

    x = x * 1.0  # convert to float
    x = np.abs(x)
    x = str(x).split('.')
    integer_part = int(x[0])
    fractional_part = float('.' + x[1])

    return sign, integer_part, fractional_part
    

def decimal_to_binary(x, places=20):
    """ Convert decimal number to binary number.
        For integer part employ repeated division by 2 method.
        For fractional part employ repeated multiplication by 2 method.

        Negative decimal signified by '-' sign."""

    assert isinstance(x, (int, float)), 'Invalid number.'
    assert places <= 50, 'The number of places must be <= 50.'

    # Split decimal number into sign, integer part, and fractional part
    sign, integer_part, fractional_part = split_number(x)

    # Convert decimal integer into binary integer
    int_binary = ''
    while integer_part != 0:
        int_binary += str(int(integer_part % 2))  # remainder is 0 or 1
        integer_part = (integer_part / 2) // 1  # get integer to left of decimal place

    # Convert decimal fraction into binary fraction
    frac_binary = ''
    counter = 0  # count iterations as computation may not converge
    while (fractional_part != 0) & (counter < places):
        counter += 1
        result = fractional_part * 2.0
        frac_binary += str(int(result // 1))  # result is 0 or 1
        fractional_part = result - (result // 1)  # get fractional number to right of decimal place

    if frac_binary == '':
        return sign + int_binary[::-1]
    else:
        return sign + int_binary[::-1] + '.' + frac_binary


def binary_to_decimal(binary_str, places=20):

    assert isinstance(binary_str, str), 'Invalid string. Enter binary as string (e.g., \'-1010.01010\')'

    # Validate integers are 0 or 1 only
    str_check = re.sub("[^0-9]", "", binary_str)
    for c in str_check:
        assert c in ['1', '0'], 'Invalid digit found in binary string: \'' + c + '\''

    # Split decimal number into sign, integer part, and fractional part
    if binary_str[0] == '-':
        sign = '-'
        binary_str = binary_str[1:]
    else:
        sign = ''

    integer_part = binary_str.split('.')[0]
    fractional_part = binary_str.split('.')[1]

    # Convert binary integer to decimal integer
    reversed_int_part = integer_part[::-1]
    p = 0
    int_sum = 0
    for s in reversed_int_part:
        if s == '1':
            int_sum += np.power(2, p)
        p += 1

    # Convert binary fraction to decimal fraction
    p = 1
    frac_sum = 0
    for s in fractional_part[:places]:
        if s == '1':
            frac_sum += 1 / np.power(2, p)
        p += 1

    # Construct decimal number
    if sign == '-':
        multiplier = -1
    else:
        multiplier = 1

    if frac_sum == 0:
        return multiplier * int(int_sum)
    else:
        return multiplier * (int_sum + frac_sum)




        


