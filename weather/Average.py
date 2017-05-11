"""Plot average based approximation."""
import math

import numpy as np

import PlotGraph


def plotConstantAverage(x_axis, temperature, rainfall):
    """Plot given data with standard average."""
    temperature_axis, rainfall_axis = PlotGraph.initGraph(
        x_axis, temperature, rainfall, "Graph with constant average")

    # plots constant average for temperature
    avg_temperature = np.average(temperature)
    temperature_axis.axhline(avg_temperature, linewidth=2, color='yellow')

    # plots constant average for rainfall
    avg_rainfall = np.average(rainfall)
    rainfall_axis.axhline(avg_rainfall, linewidth=2, color='green')


def plotPiecewiseAverage(x_axis, temperature, rainfall, intervals=20):
    """Divide data into intervals and plot the average over these intervals."""
    temperature_axis, rainfall_axis = PlotGraph.initGraph(
        x_axis, temperature, rainfall,
        "Graph with piecewise average approximation"
        + " (" + str(intervals) + " intervals)")

    # constant to scale the x values if the
    # plot's x axis does not start at 0
    lowest_x_value = x_axis[0]

    interval_size = math.ceil(len(temperature) / intervals)

    x_values = []
    y_values_temperature = []
    y_values_rainfall = []

    for i in range(intervals - 1):
        # calculates start and end index of the interval
        interval_start = i * interval_size
        interval_end = (i + 1) * interval_size
        # calculates average over the specified interval
        avg_temperature = np.average(temperature[interval_start:interval_end])
        avg_rainfall = np.average(rainfall[interval_start:interval_end])
        # uses the middle of the interval as x value
        x_value = ((interval_start + interval_end - 1) // 2) + lowest_x_value
        # inserts calculated values to the corresponding lists
        x_values.append(x_value)
        y_values_temperature.append(avg_temperature)
        y_values_rainfall.append(avg_rainfall)

    # calculates the last interval seperately
    # because its length may be different
    last_interval_start = (intervals - 1) * interval_size
    last_avg_temperature = np.average(temperature[last_interval_start:])
    last_avg_rainfall = np.average(rainfall[last_interval_start:])
    last_x_value = (
        (last_interval_start + len(temperature) - 1) // 2) + lowest_x_value
    x_values.append(last_x_value)
    y_values_temperature.append(last_avg_temperature)
    y_values_rainfall.append(last_avg_rainfall)

    # plots all values
    temperature_axis.plot(x_values, y_values_temperature,
                          linewidth=2, color="yellow")
    rainfall_axis.plot(x_values, y_values_rainfall, linewidth=2, color="green")


def plotRunningAverage(x_axis, temperature, rainfall, interval_width=20):
    """Plot the running average on given data."""
    temperature_axis, rainfall_axis = PlotGraph.initGraph(
        x_axis, temperature, rainfall,
        "Graph with running average approximation"
        + " (width of interval: " + str(interval_width) + ")")

    # constant to scale the x values if the
    # plot's x axis does not start at 0
    lowest_x_value = x_axis[0]

    x_values = []
    y_values_temperature = []
    y_values_rainfall = []

    # moves the chosen interval step by step over the whole array
    # while calculating the average over each intermediate interval
    for i in range(interval_width, len(temperature) + 1):
        # calculates start and end index of the interval
        interval_start = i - interval_width
        interval_end = i
        # calculates average over the specified interval
        avg_temperature = np.average(temperature[interval_start:interval_end])
        avg_rainfall = np.average(rainfall[interval_start:interval_end])
        # uses the middle of the interval as x value
        x_value = ((interval_start + interval_end - 1) // 2) + lowest_x_value
        # inserts calculated values to the corresponding lists
        x_values.append(x_value)
        y_values_temperature.append(avg_temperature)
        y_values_rainfall.append(avg_rainfall)

    temperature_axis.plot(x_values, y_values_temperature,
                          linewidth=2, color="yellow")
    rainfall_axis.plot(x_values, y_values_rainfall, linewidth=2, color="green")
