"""Module handling the different layers of the map."""
import PyQt5.QtCore as core
import PyQt5.QtGui as gui


class MapLayer(gui.QImage):
    """QImage as base layer containing the landscape of the map."""

    def __init__(self, width, height, color_format):
        """Initialize the landscape."""
        super(MapLayer, self).__init__(width, height, color_format)
        self.fill(core.Qt.white)
        painter = gui.QPainter(self)
        painter.setPen(gui.QPen(core.Qt.blue, 2))
        painter.drawLine(50, 50, 50, 100)
