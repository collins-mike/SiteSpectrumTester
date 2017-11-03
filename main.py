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
from PyQt4.Qt import QTextEdit


class Application(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle("Race Site Tester")
        self.createForm()
        self.foundSpec=False
        self.specan=SpecAnalyzer()
        
    def createForm(self):
        
        #=======================================================================
        # setup layout
        #=======================================================================
        self.main_frame=QWidget()
        vbox=QVBoxLayout()
        fbox=QFormLayout()
        vbox.addLayout(fbox)
        self.main_frame.setLayout(vbox)
        
        self.btn_findDevice=QPushButton("Find Spectrum Analyzer")
        self.btn_findDevice.setEnabled(True)
        self.connect(self.btn_findDevice, SIGNAL('clicked()'), self.click_find)
        self.deviceInfo=QLineEdit("No device found!")
        fbox.addRow(self.btn_findDevice,self.deviceInfo)
    
        self.btn_run=QPushButton("Run")
        self.btn_run.setEnabled(False)
        self.connect(self.btn_run, SIGNAL('clicked()'), self.click_Run)
        self.runInfo=QLineEdit("Find Spectrum analyzer before running")
        fbox.addRow(self.btn_run,self.runInfo)
        
        #=======================================================================
        # create plot
        #=======================================================================
        self.fig = Figure(figsize=(10,4))
        self.canvas = FigureCanvas(self.fig)
        
        self.canvas.setParent(self.main_frame)
        self.plot = self.fig.add_subplot(211)
        self.plot.set_title('Data, Yo',fontsize=14,fontweight=200)       
        self.plot.set_ylim([-100,-50])
        
        self.invisPlot = self.fig.add_subplot(212)
        self.invisPlot.set_title('Data, Yo',fontsize=14,fontweight=200)       
        self.invisPlot.set_ylim([-100,-50])
        
        vbox.addWidget(self.canvas)
        self.setCentralWidget(self.main_frame)
        
        
    def click_Run(self):
        TEST_NO=20
        
        progress=QProgressDialog(labelText="Running Test",minimum=0,maximum=TEST_NO*5)
        #progress.setCancelButton(None)
        progress.show()
        prog=0
        
        
        #=======================================================================
        # 5-6Ghz
        #=======================================================================
        self.invisPlot.cla()
        self.invisPlot.set_xlim([5000e6,6000e6])
        self.invisPlot.set_title('5GHz ~ 6GHz',fontsize=14,fontweight=200)
        #===================================================================
        # setup signal hound
        #===================================================================
        try:
            #setup sweep coupling if maxhold is selected it will use 100ms for sweeptime
            self.specan.sh.configureCenterSpan(5500e6,1000e6)
            self.specan.sh.configureSweepCoupling(39.45e3,39.45e3,0.05,"native","no-spur-reject")
        except:
            print "specan setup error" 
        
        for q in range(0,TEST_NO):
            dataReturn=self.specan.get_full_sweep()
                
            #get bin size in order to calculate frequencies
            traceInfo=self.specan.sh.queryTraceInfo()
            binsize=traceInfo["arr-bin-size"]
            
            #calculate frequencies from trace info

            dataiter=0
            freqArray=[]
            self.plot.cla()
            self.plot.set_xlim([5000e6,6000e6])
            self.plot.set_title('5GHz ~ 6GHz',fontsize=14,fontweight=200)
            self.plot.set_ylim([-100,-50])
            self.plot.set_xlabel("Frequency (Hz)")
            self.plot.set_ylabel("Power (dBm)")
            for i in dataReturn:
                freqArray.append(int(5000e6+(dataiter*binsize)))
                dataiter+=1
            progress.setValue(prog)   
            self.plot.plot(freqArray,dataReturn,lw=.5)      
            self.canvas.draw()
            if progress.wasCanceled():
                break
            prog+=1
            QApplication.instance().processEvents()
            
        #=======================================================================
        # 3.75-4.25GHz
        #=======================================================================
        self.invisPlot.cla()
        self.invisPlot.set_xlim([3750e6,4250e6])
        self.invisPlot.set_title('3.75GHz ~ 4.25GHz',fontsize=14,fontweight=200)
        #===================================================================
        # setup signal hound
        #===================================================================
        try:
            #setup sweep coupling if maxhold is selected it will use 100ms for sweeptime
            self.specan.sh.configureCenterSpan(4000e6,1000e6)
        except:
            print "specan setup error"    
        
        for q in range(0,TEST_NO):
            try:
                dataReturn=self.specan.get_full_sweep()
            except:
                print "error getting specan sweep"
                
            #get bin size in order to calculate frequencies
            traceInfo=self.specan.sh.queryTraceInfo()
            binsize=traceInfo["arr-bin-size"]
            
            #calculate frequencies from trace info
            print "getting frequencies"

            dataiter=0
            freqArray=[]
            self.plot.cla()
            self.plot.set_xlim([3750e6,4250e6])
            self.plot.set_title('3.75GHz ~ 4.25GHz',fontsize=14,fontweight=200)
            self.plot.set_ylim([-100,-50])
            self.plot.set_xlabel("Frequency (Hz)")
            self.plot.set_ylabel("Power (dBm)")
            for i in dataReturn:
                freqArray.append(int(3750e6+(dataiter*binsize)))
                dataiter+=1
            progress.setValue(prog)    
            self.plot.plot(freqArray,dataReturn,lw=.5)      
            self.canvas.draw()
            if progress.wasCanceled():
                break
            prog+=1
            QApplication.instance().processEvents()
            
        #=======================================================================
        # 865Mhz - 965MHz
        #=======================================================================
        self.invisPlot.cla()
        self.invisPlot.set_xlim([865e6,965e6])
        self.invisPlot.set_title('865MHz ~ 965MHz',fontsize=14,fontweight=200)
        #===================================================================
        # setup signal hound
        #===================================================================
        try:
            #setup sweep coupling if maxhold is selected it will use 100ms for sweeptime
            self.specan.sh.configureCenterSpan(915e6,100e6)
            self.specan.sh.configureSweepCoupling(39.45e3,39.45e3,0.05,"native","no-spur-reject")
        except:
            print "specan setup error"    
        
        for q in range(0,TEST_NO):
            try:
                dataReturn=self.specan.get_full_sweep()
            except:
                print "error getting specan sweep"
                
            #get bin size in order to calculate frequencies
            traceInfo=self.specan.sh.queryTraceInfo()
            binsize=traceInfo["arr-bin-size"]
            
            #calculate frequencies from trace info
            print "getting frequencies"

            dataiter=0
            freqArray=[]
            self.plot.cla()
            self.plot.set_xlim([865e6,965e6])
            self.plot.set_title('865MHz ~ 965MHz',fontsize=14,fontweight=200)
            self.plot.set_ylim([-100,-50])
            self.plot.set_xlabel("Frequency (Hz)")
            self.plot.set_ylabel("Power (dBm)")
            for i in dataReturn:
                freqArray.append(int(865e6+(dataiter*binsize)))
                dataiter+=1
            progress.setValue(prog)    
            self.plot.plot(freqArray,dataReturn,lw=.5)      
            self.canvas.draw()
            if progress.wasCanceled():
                break
            prog+=1
            QApplication.instance().processEvents()
            
            
        #=======================================================================
        # 865Mhz - 965MHz
        #=======================================================================
        self.invisPlot.cla()
        self.invisPlot.set_xlim([813e6,913e6])
        self.invisPlot.set_title('813MHz ~ 913MHz',fontsize=14,fontweight=200)
        #===================================================================
        # setup signal hound
        #===================================================================
        try:
            #setup sweep coupling if maxhold is selected it will use 100ms for sweeptime
            self.specan.sh.configureCenterSpan(863e6,100e6)
        except:
            print "specan setup error"    
        
        for q in range(0,TEST_NO):
            try:
                dataReturn=self.specan.get_full_sweep()
            except:
                print "error getting specan sweep"
                
            #get bin size in order to calculate frequencies
            traceInfo=self.specan.sh.queryTraceInfo()
            binsize=traceInfo["arr-bin-size"]
            
            #calculate frequencies from trace info
            print "getting frequencies"

            dataiter=0
            freqArray=[]
            self.plot.cla()
            self.plot.set_xlim([813e6,913e6])
            self.plot.set_title('813MHz ~ 913MHz',fontsize=14,fontweight=200)
            self.plot.set_ylim([-100,-50])
            self.plot.set_xlabel("Frequency (Hz)")
            self.plot.set_ylabel("Power (dBm)")
            for i in dataReturn:
                freqArray.append(int(813e6+(dataiter*binsize)))
                dataiter+=1
            progress.setValue(prog)    
            self.plot.plot(freqArray,dataReturn,lw=.5)      
            self.canvas.draw()
            if progress.wasCanceled():
                break
            prog+=1
            QApplication.instance().processEvents()
            
        #=======================================================================
        # Wide Band
        #=======================================================================
#         self.plot.cla()
#         self.plot.set_xlim(100e6,6000e6)
#         self.plot.set_title('Wide Band',fontsize=14,fontweight=200)
        #===================================================================
        # setup signal hound
        #===================================================================
        try:
            #setup sweep coupling if maxhold is selected it will use 100ms for sweeptime
            self.specan.sh.configureCenterSpan(3015e6,5970e6)
        except:
            print "specan setup error"    
        
        for q in range(0,TEST_NO):
            try:
                dataReturn=self.specan.get_full_sweep()
            except:
                print "error getting specan sweep"
                
            #get bin size in order to calculate frequencies
            traceInfo=self.specan.sh.queryTraceInfo()
            binsize=traceInfo["arr-bin-size"]
            
            #calculate frequencies from trace info
            print "getting frequencies"

            dataiter=0
            freqArray=[]
            self.plot.cla()
            self.plot.set_xlim(100e6,6000e6)
            self.plot.set_title('Wide Band',fontsize=14,fontweight=200)
            self.plot.set_ylim([-100,-50])
            self.plot.set_xlabel("Frequency (Hz)")
            self.plot.set_ylabel("Power (dBm)")
            for i in dataReturn:
                freqArray.append(int(30e6+(dataiter*binsize)))
                dataiter+=1
            progress.setValue(prog)  
            self.plot.plot(freqArray,dataReturn,lw=.5)      
            self.canvas.draw()
            if progress.wasCanceled():
                break
            prog+=1
            QApplication.instance().processEvents()
        
        progress.close()
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
        
        
        
        
        pass
    def click_find(self):
        self.deviceInfo.setText("Finding spectrum analyzer...")
        QApplication.instance().processEvents()
        try:
            self.foundSpec=self.specan.find_device()
            
        except:
            self.foundSpec=False
        
        if self.foundSpec:
            self.btn_findDevice.setEnabled(False)
            self.btn_run.setEnabled(True)
            self.deviceInfo.setText("Specan Found!!")
            self.specan.sh.configureGain('auto')
            
            #===================================================================
            # setup signal hound
            #===================================================================
            try:
                self.specan.sh.configureLevel(ref = 0, atten = 'auto')
                self.specan.sh.configureProcUnits("log")
                self.specan.sh.configureAcquisition("average","log-scale")
                #setup sweep coupling if maxhold is selected it will use 100ms for sweeptime
                self.specan.sh.configureCenterSpan(5500e6,1000e6)
                self.specan.sh.configureSweepCoupling(100e3,100e3,0.05,"native","no-spur-reject")
            except:
                print "specan setup error"
            
            
             
            
        else:
            self.deviceInfo.setText("No spectrum analyzer Found")
    
    
def main():
    app = QApplication(sys.argv)  
    app.setStyle(QStyleFactory.create("plastique"))
    form = Application()
    form.show()
    #form.resize(400,600)
    app.exec_()


if __name__ == '__main__':
    main()
