# -*- coding: utf-8 -*-
"""
Script developed to create an interface for modelling of irradiation profiles and 
to calculate the irradiation profiles of the LHC experiments

By Daniel Björkman 2018 - 2019
daniel.bjorkman@cern.ch


"""



import os
import numpy as np


def calcTimeline(experiment):

    lastidx = len(experiment)-3
    
    experiment[len(experiment)-2,2] = - experiment[len(experiment)-2,0]
    for i in range(lastidx,-1,-1):
        
        experiment[i,2] = -experiment[i,0] - abs(experiment[i+1,2])
    return experiment;
 
        

def readProfile(filename):
    
    #Column 1 = Time [days]
    #Column 2 = Beam intensity [particles/s] or [collisions/s]
    #Column 3 = to be filled as inverse time by function calcTimeline
    
    data = np.loadtxt(filename)
    
    ATLAS = np.zeros([data.shape[0]+2,3])
    
    ATLAS[1:len(ATLAS)-1,0:2] = data
    
    ATLAS[0:,0] = ATLAS[0:,0]/(60*60*24)

    ATLAS = calcTimeline(ATLAS)

    return ATLAS







def readLumi(filename,origo):
    import pandas as pd

    data = pd.read_csv(filename)

    lumi = np.zeros([len(data),2])
        

    for i in range(len(data)):
        
        time = data['Date Time']

        instant = datetime.datetime( int(time[i].split('-')[0].strip()), int(time[i].split('-')[1].strip()), int(time[i].split('-')[2][0:2]), int(time[i].split('-')[2].split()[1][0:2]), int(time[i].split('-')[2].split()[1].split(':')[1]), int(time[i].split('-')[2].split()[1].split(':')[2][0:2]))

        timedifference = instant - origo
        timeindays = timedifference.total_seconds()/(60*60*24)
        lumi[i,0] = timeindays
        global experiment
        lumi[i,1] = data[experiment][i]
        

    return lumi




def sinceOrigo(instant):
    return (instant -origo).total_seconds()/(60*60*24)




def setMagnitude(lumi):
    
    ATLAS = np.zeros([1,3])
    
    
    from scipy.interpolate import interp1d
    x = lumi[0:,0]
    y = lumi[0:,1]
    lumiprofile = interp1d(x,y)
    
    def calcCollisions(ATLAS,tau2, tau1, xsec):
        timediff = (tau2 - tau1).total_seconds() 
        lumidiff = lumiprofile(sinceOrigo(tau2)) - lumiprofile(sinceOrigo(tau1)) #picobarn
        collisions = 1e12*lumidiff*xsec
        newrow = [timediff/(60*60*24),collisions/timediff,0]
        ATLAS = np.vstack([ATLAS,newrow])
        ATLAS = np.vstack([ATLAS,[0,0,0]])
        return ATLAS;
        

    
    #2011
    xsec = 72E-3 #mbarn
    ATLAS = calcCollisions(ATLAS,end2011,start2011, xsec)
   
    
    #2012
    xsec = 75E-3 #mbarn
    ATLAS = calcCollisions(ATLAS,end2012,start2012, xsec)
  

    xsec = 80E-3 #mbarn
    
    #2015
    ATLAS = calcCollisions(ATLAS,end2015,start2015, xsec)

    
    #2016
    ATLAS = calcCollisions(ATLAS,end2016,start2016, xsec)

    
    #2017
    ATLAS = calcCollisions(ATLAS,end2017,start2017, xsec)
 
    
    #2018, divided in T1, T2,T3 and T4
    
    #T1
    ATLAS = calcCollisions(ATLAS,T1end,T1start, xsec)


    #T2
    ATLAS = calcCollisions(ATLAS,T2end,T2start, xsec)    

    
    #T3
    ATLAS = calcCollisions(ATLAS,T3end,T3start, xsec)    

    
    #T4
    global T4end
    global T4start
    ATLAS = calcCollisions(ATLAS,T4end,T4start, xsec)    

    
    global experiment
    if experiment == 'ALICE':
    
        #Ion run
        xsec = 8. #barn
        protonIonFactor = 500/float(6)
        
        
        timediff = (ionEnd- ionStart).total_seconds() 
        lumidiff = 1E9 #barn 
        collisions = lumidiff*xsec
        newrow = [timediff/(60*60*24),protonIonFactor*collisions/timediff,0]
        ATLAS = np.vstack([ATLAS,newrow])
        ATLAS = np.vstack([ATLAS,[0,0,0]])
    
    return ATLAS;





def calcTimingNewprofile(dates,experimentMagnitudes, origo):
    experiment = np.zeros(experimentMagnitudes.shape)
    experiment[0:,1] = experimentMagnitudes[0:,1]    
    for i in range(len(experiment)-2,0,-1):
        if experiment[i,1] == 0:
            instance = dates.pop(0)
            timediff = (origo - instance).total_seconds() - sum(experiment[i:,0])
            experiment[i,0] = timediff
            
        else:
            
            experiment[i,0] = (60*60*24)*experimentMagnitudes[i,0]
    
    experiment[0:,0] = experiment[0:,0]/(60*60*24)
    
    experiment = calcTimeline(experiment)
    return experiment



