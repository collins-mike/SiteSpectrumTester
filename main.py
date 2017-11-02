'''
Drone race site spectrum tester
Created on Nov 2, 2017 NextGen RF design

@author: Mike Collins
'''
#import libraries
import sys, os, random,csv,time
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import multiprocessing,logging

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import ticker

import openpyxl as pyxl
from openpyxl.styles import NamedStyle, Font, PatternFill, Border, Side
from openpyxl.styles.alignment import Alignment
from openpyxl.drawing.image import Image
from openpyxl import load_workbook

#import files
from SignalHound import *
from specan import *


class Application(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle("Race Site Tester")
        self.createForm()
        
    def createForm(self):
        self.main_frame=QWidget()
        vbox=QVBoxLayout()
        self.main_frame.setLayout(vbox)
        
        btn_run=QPushButton("Run")
        btn_run.setEnabled(False)
        vbox.addWidget(btn_run)
        
        self.dpi = 100
        self.fig = Figure(dpi=self.dpi)
        self.fig.set_facecolor('#DDDDDD')
        
        self.canvas = FigureCanvas(self.fig)
        canvasBox=QWidget()
        vbox.addWidget(canvasBox)
        
        self.canvas.setParent(canvasBox)
        
        
        self.setCentralWidget(self.main_frame)
    


def main():
    app = QApplication(sys.argv)  
    app.setStyle(QStyleFactory.create("plastique"))
    form = Application()
    form.show()
    form.resize(400,600)
    app.exec_()


if __name__ == '__main__':
    main()
