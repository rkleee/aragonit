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

        layout = qw.QVBoxLayout()
        snake_label = snakelabel.SnakeLabel(width, height)
        snake_label.setSpeed(speed)
        layout.addWidget(snake_label)
        self.setLayout(layout)

        # resizes the dialog according to the zoom factor
        self.setGeometry(0, 0, width * zoom_factor, height * zoom_factor)

        self.keyPressEvent = snake_label.keyPressEvent

    def showResult(self, score):
        # creates a QDialog to show the results
        result_dialog = qw.QDialog()
        result_dialog.setWindowTitle("Results")
        result_dialog.setWindowModality(qc.Qt.ApplicationModal)
        result_dialog.setAutoFillBackground(True)

        layout = qw.QVBoxLayout()

        # adds a picture according to the score
        picture_label = qw.QLabel()
        picture_label.resize(300, 300)
        if score < 5:
            picture = qg.QPixmap("snake_sad.jpg")
        elif score < 10:
            picture = qg.QPixmap("snake_normal.jpg")
        else:
            picture = qg.QPixmap("snake_happy.jpg")
        scaled_picture = picture.scaled(
            picture_label.size(), qc.Qt.KeepAspectRatio)
        picture_label.setPixmap(scaled_picture)
        picture_label.setAlignment(qc.Qt.AlignCenter)
        layout.addWidget(picture_label)

        # adds a short text
        if (score == 1):
            text = self.name + ", you have reached " + str(score) + " point."
        else:
            text = self.name + ", you have reached " + str(score) + " points."
        message_label = qw.QLabel(text)
        message_label.setAlignment(qc.Qt.AlignCenter)
        layout.addWidget(message_label)

        result_dialog.setLayout(layout)

        result_dialog.exec_()


class SettingsWidget(qw.QWidget):

    def __init__(self):
        super(SettingsWidget, self).__init__()

        # creates widget to choose the snake app's settings
        self.setWindowTitle("Snake settings")
        self.setAutoFillBackground(True)

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

        self.speed_slider = qw.QSlider(qc.Qt.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(20)
        self.speed_slider.setValue(5)
        layout.addRow(qw.QLabel("Speed:"), self.speed_slider)

        button_box = qw.QHBoxLayout()
        start_button = qw.QPushButton("Start")
        start_button.clicked.connect(self.startGame)
        stop_button = qw.QPushButton("Stop")
        # stop_button.clicked.connect(stopGame)00
        button_box.addWidget(start_button)
        button_box.addWidget(stop_button)
        layout.addRow(button_box)

        self.player_name = self.player_name_text_field.text().strip()

        self.setLayout(layout)

    def startGame(self):
        # use default values for invalid inputs
        name = ""
        height = 20
        width = 20
        zoom_factor = 10
        speed = self.speed_slider.value()

        try:
            name = self.player_name_text_field.text().strip()
        except ValueError:
            pass

        try:
            width = int(self.width_text_field.text())
        except ValueError:
            pass

        try:
            height = int(self.height_text_field.text())
        except ValueError:
            pass

        try:
            zoom_factor = int(self.zoom_factor_text_field.text())
        except ValueError:
            pass

        if name == "":
            name = "Player"
        if width < 10:
            width = default_width
        if height < 10:
            height = default_height
        if zoom_factor < 1:
            zoom_factor = default_zoom_factor

        # open game window
        game_view = GameDialog(width, height, zoom_factor, speed, name)
        game_view.exec_()


if __name__ == "__main__":
    snake_app = qw.QApplication(sys.argv)
    settings_view = SettingsWidget()
    settings_view.show()
    sys.exit(snake_app.exec_())
