# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 15:00:39 2018

@author: cbjorkma
"""

#import matplotlib.pyplot as plt

class PMI():
    
    def __init__(self, path, origo):
        import math
        self.path = path
        self.filenames = []
        self.data = []
        self.names = []
        self.origo = origo
        self.samplingpoints2017 = [29.0,33.0,35.0,40.0,43.0,46.0,55.0,48.0,60.0,63.0,106.0,119.0,129.0,136.0,142.0,145.0,151.0,153.0,158.0,162.525,168.416]              
        self.samplingpoints2018 = [343.0,343.041668,343.0833,343.18,343.208315,344.35,346.5,351.86,357.2,385.37,392.38,399.13,413.0,423.0,427.2]
        self.xpos = [595, 1207, 1697 , 1992, 5351 , 5800,7096, 7743] #Positions of PMIs in machine
        self.cooldowns = [ 343.04166667,  344.25,  350.,  374.25 ,403.,  423]
        self.cooldownsText = ['1 hour' , '30h' , '1 week' , '1m + 30h ' , '2 months' , '80 days']
        self.smooth2018 = []
        self.extrapolations = []
        self.extrapolationsXes = []
        self.FlukaData = []
        self.FlukaSD = []
        self.diffratios = []
        self.targetdoseratepercooldown = []
        self.As = []
        self.generic = []
        self.genericError = []
        self.Volume = math.pi*8*8*21.5
        
    def read(self):     
        import os
        import datetime #, timedelta
        import pandas as pd        
        import numpy as np
        
        os.chdir(self.path)

        files = os.listdir(self.path)
        files = sorted(files)
        files = filter(lambda x: x[4:7].isdigit() , files)  
        files = filter(lambda x: not x[0] == '.' , files)  
        self.filenames = files

        if os.path.isfile('dataPMI.npy'):
            self.data = np.load('dataPMI.npy')
        else:

            thefile = pd.read_excel(files[0])
            
            dataPMI = np.zeros([len(thefile),2, len(files)])
            for j in range(len(files)):
                thefile = pd.read_excel(files[j])
                time = thefile.Timestamp
                for i in range(int(0*len(thefile)),len(thefile)):
                    instant = datetime.datetime( time[i].year, time[i].month, time[i].day, time[i].hour, time[i].minute, time[i].second)
    #                print instant
                    timedifference = instant - self.origo
                    amountOfSeconds = timedifference.total_seconds()/(60*60*24)
    #                print 'file ' + str(j) + '. Seconds ' + str(amountOfSeconds) + '. value ' + str(thefile.Value[i] )
                    dataPMI[i,0,j] = amountOfSeconds
                    dataPMI[i,1,j] = thefile.Value[i]   
    #        assert dataPMI[1200,1,2] != dataPMI[1200,1,3]
            np.save('dataPMI', dataPMI)
    #        print dataPMI
            self.data = dataPMI
    def readFluka(self, path, normfactor):
        import os        
        import numpy as np
        os.chdir(path)
        
        files = os.listdir(path)
        files = sorted(files)
        #files = filter(lambda x: x[9:-8].isdigit() , files)
        files = filter(lambda x: x[0:5] == 'Fluka' , files) 
        
        
        FlukaData = np.zeros([len(files),8])
        FlukaSD = np.zeros([len(files),8])
        row = 10
        row2 = 14
        indecies = [7,9, 11 ,13 , 15 ,17,19,21]
        for i in range(len(files)):
            thefile = open(files[i],'r')
            filecontent = thefile.readlines()
            line = filecontent[row].split(' ')
            line2 = filecontent[row2].split(' ')
            for j in range(len(indecies)):
                FlukaData[i,j] = line[indecies[j]]
                FlukaSD[i,j] =  line2[indecies[j]]
        
#        #Converts data to uSv/h
#        FlukaData = 0.0036*FlukaData
#        
#        #Normalization
#        normFactor = 1 / 0.1772837
#        FlukaData = normFactor * FlukaData
        
        #Volume compensation
        #Volume = math.pi*8*8*21.5
        self.normfactor = normfactor
        self.FlukaData = FlukaData * self.normfactor /self.Volume
        
        #Convert to %
        self.FlukaSD = FlukaSD/100
    
        
    
    def calc(self):       
        import numpy as np
        from scipy.interpolate import interp1d
        from scipy.optimize import curve_fit
        import matplotlib.pyplot as plt
        alldiffs = np.zeros([8,6])
        alldiffsInterpolated = np.zeros([8,6])
        
        fig = plt.figure()
        
#        yminimum = 10000000
        data = self.data
        sampleX = self.samplingpoints2018
        xes2017 = self.samplingpoints2017
        FlukaData =self.FlukaData
        FlukaSD = self.FlukaSD
        xes = self.cooldowns
        
        smooth = np.zeros([len(sampleX),data.shape[2]])
        
        minimum = 1000000
        finished = 0
        counter = 0
        while not finished:
            counter =+ 1
            for i in range(data.shape[2]):
                ax = plt.subplot(4,2,i +1 )
    
                #Interpolate 1
                x = data[0:,0,i]
                y = data[0:,1,i]
                f = interp1d(x, y)
                smooth[0:,i] =  f(sampleX)
                diffs = f(xes) - FlukaData[0:,i]
                alldiffs[i,0:] = diffs
                diffsRatios = f(xes) / FlukaData[0:,i]
                alldiffs[i,0:] = diffsRatios
            
                #Interpolation 2
                x = sampleX
                y = f(sampleX)    
                g = interp1d(x,y)
                
             
            #    diffsRatios = g(xes) / FlukaData[0:,i]
            #    alldiffsInterpolated[i,0:] = diffsRatios
                
             
                plt.plot(data[0:,0,i], data[0:,1,i], label = 'PMI data')
                plt.errorbar(xes,FlukaData[0:,i],yerr = FlukaData[0:,i]*FlukaSD[0:,i], color = 'r', label = 'Fluka',linestyle='None', fmt='o')
                
                plt.plot(sampleX , f(sampleX) , color = 'g' , label =  'Interpolation', marker = 'o')   
            #    plt.plot(data[0:,0,i], func(data[0:,0,i], *popt), 'r--', label = 'Fitted curve')
    #            plt.errorbar(xes,FlukaData[0:,i],FlukaData[0:,i]*FlukaSD[0:,i], linestyle='None', fmt='o', color = 'r', label = 'Fluka')
            
                Title = self.filenames[i][:-5]
                textstr = Title
                
                props = dict(boxstyle='round', facecolor='white', alpha=1)
                
            
                ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14, verticalalignment='top',bbox=props)     
                
                
                
            
            #    plt.title(Title, y = 0.85)
                
                
                
                
                plt.ylabel('uSv/h')
            
            #    ax.set_yscale("log", nonposy='clip')
    #            NoBeam = ionEnd - protonEnd
            #    plt.axvline(x= (NoBeam + timedifference).total_seconds()/(60*60*24) ,linestyle = '--', color = 'black', label = 'Ion run ends' )
            #    plt.axvline(x= protonEnd.total_seconds() ,linestyle = '--', color = 'red', label = 'Proton run ends' )
                plt.legend()
            #    
                ymin = 0
                ymax = 6000 #min(g(xes))
                xmin = -10
                xmax = 480
                
                
                plt.xlim(xmin,xmax)
                plt.ylim(ymin, ymax)
            
    #            extrapolations = []
            
            #    if i%2 == 0:
                if i == data.shape[2] -1:
                    plt.xlabel('Days since end of 2016 operations', x =  -0.1, y = -1.5) # 1.10
            
                
    
                def func(xes,a,k1,k2):
                    return a*np.exp(-k1*np.power(np.log(xes),k2))
                
                
                def extrapolate(xes,initialguess):
                    for i in range(100):
                       # print 'Attempt ' +  str(i +1 )
                        guess = initialguess
                #        for j in range(len(guess)):
                #            guess[j] = initialguess[j]*(2*(np.random.rand() -np.random.rand()) + 1)
                        guess[0] = guess[0] +100*(2*np.random.rand() -1)
                        guess[1] = guess[1] +0.0005*(2*np.random.rand() -1)
                        guess[2] = guess[2] +0.0005*(2*np.random.rand() -1)      
                        try:
                #            popt, pcov = fitting(xes, f(xes),guess)
                            popt , pcov = curve_fit(lambda x,a,k1,k2: a*np.exp(-k1*np.power(np.log(x),k2)),  xes,  f(xes), p0 = guess)
                            #print 'Success!'
                            #print [x/y for x, y in zip(guess, initialguess)]
                            break
                        except RuntimeError: 
                            #print 'Failed'
                            pass
                
                    return popt
        
                ax2 = ax.twinx()
                
                #print 'Attempting: ' + Title
                
                x = data[0:,0,i]
                y = data[0:,1,i]
                
                a = 1800 
                k1 = 0.00019*3.0
                k2 = 5.25*0.82
                #timedifference = end2017 - protonEnd
                #start = timedifference.total_seconds()/(60*60*24)
    #                start = 0
                initialguess = [a,k1 ,k2] 
                popt = extrapolate(xes2017,initialguess)
                #popt , pcov = curve_fit(lambda x,a,k1,k2,c: a*np.exp(-k1*np.power(np.log(x - start),k2)) +c,  xes2017,  f(xes2017), p0 = initialguess)
                plt.plot(x[0:], func(x[0:], *popt), 'k--', label = 'Baseline dose rate')    
                
                for j in range(len(xes2017)):
                    if j == 0:
                        plt.axvline(x= xes2017[j] ,linestyle = '--', color = 'k', linewidth = 0.3, label = 'Sampling points')
                    else:
                        plt.axvline(x= xes2017[j] ,linestyle = '--', color = 'k', linewidth = 0.3)
                
                plt.xlim(xmin,xmax)
                plt.ylim(ymin, ymax)    
            
                self.extrapolations.append(func(x[0:], *popt))
                self.extrapolationsXes.append(x[0:])
                if min(func(x[0:], *popt)) < minimum:
                    minimum = min(func(x[0:], *popt))
                
                #print i
                y = FlukaData[0:,i] + func(xes, *popt)
                plt.errorbar(xes,y,yerr = y*FlukaSD[0:,i], color = 'c', label = 'Fluka mean + baseline',linestyle='None', fmt='o')
            
                plt.legend()
            
                diffsRatios = g(xes) / y
                alldiffsInterpolated[i,0:] = diffsRatios
                
                if not minimum < 1:
                    finished = 1
                    print 'Extrapolation succeful!'
                else:
                    print 'Extrapolation attempt: ' + str(counter + 2)
                    plt.clf()
          
        
                #Very strange choice of name for variable
#                alldiffsInterpolated[i,0:] = diffsRatios 
        #    plt.legend(loc = 3)
           # plt.xlabel('Days since end of 2016 operations')
        plt.suptitle('Dose rate evolution per PMI unit', fontsize = 22)        
        plt.show()        
        self.smooth2018 = smooth
        self.diffratios = alldiffsInterpolated
      #  self.extrapolations = extrapolations
        
      
        targetdoseratepercooldown = []
        for i in range(len(self.cooldowns)):
            cooldown = self.cooldowns[i]
            doseratesperposition = np.zeros(len(self.extrapolations))
            for j in range(len(self.extrapolations)):
                x = self.extrapolationsXes[j]
                y = self.extrapolations[j]
                f = interp1d(x,y)
                doseratesperposition[j] = f(cooldown)
            targetdoseratepercooldown.append(doseratesperposition)
        self.targetdoseratepercooldown = targetdoseratepercooldown
    
    def readGeneric(self, filename, path):
        import os
        os.chdir(path)
        thefile = open(filename,'r')
        cont = thefile.readlines()
        #self.generic =  [float(i) for i in cont[10].split()]
        self.generic =  np.array(cont[10].split()).astype(np.float) * self.normfactor /self.Volume
        self.genericError =  np.array(cont[14].split()).astype(np.float) /100
       
    def predictAmplitudes(self,first):
        #from scipy.optimize import minimize , rosen
        #pmi.targetdoseratepercooldown[0][4:]
        #pmi.FlukaData[0,4:]
        steps = 10000
        lbound = 0.0001
        hbound = 3
        
        Avec = []
        for i in range(len(self.FlukaData[0:,0])):
            data1 = self.targetdoseratepercooldown[i][first:]
            data2 = self.FlukaData[i,first:]
            
    
            As = np.zeros(steps)
            sums = np.zeros(steps)
            
            for i in range(steps):
                A = np.arange(lbound,hbound,(hbound - lbound)/steps)[i]
                sums[i] = sum(abs(data1 -A*data2))
                As[i] = A
                
            #print min(sums)
            idx = np.argmin(sums)
            Avec.append(As[idx])
    
        self.As = Avec
        print 'Amplitudes predicted'

    def predictAmplitudes2(self):
        #from scipy.optimize import minimize , rosen
        #pmi.targetdoseratepercooldown[0][4:]
        #pmi.FlukaData[0,4:]
        steps = 50000
        lbound = 0.1
        hbound = 9
        
        Avec = []
        for i in range(len(self.FlukaData[0:,0])):
            data1 = self.targetdoseratepercooldown[i][0:]
            data2 = self.generic[0:]
#            print i
#            print data1
#            print data2
    
            As = np.zeros(steps)
            sums = np.zeros(steps)
            
            for j in range(steps):
                A = np.arange(lbound,hbound,(hbound - lbound)/float(steps))[j]
                sums[j] = sum(abs(data1 -A*data2))
                As[j] = A
                
            #print min(sums)
            idx = np.argmin(sums)
            Avec.append(As[idx])
    
        self.As = Avec
        assert not all(x==self.As[0] for x in self.As)
        
        print 'Amplitudes predicted'



#import datetime
#import numpy as np
#import math
#
#
#
#protonEnd = datetime.datetime(2017,10,23,06,00,00)
#ionEnd = datetime.datetime(2017,12,18,06,00,00)
#end2016 = datetime.datetime(2015,11,16,06,00,00)
#end2017 = datetime.datetime(2016,11,14,06,00,00)
#manualMeasurement = datetime.datetime(2017,10,24,12,00,00)
#
#
#
#
#path = '//cern.ch/dfs/Users/c/cbjorkma/Documents/LSS 2/ActivationDetectors'
#
#x = PMI(path, end2017)
#
#assert x.path == path
#
#assert x.origo == end2017
#
#
##x.read()
##x.readFluka('//cern.ch/dfs/Users/c/cbjorkma/Documents/LSS 2/ActivationDetectors/NoLongProfile1')
##
#
##assert x.FlukaData.shape == (6L, 8L)
##



#x.calc()
#
#
#print len(x.extrapolations)















