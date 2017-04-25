import sys

from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw


class SnakeLabel(qw.QLabel):

    def __init__(self, width, height):
        super(SnakeLabel, self).__init__()

        self.setWindowTitle("Snake")
        self.setScaledContents(True)

        self.width = width
        self.height = height

        self.direction = 1

        self.timer = qc.QTimer()

        self.playing_field = qg.QImage(width, height, qg.QImage.Format_RGB32)
        self.playing_field.fill(qc.Qt.white)
        self.snake_position = [[0, 0], [1, 0], [2, 0], [3, 0]]
        for pos in self.snake_position:
            self.playing_field.setPixel(pos[0], pos[1], 0x00000000)
        self.setPixmap(qg.QPixmap.fromImage(self.playing_field))

        self.show()

        self.startGame()

    def moveSnake(self):
        x_value = self.snake_position[0][0]
        y_value = self.snake_position[0][1]
        self.playing_field.setPixel(x_value, y_value, 0xffffffff)
        self.snake_position.pop(0)

        x_value = self.snake_position[-1][0]
        y_value = self.snake_position[-1][1]

        if (x_value >= 0 and x_value <= self.width and y_value >= 0 and y_value <= self.height):
            if (self.direction == 0):
                y_value = y_value - 1
            elif (self.direction == 1):
                x_value = x_value + 1
            elif (self.direction == 2):
                y_value = y_value + 1
            elif (self.direction == 3):
                x_value = x_value - 1
        else:
            print("You've lost!")

        self.playing_field.setPixel(x_value, y_value, 0x00000000)
        self.snake_position.append([x_value, y_value])
        self.setPixmap(qg.QPixmap.fromImage(self.playing_field))

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
        self.timer.start(1000)
