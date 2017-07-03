"""Module handling the different layers of the map."""
from math import pi, sin, sqrt
from random import randrange

import numpy as np
import PyQt5.QtCore as core
import PyQt5.QtGui as gui


class MapLayer(gui.QImage):
    """QImage as a base layer containing the landscape of the map."""

    def computeLandscape(self, x_coordinate):
        """
        Return the height of the land to a given x value.

        Uses randomly shifted and stretched / compressed sinus functions
        to compute the landscape.
        """
        W = np.linspace(0.001, 0.05, 20)
        y_coordinate = 0
        for w in W:
            intermediate_result = (
                1 / sqrt(w)) * sin(w * x_coordinate + randrange(0, 2 * pi)) * randrange(-1, 1)
            y_coordinate += intermediate_result
        return y_coordinate

    def __init__(self, width, height):
        """Initialize the landscape."""
        color_data = np.zeros([width, height, 4], dtype=np.uint8)
        color_format = gui.QImage.Format_RGB32
        super(MapLayer, self).__init__(color_data, width, height, color_format)
        painter = gui.QPainter(self)
        painter.setPen(gui.QPen(core.Qt.blue, 2))
        painter.drawLine(50, 50, 50, 100)
