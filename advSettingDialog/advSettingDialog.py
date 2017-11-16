'''
Created on Nov 10, 2017

@author: Mike
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class advSettingsDialog(QDialog):
    '''
    dialog class to setup signalhound bb60c
    '''


    def __init__(self, parent=None):

        super(advSettingsDialog,self).__init__(parent)   
        self.parent=parent
        "Initialze spectrum analyzer setting dialog box"
        self.setWindowTitle("Advanced Settings")
        self.vert = QVBoxLayout() 
        
        #=======================================================================
        # setup buttons
        #=======================================================================
        self.b_box = QDialogButtonBox(QDialogButtonBox.Ok  | QDialogButtonBox.Cancel)
            
        #set button behavior
        self.connect(self.b_box, SIGNAL('rejected()'),self.click_cancel)    #behavior when "cancel" is clicked
        self.connect(self.b_box, SIGNAL('accepted()'),self.click_ok)        #behavior when "ok" is clicked
        
        #=======================================================================
        # setup table
        #=======================================================================
        self.table=QTableWidget()
        
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels(QString("Test Num;Name;Center Frequency(MHz);Frequency Span(MHz);Start Freq(MHz);End Freq(MHz);RBW(kHz);Sweep Time(ms);Sweep Count;Threshold(dBm)").split(";"))
        
        

       
        

        
        self.vert.addWidget(self.table)
        self.vert.addWidget(self.b_box)
        self.setLayout(self.vert)
        
        
    def click_ok(self):
        pass
    def click_cancel(self):
        self.close()
        
   