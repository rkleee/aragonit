import matplotlib.pyplot as plt
import numpy as np

import ReadData


def initAxes(ax1, x, rain, temperature):
    """Initialize temperature and rainfall axes."""
    # axis for temperature
    ax1.plot(x, temperature, color="red")
    ax1.tick_params('y', colors="red")
    ax1.set_xlabel("Zeitpunkt")
    ax1.set_ylabel("Temperatur")
    # ax2 with same x-axes for rain
    ax2 = ax1.twinx()
    ax2.tick_params('y', colors="blue")
    ax2.plot(x, rain, "-", color="blue")
    ax2.set_ylabel("Niederschlag")
    return (ax1, ax2)


def plotAverage(x_axis, temperature, rain):
    """Plot given data with standard average."""
    container = plt.figure()
    container.canvas.set_window_title("Plot with constant approximation")
    ax1 = container.add_subplot(111)
    (ax1, ax2) = initAxes(ax1, x_axis, rain, temperature)
    x = [x_axis[0], x_axis[-1]]
    av_temp = np.average(temperature)
    av_temp_arr = [av_temp, av_temp]
    av_rain = np.average(rain)
    av_rain_arr = [av_rain, av_rain]
    ax1.plot(x, av_temp_arr, ":", color="firebrick")
    ax2.plot(x, av_rain_arr, ":", color="royalblue")

# divides input into intervalls and calculates/plots average over these
# intervalls


def plotAverageWithIntervalls(x_axis, temperature, rain, intervals):
    container = plt.figure()
    container.canvas.set_window_title(
        "Plot with piecewise approximation using "
        + str(intervals) + " intervals"
    )
    ax1 = container.add_subplot(111)
    (ax1, ax2) = initAxes(ax1, x_axis, rain, temperature)

    # TO-DO: Implement-Average using intervalls


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


def plotGraphs(temperature, rain, start, end):
    """Plot different graphs out of the given data."""
    x_axis = np.arange(start, end)
    plotAverage(x_axis, temperature, rain)
    plotAverageWithIntervalls(x_axis, temperature, rain, 3)
    # plotRunningAverage(x_axis, temperature, rain)
    plt.show()


if __name__ == "__main__":
    start = 0
    end = 500
    # TODO: make sure that start as well as end values are valid
    (temperature, rain) = ReadData.getData(start, end)
    plotGraphs(temperature, rain, start, end)
