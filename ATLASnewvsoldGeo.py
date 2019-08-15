# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 14:49:00 2019

@author: cbjorkma
"""

#ATLASnewvsoldGeo


import os
import glob
from USRBIN import USRBIN
import math
import numpy as np








def loadGeant4(path, filename ):
    os.chdir(path)
    
    raw = np.loadtxt(filename, skiprows = 1)
    image = np.zeros([240,240])
    row = 0
    for z in range(240):
        for r in range(120):
           image[r + 120 ,z] = raw[row,4]
           image[119 -r ,z] = raw[row,4]
           row = row + 1
    return image;




#filename = 'ATLAS2_JTTcontours.dat'



import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib.gridspec as gridspec
#import matplotlib.ticker as ticker



def compare(old, new, geant4, quantity):


    fig = plt.figure()
    
    maxY = int(new.info['rmax'][0])
    widthY = int(new.info['rwidth'][0])
    maxX = int(new.info['zmax'][0])
    widthX = int(new.info['zwidth'][0])
    
    
    X, Y = np.meshgrid(range(0,maxX, widthX),range(-maxY,maxY, widthY))
    
    image1= new.cube[0:,int(new.cube.shape[1]/2), 0:]/geant4
    image2= old.cube[0:,int(old.cube.shape[1]/2), 0:]/geant4
    
    vmax1 = np.nanmax([image1.flatten()[image1.flatten() != np.inf] ])
    vmax2 = np.nanmax([image2.flatten()[image2.flatten() != np.inf] ])
    vmax = max(vmax1, vmax2)
    vmin = np.nanmin([np.nanmin(image1[np.nonzero(image1)]) , np.nanmin(image2[np.nonzero(image2)])])
    #lim = max(vmax, 1/vmin)
    lim = float(5)
    
#    print vmax
#    print vmin
    
    
    gs0 = gridspec.GridSpec(8, 2)
    
    ax = plt.subplot(gs0[:4,1])

    
    plt.pcolor(X, Y,image1, norm=LogNorm(vmin=1/lim, vmax=lim) ,cmap = 'seismic')
    cbar = plt.colorbar()
    cbar.set_label('Ratio', fontsize = 12)
    plt.title('NewGeo / Geant4')
    plt.ylabel('R [cm from IP]', fontsize = 12)
    ax = new.drawGeo(ax)
    plt.xlim(0,2400)
    plt.ylim(-1200,1200)
    
    
    ax = plt.subplot(gs0[:4,0])
    
    
    plt.pcolor(X, Y, image2, norm=LogNorm(vmin=1/lim, vmax=lim),cmap = 'seismic')
    cbar = plt.colorbar()
    cbar.set_label('Ratio', fontsize = 12)
    plt.title('OldGeo / Geant4')
    plt.ylabel('R [cm from IP]', fontsize = 12)
    ax = old.drawGeo(ax)
    plt.xlim(0,2400)
    plt.ylim(-1200,1200)
    
    ax = plt.subplot(gs0[4:,0])
    
    
    #vmax = max([image1.max(), image2.max()])
    #vmin = np.min([np.min(image1[np.nonzero(image1)]), np.min(image2[np.nonzero(image2)]) ])
    
    bins = np.logspace(np.log10(vmin),np.log10(vmax),100) #range(int(round(vmax)))
    image1hist = image1[0:int(image1.shape[0]/2),0:].flatten()
    image2hist = image2[0:int(image2.shape[0]/2),0:].flatten()
    plt.hist(image1hist[np.isfinite(image1hist)], bins = bins, label = 'New Geo / Geant4' , alpha = 0.7) #
    plt.hist(image2hist[np.isfinite(image2hist)],  bins = bins , label = 'Old Geo / Geant4', alpha = 0.6) #     

    plt.legend()
    plt.grid(linewidth = 0.3)
    plt.yscale('log', nonposy='clip')
    plt.xscale('log', nonposy='clip')
    
    plt.xlabel('Ratios', fontsize = 16)
    plt.ylabel('Counts', fontsize = 16)
    
    
    
    
    xes = range(0,2400,2400/240)
    
#    plt.plot(xes, new.centre, label = 'New Geo', linestyle = '-')
#    plt.plot(xes, old.centre, label = 'Old Geo', linestyle = '-')
#    plt.plot(xes, geant4[120,0:], label = 'Geant4', linestyle = '-')
#    ax.set_yscale('log')
#    plt.ylabel('Residual dose rate [uSv/h]' , fontsize = 12)
#    plt.legend()
#    plt.grid(linewidth = 0.3)
#    plt.title('Central axis', fontsize = 12,  y=0.85)
#    #plt.xlabel('z [cm from IP]', fontsize = 18)
#    
#    
    ax = plt.subplot(gs0[4:6,1])
    
    
    plt.plot(xes, new.centre/geant4[120,0:], label = 'New Geo/Geant4', linestyle = '-')
    plt.plot(xes, old.centre/geant4[120,0:], label = 'Old Geo/Geant4', linestyle = '-')
    plt.axhline(y=1, color='k', linestyle='-')
    plt.legend()
    plt.grid(linewidth = 0.3)
    plt.ylabel('Ratio' , fontsize = 14)
    plt.xlabel('z [cm from IP]', fontsize = 18)
    plt.title('Central axis', fontsize = 12,  y=0.85)
    
    
    ax = plt.subplot(gs0[6:,1])
    
    image1 = new.cube[0:,int(new.cube.shape[1]/2), 0:]
    image2 = old.cube[0:,int(old.cube.shape[1]/2), 0:]
    
    geant4integrated = np.zeros([240])
    image1integrated = np.zeros([240])
    image2integrated = np.zeros([240])
    for i in range(240):
        geant4integrated[i] = sum(geant4[0:,i])
        image1integrated[i] = sum(image1[0:,i])
        image2integrated[i] = sum(image2[0:,i])
        
    plt.plot(xes, image1integrated/geant4integrated, label = 'New Geo/Geant4', linestyle = '-')
    plt.plot(xes, image2integrated/geant4integrated, label = 'Old Geo/Geant4', linestyle = '-')
    plt.axhline(y=1, color='k', linestyle='-')
    plt.legend()
    plt.grid(linewidth = 0.3)
    plt.ylabel('Ratio' , fontsize = 14)
    plt.xlabel('z [cm from IP]', fontsize = 18)
    plt.title('Integrated', fontsize = 12,  y=0.85)
    
    
    
    plt.suptitle(quantity, fontsize = 18)
    
    
    plt.show()





def compareFlukaOnly(old, new, quantity):


    fig = plt.figure()
    
    maxY = int(new.info['rmax'][0])
    widthY = int(new.info['rwidth'][0])
    maxX = int(new.info['zmax'][0])
    widthX = int(new.info['zwidth'][0])
    
    
    X, Y = np.meshgrid(range(0,maxX, widthX),range(-maxY,maxY, widthY))
    
    image1= new.cube[0:,int(new.cube.shape[1]/2), 0:]
    image2= old.cube[0:,int(old.cube.shape[1]/2), 0:]
    
    image = image1/image2
    
#    vmax = np.nanmax([image.flatten()[image.flatten() != np.inf] ])
#    vmin = np.nanmin([np.nanmin(image[np.nonzero(image)]) , np.nanmin(image[np.nonzero(image)])])
#    lim = max(vmax, 1/vmin)
    
    lim = 5
    
    gs0 = gridspec.GridSpec(8, 2)
    

    
    
    ax = plt.subplot(gs0[:4,0])
    
    
    plt.pcolor(X, Y, image, norm=LogNorm(vmin=1/float(lim), vmax=lim),cmap = 'seismic')
    cbar = plt.colorbar()
    cbar.set_label('Ratio', fontsize = 12)
    plt.title('New Geo / Old Geo', fontsize = 16)
    plt.ylabel('R [cm from IP]', fontsize = 12)
    ax = old.drawGeo(ax)
    plt.xlim(0,2400)
    plt.ylim(-1200,1200)
    
    

    
    ax = plt.subplot(gs0[4:,0])
    
    plt.pcolor(X, Y, image, norm=LogNorm(vmin=1/float(lim), vmax=lim),cmap = 'seismic')
    cbar = plt.colorbar()
    cbar.set_label('Ratio', fontsize = 12)
    #plt.title('New Geo / Old Geo')
    plt.ylabel('R [cm from IP]', fontsize = 12)
    ax = old.drawGeo(ax)
    plt.xlim(0,880)
    plt.ylim(-540,540)    
    
#    #vmax = max([image1.max(), image2.max()])
#    #vmin = np.min([np.min(image1[np.nonzero(image1)]), np.min(image2[np.nonzero(image2)]) ])
#    vmax1 = np.nanmax([image1.flatten()[image1.flatten() != np.inf] ])
#    vmax2 = np.nanmax([image2.flatten()[image2.flatten() != np.inf] ])
#    vmax = max(vmax1, vmax2)
#    vmin = np.nanmin([np.nanmin(image1[np.nonzero(image1)]) , np.nanmin(image2[np.nonzero(image2)])])
#    
#    
#    #bins = range(0,int(round(vmax)), int(round(vmax)/200)) # np.logspace(np.log10(vmin),np.log10(vmax),100) #range(int(round(vmax))) # 
#    bins = np.logspace(np.log10(vmin),np.log10(vmax),100)
#    image1hist = image1[0:int(image1.shape[0]/2),0:].flatten()
#    image2hist = image2[0:int(image2.shape[0]/2),0:].flatten()
#    
#    plt.hist(image1hist[np.isfinite(image1hist)], bins = bins, label = 'New Geo ' , alpha = 0.7) #
#    plt.hist(image2hist[np.isfinite(image2hist)],  bins = bins , label = 'Old Geo ', alpha = 0.6) #     
#
#    plt.legend()
#    plt.grid(linewidth = 0.3)
#    plt.yscale('log', nonposy='clip')
#    plt.xscale('log', nonposy='clip')
#    
#    plt.xlabel('Values', fontsize = 16)
#    plt.ylabel('Counts', fontsize = 16)
    
    
    
    
    xes = range(0,2400,2400/240)
    
#    plt.plot(xes, new.centre, label = 'New Geo', linestyle = '-')
#    plt.plot(xes, old.centre, label = 'Old Geo', linestyle = '-')
#    plt.plot(xes, geant4[120,0:], label = 'Geant4', linestyle = '-')
#    ax.set_yscale('log')
#    plt.ylabel('Residual dose rate [uSv/h]' , fontsize = 12)
#    plt.legend()
#    plt.grid(linewidth = 0.3)
#    plt.title('Central axis', fontsize = 12,  y=0.85)
#    #plt.xlabel('z [cm from IP]', fontsize = 18)
#    
#    

#    ax = plt.subplot(gs0[:3,1])
#
#    plt.plot(xes, new.centre, label = 'New Geo', linestyle = '-')
#    plt.plot(xes, old.centre, label = 'Old Geo', linestyle = '-')
#    
#    plt.legend()
#    plt.grid(linewidth = 0.3)
#    plt.ylabel(unit , fontsize = 14)
#    plt.xlabel('z [cm from IP]', fontsize = 18)
#    plt.title('Central axis', fontsize = 12,  y=0.85)
    
    ax = plt.subplot(gs0[:4,1])

    
#    plt.pcolor(X, Y,image, norm=LogNorm(vmin=vmin, vmax=vmax), cmap='jet')
#    cbar = plt.colorbar()
#    cbar.set_label('Ratio', fontsize = 12)
#    plt.title('NewGeo')
#    plt.ylabel('R [cm from IP]', fontsize = 12)
#    ax = new.drawGeo(ax)
#    plt.xlim(0,2400)
#    plt.ylim(-1200,1200)        
    #ax = plt.subplot(gs0[4:6,1])
    
    
    plt.plot(xes, new.centre/old.centre, label = 'New Geo/Old Geo', linestyle = '-')
    #plt.plot(xes, old.centre, label = 'Old Geo', linestyle = '-')
    plt.axhline(y=1, color='k', linestyle='-')
    plt.legend()
    plt.grid(linewidth = 0.3)
    plt.ylabel('Ratio' , fontsize = 14)
    plt.xlabel('z [cm from IP]', fontsize = 18)
    plt.title('Central axis', fontsize = 12,  y=0.85)
    
    
    ax = plt.subplot(gs0[4:,1])
    
    image1 = new.cube[0:,int(new.cube.shape[1]/2), 0:]
    image2 = old.cube[0:,int(old.cube.shape[1]/2), 0:]
    
    image1integrated = np.zeros([240])
    image2integrated = np.zeros([240])
    for i in range(240):
        image1integrated[i] = sum(image1[0:,i])
        image2integrated[i] = sum(image2[0:,i])
        
    plt.plot(xes, image1integrated/image2integrated, label = 'New Geo/Old Geo', linestyle = '-')
    plt.axhline(y=1, color='k', linestyle='-')
    plt.legend()
    plt.grid(linewidth = 0.3)
    plt.ylabel('Ratio' , fontsize = 14)
    plt.xlabel('z [cm from IP]', fontsize = 18)
    plt.title('Integrated', fontsize = 12,  y=0.85)
    
    
    
    plt.suptitle(quantity, fontsize = 24)
    
    
    plt.show()




normfactor = 1 *math.pow(10,15)* 78.42 * math.pow(10,-3)
#

pathNew = '//rpclustergw/cluster_temp/cbjorkma/2019-07-25_09h37m18s_ATLAS5newGeo'
pathOld = '//rpclustergw/cluster_temp/cbjorkma/2019-07-25_09h37m47s_ATLAS5oldGeo'

path = '//rpclustergw/cbjorkma/ATLAS'





#----------NEW------------------------------------------------------------------------------------------
os.chdir(pathNew)
filenames = sorted(glob.glob('*.lis'))


HEHADnew = USRBIN(filenames[0], pathNew, normfactor)
HEHADnew.read()
HEHADnew.contourpath = path
HEHADnew.loadGeometryFile('ATLASclosed.dat',3,4)
HEHADnew.title = 'Hadrons > 20 MeV'
#point1.readError()
HEHADnew.calc()
#HEHADnew.plot()


Neutronsnew = USRBIN(filenames[3], pathNew, normfactor)
Neutronsnew.read()
Neutronsnew.contourpath = path
Neutronsnew.loadGeometryFile('ATLASclosed.dat',3,4)
Neutronsnew.title =  'Neutrons > 10 keV'
#point1.readError()
Neutronsnew.calc()

ChargedHadronsnew = USRBIN(filenames[4], pathNew, normfactor)
ChargedHadronsnew.read()
ChargedHadronsnew.contourpath = path
ChargedHadronsnew.loadGeometryFile('ATLASclosed.dat',3,4)
ChargedHadronsnew.title = 'Charged Hadrons'
#point1.readError()
ChargedHadronsnew.calc()

Energynew = USRBIN(filenames[2], pathNew, normfactor)
Energynew.read()
Energynew.contourpath = path
Energynew.loadGeometryFile('ATLASclosed.dat',3,4)


Dosenew = USRBIN(filenames[1], pathNew, normfactor)
Dosenew.read()


pseudodensitynew = Energynew

#newcube = np.zeros(Energynew.cube.shape)
#for x in range(int(Energynew.cube.shape[0])):
#    for y in range(int(Energynew.cube.shape[1])):
#        for z in range(int(Energynew.cube.shape[2])):
#            if Energynew.cube[x,y,z] == 0 and Dosenew.cube[x,y,z] == 0:
#                newcube[x,y,z] = 0
#            else:
#                newcube[x,y,z] = Energynew.cube[x,y,z]/Dosenew.cube[x,y,z]
#            
#newcubeB = np.divide(Energynew.cube, Dosenew.cube, out=np.zeros_like(Energynew.cube), where=Dosenew.cube!=0)            
#
##print np.max(newcube)
##print np.min(newcube)
##
##print np.max(newcubeB)
##print np.min(newcubeB)


pseudodensitynew.cube = np.divide(Energynew.cube, Dosenew.cube, out=np.zeros_like(Energynew.cube), where=Dosenew.cube!=0)   
pseudodensitynew.calc()
pseudodensitynew.title = 'Pseudo Density'



Siliconenew = USRBIN(filenames[5], pathNew, normfactor)
Siliconenew.read()
Siliconenew.contourpath = path
Siliconenew.loadGeometryFile('ATLASclosed.dat',3,4)
Siliconenew.title = 'SI1MEVNE'
#point1.readError()
Siliconenew.calc()


DoseEQnew = USRBIN(filenames[6], pathNew, normfactor)
DoseEQnew.read()
DoseEQnew.contourpath = path
DoseEQnew.loadGeometryFile('ATLASclosed.dat',3,4)
DoseEQnew.title = 'Prompt Dose EQ'
#point1.readError()
DoseEQnew.calc()

EEnew = USRBIN(filenames[-2], pathNew, normfactor)
EEnew.read()
EEnew.contourpath = path
EEnew.loadGeometryFile('ATLASclosed.dat',3,4)
EEnew.title = 'Electrons and Positrons'
#point1.readError()
EEnew.calc()





#----------OLD------------------------------------------------------------------------------------------
os.chdir(pathOld)
filenames = sorted(glob.glob('*.lis'))


HEHADold = USRBIN(filenames[0], pathOld, normfactor)
HEHADold.read()
HEHADold.contourpath = path
HEHADold.loadGeometryFile('ATLASclosed.dat',3,4)
#point1.readError()
HEHADold.calc()


Neutronsold = USRBIN(filenames[3], pathOld, normfactor)
Neutronsold.read()
Neutronsold.contourpath = path
Neutronsold.loadGeometryFile('ATLASclosed.dat',3,4)
#point1.readError()
Neutronsold.calc()


ChargedHadronsold = USRBIN(filenames[4], pathOld, normfactor)
ChargedHadronsold.read()
ChargedHadronsold.contourpath = path
ChargedHadronsold.loadGeometryFile('ATLASclosed.dat',3,4)
#point1.readError()
ChargedHadronsold.calc()

Energyold = USRBIN(filenames[2], pathOld, normfactor)
Energyold.read()
Energyold.contourpath = path
Energyold.loadGeometryFile('ATLASclosed.dat',3,4)
#point1.readError()

Doseold = USRBIN(filenames[1], pathOld, normfactor)
Doseold.read()


pseudodensityold = Energyold
pseudodensityold.cube = np.divide(Energyold.cube, Doseold.cube, out=np.zeros_like(Energyold.cube), where=Doseold.cube!=0)  
pseudodensityold.calc()


Siliconeold = USRBIN(filenames[5], pathOld, normfactor)
Siliconeold.read()
Siliconeold.contourpath = path
Siliconeold.loadGeometryFile('ATLASclosed.dat',3,4)
#point1.readError()
Siliconeold.calc()

DoseEQold = USRBIN(filenames[6], pathOld, normfactor)
DoseEQold.read()
DoseEQold.contourpath = path
DoseEQold.loadGeometryFile('ATLASclosed.dat',3,4)
#point1.readError()
DoseEQold.calc()

EEold = USRBIN(filenames[-2], pathOld, normfactor)
EEold.read()
EEold.contourpath = path
EEold.loadGeometryFile('ATLASclosed.dat',3,4)
#point1.readError()
EEold.calc()





hehad = loadGeant4(path,'Geant4hehad.dat' )
neutrons = loadGeant4(path,'Geant4neutrons.dat' )
chargedHadrons = loadGeant4(path,'Geant4chargedHadrons.dat' )
pseudodensity = loadGeant4(path,'Geant4pseudodensity.dat' )
niel = loadGeant4(path,'Geant4niel.dat' )




compare(HEHADold, HEHADnew, hehad, 'Hadrons > 20 MeV')
#compare(Neutronsold, Neutronsnew, neutrons, 'Neutrons > 10 keV')
#compare(ChargedHadronsold, ChargedHadronsnew, chargedHadrons, 'Charged Hadrons')
#compare(pseudodensityold, pseudodensitynew, pseudodensity, 'Pseudodensity')
#compare(Siliconeold, Siliconenew, niel, 'SI1MEVNE')




compareFlukaOnly(DoseEQold, DoseEQnew, 'Prompt Dose EQ')
compareFlukaOnly(HEHADold, HEHADnew, 'Hadrons > 20 MeV')
compareFlukaOnly(Neutronsold, Neutronsnew, 'Neutrons > 10 keV')
compareFlukaOnly(ChargedHadronsold, ChargedHadronsnew, 'Charged Hadrons')
compareFlukaOnly(pseudodensityold, pseudodensitynew,  'Pseudodensity')
compareFlukaOnly(Siliconeold, Siliconenew, 'SI1MEVNE')
compareFlukaOnly(EEold, EEnew, 'Electrons & Positrons')






def allintegrated(*args):
    
    xes = range(0,2400,2400/240)
    
    fig = plt.figure()
        
    
    ax = plt.subplot(121)

    for i in range(0,len(args), 2):
    
        old = args[i]
        new = args[i +1]
    
        plt.plot(xes, new.centre/old.centre, label = new.title, linestyle = '-')
        #plt.plot(xes, old.centre, label = 'Old Geo', linestyle = '-')
    plt.axhline(y=1, color='k', linestyle='-')
    plt.legend()
    plt.grid(linewidth = 0.3)
    plt.ylabel('Ratio' , fontsize = 14)
    #plt.xlabel('z [cm from IP]', fontsize = 18)
    plt.xlabel('z [cm from IP]', fontsize = 18)
    plt.title('Central axis', fontsize = 16)
    plt.xlim(0,1000)
    plt.ylim(0.65,1.3)
    
    
    ax = plt.subplot(122)
    
    for i in range(0,len(args), 2):

        old = args[i]
        new = args[i +1]        
    
        image1 = new.cube[0:,int(new.cube.shape[1]/2), 0:]
        image2 = old.cube[0:,int(old.cube.shape[1]/2), 0:]
        
        image1integrated = np.zeros([240])
        image2integrated = np.zeros([240])
        for i in range(240):
            image1integrated[i] = sum(image1[0:,i])
            image2integrated[i] = sum(image2[0:,i])
            
        plt.plot(xes, image1integrated/image2integrated, label = new.title, linestyle = '-')
    plt.axhline(y=1, color='k', linestyle='-')
    plt.legend()
    plt.grid(linewidth = 0.3)
    plt.ylabel('Ratio' , fontsize = 14)
    plt.xlabel('z [cm from IP]', fontsize = 18)
    plt.title('Integrated', fontsize = 16)
    plt.xlim(0,1000)
    plt.ylim(0.75,1.25)
    
    
    
    plt.suptitle('Fluence comparison. New/old Geometry', fontsize = 24)
    
    
    plt.show()


allintegrated(HEHADold, HEHADnew, Neutronsold, Neutronsnew,ChargedHadronsold, ChargedHadronsnew, Siliconeold, Siliconenew, DoseEQold, DoseEQnew, EEold, EEnew)

def ratioplots2d(*args):
    
    for i in range(0,len(args), 2):
        
        old = args[i]
        new = args[i +1]
        lim = 1.5
        
        fig = plt.figure()
        
        ax = plt.subplot(111)
        
        maxY = int(new.info['rmax'][0])
        widthY = int(new.info['rwidth'][0])
        maxX = int(new.info['zmax'][0])
        widthX = int(new.info['zwidth'][0])
        
        
        X, Y = np.meshgrid(range(0,maxX, widthX),range(-maxY,maxY, widthY))
        
        image1= new.cube[0:,int(new.cube.shape[1]/2), 0:]
        image2= old.cube[0:,int(old.cube.shape[1]/2), 0:]
        
        image = image1/image2
        
        plt.pcolor(X, Y, image, norm=LogNorm(vmin=1/float(lim), vmax=lim),cmap = 'seismic')
        cbar = plt.colorbar()
        cbar.set_label('Ratio', fontsize = 18)
        plt.title(new.title + '. New/Old Geo', fontsize = 16)
        plt.ylabel('R [cm from IP]', fontsize = 18)
        plt.xlabel('Z [cm from IP]', fontsize = 18)
        ax = old.drawGeo(ax)
        plt.xlim(0,900)
        plt.ylim(-300,300)
        xlength = 16
        fig.set_size_inches(xlength, xlength/1.618)
        plt.savefig(new.title[0:7] + '.pdf')
        plt.show()


ratioplots2d(HEHADold, HEHADnew , Neutronsold, Neutronsnew,ChargedHadronsold, ChargedHadronsnew, Siliconeold, Siliconenew, DoseEQold, DoseEQnew, EEold, EEnew)




def compareFlukaGeant4IM(*args):

     rstop = 40
     zstop = 80    
     lim = 1.5   
     
     
     for i in range(0,len(args), 3):
        
        old = args[i]
        new = args[i +1]
        geant4 = args[i +2]

    

        
        fig = plt.figure()
        
        
        widthY = int(new.info['rwidth'][0])
        maxY = widthY * rstop #int(new.info['rmax'][0])
        
        widthX = int(new.info['zwidth'][0])
        maxX = widthX*zstop
        
        
        X, Y = np.meshgrid(range(0,maxX, widthX),range(-maxY,maxY, widthY))
        
        
        image1= new.cube[(120-rstop):(120+rstop),int(new.cube.shape[1]/2), 0:zstop]/geant4[(120-rstop):(120+rstop), 0:zstop]
        image2= old.cube[(120-rstop):(120+rstop),int(old.cube.shape[1]/2), 0:zstop]/geant4[(120-rstop):(120+rstop), 0:zstop]
        

        lim = float(5)
        
        
        ax = plt.subplot(221)
    
        
        plt.pcolor(X, Y,image1, norm=LogNorm(vmin=1/lim, vmax=lim) ,cmap = 'seismic')
        cbar = plt.colorbar()
        cbar.set_label('Ratio', fontsize = 12)
        plt.title('NewGeo / Geant4', fontsize = 16)
        plt.ylabel('R [cm from IP]', fontsize = 12)
        plt.xlabel('Z [cm from IP]', fontsize = 12)
        ax = new.drawGeo(ax)
        plt.xlim(0,zstop*10)
        plt.ylim(-rstop*10,rstop*10)
        
        ax = plt.subplot(222)
    
        
        plt.pcolor(X, Y,image2, norm=LogNorm(vmin=1/lim, vmax=lim) ,cmap = 'seismic')
        cbar = plt.colorbar()
        cbar.set_label('Ratio', fontsize = 12)
        plt.title('Old Geo / Geant4')
        plt.ylabel('R [cm from IP]', fontsize = 12)
        plt.xlabel('Z [cm from IP]', fontsize = 12)
        plt.title('Old Geo / Geant4', fontsize = 16)
        ax = new.drawGeo(ax)
        plt.xlim(0,zstop*10)
        plt.ylim(-rstop*10,rstop*10)     
        
        ax = plt.subplot(223)
    
        vmax = max([image1.max(), image2.max()])
        vmin = np.min([np.min(image1[np.nonzero(image1)]), np.min(image2[np.nonzero(image2)]) ])
    
        bins = np.logspace(np.log10(vmin),np.log10(vmax),100) #range(int(round(vmax)))
        image1hist = image1[0:int(image1.shape[0]/2),0:].flatten()
        image2hist = image2[0:int(image2.shape[0]/2),0:].flatten()
        print sum(image1hist)/len(image1hist)
        print sum(image2hist)/len(image2hist)
        plt.hist(image1hist[np.isfinite(image1hist)], bins = bins, label = 'New Geo / Geant4' , alpha = 0.7) #
        plt.hist(image2hist[np.isfinite(image2hist)],  bins = bins , label = 'Old Geo / Geant4', alpha = 0.6) #     
    
        plt.legend()
        plt.grid(linewidth = 0.3)
        plt.yscale('log', nonposy='clip')
        plt.xscale('log', nonposy='clip')
        
        plt.xlabel('Ratios', fontsize = 16)
        plt.ylabel('Counts', fontsize = 16)
    
    
        ax = plt.subplot(224)
    
        xes = range(0,zstop*10,zstop*10/zstop)
    
        oldint = np.zeros(zstop)
        newint = np.zeros(zstop)
        geantint = np.zeros(zstop)
    
        for i in range(zstop):
            oldint[i] = sum(image2[0:,i])
            newint[i] = sum(image1[0:,i])
            geantint[i] = sum(geant4[0:,i])
    
        plt.plot(xes ,oldint, label = 'Old Geo')
        plt.plot(xes ,newint, label = 'New Geo')
        plt.plot(xes ,geantint, label = 'Geant4')
        plt.legend()
        plt.grid(linewidth = 0.3)
    
    
    
        plt.suptitle(new.title, fontsize = 22)
        xlength = 16
        fig.set_size_inches(xlength, xlength/1.618)
        plt.savefig('FLUKAGeant4_' +new.title[0:7] + '.pdf')
        plt.show()
        
        
        
        
        
compareFlukaGeant4IM(pseudodensityold, pseudodensitynew, pseudodensity)

compareFlukaGeant4IM(HEHADold, HEHADnew, hehad, Neutronsold, Neutronsnew, neutrons, ChargedHadronsold, ChargedHadronsnew, chargedHadrons, Siliconeold, Siliconenew, niel)


def compareFlukaGeant4curve(*args):

     
     #linetypes = ["-", "--" , ":", "-."]
     
     r = [2,5,7,8]
     xes = range(0,2400,2400/240)
     
     for i in range(0,len(args), 3):
        
        old = args[i]
        new = args[i +1]
        geant4 = args[i +2]

        image1 = new.cube[0:,int(new.cube.shape[1]/2), 0:]
        image2 = old.cube[0:,int(old.cube.shape[1]/2), 0:]

        fig = plt.figure()
        
        
        for j in range(len(r)):
            
            plt.subplot(2,2,j+1)
            
            plt.plot(xes,image1[120+r[j],0:], label = "New Geo")
            plt.plot(xes,image2[120+r[j],0:], label = "Old Geo") 
            plt.plot(xes,geant4[120+r[j],0:], label = "Geant4")
            plt.title("R = " + str(r[j]*10) + " cm")

            plt.legend()
            plt.grid(linewidth = 0.3)
            if j == 2 or j == 3:
                plt.xlabel('z [cm from IP]')
            
            plt.xlim(0,800)
            
        plt.suptitle(new.title, fontsize = 22)
        xlength = 16
        fig.set_size_inches(xlength, xlength/1.618)
        plt.savefig('CurvesATRs_' +new.title[0:7] + '.pdf')        
        plt.show()
        

compareFlukaGeant4curve(pseudodensityold, pseudodensitynew, pseudodensity)

compareFlukaGeant4curve(HEHADold, HEHADnew, hehad, Neutronsold, Neutronsnew, neutrons, ChargedHadronsold, ChargedHadronsnew, chargedHadrons, Siliconeold, Siliconenew, niel)

#compare(pseudodensityold, pseudodensitynew, pseudodensity, 'Pseudodensity')


        
        
        
        
        
        