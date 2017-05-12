"""Plot approximation using regression."""
import numpy as np

import PlotGraph


def linearRegression(x, y):
    """Calulate m and b for (m * x + b) for regression on x and y."""
    n = len(x)
    average_x = np.sum(x) / n
    average_y = np.sum(y) / n
    scalar_term = np.inner(x, y)
    squared_sum = np.sum(x**2)
    m = (n * average_x * average_y - scalar_term) / \
        (n * average_x * average_x - squared_sum)
    return np.array([m, average_y - m * average_x])


def quadraticRegressionMatrix(x, y):
    """Create equation system and solve it using matrix operations."""
    A = np.zeros(shape=(3, 3))
    res_a = np.inner(x**2, y)
    res_b = np.inner(x, y)
    res_c = np.sum(y)
    res = np.array([res_a, res_b, res_c])
    A[0] = [np.sum(x**4), np.sum(x**3), np.sum(x**2)]
    A[1] = [np.sum(x**3), np.sum(x**2), np.sum(x)]
    A[2] = [np.sum(x**2), np.sum(x), len(x)]
    return np.dot(np.linalg.inv(A), res)


def quadraticRegression(x, y):
    """Solve 3 x 3 equation system explicitly."""
    # define variables from equation system
    t = np.sum(x**2)
    s = np.sum(x**4) / t
    v = np.sum(x**3) / t
    k = np.sum(x) / t
    z = len(x) / t
    p = np.inner(x**2, y) / t
    j = np.inner(x, y) / t
    q = np.sum(y) / t
    # calculate solution
    temp = v * v - s
    c = ((1 - v * k) * (p * v - j * s) - (j - v * q) * temp) / \
        ((1 - v * k) * (v - k * s) - (k - v * z) * temp)
    b = (p * v - j * s - c * (v - k * s)) / temp
    a = (p - c - v * b) / s
    return np.array([a, b, c])

# coeff [m,b] evaluates m*x+b


def linearFunction(coeff, x):
    return coeff[0] * x + coeff[1]

# coeff=[a,b,c]  evaluates a*x^2+b*x+c


def quadraticFunction(coeff, x):
    return coeff[0] * x**2 + coeff[1] * x + coeff[2]


def plotLinear(x_axis, temperature, rainfall):
    """Plot linear regression."""
    temperature_axis, rainfall_axis = PlotGraph.initGraph(
        x_axis, temperature, rainfall, "Linear regression")
    coeff_temperature = linearRegression(x_axis, temperature)
    coeff_rain = linearRegression(x_axis, rainfall)
    boundary_points = np.array([x_axis[0], x_axis[len(x_axis) - 1]])
    values_temperature = linearFunction(coeff_temperature, boundary_points)
    values_rain = linearFunction(coeff_rain, boundary_points)
    temperature_axis.plot(
        boundary_points, values_temperature, linewidth=2, color="yellow")
    rainfall_axis.plot(boundary_points, values_rain,
                       linewidth=2, color="green")


def plotQuadratic(x_axis, temperature, rainfall):
    """Plot quadratic regression."""
    temperature_axis, rainfall_axis = PlotGraph.initGraph(
        x_axis, temperature, rainfall, "Quadratic regression")
    coeff_temperature = quadraticRegression(x_axis, temperature)
    coeff_rain = quadraticRegression(x_axis, rainfall)
    # check correct result with Matrix-version
    # print(coeff_rain)
    # print(quadraticRegressionMatrix(x_axis, rainfall))
    values_temperature = quadraticFunction(coeff_temperature, x_axis)
    values_rain = quadraticFunction(coeff_rain, x_axis)
    temperature_axis.plot(x_axis, values_temperature,
                          linewidth=2, color="yellow")
    rainfall_axis.plot(x_axis, values_rain, linewidth=2, color="green")


def plotPolynomial(x_axis, temperature, rainfall, degree=3):
    """Plot polynomial regression."""
    temperature_axis, rainfall_axis = PlotGraph.initGraph(
        x_axis, temperature, rainfall,
        "Polynomial regression (degree " + str(degree) + ")")

    # interpolates polynomial with data
    coeff_temperature = np.polyfit(x_axis, temperature, degree)
    coeff_rain = np.polyfit(x_axis, rainfall, degree)
    p_temperature = np.poly1d(coeff_temperature)
    p_rain = np.poly1d(coeff_rain)

    # calculates polynomial at all positions
    values_temperature = p_temperature(x_axis)
    values_rain = p_rain(x_axis)

    # plots computed approximation
    temperature_axis.plot(x_axis, values_temperature,
                          linewidth=2, color="yellow")
    rainfall_axis.plot(x_axis, values_rain, linewidth=2, color="green")
