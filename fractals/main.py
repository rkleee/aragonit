from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw
from FractalWidget import FractalWidget
import sys


class MainWindow(qw.QWidget):

        def __init__(self):
                super(MainWindow,self).__init__()
                rangeValidator=qg.QDoubleValidator()
                rangeValidator.setRange(-2,2,10)
                self.start=qw.QLineEdit()
                self.end=qw.QLineEdit()
                self.start.setValidator(rangeValidator)
                self.end.setValidator(rangeValidator)
                self.setWindowTitle("Settings for calculation")
                rangeLayout=qw.QHBoxLayout()
                rangeLayout.addWidget(self.start)
                rangeLayout.addWidget(qw.QLabel(" x "))
                rangeLayout.addWidget(self.end)
                layout=qw.QVBoxLayout()
                self.functions=["z=z^2+c","z=2/3*(z^3-2)/z","z=sinh(z)+c","z=z-11/12*(z^3-1)","z=z-11/12(z^3-1)-1/10*c","z=z^2-0.2-0.7i"]
                self.functionBox=qw.QComboBox()
                self.functionBox.addItems(self.functions)
                self.calc=qw.QPushButton("Fraktal zeichnen")
                self.calc.clicked.connect(self.draw)
                self.zoom=qw.QLineEdit()
                self.zoom.setValidator(qg.QDoubleValidator())
                self.colorSchema=qw.QLineEdit()
                propertiesLayout=qw.QHBoxLayout()
                propertiesLayout.addWidget(qw.QLabel("Zoomfaktor: "))
                propertiesLayout.addWidget(self.zoom)
                propertiesLayout.addWidget(qw.QLabel("Color schema: "))
                propertiesLayout.addWidget(self.colorSchema)
                buttonLayout=qw.QHBoxLayout()
                buttonLayout.addWidget(self.functionBox)
                buttonLayout.addWidget(self.calc)
                layout.addItem(rangeLayout)
                layout.addItem(propertiesLayout)
                layout.addItem(buttonLayout)
                self.setLayout(layout)
                self.show()

        def draw(self):
                index=self.functionBox.currentIndex()
                #create FractalWidget with all parameters
                self.fractal=FractalWidget(self.start.text(),self.end.text(),index,self.zoom.text(),self.functions[index],self.colorSchema.text())
        
if __name__ == "__main__":
        app=qw.QApplication(sys.argv)
        window=MainWindow()
        sys.exit(app.exec_())
