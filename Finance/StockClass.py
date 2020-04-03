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
from datetime import datetime
import scipy


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
        
        f = scipy.interpolate.interp1d(self.daysSinceToday, self.closingValues)
        diff = f(self.daysSinceOrigo(compare_end)) - f(daysSinceOrigo(compare_start))
    
        return diff
        
    def loadData(self):
        from_date = str(self.start_date.day) + '/' + str(self.start_date.month) + '/' + str(self.start_date.year)
        to_date = str(self.end_date.day) + '/' + str(self.end_date.month) + '/' + str(self.end_date.year)
        self.df = investpy.get_fund_historical_data(fund=self.name, country=self.country, from_date= from_date, to_date= to_date)

        self.parseDF()



    def plotMe(self):
        plt.figure()
        
        plt.plot(self.daysSinceToday, self.closingValues, label = self.name, linewidth = 2)
        plt.xlabel('[Days since today]')
        plt.ylabel('[TBI]')
        plt.xticks(rotation=45)
        plt.axvline(x=0 , label = 'Today', color = 'r', linewidth = 1)
        
        
        newyear2019 = datetime(2019,12,31,23,59,59)
        timedifference = datetime.today() - newyear2019
        newyearsOrigodifference = timedifference.total_seconds()/(60*60*24)
        plt.axvline(x= -newyearsOrigodifference, color = 'k', linestyle = '-', label = 'Year shift', linewidth = 0.5)
        for i in range(10):
            plt.axvline(x=-365*i - newyearsOrigodifference, color = 'k', linestyle = '--', linewidth = 0.5)

        plt.legend()
        
        plt.xlim(-120 , 10)
        
        plt.show()



#country = 'sweden'
#
#start_date = datetime(2019, 12, 20,)
#end_date = datetime.now()
#
#fund1 = Stock(fund, country, start_date , end_date)
#fund1.loadData()
#fund1.plotMe()











