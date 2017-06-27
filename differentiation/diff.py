from sys import maxsize

import matplotlib.pyplot as plt
import numpy as np


def computeExtremePoint(x_values, y_values, derivation_y_values, interval_width):
    """Return the data's global extreme points."""
    global_max_x_value = None
    global_max_y_value = -maxsize
    global_min_x_value = None
    global_min_y_value = maxsize
    for i in range(len(derivation_y_values) - 1):
        if derivation_y_values[i] < 0 and derivation_y_values[i + 1] > 0:
            y = y_values[i * interval_width]
            if global_min_y_value > y:
                global_min_x_value = x_values[i * interval_width]
                global_min_y_value = y
        elif derivation_y_values[i] > 0 and derivation_y_values[i + 1] < 0:
            y = y_values[i * interval_width]
            if global_max_y_value < y:
                global_max_x_value = x_values[i * interval_width]
                global_max_y_value = y
    return global_max_x_value, global_max_y_value, global_min_x_value, global_min_y_value


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


def plotFunction(function, start=-5, end=-5, steps=10, dotted=False):
    """Plot the given function on the specified interval."""
    x_values, y_values = computeFunctionValues(function, start, end, steps)
    if dotted:
        plt.plot(x_values, y_values, 'r--')
    else:
        plt.plot(x_values, y_values, 'r')


if __name__ == "__main__":
    function = np.poly1d([1, 0, -1, 1, -1, 0])  # x^5 - x^3 + x^2 -x
    correct_derivation = np.poly1d([5, 0, -3, 2, -1])  # 5*x^4 - 3*x^2 + 2*x -1

    start = -2
    end = 2
    steps = 100

    plotFunction(function, start, end, steps)
    plotFunction(correct_derivation, start, end, steps, True)

    x_values, y_values = computeFunctionValues(function, start, end, steps)

    interval_width = 2

    derivation_x_values, derivation_y_values = approximateDerivation(
        x_values, y_values, interval_width, True)
    plt.plot(derivation_x_values, derivation_y_values, '.')

    # derivation_x_values, derivation_y_values = approximateDerivation(
    #     x_values, y_values, 20, True)
    # plt.plot(derivation_x_values, derivation_y_values)

    global_max_x_value, global_max_y_value, global_min_x_value, global_min_y_value = computeExtremePoint(
        x_values, y_values, derivation_y_values, interval_width)

    if global_max_x_value is not None:
        plt.plot(global_max_x_value, global_max_y_value, 'go')
    elif global_min_x_value is not None:
        plt.plot(global_min_x_value, global_min_y_value, 'yo')

    plt.grid(True)
    plt.show()

    # step_width = (end - start) / (steps - 1)

    # h = (end - start) / (numIntervalls - 1)
    # approx1 = []
    # y = p(grid)
    # for i in range(len(y) - 1):
    #     approx1.append((y[i] + y[i + 1]) / h)
    # approx2 = []
    # for i in range(1, len(y) - 1):
    #     approx2.append((y[i - 1] + y[i + 1]) / (2 * h))
    # max_val = []
    # min_val = []
    # max_x = []
    # min_x = []
    # k = 0
    # for i in range(1, len(approx1) - 1):
    #     if approx1[i - 1] < 0 and approx1[i + 1] > 0:
    #         max_val.append(y[i])
    #         max_x.append(grid[i])
    #         print(i)
    #     elif approx1[i - 1] > 0 and approx1[i] < 0:
    #         min_val.append(y[i])
    #         min_x.append(grid[i])
    #         print(i)
    # print(max_x)
    # print(max_val)
    # y_ = p_(grid)
    # plt.plot(grid, y, '--')
    # plt.plot(grid, y_, '--')
    # grid = np.delete(grid, -1)
    # plt.plot(grid, approx1)
    # grid = np.delete(grid, 1)
    # plt.plot(grid, approx2)
    # plt.plot(max_x, max_val)
    # plt.plot(min_x, min_val)
    # plt.show()
