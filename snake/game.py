import sys

from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw


class GameView(qw.QLabel):

    def keyPressEvent(self, event):

        if event.key() == qc.Qt.Key_Up and self.direction != 2:
            self.direction = 0
        elif event.key() == qc.Qt.Key_Right and self.direction != 3:
            self.direction = 1
        elif event.key() == qc.Qt.Key_Down and self.direction != 0:
            self.direction = 2
        elif event.key() == qc.Qt.Key_Left and self.direction != 1:
            self.direction = 3

    def move(self):
        """
        Up = 0
        Right = 1
        Down = 2
        Left = 3
        """
        print(self.direction)
        x_value = self.snake_position[0][0]
        y_value = self.snake_position[0][1]
        self.playing_field.setPixel(x_value, y_value, 0xffffffff)
        self.snake_position.pop(0)

        x_value = self.snake_position[-1][0]
        y_value = self.snake_position[-1][1]

        if (self.direction == 0):
            y_value = y_value - 1
        elif (self.direction == 1):
            x_value = x_value + 1
        elif (self.direction == 2):
            y_value = y_value + 1
        elif (self.direction == 3):
            x_value = x_value - 1

        self.playing_field.setPixel(x_value, y_value, 0x00000000)
        self.snake_position.append([x_value, y_value])
        self.setPixmap(qg.QPixmap.fromImage(self.playing_field))

    def __init__(self, width, height):
        super().__init__()

        self.setWindowTitle("Snake")
        self.setScaledContents(True)

        self.width = width
        self.height = height

        self.direction = 1

        self.playing_field = qg.QImage(width, height, qg.QImage.Format_RGB32)
        self.playing_field.fill(qc.Qt.white)
        self.snake_position = [[10, 10], [11, 10], [12, 10], [13, 10]]
        self.playing_field.setPixel(10, 10, 0x00000000)
        self.playing_field.setPixel(11, 10, 0x00000000)
        self.playing_field.setPixel(12, 10, 0x00000000)
        self.playing_field.setPixel(13, 10, 0x00000000)
        self.setPixmap(qg.QPixmap.fromImage(self.playing_field))


if __name__ == "__main__":
    snake_app = qw.QApplication(sys.argv)
    game_view = GameView(100, 100)
    game_view.show()
    timer = qc.QTimer()
    timer.setInterval(10000)
    timer.timeout.connect(game_view.move)
    timer.start(1000)
    sys.exit(snake_app.exec_())
