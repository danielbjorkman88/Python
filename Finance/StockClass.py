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
    def __init__(self, name, country, start_date):
        self.name = name
        self.country = country
        self.start_date = start_date
        self.start_date_str = str(self.start_date.day) + '/' + str(self.start_date.month) + '/' + str(self.start_date.year)
        self.end_date = datetime.now()
        self.end_date_str = str(self.end_date.day) + '/' + str(self.end_date.month) + '/' + str(self.end_date.year)
        self.df = []
        self.dates = []
        self.closingValues = []
        self.closingValuesNormed = []
        self.openingValues = []
        self.daysSinceToday = []
        self.currency = []
        self.compare_start = []
        self.compare_start_str = []
        self.compare_end = []
        self.compare_end_str = []
        self.diff = []
        self.AVGline_xes = []
        self.AVGline_yes = []
        self.function = []
        self.slope = []
        self.intercept = []
        self.r_value = []
        self.p_value = []
        self.std_err = []
        self.lifespan = []
        
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
        
        if start > min(self.daysSinceToday) and stop < max(self.daysSinceToday):
            self.diff = f(stop) - f(start)
        elif stop < max(self.daysSinceToday):
            self.diff = f(stop) - 0
        else:
            self.diff = 0
        
        
        
        try:
            self.AVGline_xes = (start , stop)
            self.AVGline_yes = (f(start) , f(stop))
            xes = np.arange(start,stop)
            
            self.slope, self.intercept, self.r_value, self.p_value, self.std_err = stats.linregress(xes,f(xes))
            self.AVGline_xes = (start , stop)
            self.AVGline_yes = (self.intercept , self.intercept + self.slope*(stop - start))    
        except:
            pass
        
        year = compare_start.year
        month = compare_start.month
        day = compare_start.day
        self.compare_start_str = str(year) + "-" + str(month) + "-" + str(day)
        
        year = compare_end.year
        month = compare_end.month
        day = compare_end.day
        self.compare_end_str = str(year) + "-" + str(month) + "-" + str(day)

         
        
    def loadData(self):
        from_date = self.start_date_str
        to_date = self.end_date_str 
        
        print('Loading ' + self.name , from_date , to_date)
        try:
            self.df = investpy.get_fund_historical_data(fund=self.name, country=self.country, from_date= from_date, to_date= to_date)
        except ConnectionError:
            print('Internet connection Error')
        self.parseDF()
        if self.compare_start != [] and self.compare_end != []:
            self.calcAverage()


    def plotMe(self):
        plt.figure()
        
        plt.plot(self.daysSinceToday, self.closingValues, label = self.name, linewidth = 2)
        plt.xlabel('[Days ago]', fontsize = 12)
        plt.ylabel('Stock Price [TBI]' , fontsize = 12 )
        plt.xticks(rotation=45)
        plt.axvline(x=0 , label = 'Today', color = 'r', linewidth = 1)
        
        if self.compare_start != [] and self.compare_end != []:
            startX = self.daysSinceOrigo( self.compare_start)
            sizeX = self.daysSinceOrigo( self.compare_end) - startX
            rect = plt.Rectangle((startX, - 1000),
                                  sizeX,
                                  10000, color = 'b', alpha = 0.2 ,  linewidth=2.5)
            plt.gca().add_patch(rect)
            plt.title(self.name + ' | '+  str(self.diff) + ' | increase between ' + self.compare_start_str + ' and ' + self.compare_end_str , fontsize = 12)
        
        newyear2019 = datetime(2019,12,31,23,59,59)
        timedifference = datetime.today() - newyear2019
        newyearsOrigodifference = timedifference.total_seconds()/(60*60*24)
        plt.axvline(x= -newyearsOrigodifference, color = 'k', linestyle = '-', label = 'Year shift', linewidth = 0.5)
        for i in range(10):
            plt.axvline(x=-365*i - newyearsOrigodifference, color = 'k', linestyle = '--', linewidth = 0.5)


        plt.plot(self.AVGline_xes , self.AVGline_yes , color = 'k' , linewidth = 2 , label = 'Linear interpolation')

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











