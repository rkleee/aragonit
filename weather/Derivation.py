"""Module providing functions to compute the derivative of data."""
from math import cos, sin

import numpy as np
from matplotlib import pyplot as plt


def computeExtremePoints(x_values, y_values, deriv_y_values, interval_width):
    """Return the data's global extreme points."""
    max_x_values = []
    max_y_values = []
    min_x_values = []
    min_y_values = []
    for i in range(len(deriv_y_values) - 1):
        if deriv_y_values[i] < 0 and deriv_y_values[i + 1] > 0:
            x = x_values[i * interval_width]
            y = y_values[i * interval_width]
            min_x_values.append(x)
            min_y_values.append(y)
        elif deriv_y_values[i] > 0 and deriv_y_values[i + 1] < 0:
            x = x_values[i * interval_width]
            y = y_values[i * interval_width]
            max_x_values.append(x)
            max_y_values.append(y)
    return max_x_values, max_y_values, min_x_values, min_y_values


def approximateDerivation(x_values, y_values, interval_width=10, normal=True):
    """Approximate the derivation of the given function."""
    derivation_x_values = []
    derivation_y_values = []
    if normal:
        # use normal derivation function
        index = 0
        while (index + interval_width) < (len(x_values) - 1):
            y = (y_values[index + interval_width] -
                 y_values[index]) / interval_width
            derivation_x_values.append(x_values[index])
            derivation_y_values.append(y)
            index += interval_width
    else:
        # use alternative derivation function
        index = interval_width
        while (index + interval_width) < (len(x_values) - 1):
            y = (y_values[index + interval_width] -
                 y_values[index - interval_width]) / (2 * interval_width)
            derivation_x_values.append(x_values[index])
            derivation_y_values.append(y)
            index += interval_width
    return derivation_x_values, derivation_y_values


def computeFunctionValues(function, start=-5, end=5, steps=10):
    """Evaluate the given function on the specified interval."""
    x_values = np.linspace(start, end, steps)
    y_values = []
    for x in x_values:
        y_values.append(function(x))
    return x_values, y_values


def plotApproximatedDerivation(x_values, y_values, interval_width=10, normal=True):
    """Plot approximation derivation and its corresponding extreme points."""
    # plot given data
    plotData(x_values, y_values)
    # approximate derivation function
    deriv_x_values, deriv_y_values = approximateDerivation(
        x_values, y_values, interval_width, normal)
    # plot derivation function
    plt.plot(deriv_x_values, deriv_y_values, 'y')
    # compute all extreme points
    max_x_values, max_y_values, min_x_values, min_y_values = computeExtremePoints(
        x_values, y_values, deriv_y_values, interval_width)
    # add extreme points to the plot
    if len(max_x_values) > 0:
        plt.plot(max_x_values, max_y_values, 'co')
    if len(min_x_values) > 0:
        plt.plot(min_x_values, min_y_values, 'mo')


def plotData(x_values, y_values):
    plt.plot(x_values, y_values, 'r')


def function(x): return sin(x)


def derivation(x): return cos(x)


if __name__ == "__main__":
    start = -6
    end = 6
    steps = 500

    # get function data
    func_x_values, func_y_values = computeFunctionValues(
        function, start, end, steps)

    # plot function data and its approximated derivation
    interval_width = 5
    plotApproximatedDerivation(
        func_x_values, func_y_values, interval_width, True)

    # plot correct derivation
    deriv_x_values, deriv_y_values = computeFunctionValues(
        derivation, start, end, steps)
    plt.plot(deriv_x_values, deriv_y_values, 'r--')

    plt.grid(True)
    plt.show()
