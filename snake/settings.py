import sys

from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw

import snakelabel


class GameDialog(qw.QDialog):

    def __init__(self, width, height, zoom_factor, speed, name):
        super(GameDialog, self).__init__()

        self.setWindowTitle("Snake game")
        self.setWindowModality(qc.Qt.ApplicationModal)
        self.setAutoFillBackground(True)

        self.name = name

        layout = qw.QGridLayout()
        snake_label = snakelabel.SnakeLabel(width, height, speed)

        text = "Welcome " + name + "!"
        self.message_label = qw.QLabel(text)
        layout.addWidget(snake_label, 1, 1, 1, 1)
        layout.addWidget(self.message_label, 2, 1, 1, 1)

        self.setLayout(layout)

        # resizes the dialog according to the zoom factor
        self.setGeometry(0, 0, width * zoom_factor, height * zoom_factor)

        self.keyPressEvent = snake_label.keyPressEvent

    def printScore(self, score):
        text = self.name + ", you have reached " + str(score) + " points."
        self.message_label.setText(text)


def startGame():
    # use default values for invalid inputs
    name = ""
    height = 20
    width = 20
    zoom_factor = 10
    speed = speed_slider.value()
    try:
        name = player_name_text_field.text().strip()
    except ValueError:
        pass

    try:
        width = int(width_text_field.text())
    except ValueError:
        pass

    try:
        height = int(height_text_field.text())
    except ValueError:
        pass

    try:
        zoom_factor = int(zoom_factor_text_field.text())
    except ValueError:
        pass

    if name == "":
        name = "player"
    if width < 10:
        width = default_width
    if height < 10:
        height = default_height
    if zoom_factor < 1:
        zoom_factor = default_zoom_factor

    game_view = GameDialog(width, height, zoom_factor, speed, name)
    game_view.exec_()


snake_app = qw.QApplication(sys.argv)

# creates widget to choose the snake app's settings
settings_view = qw.QWidget()
settings_view.setWindowTitle("Snake settings")

layout = qw.QFormLayout()

player_name_text_field = qw.QLineEdit()
player_name_text_field.setToolTip("Your player's name.")
layout.addRow(qw.QLabel("Player name:"), player_name_text_field)

board_size_box = qw.QHBoxLayout()
width_text_field = qw.QLineEdit()
width_text_field.setToolTip("Width of the playing field.")
width_text_field.setValidator(qg.QIntValidator())
height_text_field = qw.QLineEdit()
height_text_field.setToolTip("Height of the playing field.")
height_text_field.setValidator(qg.QIntValidator())
board_size_box.addWidget(width_text_field)
board_size_box.addWidget(qw.QLabel("x"))
board_size_box.addWidget(height_text_field)
layout.addRow(qw.QLabel("Board size:"), board_size_box)

zoom_factor_text_field = qw.QLineEdit()
zoom_factor_text_field.setToolTip("Zoom factor.")
zoom_factor_text_field.setValidator(qg.QIntValidator())
layout.addRow(qw.QLabel("Zoom factor:"), zoom_factor_text_field)

speed_slider = qw.QSlider(qc.Qt.Horizontal)
speed_slider.setMinimum(10)
speed_slider.setMaximum(1000)
speed_slider.setValue(100)
layout.addRow(qw.QLabel("Speed:"), speed_slider)

button_box = qw.QHBoxLayout()
start_button = qw.QPushButton("Start")
start_button.clicked.connect(startGame)
stop_button = qw.QPushButton("Stop")
# stop_button.clicked.connect(stopGame)
button_box.addWidget(start_button)
button_box.addWidget(stop_button)
layout.addRow(button_box)

settings_view.setLayout(layout)

settings_view.show()

sys.exit(snake_app.exec_())
