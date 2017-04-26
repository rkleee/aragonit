import sys

from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw

import snakelabel


def startGame(self):
    # use default values for invalid inputs
    try:
        name = player_name_text_field.text()
    except ValueError:
        name = default_name

    try:
        width = int(width_text_field.text())
    except ValueError:
        width = default_width

    try:
        height = int(height_text_field.text())
    except ValueError:
        height = default_height

    try:
        zoom_factor = int(zoom_factor_text_field.text())
    except ValueError:
        zoom_factor = default_zoom_factor

    if width < 10:
        width = default_width
    if height < 10:
        height = default_height
    if zoom_factor < 1:
        zoom_factor = default_zoom_factor

    # creates dialog to play snake
    game_view = qw.QDialog()
    game_view.setWindowTitle("Snake game")
    game_view.setWindowModality(qc.Qt.ApplicationModal)
    game_view.setAutoFillBackground(True)


    # resizes the dialog according to the zoom factor
    game_view.resize(width * zoom_factor, height * zoom_factor)

    layout = qw.QGridLayout()
    snake_label = snakelabel.SnakeLabel(width, height, name)
    message_label = qw.QLabel("Play snake!")
    layout.addWidget(snake_label, 1, 1, 1, 1)
    layout.addWidget(message_label, 2, 1, 1, 1)

    game_view.setLayout(layout)

    game_view.keyPressEvent = snake_label.keyPressEvent

    game_view.exec_()


snake_app = qw.QApplication(sys.argv)

# creates widget to choose the snake app's settings
settings_view = qw.QWidget()
settings_view.setWindowTitle("Snake settings")

# sets some default values
default_name = "player"
default_height = 20
default_width = 20
default_zoom_factor = 10

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

button_box = qw.QHBoxLayout()
start_button = qw.QPushButton("Start")
start_button.clicked.connect(startGame)
stop_button = qw.QPushButton("Stop")
# stop_button.clicked.connect(self.stopGame)
button_box.addWidget(start_button)
button_box.addWidget(stop_button)
layout.addRow(button_box)

settings_view.setLayout(layout)

settings_view.show()

sys.exit(snake_app.exec_())
