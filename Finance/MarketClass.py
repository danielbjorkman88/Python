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
        self.name = names
        self.country = country
        self.start_date = start_date
        self.end_date = datetime.now()
        self.df = []
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
        
    def daysSinceOrigo(self, date):
        timedifference = date - datetime.today()
        return timedifference.total_seconds()/(60*60*24)
   













     