import sys

from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw

from FractalWidget import FractalWidget


class MainWindow(qw.QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        rangeValidator = qg.QDoubleValidator()
        rangeValidator.setRange(-2, 2, 10)
        self.startField = qw.QLineEdit()
        self.endField = qw.QLineEdit()
        self.startField.setValidator(rangeValidator)
        self.endField.setValidator(rangeValidator)
        self.setWindowTitle("Settings for calculation")
        rangeLayout = qw.QHBoxLayout()
        rangeLayout.addWidget(qw.QLabel("Field size (square): "))
        rangeLayout.addWidget(self.startField)
        rangeLayout.addWidget(qw.QLabel(" x "))
        rangeLayout.addWidget(self.endField)
        layout = qw.QVBoxLayout()
        self.functions = ["z=z^2+c", "z=2/3*(z^3-2)/z", "z=sinh(z)+c", "z=z-11/12*(z^3-1)",
                          "z=z-11/12(z^3-1)-1/10*c", "z=z^2-0.2-0.7i", "z=z^2-0.742+0.1j"]
        self.functionBox = qw.QComboBox()
        self.functionBox.addItems(self.functions)
        self.calc = qw.QPushButton("Calculate and draw")
        self.calc.clicked.connect(self.draw)
        self.zoomField = qw.QLineEdit()
        self.zoomField.setValidator(qg.QDoubleValidator())
        self.colorSchema = ["rainbow", "spring", "autumn", "viridis",
                            "magma", "Greens", "YlOrBr", "YlGnBu", "BrBG", "Spectral", "bwr"]
        self.color = qw.QComboBox()
        self.color.addItems(self.colorSchema)
        zoomLayout = qw.QHBoxLayout()
        zoomLayout.addWidget(qw.QLabel("Zoomfaktor: "))
        zoomLayout.addWidget(self.zoomField)
        colorLayout = qw.QHBoxLayout()
        colorLayout.addWidget(qw.QLabel("Color schema: "))
        colorLayout.addWidget(self.color)
        layout.addItem(rangeLayout)
        layout.addItem(zoomLayout)
        layout.addItem(colorLayout)
        layout.addWidget(self.functionBox)
        layout.addWidget(self.calc)
        self.setLayout(layout)
        self.show()

    # called on Button click instantiates FractalWidget with properties
    def draw(self):
        # get choosen function and colormap
        functionIndex = self.functionBox.currentIndex()
        functionText = self.functions[functionIndex]
        colorIndex = self.color.currentIndex()
        col = self.colorSchema[colorIndex]
        # convert zoom and intervall to floatg
        # on passError use default values
        try:
            zoom = float(self.zoomField.text())
        except ValueError:
            zoom = 0.5
        try:
            start = float(self.startField.text())
            end = float(self.endField.text())
        except ValueError:
            start = -2
            end = 2
        # create FractalWidget with all parameters
        self.fractal = FractalWidget(
            start, end, functionIndex, zoom, functionText, col)


if __name__ == "__main__":
    app = qw.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
