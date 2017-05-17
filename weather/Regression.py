"""Plot approximation using regression."""
import math

import numpy as np

import PlotGraph


def linearRegression(x, y):
    """
    Compute coefficients of linear regression polynomial.

    Uses given formula.
    """
    n = len(x)
    average_x = np.average(x)
    average_y = np.average(y)
    scalar_term = np.inner(x, y)
    squared_sum = np.sum(x**2)
    m = (n * average_x * average_y - scalar_term) / \
        (n * average_x * average_x - squared_sum)
    return np.array([m, average_y - m * average_x])


def linearRegressionMatrix(x_values, y_values):
    """
    Compute coefficients of linear regression polynomial.

    Uses the inverse matrix.
    """
    # fills the matrix
    upper_left = sum(x_values)
    upper_right = len(x_values)
    lower_left = sum([x ** 2 for x in x_values])
    matrix = np.array([[upper_left, upper_right], [lower_left, upper_left]])

    # fills the vector
    first = sum(y_values)
    second = sum([a * b for a, b in zip(x_values, y_values)])
    vector = [first, second]

    # computes coefficients using the inverse matrix
    return np.dot(np.linalg.inv(matrix), vector)


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


def linearFunction(coefficients, x_values):
    """Evaluate x values on a linear polynomial with given coefficients."""
    return [coefficients[0] * x + coefficients[1] for x in x_values]


def quadraticFunction(coefficients, x_values):
    """Evaluate x values on a quadratic polynomial with given coefficients."""
    return [coefficients[0] * (x ** 2) + coefficients[1] * x + coefficients[2] for x in x_values]


def createRegressionPolynomial(x_axis, data, degree):
    """Return coefficients of regression polynomial with given degree."""
    # computes the coefficients of the corresponding regression polynomial
    coeff_data = np.polyfit(x_axis, data, degree)
    return coeff_data


def evaluatePolynomial(coefficients, x_values):
    """Evaluate given x values to a polynomial with given coefficients."""
    # creates a function out of the given coefficients
    func_data = np.poly1d(coefficients)
    # calculates the function values for all x values
    values_data = func_data(x_values)
    return values_data


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


def plotPolynomial(x_axis, temperature, rainfall, degree=3,maxErrorDegree=16):
    """Plot polynomial regression."""
    temperature_axis, rainfall_axis = PlotGraph.initGraph(
        x_axis, temperature, rainfall,
        "Polynomial regression (degree: " + str(degree) + ")")

    # creates corresponding regression polynomial and
    # computes all necessary function values
    coeff_temperature = createRegressionPolynomial(
        x_axis, temperature, degree)
    values_temperature = evaluatePolynomial(coeff_temperature, x_axis)
    coeff_rain = createRegressionPolynomial(x_axis, rainfall, degree)
    values_rain = evaluatePolynomial(coeff_rain, x_axis)

    # plots computed approximation
    temperature_axis.plot(x_axis, values_temperature,
                          linewidth=2, color="yellow")
    rainfall_axis.plot(x_axis, values_rain, linewidth=2, color="green")

    temperature_Regression_Error = []
    rainfall_Regression_Error = []
    # calculate Average Regression Error for degrees from 0 to 10
    for degree in range(maxErrorDegree):
        temperature_Regression_Error.append(
            RegressionAverageError(x_axis, temperature, degree))
        rainfall_Regression_Error.append(
            RegressionAverageError(x_axis, rainfall, degree))
    #plot Regression Errors
    temperature_Error_axis, rainfall_Error_axis =PlotGraph.initGraph([],[],[],"RegressionError")
    temperature_Error_axis.set_xlabel("Degree of polynomial")
    temperature_Error_axis.plot(range(maxErrorDegree),temperature_Regression_Error,linewidth=2,color="red")
    rainfall_Error_axis.plot(range(maxErrorDegree),rainfall_Regression_Error,linewidth=2,color="blue")

    
    

    # To-Do: Plot degree of polynomial and corresponding Regression Error


def plotMovingLeastSquares(x_axis, temperature, rainfall, interval_width=9, degree=3):
    """Plot moving least squares (MLS) approximation."""
    temperature_axis, rainfall_axis = PlotGraph.initGraph(
        x_axis, temperature, rainfall,
        "Moving least squares (MLS) approximation (interval width: "
        + str(interval_width) + ", degree: " + str(degree) + ")")

    # constant to scale the x values if the
    # plot's x axis does not start at 0
    lowest_x_value = x_axis[0]

    x_values = []
    y_values_temperature = []
    y_values_rainfall = []

    # moves the chosen interval step by step over the whole array
    # while calculating the regression polynomial over each
    # intermediate interval and plotting the correponding function
    # value at the middle of the interval
    for i in range(interval_width, len(temperature) + 1):
        # calculates start and end index of the interval
        interval_start = i - interval_width
        interval_end = i

        # creates the specified interval of the x axis
        interval = np.arange(interval_start + lowest_x_value,
                             interval_end + lowest_x_value)

        # creates corresponding regression polynomial and
        # computes the function value of the middle x value
        coeff_temperature = createRegressionPolynomial(
            interval, temperature[interval_start:interval_end], degree)
        values_temperature = evaluatePolynomial(coeff_temperature, interval)
        coeff_rainfall = createRegressionPolynomial(
            interval, rainfall[interval_start:interval_end], degree)
        values_rainfall = evaluatePolynomial(coeff_rainfall, interval)

        # computes the x value in the middle of the interval
        x_value = ((interval_start + interval_end) // 2) + lowest_x_value
        interval_middle_index = math.floor(interval_width / 2)

        # inserts calculated values to the corresponding lists
        x_values.append(x_value)
        y_values_temperature.append(values_temperature[interval_middle_index])
        y_values_rainfall.append(values_rainfall[interval_middle_index])

    temperature_axis.plot(x_values, y_values_temperature,
                          linewidth=2, color="yellow")
    rainfall_axis.plot(x_values, y_values_rainfall, linewidth=2, color="green")

# calculates the regression error of the given polynomial with test data


def RegressionError(coeff, x_test, y_test):
    func = np.poly1d(coeff)
    return np.average((func(x_test) - y_test)**2)

# Be carefull: This implementation might be slow for big dataSets!!
# calcualtes Average Regreesion error for given data by randomply splitting data
# and fiting polyomial with given degree on the train data


def RegressionAverageError(x_axis, data, degree, n=10):
    error = 0
    # repeat n times for average
    for k in range(n):
        # randomly permute x_axis
        permuted_axis = np.random.permutation(x_axis)
        permuted_data = []
        # match x-values with data values
        for i in range(len(permuted_axis)):
            for j in range(len(x_axis)):
                if x_axis[j] == permuted_axis[i]:
                    permuted_data.append(data[j])
        # split x_values and data values in train and test set
        (x_test, x_train) = np.array_split(permuted_axis, 2)
        (values_test, values_train) = np.array_split(permuted_data, 2)
        # calculate Regression polynomial
        coeff_data = createRegressionPolynomial(x_train, values_train, degree)
        # calcualte Regression Error for this permuation
        error += RegressionError(coeff_data, x_test, values_test)
    # average over all
    return error / n
