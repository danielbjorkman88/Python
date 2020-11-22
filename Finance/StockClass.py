# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 10:56:14 2020

@author: malyr
"""

#import sys
#!{sys.executable} -m pip install investpy -U

import investpy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime
from scipy.interpolate import interp1d
from scipy import stats


class Stock:
    def __init__(self, name, country, sampling_from, compare_start , compare_end):
        self.name = name
        self.country = country
        self.sampling_from = sampling_from
        self.sampling_from_str = str(self.sampling_from.day) + '/' + str(self.sampling_from.month) + '/' + str(self.sampling_from.year)
        self.end_date = datetime.now()
        self.end_date_str = str(self.end_date.day) + '/' + str(self.end_date.month) + '/' + str(self.end_date.year)
        self.df = []
        self.dates = []
        self.closingValues = [0]
        self.closingValuesNormed = [0]
        self.openingValues = [0]
        self.daysSinceToday = [0]
        self.currency = 'SEK' #Placeholder
        self.compare_start = compare_start 
        self.compare_start_str = str(self.compare_start.year) + "-" + str(self.compare_start.month) + "-" + str(self.compare_start.day)
        self.compare_end = compare_end
        self.compare_end_str = str(self.compare_end.year) + "-" + str(self.compare_end.month) + "-" + str(self.compare_end.day)
        self.diff = []
        self.AVGline_xes = [0,0]
        self.AVGline_yes = [0,0]
        self.function = []
        self.slope = 0
        self.intercept = []
        self.r_value = []
        self.p_value = []
        self.std_err = []
        self.lifespan = []
        
        self.loadData()
        
        try:
            self.compareDates( self.compare_start, self.compare_end)
        except:
            print('Unable to compare')
        
    def parseDF(self):
        
        dates = []
        datetimes = []
        daysSinceToday = []
        today = datetime.now()
        openingValues = np.zeros(len(self.df))
        closingValues = np.zeros(len(self.df))
        
        for i in range(len(self.df)):
            datetimeObject = self.df.index[i].to_pydatetime()
            datetimes.append(datetimeObject)
            timediff = round((datetimeObject - today).total_seconds()/(60*60*24))
            daysSinceToday.append(timediff)
            
            year = self.df.index[i].year
            month = self.df.index[i].month
            day = self.df.index[i].day
            dates.append(str(year) + "-" + str(month) + "-" + str(day))
            closingValues[i] = self.df.Close[i]
            openingValues[i] = self.df.Open[i]
            

        self.dates = dates
        self.closingValues = closingValues
        self.closingValuesNormed = self.closingValues/max(self.closingValues)
        self.daysSinceToday = daysSinceToday 
        self.currency = self.df.Currency[0]
        self.lifespan = abs(min(daysSinceToday))#days
    
    def daysSinceOrigo(self, date):
        timedifference = date - datetime.today()
        return timedifference.total_seconds()/(60*60*24)
        
    def compareDates(self, compare_start, compare_end):
           
        self.compare_start = compare_start
        self.compare_end = compare_end    
        
        f = interp1d(self.daysSinceToday, self.closingValues)
        self.function = f
        stop = self.daysSinceOrigo(self.compare_end)
        start = self.daysSinceOrigo(self.compare_start)
        
        #print(start , stop , min(self.daysSinceToday))
        
        if start > min(self.daysSinceToday) and stop < max(self.daysSinceToday):
            self.diff = f(stop) - f(start)
            self.AVGline_xes = (start , stop)
            self.AVGline_yes = (f(start) , f(stop))
        elif stop < max(self.daysSinceToday):
            self.diff = f(stop) - self.closingValues[0]
            self.AVGline_xes = (min(self.daysSinceToday) , stop)
            self.AVGline_yes = (self.closingValues[0], f(stop) - 0 )
        else:
            self.diff = 0
            self.AVGline_xes = (0 , 0)
            self.AVGline_yes = (0 , 0)
        
        try:
            self.slope = ( self.AVGline_yes[1] - self.AVGline_yes[0]) / ( self.AVGline_xes[1] - self.AVGline_xes[0])
        except:
            self.slope = 0
        
        year = compare_start.year
        month = compare_start.month
        day = compare_start.day
        self.compare_start_str = str(year) + "-" + str(month) + "-" + str(day)
        
        year = compare_end.year
        month = compare_end.month
        day = compare_end.day
        self.compare_end_str = str(year) + "-" + str(month) + "-" + str(day)

         
        
    def loadData(self):
        
        print('Loading ' , self.name  )
        try:
            self.df = investpy.get_fund_historical_data(fund=self.name, country=self.country, from_date= self.sampling_from_str, to_date= self.end_date_str )
            self.parseDF()
        except ConnectionError:
            print('Internet connection Error')
        except ValueError:
            print('No data found')



    def plotMe(self):
        fig = plt.figure()

        
        plt.plot(self.daysSinceToday, self.closingValues, label = self.name + ' | k = ' + str(round(self.slope,5)), linewidth = 2)
        plt.xlabel('[Days since today]', fontsize = 12)
        plt.ylabel('Stock Value [' + self.currency + ']' , fontsize = 12 )
        plt.xticks(rotation=45)
        plt.axvline(x=0 , label = 'Today', color = 'r', linewidth = 1)
        

        startX = self.daysSinceOrigo( self.compare_start)
        sizeX = self.daysSinceOrigo( self.compare_end) - startX
        rect = plt.Rectangle((startX, - 1000),
                              sizeX,
                              10000, color = 'b', alpha = 0.2 ,  edgecolor = None)
        plt.gca().add_patch(rect)
        plt.title(self.name + ' | '+  str(self.diff) + ' | increase between ' + self.compare_start_str + ' and ' + self.compare_end_str , fontsize = 12)
    
        newyear2019 = datetime(2019,12,31,23,59,59)
        timedifference = datetime.today() - newyear2019
        newyearsOrigodifference = timedifference.total_seconds()/(60*60*24)
        plt.axvline(x= -newyearsOrigodifference, color = 'k', linestyle = '-', label = 'Year shift', linewidth = 0.5)
        for i in range(10):
            plt.axvline(x=-365*i - newyearsOrigodifference, color = 'k', linestyle = '--', linewidth = 0.5)


        plt.plot(self.AVGline_xes , self.AVGline_yes , color = 'k' , linewidth = 2  )

        plt.legend()
        plt.xlim(min(min(self.daysSinceToday)*1.1, self.daysSinceOrigo(self.compare_start))*1.1 , 10)
        plt.ylim(min(self.closingValues)*0.95,max(self.closingValues)*1.05)
        
        xlength = 12
        fig.set_size_inches(xlength, xlength/1.618)
        
        if self.AVGline_yes[1] == 0:
            print('Warning: Compare start outside sampling range')
        
        plt.show()






class Crypto(Stock):
    def loadData(self):
        
        print('Loading ' , self.name  )
        try:
            self.df = investpy.get_crypto_historical_data(crypto=self.name, from_date= self.sampling_from_str, to_date= self.end_date_str )
            self.parseDF()
        except ConnectionError:
            print('Internet connection Error')
        except ValueError:
            print('No data found')





    def plotMe(self):
        fig = plt.figure()

        
        plt.plot(self.daysSinceToday, self.closingValues, label = '{} | k = {} [val/days]'.format(self.name, round(self.slope,8)), linewidth = 2)
        plt.xlabel('[Days since today]', fontsize = 12)
        plt.ylabel('Crypto Value [' + self.currency + ']' , fontsize = 12 )
        plt.xticks(rotation=45)
        plt.axvline(x=0 , label = 'Today', color = 'r', linewidth = 1)
        

        startX = self.daysSinceOrigo( self.compare_start)
        sizeX = self.daysSinceOrigo( self.compare_end) - startX
        rect = plt.Rectangle((startX, - 1000),
                              sizeX,
                              100000000, color = 'b', alpha = 0.08 ,  edgecolor = None)
        plt.gca().add_patch(rect)
        plt.title('{} | Diff: {} | Analysis range from {} to {}'.format(self.name, self.diff, self.compare_start_str, self.compare_end_str)   , fontsize = 12)
    
        newyear2019 = datetime(2019,12,31,23,59,59)
        timedifference = datetime.today() - newyear2019
        newyearsOrigodifference = timedifference.total_seconds()/(60*60*24)
        plt.axvline(x= -newyearsOrigodifference, color = 'k', linestyle = '-', label = 'Year shift', linewidth = 0.5)
        for i in range(10):
            plt.axvline(x=-365*i - newyearsOrigodifference, color = 'k', linestyle = '--', linewidth = 0.5)


        plt.plot(self.AVGline_xes , self.AVGline_yes , color = 'k' , linewidth = 0.5  )

        plt.legend()
        plt.xlim(min(min(self.daysSinceToday)*1.1, self.daysSinceOrigo(self.compare_start))*1.1 , 10)
        plt.ylim(min(self.closingValues)*0.95,max(self.closingValues)*1.05)
        
        xlength = 12
        fig.set_size_inches(xlength, xlength/1.618)
        
        if self.AVGline_yes[1] == 0:
            print('Warning: Compare start outside sampling range')
        
        plt.show()


