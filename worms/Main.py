"""Controller module."""
import sys

import PyQt5.QtGui as gui
import PyQt5.QtWidgets as widget

import Layers

if __name__ == "__main__":
    app = widget.QApplication(sys.argv)
    display = widget.QLabel()
    world = Layers.MapLayer(300, 600, gui.QImage.Format_RGB32)
    display.setPixmap(gui.QPixmap.fromImage(world))
    display.show()
    sys.exit(app.exec_())
