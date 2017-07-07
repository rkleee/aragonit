"""The game's main application."""
import sys
import random

import PyQt5.QtCore as core
import PyQt5.QtGui as gui
import PyQt5.QtWidgets as widget

import Layers
import Objects
import Settings


class GameImage(widget.QLabel):
    """The game's main application."""

    def __init__(self, width, height):
        """Initialize the landscape and the tanks."""
        super().__init__()
        self.width = width
        self.height = height
        # specify which tank is on the move
        self.actual_tank = 0

        self._createMapImage(width, height)

    def iteration(self, tank_id, left):
        # TO DO: remove old points

        # start velocity
        v_x0 = random.uniform(10, 100)
        v_y0 = random.uniform(20, 100)
        # start at tank position
        x_base = self.tanks[tank_id][1].x_position
        y_base = self.tanks[tank_id][1].y_position

        x = x_base
        y = y_base - 1
        (x_check, y_check) = self._adjustHeight(x, y)

        i = 1

        # shooting left -> x decreases
        # otherwise x increases
        if left:
            v_x0 *= -1

        # calculate iteration and check if at top of landscape
        while y <= y_check:
            # self._updateMapImage()
            painter = gui.QPainter(self.image)
            painter.setBrush(core.Qt.black)
            x = v_x0 * i + x_base
            y = -v_y0 * i + (9.81 / 2) * i * i + y_base
            (x_check, y_check) = self._adjustHeight(x, y)
            painter.drawEllipse(x, y, 10, 10)
            painter.end()
            self.setPixmap(gui.QPixmap.fromImage(self.image))
            i = i + 1

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
            if 0 <= self.actual_tank < len(self.tanks) - 1:
                self.actual_tank += 1
            else:
                self.actual_tank -= 1
        elif event.key() == core.Qt.Key_S:
            self.iteration(self.actual_tank, True)

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
        if 0 <= tank_id < len(self.tanks):
            x_value = self.tanks[tank_id][1].x_position + direction
            y_value = self.tanks[tank_id][1].y_position
            new_x_value, new_y_value = self._adjustHeight(x_value, y_value)
            self.tanks[tank_id][1].updatePosition(new_x_value, new_y_value)

    def moveTank(self, tank_id, direction):
        """Move the tank into the given direction."""
        old_x_position = self.tanks[tank_id][1].x_position
        old_y_position = self.tanks[tank_id][1].y_position
        new_x_position = old_x_position + direction
        if 0 <= new_x_position < self.width:
            self.getNewCoordinates(tank_id, direction)
            # erase the old tank from its layer
            painter = gui.QPainter(self.tanks[tank_id][0])
            painter.setCompositionMode(gui.QPainter.CompositionMode_Clear)
            painter.setBrush(gui.QColor(0, 0, 0, 0))
            painter.drawRect(
                old_x_position, old_y_position,
                self.tanks[tank_id][1].width, self.tanks[tank_id][1].height,
            )
            painter.end()
        else:
            return
        # draw the new tank
        painter = gui.QPainter(self.tanks[tank_id][0])
        painter.drawImage(self.tanks[tank_id][1].x_position,
                          self.tanks[tank_id][1].y_position,
                          self.tanks[tank_id][1])
        painter.end()
        self._updateMapImage()

    def _updateMapImage(self):
        self.image = gui.QImage(self.width, self.height, Settings.color_format)
        painter = gui.QPainter(self.image)
        painter.drawImage(0, 0, self.background_layer)
        painter.drawImage(0, 0, self.landscape_layer)
        for i in range(len(self.tanks)):
            painter.drawImage(0, 0, self.tanks[i][0])
        painter.end()
        self.setPixmap(gui.QPixmap.fromImage(self.image))

    def _drawLayers(self):
        """Return a QImage containing all layers."""
        self.image = gui.QImage(self.width, self.height, Settings.color_format)
        painter = gui.QPainter(self.image)
        painter.drawImage(0, 0, self.background_layer)
        painter.drawImage(0, 0, self.landscape_layer)
        for i in range(len(self.tanks)):
            painter.drawImage(0, 0, self.tanks[i][0])
        painter.end()

    def _createMapImage(self, width, height):
        """Create a QImage containing all the different layers of the map."""
        # create background and landscape layer
        self.background_layer = Layers.BackgroundLayer(width, height)
        self.landscape_layer = Layers.LandscapeLayer(width, height)

        self.tanks = []

        # create first tank on its own layer
        tank_one_layer = Layers.ObjectLayer(width, height)
        tank_one = Objects.Tank(200, (height // 2), 0, core.Qt.yellow, core.Qt.cyan)
        self.tanks.append((tank_one_layer, tank_one))
        self.getNewCoordinates(self.tanks[0][1].tank_id, 0)
        tmp_painter = gui.QPainter(self.tanks[0][0])
        tmp_painter.drawImage(self.tanks[0][1].x_position,
                              self.tanks[0][1].y_position, self.tanks[0][1])
        tmp_painter.end()

        # create second tank on its own layer
        tank_two_layer = Layers.ObjectLayer(width, height)
        tank_two = Objects.Tank((self.width - 200), (height // 2),
                                1, core.Qt.green, core.Qt.red)
        self.tanks.append((tank_two_layer, tank_two))
        self.getNewCoordinates(self.tanks[1][1].tank_id, 0)
        tmp_painter = gui.QPainter(self.tanks[1][0])
        tmp_painter.drawImage(self.tanks[1][1].x_position,
                              self.tanks[1][1].y_position, self.tanks[1][1])
        tmp_painter.end()

        # draw all layers
        self._drawLayers()
        self.setPixmap(gui.QPixmap.fromImage(self.image))


if __name__ == "__main__":
    app = widget.QApplication(sys.argv)
    width = 2000
    height = 1000
    display = GameImage(width, height)
    display.setWindowTitle('Worms')
    display.setScaledContents(True)
    display.show()
    sys.exit(app.exec_())
