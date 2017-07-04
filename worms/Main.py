"""Controller module."""
import sys

import PyQt5.QtGui as gui
import PyQt5.QtWidgets as widget

import Layers


def createMapImage(width, height):
    """Create a QImage containing all the different layers of the map."""
    color_format = gui.QImage.Format_RGBA8888
    background_layer = Layers.BackgroundLayer(width, height, color_format)
    landscape_layer = Layers.LandscapeLayer(width, height, color_format)
    painter = gui.QPainter(background_layer)
    painter.drawImage(0, 0, landscape_layer)
    painter.end()
    return background_layer


if __name__ == "__main__":
    app = widget.QApplication(sys.argv)
    width = 2000
    height = 1000
    map_image = createMapImage(width, height)
    display = widget.QLabel()
    display.setPixmap(gui.QPixmap.fromImage(map_image))
    display.setScaledContents(True)
    display.show()
    sys.exit(app.exec_())
