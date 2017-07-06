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
        self.actual_tank = 0
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
            if 0 <= self.actual_tank < len(self.tanks)-1:
                self.actual_tank += 1
            else:
                self.actual_tank -= 1

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
        if 0 <= tank_id <= len(self.tanks):
            x_value = self.tanks[tank_id][1].x_position + direction
            y_value = self.tanks[tank_id][1].y_position
            new_x_value, new_y_value = self._adjustHeight(x_value, y_value)
            self.tanks[tank_id][1].x_position = new_x_value
            self.tanks[tank_id][1].y_position = new_y_value

    def moveTank(self, tank_id, direction):
        """Move the tank into the given direction."""
        old_x_position = self.tanks[tank_id][1].x_position
        old_y_position = self.tanks[tank_id][1].y_position
        new_x_position = old_x_position + direction
        if 0 <= new_x_position <= self.width:
            self.getNewCoordinates(tank_id, direction)
            # erase the old tank from its layer
            painter = gui.QPainter(self.tanks[tank_id][0])
            painter.setCompositionMode(gui.QPainter.CompositionMode_Clear)
            painter.setBrush(core.Qt.black)
            painter.drawRect(
                old_x_position, old_y_position,
                self.tanks[tank_id][1].width, self.tanks[tank_id][1].height,
            )
        else:
            return
        # draw the new tank
        painter.setCompositionMode(
            gui.QPainter.CompositionMode_SourceOver)
        painter.drawImage(self.tanks[tank_id][1].x_position,
                          self.tanks[tank_id][1].y_position, self.tanks[tank_id][1])
        painter.end()
        self._updateMapImage()

    def _updateMapImage(self):
        painter = gui.QPainter(self.background_layer)
        painter.drawImage(0, 0, self.landscape_layer)
        for i in range(len(self.tanks)):
            painter.drawImage(0, 0, self.tanks[i][0])
        painter.end()
        self.setPixmap(gui.QPixmap.fromImage(self.background_layer))

    def _createMapImage(self, width, height):
        """Create a QImage containing all the different layers of the map."""
        # create background and landscape layer
        self.background_layer = Layers.BackgroundLayer(width, height)
        self.landscape_layer = Layers.LandscapeLayer(width, height)

        self.tanks = []
        # create first tank on its own layer
        tank_one_layer = Layers.ObjectLayer(width, height)
        tank_one = Objects.Tank(150, 0, 0, core.Qt.red)
        self.tanks.append((tank_one_layer, tank_one))
        self.getNewCoordinates(self.tanks[0][1].tank_id, 0)
        tmp_painter = gui.QPainter(self.tanks[0][0])
        tmp_painter.drawImage(self.tanks[0][1].x_position,
                              self.tanks[0][1].y_position, self.tanks[0][1])
        tmp_painter.end()
        # create second tank on its own layer
        tank_two_layer = Layers.ObjectLayer(width, height)
        tank_two = Objects.Tank((self.width - 150), 0, 1, core.Qt.black)
        self.tanks.append((tank_two_layer, tank_two))
        self.getNewCoordinates(self.tanks[1][1].tank_id, 0)
        tmp_painter = gui.QPainter(self.tanks[1][0])
        tmp_painter.drawImage(self.tanks[1][1].x_position,
                              self.tanks[1][1].y_position, self.tanks[1][1])
        tmp_painter.end()
        # draw all layers on top of each other
        painter = gui.QPainter(self.background_layer)
        painter.drawImage(0, 0, self.landscape_layer)
        for i in range(len(self.tanks)):
            painter.drawImage(0, 0, self.tanks[i][0])
        painter.end()


if __name__ == "__main__":
    app = widget.QApplication(sys.argv)
    width = 2000
    height = 1000
    display = GameLabel(width, height)
    sys.exit(app.exec_())
