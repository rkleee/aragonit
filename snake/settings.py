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
        self.default_height = 200
        self.default_width = 200

        layout = qw.QFormLayout()

        self.player_name_text_field = qw.QLineEdit()
        self.player_name_text_field.setToolTip("Your player's name.")
        layout.addRow(qw.QLabel("Player name:"), self.player_name_text_field)

        board_size_box = qw.QHBoxLayout()
        self.width_text_field = qw.QLineEdit()
        self.width_text_field.setToolTip("Width of the playing field.")
        self.width_text_field.setValidator(qg.QIntValidator())
        self.height_text_field = qw.QLineEdit()
        self.height_text_field.setToolTip("Height of the playing field.")
        self.height_text_field.setValidator(qg.QIntValidator())
        board_size_box.addWidget(self.width_text_field)
        board_size_box.addWidget(qw.QLabel("x"))
        board_size_box.addWidget(self.height_text_field)
        layout.addRow(qw.QLabel("Board size:"), board_size_box)

        self.zoom_factor_text_field = qw.QLineEdit()
        self.zoom_factor_text_field.setToolTip("Zoom factor.")
        self.zoom_factor_text_field.setValidator(qg.QIntValidator())
        layout.addRow(qw.QLabel("Zoom factor:"), self.zoom_factor_text_field)

        button_box = qw.QHBoxLayout()
        start_button = qw.QPushButton("Start")
        start_button.clicked.connect(self.startGame)
        stop_button = qw.QPushButton("Stop")
        button_box.addWidget(start_button)
        button_box.addWidget(stop_button)
        layout.addRow(button_box)

        self.setLayout(layout)

    def startGame(self):
        #exception handling not necessary because of QIntValidator
        width = int (self.width_text_field.text())
        height = int (self.height_text_field.text())
        #if height or width are invalid use default values
        if width <= 0 or height <=0:
           width = self.default_width
           height = self.default_height
        game_view = snakelabel.SnakeLabel(width,height)
        game_view.setWindowTitle("Snake")
        game_view.exec_()


if __name__ == "__main__":
    snake_app = qw.QApplication(sys.argv)
    settings_view = SettingsWidget()
    settings_view.show()
    sys.exit(snake_app.exec_())
