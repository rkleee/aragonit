"""Controller module."""
import sys

import PyQt5.QtGui as gui
import PyQt5.QtWidgets as widget

import Layers

if __name__ == "__main__":
    app = widget.QApplication(sys.argv)
    width = 500
    height = 500
    world_layer = Layers.MapLayer(width, height)
    display = widget.QLabel()
    display.setPixmap(gui.QPixmap.fromImage(world_layer))
    display.show()
    sys.exit(app.exec_())
