from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw
from FractalWidget import FractalWidget
import sys


class MainWindow(qw.QWidget):

        def __init__(self):
                #super constructor
                super(MainWindow,self).__init__()
                self.setWindowTitle("Settings for calculation")
                layout=qw.QVBoxLayout()
                self.functions=["z=z^2+c","z=2/3*(z^3-2)/z","z=sinh(z)+c","z=z-11/12*(z^3-1)","z=z-11/12(z^3-1)-1/10*c","z=z^2-0.2-0.7i"]
                self.functionBox=qw.QComboBox()
                self.functionBox.addItems(self.functions)
                layout.addWidget(self.functionBox)
                self.calc=qw.QPushButton("Zeichnen")
                self.calc.clicked.connect(self.draw)
                layout.addWidget(self.calc)
                self.setLayout(layout)
                self.show()

        def draw(self):
                index=self.functionBox.currentIndex()
                self.fractal=FractalWidget(index,self.functions[index])
        
if __name__ == "__main__":
        app=qw.QApplication(sys.argv)
        window=MainWindow()
        sys.exit(app.exec_())
