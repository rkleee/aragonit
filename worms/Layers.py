"""Module handling the different layers of the map."""
from math import pi, sin, sqrt
from random import uniform

import numpy as np
import PyQt5.QtCore as core
import PyQt5.QtGui as gui


class LandLayer(gui.QImage):
    """Layer containing the land mass of the map."""

    def _computeLandscapeParameters(self):
        """Set all constant factors for landscape creation function."""
        self.landscape_compression_factor = uniform(-1, 1)
        self.landscape_offset = uniform(0, 2 * pi)
        self.landscape_parameters = np.linspace(0.001, 0.05, 200)

    def _getLandscapeHeight(self, x_coordinate):
        """
        Return the height of the land to a given x value.

        Uses the sum of different randomly shifted and stretched
        or compressed sinus functions to compute the landscape.
        """
        y_coordinate = 0
        for param in self.landscape_parameters:
            weight_factor = 1 / sqrt(param)
            intermediate_result = weight_factor * \
                sin(param * x_coordinate + self.landscape_offset) * \
                self.landscape_compression_factor
            y_coordinate += intermediate_result
        return y_coordinate

    def _createLandscape(self):
        vertical_middle = len(self.color_data[0]) // 2
        for x in range(len(self.color_data)):
            border = self._getLandscapeHeight(x) + vertical_middle
            for y in range(len(self.color_data[0])):
                if y >= border:
                    self.color_data[y][x] = [0, 150, 0, 255]

    def __init__(self, width, height, color_format):
        """Initialize the landscape."""
        self.color_data = np.zeros([width, height, 4], dtype=np.uint8)
        self._computeLandscapeParameters()
        self._createLandscape()
        super(LandLayer, self).__init__(
            self.color_data, width, height, color_format)
        # painter = gui.QPainter(self)
        # painter.setPen(gui.QPen(core.Qt.blue, 2))
        # painter.drawLine(50, 50, 50, 100)7


class SkyLayer(gui.QImage):
    """Layer containing the sky."""

    def __init__(self, width, height, color_format):
        self.color_data = np.zeros([width, height, 4], dtype=np.uint8)
        for i in range(width):
            for j in range(height):
                self.color_data[j][i] = [0, 0, 200, 255]
        super(SkyLayer, self).__init__(
            self.color_data, width, height, color_format)
