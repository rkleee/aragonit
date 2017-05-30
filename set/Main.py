"""Main module to test the CustomSet classes."""
import math

import numpy as np

import CustomSet as cs


def binomialCoefficient(n, k):
    a = math.factorial(n)
    b = math.factorial(k)
    c = math.factorial(n - k)
    return a / (b * c)


def function(x):
    return x**3 + 2 * x + 1


def plotFunction(x, y=None):
    return y == function(x)


def deltaFunction(x, y=None):
    if y is None:
        return x == 3
    else:
        return x == 1 and y == function(1)


if __name__ == "__main__":
    list1 = ["a", "b", "c", "d"]
    list2 = np.arange(0, 2)
    list3 = [function(x) for x in list2]
    set1 = cs.Set(list1)
    set2 = cs.Set(list2)
    set3 = cs.Set(list3)

    s = set2.getSpecifiedSubset(deltaFunction)

    cp_delta = cs.CartesianProduct(set2, set3, deltaFunction)
    cp_plot = cs.CartesianProduct(set2, set3, plotFunction)

    # calculate the number of different functions on the specified
    # CartesianProduct instance
    n = len(list2)
    number_func_combinations = 0
    for i in range(1, n + 1):
        number_x_values_affected_by_function = binomialCoefficient(n, i)
        for j in range(i + 1):
            number_y_values_affected_by_function = binomialCoefficient(n, j)
            number_func_combinations += number_x_values_affected_by_function \
                * number_y_values_affected_by_function
    print("Number of possible functions:", number_func_combinations)

    # check whether or not the CartesianProduct instances are functions
    if callable(cp_delta) or callable(cp_plot):
        print("Yippie! The CartesianProduct instance is a function!")
    else:
        print("Damn! Something with that __call__ thing went wrong...")

    print(cp_plot)

    cp_plot.plot()
