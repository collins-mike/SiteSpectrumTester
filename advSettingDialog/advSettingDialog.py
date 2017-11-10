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
        
        self.vert = QVBoxLayout()
        #setup item specific Gui layout of Dialog box
        self.form=QFormLayout()   
        
        self.b_box = QDialogButtonBox(QDialogButtonBox.Ok  | QDialogButtonBox.Cancel)
            
        #set button behavior
        self.connect(self.b_box, SIGNAL('rejected()'),self.click_cancel)    #behavior when "cancel" is clicked
        self.connect(self.b_box, SIGNAL('accepted()'),self.click_ok)        #behavior when "ok" is clicked
        
        "Initialze spectrum analyzer setting dialog box"
        self.setWindowTitle("Advanced Settings")
        fbox = QFormLayout()

        fbox.addRow(QLabel('<span style=" font-size:10pt; font-weight:600;">SignalHound BB60C\nSpectrum Analyzer</span>'))#add heading
        #RBW
        self.lnEd_rbw  =QLineEdit('10')
        fbox.addRow(QLabel("RBW (kHz)"),self.lnEd_rbw)
        #VBW
        self.lnEd_vbw  =QLineEdit('10')
        fbox.addRow(QLabel("VBW (kHz)"),self.lnEd_vbw)
        
        #Gain MAX=3 TODO: add automatic value correction
        hbox=QHBoxLayout()#create child hbox
        self.cb_autoGain = QCheckBox("Auto",checked=True)
        self.connect(self.cb_autoGain, SIGNAL('stateChanged(int)'), self.set_specan_AutoGain)
        self.cb_autoGain.setToolTip("Set Automatic Gain Control")
        
        self.e_cal_gain=QLineEdit("0")
        self.e_cal_gain.setEnabled(False)
        
        hbox.addWidget(QLabel('Gain: Auto or 0-3'))
        hbox.addWidget(self.cb_autoGain)
        hbox.addWidget(self.e_cal_gain)
        fbox.addRow(hbox)
        
        #Attenuation MAX=30 TODO: add automatic value correction
        hbox=QHBoxLayout()#create child hbox
        self.cb_autoAtten = QCheckBox("Auto",checked=True)
        self.connect(self.cb_autoAtten, SIGNAL('stateChanged(int)'), self.set_specan_autoAttenuation)
        self.cb_autoAtten.setToolTip("Set Automatic Attenuation Control")
        
        self.cb_cal_attenRef=QComboBox()
        self.cb_cal_attenRef.addItem('0')
        self.cb_cal_attenRef.addItem('10')
        self.cb_cal_attenRef.addItem('20')
        self.cb_cal_attenRef.addItem('30')
        self.cb_cal_attenRef.currentIndexChanged.connect(self.set_specan_autoAttenReference)
        
        self.cb_cal_attenRef.setEnabled(True)
        
        self.e_cal_atten=QLineEdit("30")
        self.e_cal_atten.setEnabled(False)
        
        hbox.addWidget(QLabel('Attenuation:'))
        hbox.addWidget(self.cb_autoAtten)
        hbox.addWidget(QLabel('Reference (dB)'))
        hbox.addWidget(self.cb_cal_attenRef)
        hbox.addWidget(QLabel('Manual (dB)'))
        hbox.addWidget(self.e_cal_atten)
        fbox.addRow(hbox)
        
        #Aquisition Detector type and scale
        hbox=QHBoxLayout()#create child hbox

        self.cb_cal_aqDet=QComboBox()
        self.cb_cal_aqDet.addItem('average')
        self.cb_cal_aqDet.addItem('min-max')
        self.cb_cal_aqDet.currentIndexChanged.connect(self.set_specan_detectorType)
        
        self.cb_cal_aqScale=QComboBox()
        self.cb_cal_aqScale.addItem('log-scale')
        self.cb_cal_aqScale.addItem('log-full-scale')
        self.cb_cal_aqScale.addItem('lin-scale')
        self.cb_cal_aqScale.addItem('lin-full-scale')
        self.cb_cal_aqScale.currentIndexChanged.connect(self.set_specan_detectorScale)
        
        
        hbox.addWidget(QLabel('Acquisition:'))
        hbox.addWidget(QLabel('Detector Type'))
        hbox.addWidget(self.cb_cal_aqDet)
        hbox.addWidget(QLabel('Scale'))
        hbox.addWidget(self.cb_cal_aqScale)
        fbox.addRow(hbox)
        
        
        self.vert.addLayout(fbox)
        self.vert.addLayout(self.form)
        self.vert.addWidget(self.b_box)
        self.setLayout(self.vert)
        
        
    def click_ok(self):
        self.apply_specanSettings()
        
    def click_cancel(self):
        self.close()
        
    def set_specan_AutoGain(self):#toggle auto-gain settings
        #=======================================================================
        #
        #          Name:    set_specan_AutoGain
        #
        #    Parameters:    None
        #
        #        Return:    None
        #
        #   Description:    this function sets the specan Gain from Auto to manual
        #                    
        #                    NOTE: this only changes Calibrator values NOT specan Values
        #
        #=======================================================================
        'toggle auto attenuation setting'
        
        if self.dia_specAn.cb_autoGain.isChecked():
            print "Gain set to AUTO"
            self.cal_gain='auto'
            self.e_cal_gain.setEnabled(False)
        else:
            print "Gain set to ManuaL"
            self.e_cal_gain.setEnabled(True)
            
    def set_specan_autoAttenuation(self):#toggle auto-gain settings
        #=======================================================================
        #
        #          Name:    set_specan_autoAttenuation
        #
        #    Parameters:    None
        #
        #        Return:    None
        #
        #   Description:    sets specan attenuation to auto or manual
        #
        #                    NOTE: this only changes Calibrator values NOT specan Values
        #                    
        #=======================================================================
        'Toggle Auto-Attenuation setting'
        if self.dia_specAn.cb_autoAtten.isChecked():
            print "Attenuation set to Auto"
            self.cal_level_atten='auto'
            self.e_cal_atten.setEnabled(False)
            self.cb_cal_attenRef.setEnabled(True)
        else:
            print "Attenuation set to Manual"
            self.e_cal_atten.setEnabled(True)
            self.cb_cal_attenRef.setEnabled(False)
            
    def set_specan_autoAttenReference(self):#set reference for auto attenuation
        #=======================================================================
        #
        #          Name:    set_specan_autoAttenReference
        #
        #    Parameters:    None
        #
        #        Return:    None
        #
        #   Description:    this functions sets the auto attenuation reference value
        #
        #                    NOTE: this only set the Calibrator values not the specan values
        #
        #=======================================================================
        'set reference value for auto attenuation'
        
        self.cal_level_ref=int(self.cb_cal_attenRef.currentText())
        print "Attenuation reference set to " + str(self.cal_level_ref)
        
    def set_specan_detectorType(self):#set detector type for acquisition
        #=======================================================================
        #
        #          Name:    set_specan_detectorType
        #
        #    Parameters:    None
        #
        #        Return:    None
        #
        #   Description:    this function sets the specan detector type
        #
        #                    NOTE: this only sets the Calibrator values not the Specan values
        #
        #=======================================================================
        'set spectrum analyzer detector type'
        self.cal_aq_detector=self.cb_cal_aqDet.currentText()
        print "Aquisition detector type set to " + str(self.cal_aq_detector)
  
    def set_specan_detectorScale(self):#set detector type for acquisition
        #=======================================================================
        #
        #          Name:    set_specan_detectorScale
        #
        #    Parameters:    None
        #
        #        Return:    None
        #
        #   Description:    this function sets the detector scaling
        #
        #                    NOTE this Only set the Calibrator Values Not the Specan Values
        #
        #=======================================================================
        'set acquisition scaling in spectrum analyzer'
        
        self.cal_aq_scale=self.cb_cal_aqScale.currentText()
        print "Aquisition scale set to " + str(self.cal_aq_scale)
        
    def apply_specanSettings(self):# apply calibration settings
        #=======================================================================
        #
        #          Name:    apply_specanSettings
        #
        #    Parameters:    None
        #
        #        Return:    None
        #
        #   Description:    this function applies all of the specan settings based on user inputs
        #
        #                    NOTE: this only applies to SIGNAL HOUND BB60c
        #
        #=======================================================================
        'apply calibration settings to specturm alalyzer'
        
        #TODO: add automatic parameter correction in case of user error
        try:
            #===================================================================
            # signalhound specan
            #===================================================================
            if(self.parent.specan.get_SpectrumAnalyzerType()=="SH"):
                
                #gain
                if self.cb_autoGain.isChecked():
                    self.cal_gain='auto'
                else:
                    #if user sets gain >3 it will be automatically corrected to 3
                    if float(self.e_cal_gain.text())>3:
                        self.e_cal_gain=3
                        self.cal_gain=3
                    else:
                        self.cal_gain=int(self.e_cal_gain.text())
                try:        
                    self.parent.specan.sh.configureGain(self.cal_gain)#set gain in specan
                except: print "could not configure specan gain" 
                
                # set attenuation
                if self.cb_autoAtten.isChecked():
                    self.cal_level_atten="auto"
                else:
                    self.cal_level_atten=float(self.e_cal_atten.text())
                try:    
                    self.parent.specan.sh.configureLevel(self.cal_level_ref , self.cal_level_atten)#set attenuation in specan
                except: print "could not configure specan attenuation"
                
                #log or linear units
                try:
                    self.parent.specan.sh.configureProcUnits("log")
                except: "could not configure specan proc units"
                    
                #data units
                try:
                    self.parent.specan.sh.configureAcquisition(str(self.cal_aq_detector),str(self.cal_aq_scale))
                except: print "could not configure specan acquisition"
                
                #rbw
                self.cal_sc_rbw=float(self.lnEd_rbw.text())*1000
                self.cal_sc_vbw=float(self.lnEd_vbw.text())*1000
                
                self.sh.configureSweepCoupling(self.cal_sc_rbw,self.cal_sc_vbw,self.cal_sc_sweepTime,"native","no-spur-reject")
                
                #sweeptime, RBW, VBW
                try:
                    self.parent.specan.set_sweeptime(self.cal_sc_sweepTime)
                except: "could not set specan sweeptime"
                
                #setup center frequency and span of test sweep
                try:
                    self.parent.specan.set_frequency(self.cal_freq,self.cal_span)
                except: print "cold not set specan frequency"
                

        except:
            print "\n\n\tcould not Configure Specan"