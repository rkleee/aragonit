"""Module to plot data with different approximations."""
import matplotlib.pyplot as plt
import numpy as np

import Average
import Interpolation
import ReadData


def plotGraphs(temperature, rainfall, start, end):
    """Plot different graphs out of given data."""
    x_axis = np.arange(start, end)

    # uses the average to approximate the data
    Average.plotConstantAverage(x_axis, temperature, rainfall)
    Average.plotPiecewiseAverage(x_axis, temperature, rainfall)
    Average.plotRunningAverage(x_axis, temperature, rainfall)

    # uses the Lagrange polynomial to approximate the data
    Interpolation.plotLagrangePolynomial(x_axis, temperature, rainfall)
    plt.show()


if __name__ == "__main__":
    start = 0
    end = 500
    # TODO: make sure that start as well as end values are valid
    (temperature, rainfall) = ReadData.getData(start, end)
    plotGraphs(temperature, rainfall, start, end)
