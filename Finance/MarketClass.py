# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 17:30:22 2020

@author: malyr
"""

from StockClass import Stock
import investpy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime
from scipy.interpolate import interp1d

class Market(Stock):
    def __init__(self, names, country, start_date):
        super().__init__(names, country, start_date)
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
        self.daysSinceToday = []
        self.currency = []
        self.compare_start = []
        self.compare_start_str = []
        self.compare_end = []
        self.compare_end_str = []
        self.diff = []
        self.AVGline_xes = []
        self.AVGline_yes = []
        
    def calc(self):
        pass

    def loadData(self):
        
        for X in self.names:
            tmp = Stock(X, self.country, self.start_date )
            tmp.loadData()
            if self.compare_start != [] and self.compare_end != []:
                tmp.compareDates(self.compare_start  , self.compare_end )
            self.stock_list.append(tmp)
        
        self.calc()
        

    def plotMe(self):
        plt.figure()
        
        for X in self.stock_list: 
            plt.plot(X.daysSinceToday, X.closingValues, label = X.name, linewidth = 2)
        
        
        plt.xlabel('[Days since today]', fontsize = 12)
        plt.ylabel('[TBI]' , fontsize = 12 )
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


        #plt.plot(self.AVGline_xes , self.AVGline_yes , color = 'k' , linewidth = 2 , label = 'Linear interpolation')

        plt.legend()
        plt.xlim(min(self.daysSinceToday)*1.1 , 10)
        plt.ylim(min(self.closingValues)*0.95,max(self.closingValues)*1.05)
        
        
        plt.show()










     