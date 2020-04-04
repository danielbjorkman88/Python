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
        self.name = names
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
        

    def loadData(self):
        
        for X in self.names:
            tmp = Stock(X, self.country, self.start_date )
            tmp.loadData()
            if self.compare_start != [] and self.compare_end != []:
                tmp.compareDates(self.compare_start  , self.compare_end )
            self.stock_list.apend(tmp)
        self.parseDF()
        

        if self.compare_start != [] and self.compare_end != []:
            self.calcAverage()











     