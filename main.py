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
        self.deviceInfo=QLineEdit("No spectrum analyzer found!")
        self.deviceInfo.setEnabled(False)
        fbox.addRow(self.btn_findDevice,self.deviceInfo)
    
        self.btn_run=QPushButton("Run")
        self.btn_run.setEnabled(False)
        self.connect(self.btn_run, SIGNAL('clicked()'), self.click_Run)
        self.runInfo=QLineEdit("Find Spectrum analyzer before running")
        self.runInfo.setEnabled(False)
        fbox.addRow(self.btn_run,self.runInfo)
        
        #=======================================================================
        # create plot
        #=======================================================================
        self.fig = Figure(figsize=(10,4))
        self.canvas = FigureCanvas(self.fig)
        
        self.canvas.setParent(self.main_frame)
        self.plot = self.fig.add_subplot(111)
        self.plot.set_title('---',fontsize=14,fontweight=200)       
        self.plot.set_ylim([-100,-50])
        
        vbox.addWidget(self.canvas)
        self.setCentralWidget(self.main_frame)
        
        
    def click_Run(self):
        TEST_NO=20
        canceled=False
        
        reDraw=False    #make true if you want plot to draw on top of eachother
        
        self.btn_run.setEnabled(False)
        self.runInfo.setText('Running Test...')
        QApplication.instance().processEvents()
        progress=QProgressDialog(labelText="Running Test",minimum=0,maximum=TEST_NO*5)
        progress.show()
        progress.move(10,10)
        prog=0
        
        
        #=======================================================================
        # 5-6Ghz
        #=======================================================================
        self.plot.cla()
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
            if not reDraw:
                self.plot.cla()
            self.plot.set_xlim([5000e6,6000e6])
            self.plot.set_title('Center: 5.5GHz    Span: 5GHz ~ 6GHz',fontsize=14,fontweight=200)
            self.plot.set_ylim([-150,-0])
            self.plot.set_xlabel("Frequency (Hz)")
            self.plot.set_ylabel("Power (dBm)")
            self.plot.grid(True)
            for i in dataReturn:
                freqArray.append(int(5000e6+(dataiter*binsize)))
                dataiter+=1
            progress.setValue(prog)   
            self.plot.plot(freqArray,dataReturn,lw=.5, color='r')      
#             self.plot.scatter(freqArray,dataReturn,c=matplotlib.cm.jet(np.abs(dataReturn)), edgecolor='none',marker=',', s=0.75)  
            self.canvas.draw()
            if progress.wasCanceled():
                canceled=True
                break
            prog+=1
            QApplication.instance().processEvents()
        
        self.canvas.print_figure('temp_5_5GHz.png')    
        
        #=======================================================================
        # 3.75-4.25GHz
        #=======================================================================
        self.plot.cla()
        #===================================================================
        # setup signal hound
        #===================================================================
        try:
            #setup sweep coupling if maxhold is selected it will use 100ms for sweeptime
            self.specan.sh.configureCenterSpan(4000e6,1000e6)
        except:
            print "specan setup error"    
        
        for testNo in range(0,TEST_NO):
            try:
                dataReturn=self.specan.get_full_sweep()
            except:
                print "error getting specan sweep"
                
            #get bin size in order to calculate frequencies
            traceInfo=self.specan.sh.queryTraceInfo()
            binsize=traceInfo["arr-bin-size"]
            
            #calculate frequencies from trace info

            dataiter=0
            freqArray=[]
            if not reDraw:
                self.plot.cla()
            self.plot.set_xlim([3750e6,4250e6])
            self.plot.set_title('Center: 4GHz    Span: 3.75GHz ~ 4.25GHz',fontsize=14,fontweight=200)
            self.plot.set_ylim([-150,-0])
            self.plot.set_xlabel("Frequency (Hz)")
            self.plot.set_ylabel("Power (dBm)")
            self.plot.grid(True)
            for i in dataReturn:
                freqArray.append(int(3750e6+(dataiter*binsize)))
                dataiter+=1
            progress.setValue(prog)    
            self.plot.plot(freqArray,dataReturn,lw=.5,c='r')      
