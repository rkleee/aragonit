"""Module to handle different objects (vehicles, etc.)."""

from math import cos, radians, sin

import PyQt5.QtCore as core
import PyQt5.QtGui as gui

import Settings


class BaseObject(gui.QImage):
    """Abstract class representing an object in the game."""

    def __init__(self, x_position, y_position, width, height):
        """Call corresponding QImage constructor."""
        self.x_position = x_position
        self.y_position = y_position
        self.width = width
        self.height = height
        super().__init__(width, height, Settings.COLOR_FORMAT)


class Tank(BaseObject):
    """Image representing a tank."""

    def __init__(self, tank_id, x_position, y_position, width, height, tank_color, cannon_color):
        """Initialize the tank."""
        super().__init__(x_position, y_position, width, height)
        # make the image fully transparent
        self.fill(gui.QColor(0, 0, 0, 0))
        # set necessary color attributes
        self.tank_id = tank_id
        self.tank_color = tank_color
        self.cannon_color = cannon_color
        self.cannon_width = 1
        # define the position of the cannon
        self.cannon_start = core.QPoint(
            (self.height // 2) - self.cannon_width, (self.width // 2))
        self.cannon_length = self.height // 2
        self.cannon_angle = 45
        self.getCannonEnd()
        # initialize a painter and paint the tank
        painter = self.createDrawPainter(self.tank_color)
        painter.drawRect(0, (self.height // 2), self.width, (self.height // 2))
        painter.end()
        painter = self.createDrawPainter(self.cannon_color)
        painter.drawLine(self.cannon_start, self.cannon_end)
        painter.end()

    def getCannonEnd(self):
        """Compute the cannon's end point."""
        # trigonometry
        tmp_x = cos(radians(self.cannon_angle + 180)) * self.cannon_length
        tmp_y = sin(radians(self.cannon_angle + 180)) * self.cannon_length
        # compute real pixel coordinates depending on the cannon's start point
        x_value = int(tmp_x + self.cannon_start.x())
        y_value = int(tmp_y + self.cannon_start.y())
        self.cannon_end = core.QPoint(x_value, y_value)

    def moveCannon(self, change_of_angle):
        """Change the angle of the cannon according to the given parameter."""
        tmp_angle = self.cannon_angle + change_of_angle
        if 0 < tmp_angle < 180:
            # erase the old cannon
            painter = self.createErasePainter()
            painter.drawLine(self.cannon_start, self.cannon_end)
            painter.end()
            # compute the new cannon's position
            self.cannon_angle = tmp_angle
            self.getCannonEnd()
            # draw the new cannon
            painter = self.createDrawPainter(self.cannon_color)
            painter.drawLine(self.cannon_start, self.cannon_end)
            painter.end()

    def createDrawPainter(self, color):
        """Create painter to (re-)draw parts of the tank."""
        painter = gui.QPainter(self)
        painter.setPen(gui.QPen(color, self.cannon_width))
        painter.setBrush(color)
        return painter

    def createErasePainter(self):
        """Create painter to erase parts of the tank."""
        painter = gui.QPainter(self)
        painter.setCompositionMode(gui.QPainter.CompositionMode_Clear)
        painter.setPen(gui.QPen(gui.QColor(0, 0, 0, 0), self.cannon_width))
        painter.setBrush(gui.QColor(0, 0, 0, 0))
        return painter
