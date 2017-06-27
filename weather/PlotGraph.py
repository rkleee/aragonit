"""Plot graph out of given data."""
import matplotlib.pyplot as plt


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
