import numpy as np
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw
import matplotlib.pyplot as plt

#Widget class for displaying Fractals
class FractalWidget(qw.QWidget):

        #constructor
        def __init__(self,start,end,functionIndex,zoomFactor,text,cmap):
                super(FractalWidget, self).__init__()
                self.setWindowTitle("Drawing: "+text)
                layout=qw.QVBoxLayout()
                self.pixmapLabel=qw.QLabel()
                layout.addWidget(self.pixmapLabel)
                self.setLayout(layout)
                #set all needed properties
                self.width=700
                self.height=700
                #zoomfactor 0.25 zooms 25% from middle in each direction -> 50%
                #zoomfactor 0.5  zooms 50% from middle in each direction -> no zoom
                self.zoomFactor=zoomFactor/2                        
                self.real=np.linspace(start,end,self.height)
                self.imag=np.linspace(start,end,self.width)
                #create colormap from count
                self.colormap=plt.get_cmap(cmap)
                self.upper_bound=2
                self.functionIndex=functionIndex
                self.maxIterations=70
                #start calculation
                self.createGrid()
                self.caluclateFractal()
                self.draw()

        #uses count to calculate colors and show fractal
        def draw(self):
                colfloat=self.colormap(self.count)
                colint=np.asarray(colfloat*255,dtype=np.uint8)
                #create image from data
                img=qg.QImage(colint.data,self.width,self.height,qg.QImage.Format_RGBA8888)
                #create pixmap with Image
                pixmap=qg.QPixmap.fromImage(img)
                self.pixmapLabel.setPixmap(pixmap)
                self.show()

        #calculates the grid to calculate the function on
        def createGrid(self):
                #build matrix with every possible complex number in this grid
                self.c=np.zeros((len(self.real),len(self.imag)),dtype=np.complex128)
                for i in range(len(self.real)):
                        self.c[i,:]=self.real[i] +1j*self.imag

        #calculates the series
        def caluclateFractal(self):
                #copy matrix for base values
                self.z=np.copy(self.c)
                #create matrix for counting
                self.count= np.zeros([len(self.real),len(self.imag)])
                #calculate sequence
                if self.functionIndex==0:
                        self.sequence0()
                if self.functionIndex==1:
                        self.sequence1()
                if self.functionIndex==2:
                        self.sequence2()
                if self.functionIndex==3:
                        self.sequence3()
                if self.functionIndex==4:
                        self.sequence4()
                if self.functionIndex==5:
                        self.sequence5()
                if self.functionIndex==6:
                        self.sequence6()                          
                #normalize values
                maximum=np.max(self.count)
                minimum=np.min(self.count)
                if maximum==0:
                        maximum=1
                self.count=(self.count-minimum)/maximum
      
        #0: z=z^2+c
        def sequence0(self):
                for i in range(self.maxIterations):
                        self.z=np.power(self.z,2)+self.c
                        self.count[np.absolute(self.z)<self.upper_bound]+=1

        #1: z=2/3*(z^3-2)/z 
        def sequence1(self):
                for i in range(self.maxIterations):
                        self.z=2/3*(np.power(self.z,3)-2)/self.z
                        self.count[np.absolute(self.z)<self.upper_bound]+=1
        
        #2: z=sinh(z)+c
        def sequence2(self):
                for i in range(self.maxIterations):
                        self.z=np.sinh(self.z)+self.c
                        self.count[np.absolute(self.z)<self.upper_bound]+=1
        
        #3: z=z-11/12*(z^3-1)
        def sequence3(self):
                for i in range(self.maxIterations):
                        self.z=self.z-11/12*(np.power(self.z,3)-1)
                        self.count[np.absolute(self.z)<self.upper_bound]+=1
        
        #4: z=z-11/12(z^3-1)-1/10*c
        def sequence4(self):
                for i in range(self.maxIterations):
                        self.z=self.z-11/12*(np.power(self.z,3)-1)-1/10*self.c
                        self.count[np.absolute(self.z)<self.upper_bound]+=1
        
        #5: z=z^2-0.2-0.7i
        def sequence5(self):
                for i in range(self.maxIterations):
                        self.z=np.square(self.z)-0.2-0.7j
                        self.count[np.absolute(self.z)<self.upper_bound]+=1

        #6: z=z^2 -0.742+0.1i
        def sequence6(self):
               for i in range(self.maxIterations):
                        self.z=np.square(self.z)-0.742+0.1j
                        self.count[np.absolute(self.z)<self.upper_bound]+=1          
                
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
                offset_x=x_axis*self.zoomFactor
                offset_y=y_axis*self.zoomFactor
                #calculate start and end points of grid
                x_start=mid_x-offset_x
                x_end=mid_x+offset_x
                y_start=mid_y-offset_y
                y_end=mid_y+offset_y
                #create axis
                self.real=np.linspace(y_start,y_end,self.width)
                self.imag=np.linspace(x_start,x_end,self.height)
                #start calcualtion
                self.createGrid()
                self.caluclateFractal()
                self.draw()

        def keyReleaseEvent(self,event):
                #I inverts zoomFactor to Zoom out
                if event.key()==qc.Qt.Key_I:
                        if self.zoomFactor<0.5:
                                self.zoomFactor+=0.5
                        elif self.zoomFactor>0.5:
                                self.zoomFactor-=0.5
                # Plus increases zoom 10%
                if event.key()==qc.Qt.Key_Plus:
                        self.zoomFactor*=0.9
                # minus decreaes zoom 10%
                if event.key()==qc.Qt.Key_Minus:
                        self.zoomFactor*=1.1
