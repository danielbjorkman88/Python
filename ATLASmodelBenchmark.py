# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 10:36:40 2019

@author: cbjorkma
"""

#ATLASbenchmark


import os
import glob
from USRBIN import USRBIN



normfactor = 0.0036
#
path = '//rpclustergw/cluster_temp/cbjorkma/OpeningScenarios/DECAY/2019-07-03_16h53m51s_ATLAS4_LS2_opening'
os.chdir(path)

filenames = sorted(glob.glob('*.lis'))


point1 = USRBIN(filenames[1], path, normfactor)
point1.read()
point1.readError()
point1.calc()




point2 = USRBIN(filenames[2], path, normfactor)
point2.read()
point2.calc()
point2.readError()



point3 = USRBIN(filenames[4], path, normfactor)
point3.read()
point3.calc()
point3.readError()



point4 = USRBIN(filenames[5], path, normfactor)
point4.read()
point4.calc()
point4.readError()





import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

import numpy as np



import matplotlib.cm as cm
import matplotlib.gridspec as gridspec


allratios = []

#--Point 1---------------------------------------------------------------------------------------------
gs = gridspec.GridSpec(4, 1)

fig = plt.figure()

stop =3
ax = plt.subplot(gs[0:stop, 0])

xmid = int(point1.cube.shape[0]/2)
ymid = int(point1.cube.shape[1]/2)
zmid = int(point1.cube.shape[2]/2)

rmax = int(point1.info['rmax'][0])
rwidth = int(point1.info['rwidth'][0])
xes = range(0 , rmax, 1)

yes = point1.cube[xmid:, ymid, zmid]
plt.step(xes, yes , label = 'FLUKA', color = "C0" )



yeserrorSim = point1.cubeErrors[xmid:, ymid, zmid]/100
yerrorsabsolut = yes*yeserrorSim
plt.errorbar(xes -0.5* rwidth*np.ones(len(xes)),yes, yerr = yerrorsabsolut  , linestyle='None', color = "C0")


locs = [40 , 80, 120 , 160 , 200 , 240, 280]

ARpoints = [18.2 , 12.8, 7.3 , 6.3 , 3.6 , 2.6 , 1.4]
ALpoints = [16.1 , 14.2, 8.7, 5.6 , 3.9 , 2.2 , 1.2]

yerrorsMes = 0.2*np.ones(len(locs));

plt.errorbar(locs, ARpoints, yerr = yerrorsMes, linestyle='None', label = 'AR side', marker = "." , markersize=12, color = "C1")
plt.errorbar(locs, ALpoints , yerr = yerrorsMes, linestyle='None', label = 'AL side', marker = "." , markersize=12, color = "C2")


plt.grid(linewidth = 0.2)

plt.ylabel('uSv/h', fontsize = 16)


ax.set_yscale('log')
plt.legend()

xmin = -20
xmax = 300
plt.xlim(xmin,xmax)
plt.title('40 cm distance ', fontsize = 16)

ax = plt.subplot(gs[stop:, 0])

f = interp1d(xes, yes)

ratiosAR = f(locs) /ARpoints
ratiosAL = f(locs) /ALpoints 

maximum = max(max(ratiosAR), max(ratiosAL))
minimum = min(min(ratiosAR), min(ratiosAL))

ferrors = interp1d(xes, yeserrorSim )

import math

ratioerrors = map(lambda x,y: math.sqrt(x*x + y*y ), yerrorsMes, ferrors(locs))

plt.errorbar(locs, ratiosAR , yerr = ratiosAR * ratioerrors, linestyle='None', label = 'AR side', marker = "." , markersize=12, color = "C1")
plt.errorbar(locs, ratiosAL , yerr = ratiosAL *ratioerrors, linestyle='None', label = 'AL side', marker = "." , markersize=12, color = "C2")

allratios.extend(ratiosAR)
allratios.extend(ratiosAL)


plt.ylim(0.1* minimum, maximum*1.4)
plt.axhline(y=1, color='k', linestyle='-')
plt.grid(linewidth = 0.2)
plt.ylabel('Ratios', fontsize = 16)
plt.xlabel('R [cm from IP]', fontsize = 16)
plt.legend()
plt.xlim(xmin,xmax)



plt.suptitle('ATLAS Benchmark. Measurement positon 1: Inner barrel', fontsize = 22)

xlength = 12

fig.set_size_inches(xlength, xlength/1.618)



plt.show()

plt.savefig('BenchmarkPoint1.pdf')






#--Point 2---------------------------------------------------------------------------------------------
gs = gridspec.GridSpec(4, 3)


locs = [104 , 239]

ARcontact = [12.2 , 1.8]
ALcontact = [10.6 ,1.8]


ARdist = [13.3, 2.7]



ALdist = [ 12.5, 2.3]

mid = [89 , 47]







fig = plt.figure()

stop = 3

rmax = int(point2.info['rmax'][0])
rwidth = int(point2.info['rwidth'][0])

#xes = range(-rmax + rwidth/2, rmax + rwidth/2 , rwidth)


xes = range(0 , rmax, rwidth)
#xes.append(rmax)


ymid = int(point2.cube.shape[1]/2)
zend = int(point2.cube.shape[2]) -1
xmid = int(point2.cube.shape[0]/2)



ax = plt.subplot(gs[0:stop, 0])

zes = range(int(point2.info['zmin'][0]) , int(point2.info['zmax'][0]), int(point2.info['zwidth'][0]))

zwidth = int(point2.info['zwidth'][0])

yes = point2.cube[xmid, ymid, 0:]
plt.step(zes, yes , label = 'FLUKA')

yeserrorSim = point2.cubeErrors[xmid, ymid, 0:]/100
yerrorsabsolut = yes*yeserrorSim
plt.errorbar(zes -0.5*zwidth* np.ones(len(zes)),yes, yerr = yerrorsabsolut , linestyle='None' , color = "C0")


midloc = [int(point2.info['zmax'][0]) -3  , int(point2.info['zmax'][0]) -3 -26 ]

yerrorsMes = 0.2*np.ones(len(midloc));
plt.errorbar(midloc, mid, yerr = yerrorsMes, linestyle='None', label = 'Measurement', marker = "." , markersize=12, color = 'C3')
ax.set_yscale('log')
plt.legend()
plt.ylabel('uSv/h', fontsize = 16)
plt.grid(linewidth = 0.2)
plt.xlabel('Z [cm from IP]', fontsize = 16)


plt.title('Axial ', fontsize = 16)

plt.xlim(point2.info['zmin'][0], point2.info['zmax'][0])


ax = plt.subplot(gs[stop:, 0])

f = interp1d(zes, yes)

ratiosMid = f(midloc) /mid

ferrors = interp1d(zes, yeserrorSim )
ratioerrors = map(lambda x,y: math.sqrt(x*x + y*y ), yerrorsMes, ferrors(midloc))
plt.errorbar(midloc, ratiosMid , yerr = ratiosMid * ratioerrors, linestyle='None', label = 'Fluka/measurement', marker = "." , markersize=12)

allratios.append(ratiosMid[1])


plt.ylim(0.3, 1.1)
plt.axhline(y=1, color='k', linestyle='-')
plt.grid(linewidth = 0.2)
#plt.ylabel('Ratios', fontsize = 16)
plt.xlabel('Z [cm from IP]', fontsize = 16)
plt.legend()
plt.xlim(point2.info['zmin'][0], point2.info['zmax'][0])











ax = plt.subplot(gs[0:stop, 1])

#xes = range(int(point2.cube.shape[0]))



zContact = zend -3
yes = point2.cube[xmid:, ymid, zContact]
plt.step(xes, yes , label = 'FLUKA')

yeserrorSim = point2.cubeErrors[xmid:, ymid, zContact]/100
yerrorsabsolut = yes*yeserrorSim
plt.errorbar(xes -0.5*rwidth* np.ones(len(xes)),yes, yerr = yerrorsabsolut , linestyle='None' , color = "C0")




yerrorsMes = 0.2*np.ones(len(locs));
plt.errorbar(locs, ARcontact, yerr = yerrorsMes, linestyle='None', label = 'AR side', marker = "." , markersize=12)
plt.errorbar(locs, ALcontact, yerr = yerrorsMes ,linestyle='None', label = 'AL side', marker = "." , markersize=12)
plt.errorbar(2, mid[0], yerr = 0.2,linestyle='None', label = 'Axis measurement', marker = "." , markersize=12)
plt.title('Upon contact' , fontsize = 16)



plt.grid(linewidth = 0.2)

#plt.ylabel('uSv/h', fontsize = 16)

plt.xlabel('R [cm from IP]', fontsize = 16)
ax.set_yscale('log')
plt.legend()
plt.xlim(xmin,xmax)



ax = plt.subplot(gs[stop:, 1])

f = interp1d(xes, yes)

ratiosAR = f(locs) /ARcontact
ratiosAL = f(locs) /ALcontact
ratiosMid = f(0) / mid[0]


ferrors = interp1d(xes, yeserrorSim )


ratioerrors = map(lambda x,y: math.sqrt(x*x + y*y ), yerrorsMes, ferrors(locs))

ratioerrorsMid = math.sqrt(0.2**2 + ferrors(0)**2)

plt.errorbar(locs, ratiosAR , yerr = ratiosAR * ratioerrors, linestyle='None', label = 'AR side', marker = "." , markersize=12, color = "C1")
plt.errorbar(locs, ratiosAL , yerr = ratiosAL *ratioerrors, linestyle='None', label = 'AL side', marker = "." , markersize=12, color = "C2")
plt.errorbar(0, ratiosMid , yerr = ratiosMid *ratioerrorsMid, linestyle='None', label = 'Axial measurement', marker = "." , markersize=12, color = "C3")

allratios.extend(ratiosAR)
allratios.extend(ratiosAL)


maximum = max(max(ratiosAR), max(ratiosAL), ratiosMid)
minimum = min(min(ratiosAR), min(ratiosAL), ratiosMid)
plt.ylim(0.6* minimum, 1.1)
plt.axhline(y=1, color='k', linestyle='-')
plt.grid(linewidth = 0.2)
#plt.ylabel('Ratios', fontsize = 16)
plt.xlabel('R [cm from IP]', fontsize = 16)
plt.legend()
plt.xlim(xmin,xmax)





ax = plt.subplot(gs[0:stop, 2])


z40 = zContact -40
yes = point2.cube[xmid:, ymid, z40]
plt.step(xes, yes , label = 'FLUKA')


yeserrorSim = point2.cubeErrors[xmid:, ymid, z40]/100
yerrorsabsolut = yes*yeserrorSim
plt.errorbar(xes -0.5*rwidth* np.ones(len(xes)),yes, yerr = yerrorsabsolut , linestyle='None' , color = "C0")


yerrorsMes = 0.2*np.ones(len(locs));
plt.errorbar(locs, ARdist, yerr = yerrorsMes, linestyle='None', label = 'AR side', marker = "." , markersize=12)
plt.errorbar(locs, ALdist, yerr = yerrorsMes, linestyle='None', label = 'AL side', marker = "." , markersize=12)

plt.title('40 cm distance ', fontsize = 16)

plt.grid(linewidth = 0.2)

#plt.ylabel('uSv/h', fontsize = 16)

plt.xlabel('R [cm from IP]', fontsize = 16)
ax.set_yscale('log')
plt.legend()
plt.xlim(xmin,xmax)


ax = plt.subplot(gs[stop:, 2])


f = interp1d(xes, yes)

ratiosAR = f(locs) /ARdist
ratiosAL = f(locs) /ALdist


ferrors = interp1d(xes, yeserrorSim )


ratioerrors = map(lambda x,y: math.sqrt(x*x + y*y ), yerrorsMes, ferrors(locs))

ratioerrorsMid = math.sqrt(0.2**2 + ferrors(0)**2)

plt.errorbar(locs, ratiosAR , yerr = ratiosAR * ratioerrors, linestyle='None', label = 'AR side', marker = "." , markersize=12, color = "C1")
plt.errorbar(locs, ratiosAL , yerr = ratiosAL *ratioerrors, linestyle='None', label = 'AL side', marker = "." , markersize=12, color = "C2")

allratios.extend(ratiosAR)
allratios.extend(ratiosAL)

plt.ylim(0.34, 1.1)
plt.axhline(y=1, color='k', linestyle='-')
plt.grid(linewidth = 0.2)
#plt.ylabel('Ratios', fontsize = 16)
plt.xlabel('R [cm from IP]', fontsize = 16)
plt.legend()
plt.xlim(xmin,xmax)










#plt.suptitle('Inner extended barrel', fontsize = 22)



plt.suptitle('ATLAS Benchmark. Measurement positon 2: Inner extended barrel', fontsize = 22)

xlength = 12

fig.set_size_inches(xlength, xlength/1.618)

plt.savefig('BenchmarkPoint2.pdf')


plt.show()



















#--Point 3---------------------------------------------------------------------------------------------
gs = gridspec.GridSpec(4, 1)

fig = plt.figure()

stop =3
ax = plt.subplot(gs[0:stop, 0])

xmid = int(point3.cube.shape[0]/2)
ymid = int(point3.cube.shape[1]/2)
zmid = int(point3.cube.shape[2]/2)

rmax = int(point3.info['rmax'][0])
rwidth = int(point3.info['rwidth'][0])
xes = range(0 , rmax, 1)

yes = point3.cube[xmid:, ymid, zmid]
plt.step(xes, yes , label = 'FLUKA', color = "C0" )



yeserrorSim = point3.cubeErrors[xmid:, ymid, zmid]/100
yerrorsabsolut = yes*yeserrorSim
plt.errorbar(xes -0.5*rwidth* np.ones(len(xes)),yes, yerr = yerrorsabsolut  , linestyle='None', color = "C0")

locs = [ 80, 120 , 160 , 200 , 240]

ARpoints = [9.7 , 4.0 , 2.2 , 0.75 , 0.6]
ALpoints = [11.2 , 4.6 , 1.7 , 0.8 , 0.6]


yerrorsMes = 0.2*np.ones(len(locs));
plt.errorbar(locs, ARpoints,yerr = yerrorsMes, linestyle='None', label = 'AR side', marker = "." , markersize=12, color = "C1")
plt.errorbar(locs, ALpoints,yerr = yerrorsMes, linestyle='None', label = 'AL side', marker = "." , markersize=12, color = "C2")


plt.grid(linewidth = 0.2)

plt.ylabel('uSv/h', fontsize = 16)


ax.set_yscale('log')
plt.legend()

xmin = 0
xmax = 300
plt.xlim(xmin,xmax)
plt.title('40 cm distance ', fontsize = 16)

ax = plt.subplot(gs[stop:, 0])

f = interp1d(xes, yes)

ratiosAR = f(locs) /ARpoints
ratiosAL = f(locs) /ALpoints 

maximum = max(max(ratiosAR), max(ratiosAL))
minimum = min(min(ratiosAR), min(ratiosAL))

ferrors = interp1d(xes, yeserrorSim )

import math

ratioerrors = map(lambda x,y: math.sqrt(x*x + y*y ), yerrorsMes, ferrors(locs))

plt.errorbar(locs, ratiosAR , yerr = ratiosAR * ratioerrors, linestyle='None', label = 'AR side', marker = "." , markersize=12, color = "C1")
plt.errorbar(locs, ratiosAL , yerr = ratiosAL *ratioerrors, linestyle='None', label = 'AL side', marker = "." , markersize=12, color = "C2")

allratios.extend(ratiosAR)
allratios.extend(ratiosAL)


plt.ylim(0.1* minimum, maximum*1.4)
plt.axhline(y=1, color='k', linestyle='-')
plt.grid(linewidth = 0.2)
plt.ylabel('Ratios', fontsize = 16)
plt.xlabel('R [cm from IP]', fontsize = 16)
plt.legend()
plt.xlim(xmin,xmax)



plt.suptitle('ATLAS Benchmark. Measurement positon 3: Outer extended barrel', fontsize = 22)

xlength = 12

fig.set_size_inches(xlength, xlength/1.618)

plt.savefig('BenchmarkPoint3.pdf')


plt.show()







#--Point 4---------------------------------------------------------------------------------------------
gs = gridspec.GridSpec(4, 2)

fig = plt.figure()

stop =3
ax = plt.subplot(gs[0:stop, 0])

xmid = int(point4.cube.shape[0]/2)
ymid = int(point4.cube.shape[1]/2)
zmid = int(point4.cube.shape[2]/2)

rmax = int(point4.info['rmax'][0])
rwidth = int(point4.info['rwidth'][0])
xes = range(0 , rmax, 1)

zcontact = int(point4.info['zbin'][0]-4)

yes = point4.cube[xmid:, ymid, zcontact]
plt.step(xes, yes , label = 'FLUKA', color = "C0" )



yeserrorSim = point4.cubeErrors[xmid:, ymid, zcontact]/100
yerrorsabsolut = yes*yeserrorSim
plt.errorbar(xes -0.5*rwidth* np.ones(len(xes)),yes, yerr = yerrorsabsolut  , linestyle='None', color = "C0")

locs = [ 28.2 , 74.91 , 130.6 , 220]

contact = [98.8 , 13.5 , 1.1 , 0.3 ]
dist = [29 , 13.8 , 3.5 , 0.9 ]


yerrorsMes = 0.2*np.ones(len(locs));
plt.errorbar(locs, contact,yerr = yerrorsMes, linestyle='None', label = 'Measurement', marker = "." , markersize=12, color = "C1")
#plt.errorbar(locs, ALpoints,yerr = yerrorsMes, linestyle='None', label = 'AL side', marker = "." , markersize=12, color = "C2")


plt.grid(linewidth = 0.2)

plt.ylabel('uSv/h', fontsize = 16)


ax.set_yscale('log')
plt.legend()

xmin = 0
xmax = 300
plt.xlim(xmin,xmax)
plt.title('Upon contact', fontsize = 16)

ax = plt.subplot(gs[stop:, 0])

f = interp1d(xes, yes)

ratios = f(locs) /contact




ferrors = interp1d(xes, yeserrorSim )

import math

ratioerrors = map(lambda x,y: math.sqrt(x*x + y*y ), yerrorsMes, ferrors(locs))

plt.errorbar(locs, ratios , yerr = ratios * ratioerrors, linestyle='None', label = 'Measurement', marker = "." , markersize=12, color = "C1")

allratios.extend(ratios)


plt.ylim(0.05, 1.1)
plt.axhline(y=1, color='k', linestyle='-')
plt.grid(linewidth = 0.2)
plt.ylabel('Ratios', fontsize = 16)
plt.xlabel('R [cm from IP]', fontsize = 16)
plt.legend()
plt.xlim(xmin,xmax)








ax = plt.subplot(gs[0:stop, 1])



zdist = int(point4.info['zbin'][0]-4 - 40)

yes = point4.cube[xmid:, ymid, zdist]
plt.step(xes, yes , label = 'FLUKA', color = "C0" )



yeserrorSim = point4.cubeErrors[xmid:, ymid, zdist]/100
yerrorsabsolut = yes*yeserrorSim
plt.errorbar(xes -0.5*rwidth* np.ones(len(xes)),yes, yerr = yerrorsabsolut  , linestyle='None', color = "C0")

locs = [ 28.2 , 74.91 , 130.6 , 220]




yerrorsMes = 0.2*np.ones(len(locs));
plt.errorbar(locs, dist,yerr = yerrorsMes, linestyle='None', label = 'Measurement', marker = "." , markersize=12, color = "C1")
#plt.errorbar(locs, ALpoints,yerr = yerrorsMes, linestyle='None', label = 'AL side', marker = "." , markersize=12, color = "C2")


plt.grid(linewidth = 0.2)

plt.ylabel('uSv/h', fontsize = 16)


ax.set_yscale('log')
plt.legend()

xmin = 0
xmax = 300
plt.xlim(xmin,xmax)


plt.title('40 cm distance', fontsize = 16)



ax = plt.subplot(gs[stop:, 1])

f = interp1d(xes, yes)

ratios = f(locs) /dist




ferrors = interp1d(xes, yeserrorSim )

import math

ratioerrors = map(lambda x,y: math.sqrt(x*x + y*y ), yerrorsMes, ferrors(locs))

plt.errorbar(locs, ratios , yerr = ratios * ratioerrors, linestyle='None', label = 'Measurement', marker = "." , markersize=12, color = "C1")

allratios.extend(ratios)

plt.ylim(0.05, 1.1)
plt.axhline(y=1, color='k', linestyle='-')
plt.grid(linewidth = 0.2)
plt.ylabel('Ratios', fontsize = 16)
plt.xlabel('R [cm from IP]', fontsize = 16)
plt.legend()
plt.xlim(xmin,xmax)


plt.suptitle('ATLAS Benchmark. Measurement positon 4: Small Wheel', fontsize = 22)

xlength = 12

fig.set_size_inches(xlength, xlength/1.618)

plt.savefig('BenchmarkPoint4.pdf')


plt.show()








fig = plt.figure()

ax = plt.subplot(111)

factor = float(50)

n, bins, patches = plt.hist(allratios, alpha = 1, bins = (1/factor)*np.arange(0, int(factor*max(allratios))), log=False, label = 'Fluka/Measurement')


plt.legend()
plt.title('Measurement campaign summary', fontsize = 22)
plt.xlabel('Ratios', fontsize =16)
plt.ylabel('Counts', fontsize =16)
plt.grid(linewidth = 0.2)
#ax.set_yscale('log')

xlength = 12

fig.set_size_inches(xlength, xlength/1.618)

plt.savefig('ATLASsummary.pdf')

plt.show()













fig = plt.figure()

ax = plt.subplot(111)

n, bins, patches = plt.hist(point1.cubeErrors.flatten(), bins = 0.01*np.arange(0, 100*int(np.max(point1.cubeErrors)), 10), label = "Point1 errors", alpha = 0.5, log=False)
plt.hist(point2.cubeErrors.flatten(), bins = bins, label = "Point2 errors", alpha = 0.5, log=False)
plt.hist(point3.cubeErrors.flatten(), bins = bins, label = "Point3 errors", alpha = 0.5, log=False)
plt.hist(point4.cubeErrors.flatten(), bins = bins, label = "Point4 errors", alpha = 0.5, log=False)

plt.legend()
plt.title('Error distribution', fontsize = 22)
plt.xlabel('Error [%]', fontsize =16)
plt.ylabel('Counts', fontsize =16)
#ax.set_yscale('log')
plt.show()


