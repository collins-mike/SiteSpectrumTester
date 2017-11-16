'''
Created on Nov 10, 2017

@author: Mike
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from SpecTest import SpecTest

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
        self.resize(1000,400)
        #=======================================================================
        # setup buttons
        #=======================================================================
        self.b_box = QDialogButtonBox(QDialogButtonBox.Ok  | QDialogButtonBox.Cancel)
            
        #set button behavior
        self.connect(self.b_box, SIGNAL('rejected()'),self.click_cancel)    #behavior when "cancel" is clicked
        self.connect(self.b_box, SIGNAL('accepted()'),self.click_ok)        #behavior when "ok" is clicked
        
        self.btn_add=QPushButton("Add")
        self.connect(self.btn_add, SIGNAL('clicked()'), self.click_add)
        
        self.btn_remove=QPushButton("Remove")
        self.connect(self.btn_add, SIGNAL('clicked()'), self.click_remove)
        
        #=======================================================================
        # setup table
        #=======================================================================
        self.table=QTableWidget()
        
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(QString("Name;Center Frequency(MHz);Frequency Span(MHz);Start Freq(MHz);End Freq(MHz);RBW(kHz);Sweep Time(ms);Sweep Count;Threshold(dBm)").split(";"))
        self.table.setRowCount(0)
        header = self.table.horizontalHeader()
        header.setResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
        
        self.disableTableModification=True
        
        self.table.currentItemChanged.connect(self.setTableValues) 

       
        

        self.vert.addWidget(self.btn_add)
        self.vert.addWidget(self.table)
        
        self.vert.addWidget(self.b_box)
        self.setLayout(self.vert)
        
        
    def click_ok(self):
        self.setTableValues()
            
            
        self.close()
        
    def click_cancel(self):
        self.close()
    
    def click_add(self):
        self.parent.testList.append(SpecTest(parent=self.parent, plot=self.parent.plot, testNum=len(self.parent.testList)-1, name="New Test",rbw=100,sweepTime=0.01,sweepNum=20,freqCenter=1e9,freqSpan=1e9,threshold=-50))
        self.updateTable()
        
    def click_remove(self):
        pass
        
        
    def changeItem(self):
        if self.disableTableModification:
            pass
        else:
            self.setTableValues()
    
    def setTableValues(self):
        
        if self.disableTableModification:
            pass
        else:
            for i in range(len(self.parent.testList)):
                self.parent.testList[i].name=str(self.table.item(i,0).text())
                self.parent.testList[i].freqCenter=int(float(self.table.item(i,1).text()))*1e6
                center=self.parent.testList[i]
                self.parent.testList[i].freqSpan=int(float(self.table.item(i,2).text()))*1e6
                span=self.parent.testList[i]
                self.parent.testList[i].rbw=int(float(self.table.item(i,5).text()))*1e3
                self.parent.testList[i].sweepTime=float(self.table.item(i,6).text())/1e3
                self.parent.testList[i].sweepNum=int(float(self.table.item(i,7).text()))
                self.parent.testList[i].threshold=int(float(self.table.item(i,8).text()))
                
                
                
                
            self.updateTable()
            
    def updateTable(self):
        rows=len(self.parent.testList)
        self.table.setRowCount(rows)
        
        for i in range(rows):
            self.parent.testList[1]
            self.table.setItem(i,0,QTableWidgetItem(str(self.parent.testList[i].name)))
            center=self.parent.testList[i].freqCenter
            self.table.setItem(i,1,QTableWidgetItem(str(center/1e6)))
            span=self.parent.testList[i].freqSpan
            self.table.setItem(i,2,QTableWidgetItem(str(span/1e6)))
            
            start=int(center-span/2)
            item=QTableWidgetItem(str(start/1e6))
            item.setFlags( ~(Qt.ItemIsSelectable |  Qt.ItemIsEnabled) )
            self.table.setItem(i,3,item)
            
            end=int(center+span/2)
            item=QTableWidgetItem(str(end/1e6))
            item.setFlags( ~(Qt.ItemIsSelectable |  Qt.ItemIsEnabled) )
            self.table.setItem(i,4,item)
            
            
            self.table.setItem(i,5,QTableWidgetItem(str(self.parent.testList[i].rbw/1e3)))
            self.table.setItem(i,6,QTableWidgetItem(str(self.parent.testList[i].sweepTime*1e3)))
            self.table.setItem(i,7,QTableWidgetItem(str(self.parent.testList[i].sweepNum)))
            self.table.setItem(i,8,QTableWidgetItem(str(self.parent.testList[i].threshold)))
   
   
   
   
   
   
   
   
#EOF