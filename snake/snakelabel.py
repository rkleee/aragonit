import sys

from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw


class SnakeLabel(qw.QLabel):

    def __init__(self,base_width, base_height,width, height):
        super(SnakeLabel, self).__init__()
        #move label to (400,100) and set width and height
        self.setGeometry(base_width,base_height,width,height)
        self.setWindowTitle("Snake")
        self.setScaledContents(True)

        self.width = width
        self.height = height

        self.snake_color = 0x00000000  # black
        self.background_color = 0xffffffff  # white
        self.direction = 1

        self.timer = qc.QTimer()

        self.playing_field = qg.QImage(width, height, qg.QImage.Format_RGB32)
        self.playing_field.fill(self.background_color)

        # first position of list is last position of snake
        self.snake_position = [[0, 0], [1, 0], [2, 0], [3, 0]]
        for pos in self.snake_position:
            self.playing_field.setPixel(pos[0], pos[1], self.snake_color)
        self.setPixmap(qg.QPixmap.fromImage(self.playing_field))

        self.show()

        self.startGame()

    def moveSnake(self):
        # get end of snake
        x_value = self.snake_position[0][0]
        y_value = self.snake_position[0][1]
        # delete end of snake
        self.playing_field.setPixel(x_value, y_value, self.background_color)
        self.snake_position.pop(0)

        # get beginning of snake
        x_value = self.snake_position[-1][0]
        y_value = self.snake_position[-1][1]

        # calculate new beginning of snake
        if (self.direction == 0):
            y_value = y_value - 1
        elif (self.direction == 1):
            x_value = x_value + 1
        elif (self.direction == 2):
            y_value = y_value + 1
        elif (self.direction == 3):
            x_value = x_value - 1

        # only draw snake if beginning of snake is valid
        if not self.crossedBorder(x_value, y_value):
            self.playing_field.setPixel(x_value, y_value, self.snake_color)
            self.snake_position.append([x_value, y_value])
            self.setPixmap(qg.QPixmap.fromImage(self.playing_field))
        else:
            print("You've lost!")
            self.stopGame()

    def crossedBorder(self, x, y):
        """Returns true if coordinates are out of range."""
        return x < 0 or x >= self.width or y < 0 or y >= self.height

    def keyPressEvent(self, event):
        """
        Translates the pressed key into an integer and
        stores it into the "direction" variable. Only allows
        direction changes to the right or to the left relative to
        the actual moving direction.

        Up = 0
        Right = 1
        Down = 2
        Left = 3
        """
        if event.key() == qc.Qt.Key_Up and self.direction != 2:
            self.direction = 0
        elif event.key() == qc.Qt.Key_Right and self.direction != 3:
            self.direction = 1
        elif event.key() == qc.Qt.Key_Down and self.direction != 0:
            self.direction = 2
        elif event.key() == qc.Qt.Key_Left and self.direction != 1:
            self.direction = 3

    def startGame(self):
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.moveSnake)
        self.timer.start(100)

    def stopGame(self):
        self.timer.stop()
