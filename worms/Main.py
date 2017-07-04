"""The game's start script."""
import sys

import PyQt5.QtGui as gui
import PyQt5.QtWidgets as widget

import Layers
import Objects


def getLandscapeCoordinate(layer, x_value, height):
    y_value = 0
    for y_value in range(height):
        alpha = layer.pixelColor(x_value, y_value).alpha()
        if alpha != 0:
            return y_value
    return y_value


def createMapImage(width, height):
    """Create a QImage containing all the different layers of the map."""
    color_format = gui.QImage.Format_RGBA8888
    background_layer = Layers.BackgroundLayer(width, height, color_format)
    landscape_layer = Layers.LandscapeLayer(width, height, color_format)
    tank_one = Objects.Tank(color_format)
    painter = gui.QPainter(background_layer)
    painter.drawImage(0, 0, landscape_layer)
    x = 150
    y = getLandscapeCoordinate(landscape_layer, x, height)
    print(y)
    painter.drawImage(x, y, tank_one)
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
