#
#Actiwiz Fluence and Actiwiz fluence plot
#
# Code for parsing and plotting particle fluence data
#
#Call:
#fig = plt.figure()
#data = ActiwizFluence(path, volume)
#ax = plt.subplot(111)
#ActiwizFluencePlot(data, ax, prim)
#
#prim is optional, as it is set to 1 by default
#
#
# Required python libraries: Numpy, Matplotlib
#
# Developed by Daniel Bjorkman at CERN 2017
# daniel.bjorkman@cern.ch

def ActiwizFluence(path,volume = 1):
    
    import os
    os.chdir(path)
    
    
    import numpy as np
    
    from os import listdir
    from os.path import isfile, join
    
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]           
    files = filter(lambda x: x[-4:] == '.txt' , onlyfiles)
    #print files
    #print 'hello'
    
    #files = filter(lambda x: x[-8:-4] == 'NEUT'or x[-8:-4] == 'PROT' or x[-8:-4] == '_PI+' or x[-8:-4] == '_PI-', files)
    #files = filter(lambda x: x[-7:-4] == 'Neu'or x[-7:-4] == 'Pro' or x[-7:-4] == 'Pi+' or x[-7:-4] == 'Pi-', files)
    #files = filter(lambda x: x[-7:-4] == 'neu'or x[-7:-4] == 'pro' or x[-7:-4] == 'pi+' or x[-7:-4] == 'pi-', files)
    files = sorted(files)      
    #print files
                   
         
    Out = []
    particles = []
   
    
    for i in range(len(files)):
    
        filename = files[i]
        
        f = open(filename,'r') 
        lines = f.readlines()
        
        particles.append( lines[0].split(' ')[4][:-1])
        
        
        data = np.loadtxt(filename, skiprows = 2, dtype='float')
        
        data[0:,2] = data[0:,2]/volume
        Out.append(data)

  
    Out.append(particles)
    return Out
 
def ActiwizFluencePlot(In ,ax, prim =1, line = '-'):

    import matplotlib.pyplot as plt
    
    for i in range(len(In) -1):

        data = In[i]
        particle = In[len(In)-1][i]        

        #plt.loglog((data[0:,0] +  data[0:,1])/2, data[0:,2],label= particle)
        xes = (data[0:,0] +  data[0:,1])/2
        plt.errorbar(xes, xes*prim*data[0:,2], yerr = xes*data[0:,3]*data[0:,2], label= particle, linestyle = line)
        ax.set_xscale("log", nonposx='clip')
        ax.set_yscale("log", nonposy='clip')
        plt.xlabel('E [GeV]', fontsize = 13)
        if prim == 1:
            plt.ylabel('E * Fluence [GeVcm-2pp-1]', fontsize = 16)
        else:
            plt.ylabel('E * Fluence [GeVcm-2]', fontsize = 16)
        plt.grid(True)
        plt.legend()



#path = '//rpclustersrv1/cbjorkma/LSS2/Fluence/ZSa/Out73_dir'
#
#
#data = ActiwizFluence(path, 1)