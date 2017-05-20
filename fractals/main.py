import numpy as np
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw
import matplotlib.pyplot as plt
import sys

if __name__ == "__main__":
        width=500
        height=500
        real=np.linspace(-1,1,width)
        imag=np.linspace(-1,1,height)
        upper_bound=2
        #build matrix with every possible complex number in this grid
        c=np.zeros((len(real),len(imag)),dtype=np.complex128)
        for i in range(len(real)):
                c[i,:]=real[i] +1j*imag
        #copy matrix for base values
        z=np.copy(c)
        #create matrix for counting
        count= np.zeros([len(real),len(imag)]) 
        #calculate sequence
        for i in range(80):
                z=np.square(z)+c
                #if z is in M count
                count[np.absolute(z)<upper_bound]+=1

        #copied this to calculate the actuall colors
        maximum=np.max(count)
        minimum=np.min(count)
        if maximum==0:
                maximum=1
        count=(count-minimum)/maximum
        colormap=plt.get_cmap('RdYlBu')
        colfloat=colormap(count)
        colint=np.asarray(colfloat*255,dtype=np.uint8)
        #create image from data
        img=qg.QImage(colint.data,width,height,qg.QImage.Format_RGBA8888)
        #qt-stuff and show image
        app=qw.QApplication(sys.argv)
        w=qw.QWidget()
        pixmap=qg.QPixmap.fromImage(img)
        l=qw.QLabel()
        l.setPixmap(pixmap)
        layout=qw.QVBoxLayout()
        layout.addWidget(l)
        w.setLayout(layout)
        l.setScaledContents(True)
        w.show()
        sys.exit(app.exec_())