#             self.plot.scatter(freqArray,dataReturn,c=matplotlib.cm.jet(np.abs(dataReturn)), edgecolor='none',marker=',', s=0.75)  
            self.canvas.draw()
            if progress.wasCanceled():
                canceled=True
                break
            prog+=1
            QApplication.instance().processEvents()
            
        self.canvas.print_figure('temp_4GHz.png')  
        
        #=======================================================================
        # 865Mhz - 965MHz
        #=======================================================================
        self.plot.cla()
        #===================================================================
        # setup signal hound
        #===================================================================
        try:
            #setup sweep coupling if maxhold is selected it will use 100ms for sweeptime
            self.specan.sh.configureCenterSpan(915e6,100e6)
            self.specan.sh.configureSweepCoupling(39.45e3,39.45e3,0.05,"native","no-spur-reject")
        except:
            print "specan setup error"    
        
        for testNo in range(0,TEST_NO):
            try:
                dataReturn=self.specan.get_full_sweep()
            except:
                print "error getting specan sweep"
                
            #get bin size in order to calculate frequencies
            traceInfo=self.specan.sh.queryTraceInfo()
            binsize=traceInfo["arr-bin-size"]
            
            #calculate frequencies from trace info

            dataiter=0
            freqArray=[]
            if not reDraw:
                self.plot.cla()
            self.plot.set_xlim([865e6,965e6])
            self.plot.set_title('Center: 915MHz    Span: 865MHz ~ 965MHz',fontsize=14,fontweight=200)
            self.plot.set_ylim([-150,-0])
            self.plot.set_xlabel("Frequency (Hz)")
            self.plot.set_ylabel("Power (dBm)")
            self.plot.grid(True)
            for i in dataReturn:
                freqArray.append(int(865e6+(dataiter*binsize)))
                dataiter+=1
            progress.setValue(prog)    
            self.plot.plot(freqArray,dataReturn,lw=.5,c='r')     
#             self.plot.scatter(freqArray,dataReturn,c=matplotlib.cm.jet(np.abs(dataReturn)), edgecolor='none',marker=',', s=0.75)    
            self.canvas.draw()
            if progress.wasCanceled():
                canceled=True
                break
            prog+=1
            QApplication.instance().processEvents()
            
        self.canvas.print_figure('temp_915MHz.png')  
            
        #=======================================================================
        # 865Mhz - 965MHz
        #=======================================================================
        self.plot.cla()
        #===================================================================
        # setup signal hound
        #===================================================================
        try:
            #setup sweep coupling if maxhold is selected it will use 100ms for sweeptime
            self.specan.sh.configureCenterSpan(863e6,100e6)
        except:
            print "specan setup error"    
        
        for testNo in range(0,TEST_NO):
            try:
                dataReturn=self.specan.get_full_sweep()
            except:
                print "error getting specan sweep"
                
            #get bin size in order to calculate frequencies
            traceInfo=self.specan.sh.queryTraceInfo()
            binsize=traceInfo["arr-bin-size"]
            
            #calculate frequencies from trace info

            dataiter=0
            freqArray=[]
            if not reDraw:
                self.plot.cla()
            self.plot.set_xlim([813e6,913e6])
            self.plot.set_title('Center: 863MHz    Span: 813MHz ~ 913MHz',fontsize=14,fontweight=200)
            self.plot.set_ylim([-150,-0])
            self.plot.set_xlabel("Frequency (Hz)")
            self.plot.set_ylabel("Power (dBm)")
            self.plot.grid(True)
            for i in dataReturn:
                freqArray.append(int(813e6+(dataiter*binsize)))
                dataiter+=1
            progress.setValue(prog)    
            self.plot.plot(freqArray,dataReturn,lw=.5, c='r')      
#             self.plot.scatter(freqArray,dataReturn,c=matplotlib.cm.jet(np.abs(dataReturn)), edgecolor='none',marker=',', s=0.75)  
            self.canvas.draw()
            if progress.wasCanceled():
                canceled=True
                break
            prog+=1
            QApplication.instance().processEvents()
            
        self.canvas.print_figure('temp_863MHz.png')  
            
        #=======================================================================
        # Wide Band
        #=======================================================================
        self.plot.cla()
