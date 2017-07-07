"""Module to handle different objects (vehicles, etc.)."""

import PyQt5.QtCore as core
import PyQt5.QtGui as gui

import Settings


class Tank(gui.QImage):
    """Image representing a tank."""

    def _createPainter(self, color):
        painter = gui.QPainter(self)
        painter.setPen(gui.QPen(color, 5))
        painter.setBrush(color)
        return painter

    def __init__(self, x_position, y_position, tank_id, tank_color, cannon_color):
        """Initialize the tank."""
        self.width = 100
        self.height = 100

        self.updatePosition(x_position, y_position)

        self.tank_id = tank_id
        self.tank_color = tank_color
        self.cannon_color = cannon_color

        self.cannon_length = self.height // 2
        self.cannon_angle = 90
        self.cannon_start = core.QPoint((self.height // 2), (self.width // 2))
        self.cannon_end = core.QPoint((self.width // 2), 0)
        # create a fully transparent image
        super().__init__(self.width, self.height, Settings.color_format)
        self.fill(gui.QColor(0, 0, 0, 0))
        # initialize a painter and paint the tank
        painter = self._createPainter(self.tank_color)
        painter.drawRect(0, (self.height // 2), self.width, (self.height // 2))
        painter.end()
        painter = self._createPainter(self.cannon_color)
        painter.drawLine(self.cannon_start, self.cannon_end)
        painter.end()

    def updatePosition(self, new_x_position, new_y_position):
        """Update the scaled position."""
        self.x_position = new_x_position
        self.y_position = new_y_position - self.height

    def moveCannonRight(self):
        """Move cannon to the right and repaint the tank."""
        painter = self._createPainter(self)
        painter.end()

    def moveCannonLeft(self):
        """Move cannon to the left and repaint the tank."""
        painter = self._createPainter(self)
        painter.end()