"""Module handling the different layers of the map."""
from math import pi, sin, sqrt
from random import uniform

import numpy as np
import PyQt5.QtCore as core
import PyQt5.QtGui as gui

import Settings


class BaseLayer(gui.QImage):
    """Abstract class representing a layer of the map."""

    def __init__(self, color_data=None):
        """Call corresponding QImage constructor."""
        if color_data is None:
            super().__init__(
                Settings.WIDTH,
                Settings.HEIGHT,
                Settings.COLOR_FORMAT
            )
        elif len(color_data) == Settings.HEIGHT \
                and len(color_data[0]) == Settings.WIDTH \
                and len(color_data[0, 0] == 4):
            super().__init__(
                color_data,
                Settings.WIDTH,
                Settings.HEIGHT,
                Settings.COLOR_FORMAT
            )
        else:
            raise ValueError(
                "The shape of the color data matrix does not fit.")


class LandscapeLayer(BaseLayer):
    """Layer containing the landscape of the map."""

    def __init__(self):
        """Initialize the landscape."""
        # set constant factors for the landscape creation function
        self.landscape_compression_factor = uniform(-1.0, 1.0)
        self.landscape_offset = uniform(0.0, 2.0 * pi)
        self.landscape_parameters = np.linspace(0.001, 0.05, 200)
        # create and draw the landscape accordingly
        color_data = self.createLandscapeData()
        super().__init__(color_data)

    def getLandscapeHeight(self, x_value):
        """
        Return the height of the land to a given x value.

        Uses the sum of different randomly shifted and stretched
        or compressed sinus functions to compute the landscape.
        """
        y_coordinate = 0
        for param in self.landscape_parameters:
            weight_factor = 1 / sqrt(param)
            intermediate_result = weight_factor * \
                sin(param * x_value + self.landscape_offset) * \
                self.landscape_compression_factor
            y_coordinate += intermediate_result
        return y_coordinate

    def createLandscapeData(self):
        """Create a matrix containing the landscape's color data."""
        landscape_color_data = np.zeros(
            [Settings.HEIGHT, Settings.WIDTH, 4], dtype=np.uint8
        )
        land_color = [139, 69, 19, 255]  # brown
        vertical_middle = len(landscape_color_data) / 2
        for x in range(len(landscape_color_data[0])):
            border = self.getLandscapeHeight(x) + vertical_middle
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


class BackgroundLayer(BaseLayer):
    """Layer containing the background of the map."""

    def __init__(self):
        """Initialize the background."""
        super().__init__()
        # use a simple blue sky as background
        self.fill(core.Qt.blue)


class ObjectLayer(BaseLayer):
    """Layer containing the objects of the game."""

    def __init__(self):
        """Initialize the layer fully transparent."""
        super().__init__()
        self.fill(gui.QColor(0, 0, 0, 0))
