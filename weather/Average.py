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
    # colours the entries on the temperature axis
    temperature_axis.tick_params('y', colors="r")
    # sets appropriate labels
    temperature_axis.set_xlabel("Zeitpunkt")
    temperature_axis.set_ylabel("Temperatur")

    # axis for rainfall data
    # uses the same x axis as for the temperature plot
    rainfall_axis = temperature_axis.twinx()
    # plots the rainfall data
    rainfall_axis.plot(x_axis, rainfall, color="b")
    # colours the entries on the rainfall axis
    rainfall_axis.tick_params('y', colors="b")
    # sets appropriate labels
    rainfall_axis.set_ylabel("Niederschlag")

    # return both axes for further processing
    return (temperature_axis, rainfall_axis)


def plotConstantAverage(x_axis, temperature, rainfall):
    """Plot given data with standard average."""
    temperature_axis, rainfall_axis = initGraph(
        x_axis, temperature, rainfall, "Graph with constant average")

    # plots constant average for temperature
    avg_temperature = np.average(temperature)
    temperature_axis.axhline(avg_temperature, linewidth=1, color='yellow')

    # plots constant average for rainfall
    avg_rainfall = np.average(rainfall)
    rainfall_axis.axhline(avg_rainfall, linewidth=1, color='green')


def plotPiecewiseAverage(x_axis, temperature, rainfall, num_of_intervals=20):
    """Divide data into intervals and plot the average over these intervals."""
    temperature_axis, rainfall_axis = initGraph(
        x_axis, temperature, rainfall,
        "Graph with piecewise average approximation"
        + " (" + str(num_of_intervals) + " intervals)")

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
        x_value = (interval_start + interval_end - 1) // 2
        # inserts calculated values to the corresponding lists
        x_values.append(x_value)
        y_values_temperature.append(avg_temperature)
        y_values_rainfall.append(avg_rainfall)

    # calculates the last interval seperately
    # because its length may be different
    last_interval_start = (num_of_intervals - 1) * interval_size
    last_avg_temperature = np.average(temperature[last_interval_start:])
    last_avg_rainfall = np.average(rainfall[last_interval_start:])
    last_x_value = (last_interval_start + len(temperature) - 1) // 2
    x_values.append(last_x_value)
    y_values_temperature.append(last_avg_temperature)
    y_values_rainfall.append(last_avg_rainfall)

    # plots all values
    temperature_axis.plot(x_values, y_values_temperature, color="yellow")
    rainfall_axis.plot(x_values, y_values_rainfall, color="green")


def plotRunningAverage(x_axis, temperature, rainfall, interval_width=30):
    """Plot the running average on given data."""
    temperature_axis, rainfall_axis = initGraph(
        x_axis, temperature, rainfall,
        "Graph with running average approximation"
        + " (width of interval: " + str(interval_width) + ")")

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
        x_value = (interval_start + interval_end - 1) // 2
        # inserts calculated values to the corresponding lists
        x_values.append(x_value)
        y_values_temperature.append(avg_temperature)
        y_values_rainfall.append(avg_rainfall)

    temperature_axis.plot(x_values, y_values_temperature, color="yellow")
    rainfall_axis.plot(x_values, y_values_rainfall, color="green")


def plotGraphs(temperature, rainfall, start, end):
    """Plot different graphs out of given data."""
    x_axis = np.arange(start, end)
    plotConstantAverage(x_axis, temperature, rainfall)
    plotPiecewiseAverage(x_axis, temperature, rainfall)
    plotRunningAverage(x_axis, temperature, rainfall)
    plt.show()


if __name__ == "__main__":
    start = 0
    end = 500
    # TODO: make sure that start as well as end values are valid
    (temperature, rainfall) = ReadData.getData(start, end)
    plotGraphs(temperature, rainfall, start, end)
