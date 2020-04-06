# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 17:30:22 2020

@author: malyr
"""

from StockClass import Stock
#import investpy
#import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime
#from scipy.interpolate import interp1d
#import operator

class Market(Stock):
    def __init__(self, marketName, names, country, start_date, compare_start , compare_end):
        #super().__init__(marketName, country, start_date, compare_start , compare_end)
        self.marketName = marketName
        self.names = names
        self.country = country
        self.start_date = start_date
        self.start_date_str = str(self.start_date.day) + '/' + str(self.start_date.month) + '/' + str(self.start_date.year)
        self.end_date = datetime.now()
        self.end_date_str = str(self.end_date.day) + '/' + str(self.end_date.month) + '/' + str(self.end_date.year)
        self.stock_list = []
        self.dates = []
        self.closingValues = []
        self.openingValues = []
        self.daysSinceToday = (0 , 0)
        self.compare_start = compare_start 
        self.compare_start_str = str(self.compare_start.year) + "-" + str(self.compare_start.month) + "-" + str(self.compare_start.day)
        self.compare_end = compare_end
        self.compare_end_str = str(self.compare_end.year) + "-" + str(self.compare_end.month) + "-" + str(self.compare_end.day)
        self.diff = []
        self.AVGline_xes = []
        self.AVGline_yes = []

        
        self.loadData()
        self.currency = self.stock_list[0].currency
        self.compareDates(self.compare_start, self.compare_end)

    def compareDates(self, compare_start, compare_end):
        self.compare_start = compare_start
        self.compare_end = compare_end
        
        
     
        year = compare_start.year
        month = compare_start.month
        day = compare_start.day
        self.compare_start_str = str(year) + "-" + str(month) + "-" + str(day)
        
        year = compare_end.year
        month = compare_end.month
        day = compare_end.day
        self.compare_end_str = str(year) + "-" + str(month) + "-" + str(day)
        
        for X in self.stock_list:
            X.compareDates(self.compare_start  , self.compare_end )
            
        
        self.stock_list.sort(key = lambda x: x.diff , reverse= True)

    def loadData(self):
        
        print('Loading ' + self.marketName + '...')
        
        for X in self.names:
            try:
                tmp = Stock(X, self.country, self.start_date, self.compare_start , self.compare_end )
                tmp.compareDates(self.compare_start  , self.compare_end )
                self.stock_list.append(tmp)
                if min(tmp.daysSinceToday) < min(self.daysSinceToday):
                    self.daysSinceToday = tmp.daysSinceToday
            except:
                print(X + ' not loaded')
                pass
        

    def plotMe(self):
        plt.figure()
        
        plt.subplot(111)
        
        for X in self.stock_list: 
            try:
                plt.plot(X.daysSinceToday, X.closingValues, label = X.name + ' | '+ str(round(X.diff,2)), linewidth = 2)
            except:
                plt.plot(X.daysSinceToday, X.closingValues, label = X.name + ' | ' , linewidth = 2)
        
        
        plt.xlabel('[Days since today]', fontsize = 12)
        plt.ylabel('Stock Value [' + self.currency + ']' , fontsize = 12 )
        plt.xticks(rotation=45)
        plt.axvline(x=0 , label = 'Today', color = 'r', linewidth = 1)
        
        
        startX = self.daysSinceOrigo( self.compare_start)
        sizeX = self.daysSinceOrigo( self.compare_end) - startX
        rect = plt.Rectangle((startX, - 1000),
                              sizeX,
                              10000, color = 'b', alpha = 0.1 ,  edgecolor = None)
        plt.gca().add_patch(rect)
        plt.title(self.marketName + ' | Between ' + self.compare_start_str + ' and ' + self.compare_end_str , fontsize = 12)
    
        newyear2019 = datetime(2019,12,31,23,59,59)
        timedifference = datetime.today() - newyear2019
        newyearsOrigodifference = timedifference.total_seconds()/(60*60*24)
        plt.axvline(x= -newyearsOrigodifference, color = 'k', linestyle = '-', label = 'Year shift', linewidth = 0.5)
        for i in range(10):
            plt.axvline(x=-365*i - newyearsOrigodifference, color = 'k', linestyle = '--', linewidth = 0.5)


        #plt.plot(self.AVGline_xes , self.AVGline_yes , color = 'k' , linewidth = 2 , label = 'Linear interpolation')

        plt.legend()
        plt.xlim(min(self.daysSinceToday)*1.02 , 10)
        #plt.ylim(min(self.closingValues)*0.95,max(self.closingValues)*1.05)
        
        
#        plt.subplot(212)
#        
#        spanlength = (self.compare_end - self.compare_start).total_seconds()/(60*60*24)
#        
#        for X in self.stock_list:
#            xes = (- spanlength/2 , spanlength/2 )
#            print(X.slope, xes[0], X.slope , xes[1])
#            yes = (X.slope*xes[0], X.slope*xes[1])
#            plt.plot(xes,yes , label = X.name)
#            
#        plt.legend()
#        
#        plt.xlabel('[Days of compare period]')
        
        plt.show()










     