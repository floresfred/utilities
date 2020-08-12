#!/usr/bin/env python

__author__ = 'Fred Flores'
__version__ = '0.0.1'
__date__ = '2020-05-05'
__email__ = 'fredflorescfa@gmail.com'


"""Generate and Compare Data Distributions."""

from utilities import util
import numpy as np
from scipy.stats import powerlaw, norm, expon, lognorm, laplace, kstwobign, kstest, ks_2samp
import pandas as pd
import matplotlib.pyplot as plt


def set_distribution(name='norm', loc=0, scale=1, shape=1):
    distribution = {'norm': (norm(loc=loc, scale=scale),
                             r'Normal Distribution',
                             r'$p(x)=\frac{\exp(-x^2/2)}{\sqrt{2\pi}}$' + r'loc = {:.2f}, scale = {:.2f}'.format(loc, scale)),
                    'expon': (expon(loc=loc, scale=scale),
                              r'Exponential Distribution',
                              r'$p(x)=\exp(-x)}$' + r'loc = {:.2f}, scale = {:.2f}'.format(loc, scale)),
                    'powerlaw': (powerlaw(a=shape+1),
                                 r'Power Law Distribution',
                                 r'$p(x,\alpha)=\alpha x^{\alpha-1}$' + r', $\alpha-1 = {:.2f}$'.format(shape)),
                    'lognorm': (lognorm(s=shape),
                                r'Lognormal Distribution',
                                r'$p(x,s)=\frac{1}{sx\sqrt{2\pi}} exp(-\frac{\log^2(x)}{2s^2})$' +
                                r', $shape = {:.2f}$'.format(shape))}
    return distribution[name]


def plot_distribution(name='norm', sample_size=10000, loc=0, scale=1, bins=None, color='royalblue',
                      shape=1, figsize=(12, 4), log_scale=True):
    """ Plot theoretical distribution and a random sample from the same distribution. """
    dist = set_distribution(name=name, loc=loc, scale=scale, shape=shape)
    y = dist[0].rvs(size=sample_size)

    x = np.linspace(dist[0].ppf(0), dist[0].ppf(1), 100)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    plt.suptitle(dist[1] + ', ' + dist[2], y=1.03, fontsize=12)

    ax1.hist(y, density=True, bins=bins, alpha=.5,
             label='Random Sample (N = {:0d})'.format(sample_size), color=color)
    ax1.plot(x, dist[0].pdf(x), 'k-', lw=2, label='Theoretical Distribution')  # histtype='stepfilled',
    ax1.set_title('PDF')

    ax1.set_ylabel(r'$p(x)$')
    ax1.set_xlabel(r'$x$')
    ax1.legend(loc='best', frameon=False)

    ax2.hist(y, density=True, cumulative=True, alpha=.5,
             label='Random Sample (N = {:0d})'.format(sample_size), color=color)
    ax2.plot(x, dist[0].cdf(x), 'k-', lw=2, label='Theoretical Distribution')
    ax2.set_title('CDF')

    if log_scale:
        ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax2.set_xscale('log')
        ax2.set_yscale('log')
        ax1.set_ylabel(r'$log(p(x))$')
        ax1.set_xlabel(r'$log(x)$')
        ax2.set_ylabel(r'$log(\Phi(x))$')
        ax2.set_xlabel(r'$log(x)$')
    else:
        ax1.set_ylabel(r'$p(x)$')
        ax1.set_xlabel(r'$x$')
        ax2.set_ylabel(r'$\Phi(x)$')
        ax2.set_xlabel(r'$x$')

    plt.show()


def plot_empirical_distribution(y, title='title', bins=None, color='royalblue', figsize=(12, 4), log_scale=True):

    """ Plot empirical distribution and a random sample from the same distribution. """

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    plt.suptitle(title, y=1.03, fontsize=12)

    ax1.hist(y, density=True, bins=bins, alpha=.5, color=color)
    ax1.set_title('PDF')

    ax2.hist(y, density=True, cumulative=True, alpha=.5, color=color)
    ax2.set_title('CDF')

    if log_scale:
        ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax2.set_xscale('log')
        ax2.set_yscale('log')
        ax1.set_ylabel(r'$log[p(x)]$')
        ax1.set_xlabel(r'$log(x)$')
        ax2.set_ylabel(r'$log[\Phi(x)]$')
        ax2.set_xlabel(r'$log(x)$')
    else:
        ax1.set_ylabel(r'$p(x)$')
        ax1.set_xlabel(r'$x$')
        ax2.set_ylabel(r'$\Phi(x)$')
        ax2.set_xlabel(r'$x$')

    plt.show()


