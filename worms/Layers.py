"""Module handling the different layers of the map."""
from math import pi, sin, sqrt
from random import uniform

import numpy as np
import PyQt5.QtCore as core
import PyQt5.QtGui as gui


class LandscapeLayer(gui.QImage):
    """Layer containing the land mass of the map."""

    def _computeLandscapeParameters(self):
        """Set constant factors for landscape creation function."""
        self.landscape_compression_factor = uniform(-1.0, 1.0)
        self.landscape_offset = uniform(0.0, 2.0 * pi)
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
        """Create a random landscape."""
        vertical_middle = len(self.color_data) / 2
        for x in range(len(self.color_data[0])):
            border = self._getLandscapeHeight(x) + vertical_middle
            for y in range(len(self.color_data)):
                if y >= border:
                    self.color_data[y, x, :] = self.land_color

    def __init__(self, width, height, color_format):
        """Initialize the landscape."""
        # set the color for the land
        self.land_color = [139, 69, 19, 255]
        # create a 3 dimensional matrix representing the image's color data
        self.color_data = np.zeros([height, width, 4], dtype=np.uint8)
        # initialize the landscape
        self._computeLandscapeParameters()
        self._createLandscape()
        super().__init__(self.color_data, width, height, color_format)
        # painter = gui.QPainter(self)
        # painter.setPen(gui.QPen(core.Qt.blue, 2))
        # painter.drawLine(50, 50, 50, 100)


class BackgroundLayer(gui.QImage):
    """Layer containing the background of the map."""

    def __init__(self, width, height, color_format):
        """Initialize the background."""
        super().__init__(width, height, color_format)
        # use a simple blue sky as background
        self.fill(core.Qt.blue)