def numberCollisions(experiment):
    return sum(experiment[0:,1]*experiment[0:,0])*24*60*60




def plot(*args):
    
    prev = args[0]
    new = args[1]
    origo = args[2]
    title = args[3]
    
    
    
    
    import matplotlib.pyplot as plt
    
    newyear2018 = datetime.datetime(2018,12,31,23,59,59)
    timedifference = origo - newyear2018
    newyearsOrigodifference = timedifference.total_seconds()/(60*60*24)
    
    
    
    
    fig = plt.figure()
    
    
    ax = fig.add_subplot(111)
    
    
    try:
        ax.step(prev[0:,2], prev[0:,1], label = 'Old Profile, #Collisons= ' + str(numberCollisions(prev)) ,where='post') #
    except:
        pass
      
    try:
        ax.step(new[0:,2], new[0:,1] , label = 'New Profile, #Collisons= ' + str(numberCollisions(new)),where='post') 
    except:
        pass         
    
    
    plt.axvline(x=-365*1 - newyearsOrigodifference, color = 'k', linestyle = '--', label = 'Year shift')
    plt.axvline(x=-365*2 - newyearsOrigodifference, color = 'k', linestyle = '--')
    plt.axvline(x=-365*3 - newyearsOrigodifference, color = 'k', linestyle = '--')
    plt.axvline(x=-365*4 - newyearsOrigodifference, color = 'k', linestyle = '--')
    plt.axvline(x=-365*5 - newyearsOrigodifference, color = 'k', linestyle = '--')
    plt.axvline(x=-365*6 - newyearsOrigodifference, color = 'k', linestyle = '--')
    plt.axvline(x=-365*7 - newyearsOrigodifference, color = 'k', linestyle = '--')
    plt.axvline(x=-365*8 - newyearsOrigodifference, color = 'k', linestyle = '--')
    
    plt.legend(loc = 2, prop={'size': 16})
    

    
    plt.xlabel('Time [days until ' + str(origo.day) + '/' + str(origo.month) + '/' + str(origo.year) + ']',  fontsize = 16)
    
    ax.set_ylabel('Beam intensity [collisions/s]',  fontsize = 16)
    
    
    
    ax2 = ax.twinx()
    
    lumicolor = 'm'
    
    #Lumi divided by 1000 to be expressed in fb-1 instead of pb-1
    ax2.plot(lumi[0:,0],lumi[0:,1]/1000, label = 'Integrated Luminosity', linestyle = '--', color = lumicolor)
    
    
    ax2.tick_params(axis='y', colors=lumicolor)
    
    ax2.set_ylabel('Integrated luminosity [fb-1]',  fontsize = 16)
    
    plt.title(title, fontsize = 20)
    
    
    xlength = 12
    
    fig.set_size_inches(xlength, xlength/1.618)
    
    plt.show()
    
    try:
        plt.savefig(args[4])
    except:
        pass;





def collisionsCheck(ATLAS, lumi):
    
    from scipy.interpolate import interp1d
    x = lumi[0:,0]
    y = lumi[0:,1]
    lumiprofile = interp1d(x,y)
    
    #2011
    xsec = 72E-3 #mbarn
    endfirstxsec = sinceOrigo(datetime.datetime(2011, 12, 30, 00, 00))
    lumiCollisions = 1e12*lumiprofile(endfirstxsec)*xsec
    
    #2012
    xsec = 75E-3 #mbarn
    endsecondxsec = sinceOrigo(datetime.datetime(2012, 12, 30, 00, 00))
    lumiCollisions = lumiCollisions + 1e12*(lumiprofile(endsecondxsec) - lumiprofile(endfirstxsec))*xsec
    
    #2015 - 2018    
    xsec = 80E-3 #mbarn
    endlastxsec = sinceOrigo(datetime.datetime(2018, 10, 30, 00, 00))
    lumiCollisions = lumiCollisions +  1e12*(lumiprofile(endlastxsec) - lumiprofile(endsecondxsec))*xsec
    
    global experiment
    
    if experiment == 'ALICE':
        #Ion run  
        xsec = 8. #barn
        protonIonFactor = 500/float(6)
        lumidiff = 1E9 #barn-1
        collisions = lumidiff*xsec
        ppcollisionsOfIonRun = collisions*protonIonFactor
        lumiCollisions = lumiCollisions + ppcollisionsOfIonRun
    
    print experiment + ' #Collisions/Lumi collisions = '
    print str(numberCollisions(ATLAS)/lumiCollisions)

    print ' '
    
    


