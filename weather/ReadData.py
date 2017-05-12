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
    # loads all data from given file
    data = loadData("mannheim.txt")
    # column index for temperature
    TX = 6
    # column index for rainfall
    RR = 12
    # chooses and returns the relevant parts of the data
    temperature = getDataSegment(data, TX, start, end)
    rainfall = getDataSegment(data, RR, start, end)
    return (temperature, rainfall)
