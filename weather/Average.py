"""Module to plot data with its average values."""
import math

import matplotlib.pyplot as plt
import numpy as np

import ReadData


def initGraph(x_axis, temperature, rainfall, title="Plot"):
    """Initialize graph to plot temperature and rainfall values."""
    figure, temperature_axis = plt.subplots()
    figure.canvas.set_window_title(title)

    # axis for temperature data
    # plots the temperature data
    temperature_axis.plot(x_axis, temperature, color="r")
    # colours the values on the temperature axis
    temperature_axis.tick_params('y', colors="r")
    # sets appropriate labels
    temperature_axis.set_xlabel("Zeitpunkt")
    temperature_axis.set_ylabel("Temperatur")

    # axis for rainfall data
    # uses the same x axis as for the temperature plot
    rainfall_axis = temperature_axis.twinx()
    # plots the rainfall data
    rainfall_axis.plot(x_axis, rainfall, color="b")
    # colours the values on the rainfall axis
    rainfall_axis.tick_params('y', colors="b")
    # sets appropriate labels
    rainfall_axis.set_ylabel("Niederschlag")


def plotConstantAverage(x_axis, temperature, rainfall):
    """Plot given data with standard average."""
    initGraph(x_axis, temperature, rainfall, "Graph with constant average")

    # plots constant average for temperature
    avg_temperature = np.average(temperature)
    plt.axhline(avg_temperature, linewidth=1, color='r')

    # plots constant average for rainfall
    avg_rainfall = np.average(rainfall)
    plt.axhline(avg_rainfall, linewidth=1, color='b')


def plotPiecewiseAverage(x_axis, temperature, rainfall, num_of_intervals):
    """Divide data into intervals and plot the average over these intervals."""
    initGraph(x_axis, temperature, rainfall,
              "Graph with piecewise average approximation")

    interval_size = math.ceil(len(temperature) / num_of_intervals)

    x_values = []
    y_values_temperature = []
    y_values_rainfall = []

    for i in range(num_of_intervals - 1):
        # calculates start and end index of the interval
        interval_start = i * interval_size
        interval_end = (i + 1) * interval_size
        # calculates average over the specified interval
        avg_temperature = np.average(temperature[interval_start:interval_end])
        avg_rainfall = np.average(rainfall[interval_start:interval_end])
        # uses the middle of the interval as x value
        x_value = (interval_start + interval_end) // 2
        # inserts all values to the lists
        x_values.append(x_value)
        y_values_temperature.append(avg_temperature)
        y_values_rainfall.append(avg_rainfall)

    # calculates the last interval seperately
    # because its length may be different
    last_interval_start = (num_of_intervals - 1) * interval_size
    last_avg_temperature = np.average(temperature[last_interval_start:])
    last_avg_rainfall = np.average(rainfall[last_interval_start:])
    last_x_value = (last_interval_start + len(temperature)) // 2
    x_values.append(last_x_value)
    y_values_temperature.append(last_avg_temperature)
    y_values_rainfall.append(last_avg_rainfall)

    # plots all values
    plt.plot(x_values, y_values_temperature, color="r")
    plt.plot(x_values, y_values_rainfall, color="b")


def plotRunningAverage(x_axis, temperature, rain):
    container = plt.figure()
    container.canvas.set_window_title("Plot with running average")
    ax1 = container.add_subplot(111)
    (ax1, ax2) = initAxes(ax1, x_axis, rain, temperature)

    intervalWidth = 10

    x_values = []
    y_values = []
    for i in range(len(temperature) - intervalWidth):
        avg = np.average(temperature[i:(intervalWidth + i)])
        x_values.append(((intervalWidth + i) - i) / 2)
        y_values.append(avg)
    ax1.plot(x_values, y_values, ":",  color="firebrick")

    x_values = []
    y_values = []
    for i in range(len(rain)):
        avg = np.average(temperature[:i])
        x_values.append(i / 2)
        y_values.append(avg)
    ax2.plot(x_values, y_values, ":", color="royalblue")


def plotGraphs(temperature, rainfall, start, end):
    """Plot different graphs out of given data."""
    x_axis = np.arange(start, end)
    plotConstantAverage(x_axis, temperature, rainfall)
    plotPiecewiseAverage(x_axis, temperature, rainfall, 17)
    # plotAverageWithIntervalls(x_axis, temperature, rain, 3)
    # plotRunningAverage(x_axis, temperature, rain)
    plt.show()


if __name__ == "__main__":
    start = 0
    end = 500
    # TODO: make sure that start as well as end values are valid
    (temperature, rainfall) = ReadData.getData(start, end)
    plotGraphs(temperature, rainfall, start, end)
