import sys

from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw


class SettingsView(qw.QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Snake settings")
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
        highscore_button = qw.QPushButton("Highscore")
        button_box.addWidget(start_button)
        button_box.addWidget(highscore_button)
        layout.addRow(button_box)

        self.setLayout(layout)


if __name__ == "__main__":
    settings_app = qw.QApplication(sys.argv)
    settings_view = SettingsView()
    settings_view.show()
    sys.exit(settings_app.exec_())
