"""The game's start script."""
import sys

import PyQt5.QtGui as gui
import PyQt5.QtWidgets as widget
import PyQt5.QtCore as core

import Layers
import Objects


def getLandscapeCoordinate(layer, x_value, height):
    y_value = 0
    for y_value in range(height):
        alpha = layer.pixelColor(x_value, y_value).alpha()
        if alpha != 0:
            return y_value
    return y_value
    
class ApplicationLabel(widget.QLabel):
     
    def __init__(self,width,height):
        
        super().__init__()
        self.w = width
        self.h = height
        self.setWindowTitle('Worms')
        self.createMapImage(width,height)
        self.setPixmap(gui.QPixmap.fromImage(self.background_layer))
        self.setScaledContents(True)
        self.show()
        
    def keyPressEvent(self,e):
        if e.key() == core.Qt.Key_Left:
                self.updateTankPosition(-10)
                
        if e.key() == core.Qt.Key_Right:
                self.updateTankPosition(10)
                
                
    def updateTankPosition(self,offset):
        # change x positon of tank and get  new y position
        old_x =self.tank_x
        # prevent invalid position
        if old_x + offset >= self.w or old_x - offset <= 0:
                return
        self.tank_x +=offset
        y=getLandscapeCoordinate(self.landscape_layer,self.tank_x, self.h)
        
        # clear old image
        painter =gui.QPainter(self.background_layer)
        painter.eraseRect(0, 0, self.w, self.h)
        painter.end()
        
        # recreate background-Layer
        self.background_layer = Layers  .BackgroundLayer(self.w, self.h, self.color_format)
        
        # paint everthing new
        painter = gui.QPainter(self.background_layer)
        painter.drawImage(0, 0, self.landscape_layer)
        painter.drawImage(self.tank_x,y,self.tank_one)
        painter.end()
        self.setPixmap(gui.QPixmap.fromImage(self.background_layer))
               
    def createMapImage(self,width, height):
        """Create a QImage containing all the different layers of the map."""
        self.color_format = gui.QImage.Format_RGBA8888
        self.background_layer = Layers.BackgroundLayer(width, height, self.color_format)
        self.landscape_layer = Layers.LandscapeLayer(width, height, self.color_format)
        self.tank_one = Objects.Tank(self.color_format)
        painter = gui.QPainter(self.background_layer)
        painter.drawImage(0, 0, self.landscape_layer)
        self.tank_x = 150
        y = getLandscapeCoordinate(self.landscape_layer, self.tank_x, height)
        print(y)
        painter.drawImage(self.tank_x, y, self.tank_one)
        painter.end()

if __name__ == "__main__":
    app = widget.QApplication(sys.argv)
    width = 2000
    height = 1000       
    display = ApplicationLabel(width,height)
    sys.exit(app.exec_())
