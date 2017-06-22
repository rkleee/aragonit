"""Module providing functions to compute the derivative of data."""
import matplotlib.pyplot as plt
import numpy as np

import PlotGraph


def calcDerivation(data, interval_width=1, normal=True):
    x_values = []
    y_values = []

    number_of_intervals = len(data) // interval_width
    if normal:
        # use normal derivation function
        for i in range(number_of_intervals - 1):
            x = i * interval_width
            y = (data[x + interval_width] - data[x]) / interval_width
            x_values.append(x)
            y_values.append(y)
    else:
        # use alternative derivation function
        for i in range(number_of_intervals - 1):
            value = (data[(i * interval_width) + interval_width] -
                     data[(i * interval_width) - interval_width]) / (2 * interval_width)
            derivation.append(value)
    return x_values, y_values


def plotDerivation(x_axis, temperature, rainfall, interval_width=1, normal_derivation=True):
    """Plot approximated derivation of given data."""
    temperature_axis, rainfall_axis = PlotGraph.initGraph(
        x_axis, temperature, rainfall, "Derivation")

    if normal_derivation:
        temperature_x_values, temperature_y_values = calcDerivation(
            temperature, interval_width, True)
        rainfall_x_values, rainfall_y_values = calcDerivation(
            rainfall, interval_width, True)
    else:
        temperature_x_values, temperature_y_values = calcDerivation(
            temperature, interval_width, False)
        rainfall_x_values, rainfall_y_values = calcDerivation(
            rainfall, interval_width, False)

    temperature_axis.plot(
        temperature_x_values, temperature_y_values, linewidth=2, color="yellow")
    rainfall_axis.plot(
        rainfall_x_values, rainfall_y_values, linewidth=2, color="green")
