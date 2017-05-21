import numpy as np
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw
import matplotlib.pyplot as plt
import sys

#Widget class for displaying Fractals
class FractalWidget(qw.QWidget):

        #constructor
        def __init__(self):
                super(FractalWidget, self).__init__()
                self.l=l=qw.QLabel()
                layout=qw.QVBoxLayout()
                layout.addWidget(l)
                self.setLayout(layout)
                self.width=1080
                self.height=1080
                self.real=np.linspace(-2,2,self.width)
                self.imag=np.linspace(-2,2,self.height)
                self.upper_bound=2
                self.createGrid()
                self.caluclateFractal()
                self.draw()

        #uses count to calculate colors and show fractal
        def draw(self):
                #create colormap from count
                colormap=plt.get_cmap('magma')
                colfloat=colormap(self.count)
                colint=np.asarray(colfloat*255,dtype=np.uint8)
                #create image from data
                img=qg.QImage(colint.data,self.width,self.height,qg.QImage.Format_RGBA8888)
                #create pixmap with Image
                pixmap=qg.QPixmap.fromImage(img)
                self.l.setPixmap(pixmap)
                self.show()

        #calculates the grid to calculate the function on
        def createGrid(self):
                #build matrix with every possible complex number in this grid
                self.c=np.zeros((len(self.real),len(self.imag)),dtype=np.complex128)
                for i in range(len(self.real)):
                        self.c[i,:]=self.real[i] +1j*self.imag

        #calculates the series
        def caluclateFractal(self,maxIterations=100):
                #copy matrix for base values
                self.z=np.copy(self.c)
                #create matrix for counting
                self.count= np.zeros([len(self.real),len(self.imag)])
                #calculate sequence
                for i in range(maxIterations):
                        self.function()
                        #if z is in M count
                        self.count[np.absolute(self.z)<self.upper_bound]+=1
                #normalize values
                maximum=np.max(self.count)
                minimum=np.min(self.count)
                if maximum==0:
                        maximum=1
                self.count=(self.count-minimum)/maximum
                #eventually stretch points, to make bigger color difference
                #self.count*=4       

        #this function is evaluated
        def function(self):
                #just some hardcoded functions for fancy testing
                #self.z=np.sinh(self.z)+self.c
                #self.z=self.c+np.multiply(np.square(self.z),np.square(self.z))
                #self.z=self.z-11/12*(np.multiply(self.z,np.square(self.z))-1)
                #self.z=np.square(self.z)+self.c
                #self.z=self.z-11/12*(np.multiply(self.z,np.square(self.z))-1)-1/10*self.c
                #self.z=np.square(self.z)-0.2-0.7j
                #k=0.45
                #self.z=(np.multiply(self.z,np.square(self.z))+k)/(np.multiply(self.z,np.square(self.z))-k)
                #self.z=(-4.0004*self.z**5+0.005-0.005j)/(-4j*self.z**4+0.001j)
                self.z=2/3*(self.z**3-2)/self.z
                 
        #mouse event for zooming in the clicked position will be used center
        def mouseReleaseEvent(self,e):
                #length of real and imag. axis
                y_axis=self.real[len(self.real)-1]-self.real[0]
                x_axis=self.imag[len(self.imag)-1]-self.imag[0]
                #scale pixel values accoring to size
                scale_y=self.width/y_axis
                scale_x=self.height/x_axis
                #calculate new center
                mid_x=e.x()/scale_x +self.imag[0]
                mid_y=e.y()/scale_y + self.real[0]
                #zoom 50% in
                offset_x=x_axis/4
                offset_y=y_axis/4
                #calculate start and end points of grid
                x_start=mid_x-offset_x
                x_end=mid_x+offset_x
                y_start=mid_y-offset_y
                y_end=mid_y+offset_y
                #create axis
                self.real=np.linspace(y_start,y_end,self.width)
                self.imag=np.linspace(x_start,x_end,self.height)
                self.createGrid()
                self.caluclateFractal()
                self.draw()

if __name__ == "__main__":
        app=qw.QApplication(sys.argv)
        w=FractalWidget()
        sys.exit(app.exec_())
