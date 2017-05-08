"""Module to read the data file."""
import numpy as np


def loadData(fileName):
    """Load data from given file."""
    return np.loadtxt(fileName, comments="#", skiprows=3)


def getDataSegment(data, start, end, column):
    """Return the values of a given column in the given interval."""
    return data[start:end:, column]


def getData(start, end):
    """Return temperature and rainfall values in the given interval."""
    # column index for temperature
    TX = 6
    # column index for rainfall
    RR = 12
    # loads relevant data from file
    data = loadData("data.txt")
    temperature = getDataSegment(data, start, end, TX)
    rainfall = getDataSegment(data, start, end, RR)
    return (temperature, rainfall)
