"""The game's main application."""
import random
import sys
from math import cos, sin, sqrt

import PyQt5.QtCore as core
import PyQt5.QtGui as gui
import PyQt5.QtWidgets as widget

import Layers
import Objects
import Settings


class GameLabel(widget.QLabel):
    """The game's main application."""

    def __init__(self):
        """Initialize the game."""
        super().__init__()
        self.width = Settings.WIDTH
        self.height = Settings.HEIGHT

        self.world_image = gui.QImage(
            self.width, self.height, Settings.COLOR_FORMAT)
        self.object_image = gui.QImage(
            self.width, self.height, Settings.COLOR_FORMAT)
        self.game_image = gui.QImage(
            self.width, self.height, Settings.COLOR_FORMAT)

        # list of tanks currently on the map
        self.tanks = []
        # list of other objects currently on the map
        self.objects = []

        self.cannon_ellipses = []

        # timer for drawing path of bullet
        self.timer = core.QTimer()
        self.timer.setInterval(80)
        self.timer.timeout.connect(self.drawBulletPath)

        # specify which tank is on the move
        self.actual_tank_id = 0

        self.createMapImage()

    def iteration(self, tank_id):
        # TO DO:
        # -draw each point and after that remove all points
        # -and draw crater
        # -use correct angle for starting velocity

        # start velocity
        v = random.uniform(10, 100)
        angle = self.tanks[tank_id].cannon_angle

        # use angle to calculate start position
        # not working correctly
        v_x0 = v * cos(angle)
        v_y0 = v * sin(angle)

        # start at tank position
        (x_base, y_base) = self.tanks[tank_id].getAbsoluteCannonEnd()
        x = x_base
        y = y_base - 1
        (x_check, y_check) = self.adjustHeight(x, y)

        i = 1

        # calculate iteration and check if at top of landscape
        while y <= y_check:
            x = v_x0 * i + x_base
            y = -v_y0 * i + (9.81 / 2) * i * i + y_base
            (x_check, y_check) = self.adjustHeight(x, y)
            self.cannon_ellipses.append(core.QRectF(x, y, 15, 15))
            i = i + 1
        self.vel = sqrt(v_x0**2 + (-v_y0 + 9.81 * i)**2)

        self.drawIndex = 0
        self.crater_x = x
        self.crater_y = y
        self.timer.start()

    def keyPressEvent(self, event):
        """Move the tank and its cannon."""
        if event.key() == core.Qt.Key_Left:
            self.moveTank(self.actual_tank_id, -10)
        elif event.key() == core.Qt.Key_Up:
            self.moveCannon(self.actual_tank_id, -10)
        elif event.key() == core.Qt.Key_Right:
            self.moveTank(self.actual_tank_id, 10)
        elif event.key() == core.Qt.Key_Down:
            self.moveCannon(self.actual_tank_id, 10)
        elif event.key() == core.Qt.Key_C:
            if self.actual_tank_id == len(self.tanks) - 1:
                self.actual_tank_id = 0
            else:
                self.actual_tank_id += 1
        elif event.key() == core.Qt.Key_S:
            self.iteration(self.actual_tank_id)

    def adjustHeight(self, x_value, y_value):
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

    def getNewCoordinates(self, tank_id, change_of_x_value):
        """Compute new coordinates of the tank."""
        if 0 <= tank_id < len(self.tanks):
            x_value = self.tanks[tank_id].x_position + change_of_x_value
            y_value = self.tanks[tank_id].y_position
            new_x_value, new_y_value = self.adjustHeight(x_value, y_value)
            # scale the y coordinate so that the tank stands on top
            # of the landscape and not slightly underneath
            scaled_y_value = new_y_value - self.tanks[tank_id].height
            self.tanks[tank_id].x_position = new_x_value
            self.tanks[tank_id].y_position = scaled_y_value

    def moveTank(self, tank_id, change_of_x_value):
        """Move the tank into the given direction."""
        old_x_position = self.tanks[tank_id].x_position
        old_y_position = self.tanks[tank_id].y_position
        new_x_position = old_x_position + change_of_x_value
        if 0 <= new_x_position < self.width:
            self.getNewCoordinates(tank_id, change_of_x_value)
            # erase the old tank from its layer
            painter = gui.QPainter(self.object_layer)
            painter.setCompositionMode(gui.QPainter.CompositionMode_Clear)
            painter.setBrush(gui.QColor(0, 0, 0, 0))
            painter.drawRect(
                old_x_position, old_y_position,
                self.tanks[tank_id].width, self.tanks[tank_id].height,
            )
            painter.end()
            # draw the new tank
            painter = gui.QPainter(self.object_layer)
            painter.drawImage(
                self.tanks[tank_id].x_position, self.tanks[tank_id].y_position, self.tanks[tank_id])
            painter.end()
            self.updateMap(False)

    def moveCannon(self, tank_id, change_of_angle):
        """Move the cannon and draw its new position."""
        self.tanks[tank_id].moveCannon(change_of_angle)
        self.updateMap(False)

    def drawBulletPath(self):
        if self.cannon_ellipses and self.drawIndex < len(self.cannon_ellipses):
            self.updateMap(False)
            painter = gui.QPainter(self.object_image)
            painter.setBrush(core.Qt.black)
            painter.drawEllipse(self.cannon_ellipses[self.drawIndex])
            painter.end()
            self.updateMap(False, False)
            self.drawIndex += 1
        else:
            self.timer.stop()
            self.cannon_ellipses = []
            # create crater at end position
            self.landscape_layer.drawCrater(
                self.crater_x, self.crater_y, 0.6 * self.vel)
            self.updateMap(True)

    def updateMap(self, background_changed, objects_changed=True):
        """Draw the actual map with all objects."""
        # erase the old image
        self.game_image.fill(gui.QColor(0, 0, 0, 0))
        # paint the new image
        if background_changed:
            self.drawMap()
        if objects_changed:
            self.drawObjects()
        self.drawGame()
        self.setPixmap(gui.QPixmap.fromImage(self.game_image))

    def drawMap(self):
        """Draw background and landscape."""
        # erase the old image
        self.world_image.fill(gui.QColor(0, 0, 0, 0))
        # paint the new image
        painter = gui.QPainter(self.world_image)
        painter.drawImage(0, 0, self.background_layer)
        painter.drawImage(0, 0, self.landscape_layer)
        painter.end()

    def drawObjects(self):
        """Draw tanks and other objects."""
        # erase all objects
        self.object_image.fill(gui.QColor(0, 0, 0, 0))
        # draw new objects
        painter = gui.QPainter(self.object_image)
        # tanks
        for tank in self.tanks:
            painter.drawImage(tank.x_position, tank.y_position, tank)
        # other objects
        for item in self.objects:
            painter.drawImage(item.x_position, item.y_position, item)

    def drawGame(self):
        """Draw the whole game image."""
        # erase the old image
        self.game_image.fill(gui.QColor(0, 0, 0, 0))
        # paint the new image
        painter = gui.QPainter(self.game_image)
        painter.drawImage(0, 0, self.world_image)
        painter.drawImage(0, 0, self.object_image)
        painter.end()

    def createMapImage(self):
        """Create a QImage containing all the different layers of the map."""
        # create background, landscape and object layer
        self.background_layer = Layers.BackgroundLayer()
        self.landscape_layer = Layers.LandscapeLayer()
        self.object_layer = Layers.ObjectLayer()

        # create first tank
        tank_one = Objects.Tank(0, 200, (self.height // 2),
                                100, 100, core.Qt.yellow, core.Qt.cyan)
        self.tanks.append(tank_one)
        self.getNewCoordinates(self.tanks[0].tank_id, 0)
        tmp_painter = gui.QPainter(self.object_layer)
        tmp_painter.drawImage(self.tanks[0].x_position,
                              self.tanks[0].y_position, self.tanks[0])

        # create second tank
        tank_two = Objects.Tank(
            1, (self.width - 200), (self.height // 2),
            100, 100, core.Qt.black, core.Qt.red
        )
        self.tanks.append(tank_two)
        self.getNewCoordinates(self.tanks[1].tank_id, 0)
        tmp_painter = gui.QPainter(self.object_layer)
        tmp_painter.drawImage(self.tanks[1].x_position,
                              self.tanks[1].y_position, self.tanks[1])
        tmp_painter.end()

        # draw all layers
        self.drawMap()
        self.drawObjects()
        self.drawGame()
        self.setPixmap(gui.QPixmap.fromImage(self.game_image))


if __name__ == "__main__":
    app = widget.QApplication(sys.argv)
    display = GameLabel()
    display.setWindowTitle('Worms')
    display.setScaledContents(True)
    display.show()
    sys.exit(app.exec_())