def writeProfile(experiment, outname):

    
    f = open(outname, 'wb')
    f.write('* ..+....1....+....2....+....3....+....4....+....5....+....6....+....7....+....8\n')
    now = datetime.datetime.now()
    f.write('* Profile written by irradiation profile script on '+str(now) + '\n')
    for i in range(len(experiment)):
        if experiment[i,0] == 0:
            pass
        else:
            if i  % 3 == 1:
                string = 'IRRPROFI  '
  
            #round to closest second/integer
            val1 = int(round(experiment[i,0]*24*60*60))
            val2 = int(round(experiment[i,1]))
            
            if len(str(val1)) >10: 
                string = string + ("%.4e" % val1).rjust(10)
            else:
                string = string + str(val1).rjust(10)
            
            if len(str(val2)) >10:
                string = string + ("%.4e" % val2).rjust(10)
            else:
                string = string + str(val2).rjust(10)
            
            if i  % 3 == 0 or  i +2 == len(experiment):
                f.write(string + '\n')
                
            
    f.close()









import datetime
#


LS2 = datetime.datetime(2018,10,23,13,22,00) #end of proton-proton run
LS2ion = datetime.datetime(2018,12,3,06,00,00) # end of ion run



end2011 = datetime.datetime(2011,10,30,9,57,00)
end2012 = datetime.datetime(2012,12,16,11,58,00)
end2015 = datetime.datetime(2015,11,21,19,22,00)
end2016 = datetime.datetime(2016,10,26,07,49,00)
end2017 = datetime.datetime(2017,11,26,00,29,00)



start2011 = datetime.datetime(2011,3,13,13,35,9)
start2012 = datetime.datetime(2012,4,6,23,15,36)
start2015 = datetime.datetime(2015,6,5,23,17,23)
start2016 = datetime.datetime(2016,4,22,22,38,37)
start2017 = datetime.datetime(2017,5,23,14,45,27)




#2018
T1end = datetime.datetime(2018,6,11,23,39,11)
T1start = datetime.datetime(2018,4,17,11,00,23)

T2end =  datetime.datetime(2018,7,22,18,22,43)
T2start = datetime.datetime(2018,6,26,19,22,10)

T3end = datetime.datetime(2018,9,10,03,18,45)
T3start = datetime.datetime(2018,8,1,2,8,37)

T4end =  LS2 #end of proton-proton run
T4start = datetime.datetime(2018,9,23,17,55,33)


# Ion run
ionEnd = LS2ion
ionStart = datetime.datetime(2018,11,8,00,00,00)



datesAtlas = []
datesAtlas.append(T3end)
datesAtlas.append(T2end)
datesAtlas.append(T1end)
datesAtlas.append(end2017)
datesAtlas.append(end2016)
datesAtlas.append(end2015)
datesAtlas.append(end2012)
datesAtlas.append(end2011)

from copy import deepcopy

datesAlice = deepcopy(datesAtlas)
datesAlice.insert(0,T4end) #add ion run
datesCMS = deepcopy(datesAtlas)
datesLHCb = deepcopy(datesAtlas)



path = '//cern.ch/dfs/Users/c/cbjorkma/Documents/Irrprofi'
os.chdir(path)




experiment = 'ALICE'
origo = LS2ion
ALICE = readProfile('ALICEold.txt')
filename = 'lumiData.csv'
lumi = readLumi(filename, origo)
newALICE = setMagnitude(lumi)
newALICE = calcTimingNewprofile(datesAlice, newALICE, origo)
plot(ALICE, newALICE, origo, experiment, 'ALICE.pdf')
collisionsCheck(newALICE, lumi)
writeProfile(newALICE, 'AliceIrradiationProfileLS2.inp')



experiment = 'ATLAS'
origo = LS2
ATLAS = readProfile('ATLASold.txt')
filename = 'lumiData.csv'
lumi = readLumi(filename, origo)
newATLAS = setMagnitude(lumi)
newATLAS = calcTimingNewprofile(datesAtlas, newATLAS, origo)
plot(ATLAS, newATLAS, origo, experiment , 'ATLAS.pdf')
collisionsCheck(newATLAS, lumi)
writeProfile(newATLAS, 'AtlasIrradiationProfileLS2.inp')



experiment = 'CMS'
origo = LS2
CMS = readProfile('CMSold.txt')
filename = 'lumiData.csv'
lumi = readLumi(filename, origo)
newCMS = setMagnitude(lumi)
newCMS = calcTimingNewprofile(datesCMS, newCMS, origo)
plot(CMS, newCMS, origo, experiment, 'CMS.pdf')
collisionsCheck(newCMS, lumi)
writeProfile(newCMS, 'CMSIrradiationProfileLS2.inp')


experiment = 'LHCb'
origo = LS2
#LHCb = readProfile('LHCbOld.txt')
filename = 'lumiData.csv'
lumi = readLumi(filename, origo)
newLHCb = setMagnitude(lumi)
newLHCb = calcTimingNewprofile(datesLHCb, newLHCb, origo)
plot([], newLHCb, origo, experiment, 'LHCb.pdf')
collisionsCheck(newLHCb, lumi)
writeProfile(newLHCb, 'LHCbIrradiationProfileLS2.inp')




















