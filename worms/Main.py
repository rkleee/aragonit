"""Controller module."""
import sys

import PyQt5.QtGui as gui
import PyQt5.QtWidgets as widget

import Layers


def drawMap(width, height):
    color_format = gui.QImage.Format_RGBA8888
    sky_layer = Layers.SkyLayer(width, height, color_format)
    land_layer = Layers.LandLayer(width, height, color_format)
    painter = gui.QPainter(sky_layer)
    painter.drawImage(0, 0, land_layer)
    painter.end()
    return sky_layer


if __name__ == "__main__":
    app = widget.QApplication(sys.argv)
    width = 500
    height = 500
    world = drawMap(width, height)
    display = widget.QLabel()
    display.setPixmap(gui.QPixmap.fromImage(world))
    display.show()
    sys.exit(app.exec_())
