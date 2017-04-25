import sys

from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw

import snakelabel


class SettingsWidget(qw.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Snake")

        self.direction = 1

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
        start_button.clicked.connect(self.startGame)
        stop_button = qw.QPushButton("Stop")
        button_box.addWidget(start_button)
        button_box.addWidget(stop_button)
        layout.addRow(button_box)

        self.setLayout(layout)

    def startGame(self):

        game_view = snakelabel.SnakeLabel(100, 100)
        game_view.setWindowTitle("Snake")
        game_view.exec_()


if __name__ == "__main__":
    snake_app = qw.QApplication(sys.argv)
    settings_view = SettingsWidget()
    settings_view.show()
    sys.exit(snake_app.exec_())
