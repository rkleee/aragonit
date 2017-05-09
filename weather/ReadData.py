"""Module to read the data file."""
import numpy as np


def loadData(fileName):
    """Create matrix representation of given textfile."""
    return np.loadtxt(fileName, comments="#", skiprows=3)


def getDataSegment(data, column, start, end):
    """Return the values of a given column in the given interval."""
    return data[start:end, column]


def getData(start, end):
    """Return temperature and rainfall values in the given interval."""
    # loads relevant data from file
    data = loadData("data.txt")
    # column index for temperature
    TX = 6
    # column index for rainfall
    RR = 12
    temperature = getDataSegment(data, TX, start, end)
    rainfall = getDataSegment(data, RR, start, end)
    return (temperature, rainfall)
