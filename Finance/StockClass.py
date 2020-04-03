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



class Stock:
    def __init__(self, name, country, start_date , end_date):
        self.name = name
        self.country = country
        self.start_date = start_date
        self.end_date = end_date
        self.df = []
        self.dates = []
        self.closingValues = []
        self.openingValues = []
        self.daysSinceToday = []
        self.currency = []
        self.compare_start = []
        self.compare_end = []
        self.diff = []
        self.AVGline_xes = []
        self.AVGline_yes = []
        
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
        self.daysSinceToday = daysSinceToday 
        self.currency = self.df.Currency[0]
    
    def daysSinceOrigo(self, date):
        timedifference = date - datetime.today()
        return timedifference.total_seconds()/(60*60*24)
        
    def compareDates(self, compare_start, compare_end):
        
        f = interp1d(self.daysSinceToday, self.closingValues)
        stop = self.daysSinceOrigo(compare_end)
        start = self.daysSinceOrigo(compare_start)
        diff = f(stop) - f(start)
        
        self.AVGline_xes = (start , stop)
        self.AVGline_yes = (f(start) , f(stop))
        self.compare_start = compare_start
        self.compare_end = compare_end
        self.diff = diff
    
        return diff
         
        
    def loadData(self):
        from_date = str(self.start_date.day) + '/' + str(self.start_date.month) + '/' + str(self.start_date.year)
        to_date = str(self.end_date.day) + '/' + str(self.end_date.month) + '/' + str(self.end_date.year)
        self.df = investpy.get_fund_historical_data(fund=self.name, country=self.country, from_date= from_date, to_date= to_date)

        self.parseDF()
        if self.compare_start != [] and self.compare_end != []:
            self.calcAverage()


    def plotMe(self):
        plt.figure()
        
        plt.plot(self.daysSinceToday, self.closingValues, label = self.name, linewidth = 2)
        plt.xlabel('[Days since today]')
        plt.ylabel('[TBI]')
        plt.xticks(rotation=45)
        plt.axvline(x=0 , label = 'Today', color = 'r', linewidth = 1)
        
        if self.compare_start != [] and self.compare_end != []:
            startX = self.daysSinceOrigo( self.compare_start)
            sizeX = self.daysSinceOrigo( self.compare_end) - startX
            rect = plt.Rectangle((startX, - 1000),
                                  sizeX,
                                  10000, color = 'b', alpha = 0.2 ,  linewidth=2.5)
            plt.gca().add_patch(rect)
        
        newyear2019 = datetime(2019,12,31,23,59,59)
        timedifference = datetime.today() - newyear2019
        newyearsOrigodifference = timedifference.total_seconds()/(60*60*24)
        plt.axvline(x= -newyearsOrigodifference, color = 'k', linestyle = '-', label = 'Year shift', linewidth = 0.5)
        for i in range(10):
            plt.axvline(x=-365*i - newyearsOrigodifference, color = 'k', linestyle = '--', linewidth = 0.5)


        plt.plot(self.AVGline_xes , self.AVGline_yes , color = 'k' , linewidth = 2 , label = 'AVGline')

        plt.legend()
        plt.xlim(min(self.daysSinceToday)*1.1 , 10)
        plt.ylim(min(self.closingValues)*0.95,max(self.closingValues)*1.05)
        
        plt.show()



#country = 'sweden'
#
#start_date = datetime(2019, 12, 20,)
#end_date = datetime.now()
#
#fund1 = Stock(fund, country, start_date , end_date)
#fund1.loadData()
#fund1.plotMe()











