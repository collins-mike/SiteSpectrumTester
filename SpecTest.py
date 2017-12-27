'''
Created on Nov 16, 2017

@author: Mike
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy
# import peakutils
# from peakutils.plot import plot as pplot
from matplotlib import pyplot
from detect_peaks import detect_peaks

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
        self.dataReturn=[]
        self.datahold=[]
        self.freqArray=[]
        
    
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
#         self.dataReturn[:]=[]
        self.datahold[:]=[]

        try:
            self.parent.specan.sh.configureSweepCoupling(self.rbw,self.rbw,self.sweepTime,"native","no-spur-reject")
            
            self.parent.specan.sh.configureCenterSpan(self.freqCenter,self.freqSpan)
        except:
            print "specan setup error"  
              
        self.plot.cla()
        for testNo in range(0,self.sweepNum):
            try:
                self.dataReturn=self.parent.specan.get_full_sweep()
            except:
                print "error getting specan sweep"
            self.parent.progress.setLabel(QLabel("\n Running Test: "+self.name+"    (Sweep "+str(testNo)+"/"+str(self.sweepNum)+")"))
            
            #get bin size in order to calculate frequencies
            traceInfo=self.parent.specan.sh.queryTraceInfo()
            binsize=traceInfo["arr-bin-size"]
            
            #calculate frequencies from trace info

            dataiter=0
            self.freqArray=[]
            limitArray=[]
            peak[:]=[]
            peakFreq[:]=[]
            avArray=[]
            average=0
            
            startFreq=(self.freqCenter-self.freqSpan/2)
            endFreq=(self.freqCenter+self.freqSpan/2)

            self.plot.cla()
            self.plot.set_xlim([startFreq,endFreq])
        
            self.plot.set_ylim([-150,-0])
            self.plot.set_xlabel("Frequency (MHz)")
            self.plot.set_ylabel("Power (dBm)")
            self.plot.grid(True)
            self.plot.minorticks_on()
#             self.plot.set_facecolor("#white")
            self.plot.grid(which='minor', linestyle=':', linewidth='0.5', color='grey',zorder=0)
            self.plot.grid(which='major', linestyle='-', linewidth='0.7', color='#606060',zorder=0)
        
            for i in self.dataReturn:
                frequency=int(startFreq+(dataiter*binsize))
                self.freqArray.append(frequency)
                dataLen=len(self.dataReturn)
                if dataiter+1>len(self.datahold):
                    self.datahold.append(i)
                elif i>self.datahold[dataiter]:
                    self.datahold[dataiter]=i;
                
                #===============================================================
                # average
                #===============================================================
                average=(((average*dataiter)+i)/(dataiter+1))
                
                limitArray.append(self.threshold)
                avArray.append(average)
                

                dataiter+=1
                
            
            #===================================================================
            # plot progress
            #===================================================================
            
            indexes = detect_peaks(self.datahold, mph=self.threshold-2, mpd=round(dataLen/15), threshold=0, edge='rising')
            for i in indexes:
                print 1
                peakFreq.append(self.freqArray[i])
                peak.append(self.datahold[i])
            
            
            self.parent.progress.setValue(self.parent.PROG)    
#             self.plot.plot(freqArray,self.dataReturn,lw=.5, c='#78dee8',zorder=2,label="Field Strength")      
#             self.plot.plot(freqArray,limitArray,lw=1, c='#e87878',zorder=1,label="Limit Threshold") 
            self.plot.plot(self.freqArray,self.datahold,lw=.5, c='b',zorder=2,label="Power (dBm)")      
            self.plot.plot(self.freqArray,limitArray,lw=1.5, c='r',zorder=1,label="Limit Threshold ("+str(self.threshold)+"dBm)") 
            
#             self.plot.plot(self.freqArray,avArray,lw=1, c='#0f0f0f') 
#             self.plot.scatter(peakFreq,peak,marker='d',color='#85d37c',s=20,zorder=3,label="Peaks")
            self.plot.scatter(peakFreq,peak,marker='d',color='black',s=20,zorder=3,label="Peaks (MHz)")
            i=0
            for p in peakFreq:
#                 self.plot.annotate(str((int(p/1e6)))+"MHz", (p-100,peak[i]+5), fontsize=9, horizontalalignment='center', color="#85d37c")
                self.plot.annotate(str((int(p/1e6)))+"MHz\n"+str(format(peak[i],'.2f'))+"(dBm)", (p-100,peak[i]+5), fontsize=7, weight="bold", horizontalalignment='center', color="black")
                
                i+=1
            leg=self.plot.legend(bbox_to_anchor=(1, 0.2), loc=1, borderaxespad=0.)
            frm=leg.get_frame()
#             frm.set_facecolor("black")
#             frm.set_edgecolor("white")
            
            self.plot.set_title(str(self.name)+'\nCenter: ' + str(self.freqCenter/1e6) + 'MHz    Span: ' + str(startFreq/1e6) + 'MHz ~ ' + str(endFreq/1e6) + 'MHz    RBW: '+str((self.rbw/1e6))+'MHz    SweepTime: '+str((self.sweepTime*1000))+'ms',fontsize=12)
            
            ticks = self.plot.get_xticks()/10e5
            self.plot.set_xticklabels(ticks)
            self.parent.fig.tight_layout()
            
            self.parent.canvas.draw()
            
            

            self.parent.PROG+=1    
            self.parent.updateUi()
            if self.parent.progress.wasCanceled():
                return True
                break
            
        #Save plot to temp file        
        plotImgName = 'temp_' + str(self.testNum) + '.png' 
        self.parent.plotImageList.append(plotImgName)
        
        self.parent.canvas.print_figure(plotImgName)  
        
        return False 
    
    
    
    
    