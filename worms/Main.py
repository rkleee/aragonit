"""The game's main application."""
import sys

import PyQt5.QtCore as core
import PyQt5.QtGui as gui
import PyQt5.QtWidgets as widget

import Layers
import Objects


class GameLabel(widget.QLabel):
    """The game's main application."""

    def __init__(self, width, height):
        """Initialize the landscape and the tanks."""
        super().__init__()
        self.width = width
        self.height = height
        self.setWindowTitle('Worms')
        # specify which tank is on the move
        self.actual_tank = 1
        self._createMapImage(width, height)
        self.setPixmap(gui.QPixmap.fromImage(self.background_layer))
        self.setScaledContents(True)
        self.show()

    def keyPressEvent(self, event):
        """Move the tank and its cannon."""
        if event.key() == core.Qt.Key_Left:
            self.moveTank(self.actual_tank, -10)
        elif event.key() == core.Qt.Key_Up:
            pass
        elif event.key() == core.Qt.Key_Right:
            self.moveTank(self.actual_tank, 10)
        elif event.key() == core.Qt.Key_Down:
            pass
        elif event.key() == core.Qt.Key_C:
            if self.actual_tank == 1:
                self.actual_tank = 2
            else:
                self.actual_tank = 1

    def _adjustHeight(self, x_value, y_value):
        """
        Vertically move the given point to a valid position.

        The point should be directly on top of the landscape.
        """
        alpha = self.landscape_layer.pixelColor(
            x_value, y_value).alpha()
        if alpha != 0:
            # new position is invalid because it lies within the
            # landscape, so continue searching upwards.
            y_value -= 1
            while y_value > 0:
                alpha = self.landscape_layer.pixelColor(
                    x_value, y_value).alpha()
                if alpha == 0:
                    break
                y_value -= 1
        else:
            # new position may be invalid because it lies above the
            # landscape, so continue searching downwards
            y_value += 1
            while y_value < self.height:
                alpha = self.landscape_layer.pixelColor(
                    x_value, y_value).alpha()
                if alpha != 0:
                    break
                y_value += 1
        return x_value, y_value

    def getNewCoordinates(self, tank_id, direction):
        """Compute new coordinates of the tank."""
        if tank_id == 1:
            x_value = self.tank_one.x_position + direction
            y_value = self.tank_one.y_position
            new_x_value, new_y_value = self._adjustHeight(x_value, y_value)
            self.tank_one.x_position = new_x_value
            self.tank_one.y_position = new_y_value
        elif tank_id == 2:
            x_value = self.tank_two.x_position + direction
            y_value = self.tank_two.y_position
            new_x_value, new_y_value = self._adjustHeight(x_value, y_value)
            self.tank_two.x_position = new_x_value
            self.tank_two.y_position = new_y_value

    def moveTank(self, tank_id, direction):
        """Move the tank into the given direction."""
        # TODO: Restructure this function to support more than
        # two tanks without duplicating the code.
        if tank_id == 1:
            old_x_position = self.tank_one.x_position
            old_y_position = self.tank_one.y_position
            new_x_position = old_x_position + direction
            if new_x_position >= 0 and new_x_position <= self.width:
                self.getNewCoordinates(tank_id, direction)
                # erase the old tank from its layer
                painter = gui.QPainter(self.tank_one_layer)
                painter.setCompositionMode(gui.QPainter.CompositionMode_Clear)
                painter.setBrush(core.Qt.black)
                painter.drawRect(
                    old_x_position, old_y_position,
                    self.tank_one.width, self.tank_one.height,
                )
                # draw the new tank
                painter.setCompositionMode(
                    gui.QPainter.CompositionMode_SourceOver)
                painter.drawImage(self.tank_one.x_position,
                                  self.tank_one.y_position, self.tank_one)
                painter.end()
                self._updateMapImage()
        elif tank_id == 2:
            old_x_position = self.tank_two.x_position
            old_y_position = self.tank_two.y_position
            new_x_position = old_x_position + direction
            if new_x_position >= 0 and new_x_position <= self.width:
                self.getNewCoordinates(tank_id, direction)
                # erase the old tank from its layer
                painter = gui.QPainter(self.tank_two_layer)
                painter.setCompositionMode(gui.QPainter.CompositionMode_Clear)
                painter.setBrush(core.Qt.black)
                painter.drawRect(
                    old_x_position, old_y_position,
                    self.tank_two.width, self.tank_two.height,
                )
                # draw the new tank
                painter.setCompositionMode(
                    gui.QPainter.CompositionMode_SourceOver)
                painter.drawImage(self.tank_two.x_position,
                                  self.tank_two.y_position, self.tank_two)
                painter.end()
                self._updateMapImage()

    def _updateMapImage(self):
        painter = gui.QPainter(self.background_layer)
        painter.drawImage(0, 0, self.landscape_layer)
        painter.drawImage(0, 0, self.tank_one_layer)
        painter.drawImage(0, 0, self.tank_two_layer)
        painter.end()
        self.setPixmap(gui.QPixmap.fromImage(self.background_layer))

    def _createMapImage(self, width, height):
        """Create a QImage containing all the different layers of the map."""
        # create background and landscape layer
        self.background_layer = Layers.BackgroundLayer(width, height)
        self.landscape_layer = Layers.LandscapeLayer(width, height)
        # create first tank on its own layer
        self.tank_one_layer = Layers.ObjectLayer(width, height)
        self.tank_one = Objects.Tank(150, 0, 1, core.Qt.red)
        self.getNewCoordinates(self.tank_one.tank_id, 0)
        tmp_painter = gui.QPainter(self.tank_one_layer)
        tmp_painter.drawImage(self.tank_one.x_position,
                              self.tank_one.y_position, self.tank_one)
        tmp_painter.end()
        # create second tank on its own layer
        self.tank_two_layer = Layers.ObjectLayer(width, height)
        self.tank_two = Objects.Tank((self.width - 150), 0, 2, core.Qt.black)
        self.getNewCoordinates(self.tank_two.tank_id, 0)
        tmp_painter = gui.QPainter(self.tank_two_layer)
        tmp_painter.drawImage(self.tank_two.x_position,
                              self.tank_two.y_position, self.tank_two)
        tmp_painter.end()
        # draw all layers on top of each other
        painter = gui.QPainter(self.background_layer)
        painter.drawImage(0, 0, self.landscape_layer)
        painter.drawImage(0, 0, self.tank_one_layer)
        painter.drawImage(0, 0, self.tank_two_layer)
        painter.end()


if __name__ == "__main__":
    app = widget.QApplication(sys.argv)
    width = 2000
    height = 1000
    display = GameLabel(width, height)
    sys.exit(app.exec_())
