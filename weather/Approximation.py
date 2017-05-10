"""Module to plot data with its corresponding approximation."""
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
    temperature_axis.plot(x_axis, temperature, linewidth=1, color="r")
    # colours the entries on the temperature axis
    temperature_axis.tick_params('y', colors="r")
    # sets appropriate labels
    temperature_axis.set_xlabel("Zeitpunkt")
    temperature_axis.set_ylabel("Temperatur")

    # axis for rainfall data
    # uses the same x axis as for the temperature plot
    rainfall_axis = temperature_axis.twinx()
    # plots the rainfall data
    rainfall_axis.plot(x_axis, rainfall, linewidth=1, color="b")
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
    temperature_axis.axhline(avg_temperature, linewidth=2, color='yellow')

    # plots constant average for rainfall
    avg_rainfall = np.average(rainfall)
    rainfall_axis.axhline(avg_rainfall, linewidth=2, color='green')


def plotPiecewiseAverage(x_axis, temperature, rainfall, intervals=20):
    """Divide data into intervals and plot the average over these intervals."""
    temperature_axis, rainfall_axis = initGraph(
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


def plotRunningAverage(x_axis, temperature, rainfall, interval_width=30):
    """Plot the running average on given data."""
    temperature_axis, rainfall_axis = initGraph(
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


def calcLagrangePolynomial(x, k, x_values):
    """Calculate the specified Lagrange polynomial."""
    intermediate_result = 1
    n = len(x_values)
    for j in range(n):
        if (j != k):
            intermediate_result *= (x -
                                    x_values[j]) / (x_values[k] - x_values[j])
    return intermediate_result


def calcInterpolationPolynomial(x, x_values, y_values):
    """Use Lagrange interpolation to compute the function value of x."""
    result = 0
    n = len(y_values)
    for k in range(n):
        result += y_values[k] * calcLagrangePolynomial(x, k, x_values)
    return result


def plotLagrangePolynomial(x_axis, temperature, rainfall, control_points=10):
    """Use Lagrange interpolation to approximate the data."""
    temperature_axis, rainfall_axis = initGraph(
        x_axis, temperature, rainfall,
        "Approximation with Lagrange polynomial")

    # gets x values of equally distributed points within the data
    x_chosen_points = np.linspace(x_axis[0], x_axis[-1], control_points,
                                  endpoint=False, dtype=np.int16)

    # constant to scale the x values if the
    # plot's x axis does not start at 0
    lowest_x_value = x_axis[0]

    # gets the corresponding y values
    y_chosen_points_temperature = []
    y_chosen_points_rainfall = []
    for x in x_chosen_points:
        y_chosen_points_temperature.append(
            temperature[int(x - lowest_x_value)])
        y_chosen_points_rainfall.append(rainfall[int(x - lowest_x_value)])

    # plots all chosen points
    temperature_axis.plot(
        x_chosen_points, y_chosen_points_temperature, 'o', color="yellow")
    rainfall_axis.plot(
        x_chosen_points, y_chosen_points_rainfall, 'o', color="green")

    # computes and evaluates the corresponding interpolation polynomial
    y_values_temperature = []
    y_values_rainfall = []
    for x in x_axis:
        y_temperature = calcInterpolationPolynomial(
            x, x_chosen_points, y_chosen_points_temperature)
        y_values_temperature.append(y_temperature)

        y_rainfall = calcInterpolationPolynomial(
            x, x_chosen_points, y_chosen_points_rainfall)
        y_values_rainfall.append(y_rainfall)

    # plots both interpolation polynomials
    temperature_axis.plot(x_axis, y_values_temperature,
                          linewidth=2, color="yellow")
    rainfall_axis.plot(x_axis, y_values_rainfall, linewidth=2, color="green")


def plotGraphs(temperature, rainfall, start, end):
    """Plot different graphs out of given data."""
    x_axis = np.arange(start, end)

    # uses the average to approximate the data
    plotConstantAverage(x_axis, temperature, rainfall)
    plotPiecewiseAverage(x_axis, temperature, rainfall)
    plotRunningAverage(x_axis, temperature, rainfall)

    # uses the Lagrange polynomial to approximate the data
    plotLagrangePolynomial(x_axis, temperature, rainfall)
    plt.show()


if __name__ == "__main__":
    start = 120
    end = 240
    # TODO: make sure that start as well as end values are valid
    (temperature, rainfall) = ReadData.getData(start, end)
    plotGraphs(temperature, rainfall, start, end)
