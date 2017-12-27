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
        self.freqCenter=freqCenter
        self.freqSpan=freqSpan
        self.threshold=threshold
        self.dataReturn=[]
        self.datahold=[]
        self.freqArray=[]
        self.peakArray=[]
        self.peakFreqArray=[]
        self.title=""
        self.dataMax=-20
        self.dataMin=-100
    
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
        #clear arrays for plotting
        self.peakArray[:]=[]
        self.peakFreqArray[:]=[]
        self.datahold[:]=[]
        self.dataMax=self.threshold+20
        self.dataMin=self.threshold-20
        #setup spectrum analyzer
        try:
            self.parent.specan.sh.configureSweepCoupling(self.rbw,self.rbw,self.sweepTime,"native","no-spur-reject")
            
            self.parent.specan.sh.configureCenterSpan(self.freqCenter,self.freqSpan)
        except:
            print "specan setup error"  
        
        #clear plot      
        self.plot.cla()
        
        #run 
        for testNo in range(0,self.sweepNum):
            #get sweep from spectrum analyzer
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
            self.freqArray[:]=[]
            limitArray=[]
            self.peakArray[:]=[]
            self.peakFreqArray[:]=[]
            
            startFreq=(self.freqCenter-self.freqSpan/2)
            endFreq=(self.freqCenter+self.freqSpan/2)

            #clear/setup plot
            self.plot.cla()
            self.plot.set_xlim([startFreq,endFreq])
        
            
                
                
            self.plot.set_xlabel("Frequency (MHz)")
            self.plot.set_ylabel("Power (dBm)")
            self.plot.grid(True)
            self.plot.minorticks_on()
            self.plot.grid(which='minor', linestyle=':', linewidth='0.5', color='grey',zorder=0)
            self.plot.grid(which='major', linestyle='-', linewidth='0.7', color='#606060',zorder=0)
        
            #build arrays for plotting
            for i in self.dataReturn:
                frequency=int(startFreq+(dataiter*binsize))
                
                self.freqArray.append(frequency)
                
                dataLen=len(self.dataReturn)
                
                if dataiter+1>len(self.datahold):
                    self.datahold.append(i)
                    
                elif i>self.datahold[dataiter]:
                    self.datahold[dataiter]=i;
                
                limitArray.append(self.threshold)

                dataiter+=1
            
            
            if max(self.datahold)>self.dataMax:
                self.dataMax=max(self.datahold)+20
            if min(self.datahold)<self.dataMin:
                self.dataMin=min(self.datahold)-20

            self.plot.set_ylim([self.dataMin,self.dataMax])
            
            #===================================================================
            # plot progress
            #===================================================================
            
            #get peaks
            indexes = detect_peaks(self.datahold, mph=self.threshold-2, mpd=round(dataLen/15), threshold=0, edge='rising')
            for i in indexes:
                self.peakFreqArray.append(self.freqArray[i])
                self.peakArray.append(self.datahold[i])
            
            #update progress bar
            self.parent.progress.setValue(self.parent.PROG)     

            #plot data, limit and peaks
            self.plot.plot(self.freqArray,self.datahold,lw=.5, c='b',zorder=2,label="Power (dBm)")      
            self.plot.plot(self.freqArray,limitArray,lw=1.5, c='r',zorder=1,label="Limit Threshold ("+str(self.threshold)+"dBm)") 
            
            self.plot.scatter(self.peakFreqArray,self.peakArray,marker='d',color='black',s=20,zorder=3,label="Peaks (MHz)")
            i=0
            
            #create peak info
            for p in self.peakFreqArray:
                self.plot.annotate(str((int(p/1e6)))+"MHz\n"+str(format(self.peakArray[i],'.2f'))+"(dBm)", (p-100,self.peakArray[i]+1), fontsize=7, weight="bold", horizontalalignment='center', color="black")
                
                i+=1
            #create legend
            leg=self.plot.legend(bbox_to_anchor=(1, 0.2), loc=1, borderaxespad=0.)
#             frm=leg.get_frame()
#             frm.set_facecolor("black")
#             frm.set_edgecolor("white")
            
            #set plot title and info
            self.title=str(self.name)+'\nCenter: ' + str(self.freqCenter/1e6) + 'MHz    Span: ' + str(startFreq/1e6) + 'MHz ~ ' + str(endFreq/1e6) + 'MHz    RBW: '+str((self.rbw/1e6))+'MHz    SweepTime: '+str((self.sweepTime*1000))+'ms'
            
            self.plot.set_title(self.title,fontsize=12)
            
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
    
    
    
    
    