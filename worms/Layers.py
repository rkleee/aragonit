"""Module handling the different layers of the map."""
from math import pi, sin, sqrt
from random import uniform

import numpy as np
import PyQt5.QtCore as core
import PyQt5.QtGui as gui

import Settings


class LandscapeLayer(gui.QImage):
    """Layer containing the landscape of the map."""

    def __init__(self, width, height):
        """Initialize the landscape."""
        # set constant factors for the landscape creation function
        self.landscape_compression_factor = uniform(-1.0, 1.0)
        self.landscape_offset = uniform(0.0, 2.0 * pi)
        self.landscape_parameters = np.linspace(0.001, 0.05, 200)
        # create and draw the landscape accordingly
        color_data = self._createLandscapeData(width, height)
        super().__init__(color_data, width, height, Settings.color_format)

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

    def _createLandscapeData(self, width, height):
        """Create a matrix containing the landscape's color data."""
        landscape_color_data = np.zeros([height, width, 4], dtype=np.uint8)
        land_color = [139, 69, 19, 255]  # brown
        vertical_middle = len(landscape_color_data) / 2
        for x in range(len(landscape_color_data[0])):
            border = self._getLandscapeHeight(x) + vertical_middle
            for y in range(len(landscape_color_data)):
                if y >= border:
                    landscape_color_data[y, x, :] = land_color
        return landscape_color_data

    def drawCrater(self, x_value, y_value, diameter):
        """Draw a crater on the given position with the given diameter."""
        painter = gui.QPainter(self)
        painter.setCompositionMode(gui.QPainter.CompositionMode_Clear)
        painter.setBrush(gui.QColor(0, 0, 0, 0))
        painter.drawEllipse(core.QPoint(
            x_value, y_value), diameter, diameter)
        painter.end()


class BackgroundLayer(gui.QImage):
    """Layer containing the background of the map."""

    def __init__(self, width, height):
        """Initialize the background."""
        super().__init__(width, height, Settings.color_format)
        # use a simple blue sky as background
        self.fill(core.Qt.blue)


class ObjectLayer(gui.QImage):
    """Layer containing the objects of the game."""

    def __init__(self, width, height):
        """Initialize the layer fully transparent."""
        super().__init__(width, height, Settings.color_format)
        self.fill(gui.QColor(0, 0, 0, 0))
