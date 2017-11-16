'''
Created on Nov 16, 2017

@author: Mike
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class SpecTest(object):
    '''
    classdocs
    '''


    def __init__(self, parent=None, plot=None, testNum=None, name="",rbw=100e3,sweepTime=0.1,sweepNum=20,freqCenter=1e9,freqSpan=1e9,threshold=100):
        '''
        Constructor
        '''
        self.parent=parent
        self.plot=plot
        self.testNum=testNum
        self.rbw=rbw
        self.sweepTime=sweepTime
        self.sweepNum=sweepNum
        self.name=name
        self.sweepNum=sweepNum
        self.freqCenter=freqCenter
        self.freqSpan=freqSpan
        self.threshold=threshold
        self.PROG=0
        
    
    def runSweep(self):
#=======================================================================
#
#          Name:    runSweep    
#
#    Parameters:    reps
#
#        Return:    True if test is canceled else False
#
#   Description:    
#
#=======================================================================
        peak=[]
        peakFreq=[]
        
        for i in range(3):
            peak.append(-9999)
            peakFreq.append(0)
        
        try:
            self.parent.specan.sh.configureSweepCoupling(self.rbw,self.rbw,self.sweepTime,"native","no-spur-reject")
            
            self.parent.specan.sh.configureCenterSpan(self.freqCenter,self.freqSpan)
        except:
            print "specan setup error"  
              
        self.plot.cla()
        for testNo in range(0,self.sweepNum):
#             try:
                dataReturn=self.parent.specan.get_full_sweep()
            
                
                #get bin size in order to calculate frequencies
                traceInfo=self.parent.specan.sh.queryTraceInfo()
                binsize=traceInfo["arr-bin-size"]
                
                #calculate frequencies from trace info
    
                dataiter=0
                freqArray=[]
                limitArray=[]
                average=0
                
                startFreq=(self.freqCenter-self.freqSpan/2)
                endFreq=(self.freqCenter+self.freqSpan/2)
    
                self.plot.cla()
                self.plot.set_xlim([startFreq,endFreq])
    #             self.plot.set_title('Center: ' + str(freqCenter/1e6) + 'MHz    Span: ' + str(startFreq/1e6) + 'MHz ~ ' + str(endFreq/1e6) + 'MHz',fontsize=14,fontweight=200)
                self.plot.set_title('Center: ' + str(self.freqCenter/1e6) + 'MHz    Span: ' + str(startFreq/1e6) + 'MHz ~ ' + str(endFreq/1e6) + 'MHz    RBW: '+str((self.rbw/1000))+'KHz    SweepTime: '+str((self.sweepTime*1000))+'ms')
                self.plot.set_ylim([-150,-0])
                self.plot.set_xlabel("Frequency (Hz)")
                self.plot.set_ylabel("Power (dBm)")
                self.plot.grid(True)
                self.parent.fig.tight_layout()
                
                for i in dataReturn:
                    frequency=int(startFreq+(dataiter*binsize))
                    freqArray.append(frequency)
                    dataLen=len(dataReturn)
                    
                    
                    average=(((average*dataiter)+abs(i))/(dataiter+1))
                    
                    limitArray.append(self.threshold)
                    
                    if i>peak[0]:
                        peak[0]=i
                        peakFreq[0]=frequency
                        
                    if i>peak[1] and (peakFreq[1]<(peakFreq[0]-5000) or peakFreq[1]>(peakFreq[0]+5000)):
                        peak[1]=i
                        peakFreq[1]=frequency
                        
                        
#                     if i>peak[2] and peakFreq[2]<(peakFreq[0]+(dataLen/10)):
#                         peak[1]=i
#                         peakFreq[1]=frequency
                                
                    dataiter+=1
                
                
                 
                self.parent.progress.setValue(self.PROG)    
                self.plot.plot(freqArray,dataReturn,lw=.5, c='r')      
                self.plot.plot(freqArray,limitArray,lw=1, c='b') 
                
                self.plot.scatter(peakFreq,peak,marker='d',color='black',s=100)
    
                self.parent.canvas.draw()
                
                if self.parent.progress.wasCanceled():
                    return True
                    break
                
                self.PROG+=1
                self.parent.updateUi()
#             except:
#                 print "error getting specan sweep"
        
        #Save plot to temp file        
        plotImgName = 'temp_' + str(self.testNum) + '.png' 
        self.parent.plotImageList.append(plotImgName)
        
        self.parent.canvas.print_figure(plotImgName)  
        
        return False 