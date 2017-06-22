"""Plot approximation using Lagrange polynomials."""
import numpy as np

import PlotGraph


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


def plotLagrangePolynomial(x_axis, temperature, rainfall, control_points=5):
    """Use Lagrange interpolation to approximate the data."""
    temperature_axis, rainfall_axis = PlotGraph.initGraph(
        x_axis, temperature, rainfall,
        "Approximation using Lagrange polynomials")

    # gets x values of equally distributed points within the data
    x_chosen_points = np.linspace(x_axis[0], x_axis[-1], control_points,
                                  endpoint=False, dtype=np.int64)

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

    # makes sure that unimportant x values (i.e. values smaller than
    # the smallest x value of all chosen points or greater than the biggest)
    # are excluded regarding the plot of the Lagrange polynomial
    x_axis = np.arange(x_chosen_points[0], x_chosen_points[-1] + 1)

    x_values_temperature = []
    x_values_rainfall = []
    y_values_temperature = []
    y_values_rainfall = []

    # computes and evaluates the corresponding interpolation polynomial
    for x in x_axis:
        # interpolates the temperature data
        y_temperature = calcInterpolationPolynomial(
            x, x_chosen_points, y_chosen_points_temperature)
        x_values_temperature.append(x)
        y_values_temperature.append(y_temperature)

        # interpolates the rainfall data
        y_rainfall = calcInterpolationPolynomial(
            x, x_chosen_points, y_chosen_points_rainfall)
        x_values_rainfall.append(x)
        y_values_rainfall.append(y_rainfall)

    # displays interpolated data
    temperature_axis.plot(x_values_temperature, y_values_temperature,
                          linewidth=2, color="yellow")
    rainfall_axis.plot(x_values_rainfall, y_values_rainfall,
                       linewidth=2, color="green")