#         self.plot.set_xlim(100e6,6000e6)
#         self.plot.set_title('Wide Band',fontsize=14,fontweight=200)
        #===================================================================
        # setup signal hound
        #===================================================================
        try:
            #setup sweep coupling if maxhold is selected it will use 100ms for sweeptime
            self.specan.sh.configureCenterSpan(3015e6,5970e6)
            self.specan.sh.configureSweepCoupling(300e3,300e3,0.001,"native","no-spur-reject")
        except:
            print "specan setup error"    
        
        for testNo in range(0,TEST_NO):
            try:
                dataReturn=self.specan.get_full_sweep()
            except:
                print "error getting specan sweep"
                
            #get bin size in order to calculate frequencies
            traceInfo=self.specan.sh.queryTraceInfo()
            binsize=traceInfo["arr-bin-size"]
            
            #calculate frequencies from trace info
            dataiter=0
            freqArray=[]
            if not reDraw:
                self.plot.cla()
            self.plot.set_xlim(100e6,6000e6)
            self.plot.set_title('Wide Band    Span: (0~6GHz)',fontsize=14,fontweight=200)
            self.plot.set_ylim([-150,-0])
            self.plot.set_xlabel("Frequency (Hz)")
            self.plot.set_ylabel("Power (dBm)")
            self.plot.grid(True)
            for i in dataReturn:
                freqArray.append(int(30e6+(dataiter*binsize)))
                dataiter+=1
            progress.setValue(prog)  
            self.plot.plot(freqArray,dataReturn,lw=.5, c='r')      
#             self.plot.scatter(freqArray,dataReturn,c=matplotlib.cm.jet(np.abs(dataReturn)), edgecolor='none',marker=',', s=0.75)  
            self.canvas.draw()
            if progress.wasCanceled():
                canceled=True
                break
            prog+=1
            QApplication.instance().processEvents()
        
        self.canvas.print_figure('temp_WideBand.png')  
        
        progress.close()
        
        msg = QMessageBox()
        msg.setInformativeText("Test complete. would you like to save this data?")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.buttonClicked.connect(self.msgbtn)
        if canceled==False:
            msg.exec_()
            
        self.runInfo.setText('Ready to run test')
        self.btn_run.setEnabled(True)
        
    def msgbtn(self,i):
        print "Button pressed is:",i.text()
        if i.text()== "&Yes":
            self.saveData()
            
        elif i.text()== "No":
            pass    
        
    def saveData(self):
        file_choices = "Excel Workbook ( *.xlsx)"
        path = unicode(QFileDialog.getSaveFileName(self, 
                        'Save', '', 
                        file_choices))
        
        
        
        if path:
            wb = pyxl.Workbook()
            ws = wb.create_sheet("Race Site SPectrum Test", 0)
            
            img = Image('temp_5_5GHz.png')
            ws.add_image(img, 'A1')
            
            img = Image('temp_4GHz.png')
            ws.add_image(img, 'A25')
            
            img = Image('temp_915MHz.png')
            ws.add_image(img, 'A50')
            
            img = Image('temp_863MHz.png')
            ws.add_image(img, 'A75')
            
            img = Image('temp_WideBand.png')
            ws.add_image(img, 'A100')
            
            
        try:
            wb.save(path)
        except: 
            print "Error"
            self.show_errorDialog("File Save Error!", "Unable to save report!", "Ensure report is not open in another program.")
                  
            
        
    def click_find(self):
        self.deviceInfo.setText("Finding spectrum analyzer...")
        self.btn_findDevice.setEnabled(False)
        QApplication.instance().processEvents()
        try:
            self.foundSpec=self.specan.find_device()
            
        except:
            self.foundSpec=False
        
        if self.foundSpec:
            self.btn_findDevice.setEnabled(False)
            self.btn_run.setEnabled(True)
            self.deviceInfo.setText("Spectrum analyzer found!! (SH BB60C)")
            self.runInfo.setText("Ready to run test")
            self.specan.sh.configureGain('auto')
            
            #===================================================================
            # setup signal hound
            #===================================================================
            try:
                self.specan.sh.configureLevel(ref = 0, atten = 'auto')
                self.specan.sh.configureProcUnits("log")
                self.specan.sh.configureAcquisition("Average","log-scale")
                self.specan.sh.configureCenterSpan(5500e6,1000e6)
                self.specan.sh.configureSweepCoupling(100e3,100e3,0.09,"native","no-spur-reject")
                self.specan.sh.configureGain('auto')
            except:
                print "specan setup error"
            
            
             
            
        else:
            self.deviceInfo.setText("No spectrum analyzer Found")
            self.btn_findDevice.setEnabled(True)
    
    
def main():
    app = QApplication(sys.argv)  
    app.setStyle(QStyleFactory.create("plastique"))
    form = Application()
    form.show()
    #form.resize(400,600)
    app.exec_()


if __name__ == '__main__':
    main()
