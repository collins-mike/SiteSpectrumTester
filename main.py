'''
Drone race site spectrum tester
Created on Nov 2, 2017 NextGen RF design

@author: Mike Collins
'''

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


if __name__ == '__main__':
    print "Hello Mike"
    pass