def numpy_array(x):
    """Transform pandas series or list to numpy array."""
    data_types = {pd.core.series.Series: (lambda x: x.values),
                  np.ndarray: (lambda x: x),
                  list: (lambda x: np.array(x))}

    assert type(x) in data_types.keys(), 'invalid data type. Enter numpy array, pandas series , or list of float.'

    return data_types[type(x)](x)


def cdf(x, plot=True):
    x = np.sort(numpy_array(x))
    n = len(x)
    y = np.arange(1, n+1, dtype=float)/n

    if plot:
        plt.figure(figsize=(6, 4))
        plt.step(x, y, c='royalblue', where='pre')
        plt.title('Cumulative Density Function (CDF)')
        plt.xlabel(r'$x$')
        plt.ylabel(r'$\Phi(X \leq x)$')
        plt.legend(frameon=False)
        plt.yticks(np.arange(0, 1.1, step=.1))
        plt.axhline(0.5, c='grey', ls='--', lw=1)
        plt.show()

    return x, y


def ks_2sample(x, y, confidence_interval=0.90, plot=True, bins=100, figsize=(12, 6)):
    """Compute the Kolmogorov-Smirnoff Distance between 2 sample distributions: CDF(x) and CDF(y).
       Null hypothesis: x and y are samples drawn from the same underlying distribution.

       p-value < threshold confidence level e.g., 0.01, 1% ==> reject null hypotheses."""

    x = np.sort(numpy_array(x))
    y = np.sort(numpy_array(y))
    z = np.sort(numpy_array(list(set(x).union(set(y)))))  # superset of values

    # Compute the CDFs for the superset of values (x and y).
    # np.searchsorted() reindexes the original array by inserting superset values
    # and maintaining order of original indices. Furthermore, it handles repetitive values.
    cdfx = np.searchsorted(x, z, side='right') / len(x)
    cdfy = np.searchsorted(y, z, side='right') / len(y)

    # Compute the maximum, absolute difference between the CDFs (vertical distance in plot).
    max_abs_diff = np.max(np.abs(cdfx - cdfy))
    max_loc = np.argmax(np.abs(cdfx - cdfy))  # returns the first occurrence only
    vline_bot = np.min([cdfx[max_loc], cdfy[max_loc]])
    vline_top = np.max([cdfx[max_loc], cdfy[max_loc]])

    # Use scipy implementation to compare distance ("max_abs_diff" should equal "distance")
    distance, p_value = ks_2samp(x, y, alternative='two-sided', mode='auto')
    critical_value = kstwobign.ppf(confidence_interval) * np.sqrt((len(x)+len(y)) / (len(x)*len(y)))

    color1 = 'darkblue'
    color2 = 'darkred'

    if plot:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

        # PDFs
        label1 = r'$n_1={:0d}$, $\mu_1={:.2f}$, $\sigma_1={:.2f}$'.format(len(x), np.mean(x), np.std(x))
        label2 = r'$n_2={:0d}$, $\mu_2={:.2f}$, $\sigma_2={:.2f}$'.format(len(y), np.mean(y), np.std(y))
        ax1.hist(x, bins=bins, density=True, edgecolor=None, facecolor=color1, label=label1, lw=1.5, alpha=0.5)
        ax1.hist(y, bins=bins, density=True, edgecolor=None, facecolor=color2, label=label2, lw=1.5, alpha=0.5)
        ax1.set_title('PDF')
        ax1.set_xlabel(r'$x$')
        ax1.set_ylabel(r'$\phi(x)$')
        ax1.legend(frameon=False, loc='upper center')

        # CDFs
        ks_text = r'$d_{KS}=' + r'{:.4f}$, $cv={:.4f}$ ($\alpha={:.2f}$)'.\
            format(distance, critical_value, confidence_interval)
        ax2.plot(z, cdfx, c=color1, label='$CDF_1$', lw=1.5, alpha=0.5)
        ax2.plot(z, cdfy, c=color2, label='$CDF_2$', lw=1.5, alpha=0.5)
        ax2.set_title(r'CDF')
        ax2.set_xlabel(r'$x$')
        ax2.set_ylabel(r'$\Phi(X \leq x)$')
        ax2.set_yticks(np.arange(0, 1.2, step=.1))
        ax2.set_ylim(0, 1.2)
        ax2.vlines(z[max_loc], vline_bot, vline_top, lw=1, ls='--', colors='grey', label=ks_text)
        ax2.axhline(vline_top, np.min(z), np.max(z), lw=1, ls='--', c='grey')
        ax2.axhline(vline_bot, np.min(z), np.max(z), lw=1, ls='--', c='grey')
        ax2.legend(frameon=False, loc='best')  #  bbox_to_anchor=(0, 1)
        plt.show()

    return distance, p_value


