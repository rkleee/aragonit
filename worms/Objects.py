"""Module handling the different objects (vehicles, etc.) of the game."""

import PyQt5.QtCore as core
import PyQt5.QtGui as gui


class Tank(gui.QImage):
    """Image representing a tank."""

    def __init__(self, color_format):
        """Initialize the tank."""
        width = 50
        height = 50
        super().__init__(width, height, color_format)
        self.fill(gui.QColor(0, 0, 0, 0))
        painter = gui.QPainter(self)
        painter.setPen(gui.QPen(core.Qt.black, 5))
        painter.setBrush(core.Qt.black)
        painter.drawRect(0, 20, 50, 30)
        painter.drawLine(core.QPoint(25, 19), core.QPoint(50, 0))
        painter.end()
