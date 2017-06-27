from math import cos, sin

import matplotlib.pyplot as plt
import numpy as np


def computeExtremePoint(x_values, y_values, derivation_y_values, interval_width):
    """Return the data's global extreme points."""
    max_x_values = []
    max_y_values = []
    min_x_values = []
    min_y_values = []
    for i in range(len(derivation_y_values) - 1):
        if derivation_y_values[i] < 0 and derivation_y_values[i + 1] > 0:
            x = x_values[i * interval_width]
            y = y_values[i * interval_width]
            min_x_values.append(x)
            min_y_values.append(y)
        elif derivation_y_values[i] > 0 and derivation_y_values[i + 1] < 0:
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


def function(x): return sin(x)


def correct_derivation(x): return cos(x)


if __name__ == "__main__":
    start = -6
    end = 6
    steps = 200

    x_values, y_values = computeFunctionValues(
        correct_derivation, start, end, steps)
    plt.plot(x_values, y_values, 'r--')

    x_values, y_values = computeFunctionValues(function, start, end, steps)
    plt.plot(x_values, y_values, 'r')

    interval_width = 5

    derivation_x_values, derivation_y_values = approximateDerivation(
        x_values, y_values, interval_width, True)
    plt.plot(derivation_x_values, derivation_y_values, '.')

    max_x_values, max_y_values, min_x_values, min_y_values = computeExtremePoint(
        x_values, y_values, derivation_y_values, interval_width)
    if len(max_x_values) != 0:
        plt.plot(max_x_values, max_y_values, 'go')
    if len(min_x_values) != 0:
        plt.plot(min_x_values, min_y_values, 'yo')

    plt.grid(True)
    plt.show()
