"""Module to plot data using different approximation methods."""
import matplotlib.pyplot as plt
import numpy as np

import Average
import Derivation
import Interpolation
import ReadData
import Regression


def plotGraphs(temperature, rainfall, start, end):
    """Plot different graphs out of given data."""
    x_axis = np.arange(start, end)

    # use the average to approximate data
    # Average.plotConstant(x_axis, temperature, rainfall)
    # Average.plotPiecewise(x_axis, temperature, rainfall)
    # Average.plotRunning(x_axis, temperature, rainfall)

    # use the Lagrange polynomial to approximate data
    # Interpolation.plotLagrangePolynomial(x_axis, temperature, rainfall)

    # Regression.plotLinear(x_axis, temperature, rainfall)
    # Regression.plotQuadratic(x_axis, temperature, rainfall)
    # Regression.plotPolynomial(x_axis, temperature, rainfall, 3)
    # Regression.plotMovingLeastSquares(x_axis, temperature, rainfall)

    Derivation.plotDerivation(x_axis, temperature, rainfall, 20)
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    start = 210
    end = 425
    # TODO: make sure that start as well as end values are valid
    (temperature, rainfall) = ReadData.getData(start, end)
    plotGraphs(temperature, rainfall, start, end)
