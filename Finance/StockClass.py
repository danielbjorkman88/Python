# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 10:56:14 2020

@author: malyr
"""

#historial web scraping

#import sys
#!{sys.executable} -m pip install investpy -U

import investpy
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
#import datetime
#'01/01/2015', end='01/01/2019',

#df = investpy.get_stock_recent_data(stock='bbva', country='spain',  as_json=False, order='ascending')
#
#
#funds_ = investpy.get_fund_historical_data(fund='bbva multiactivo conservador pp', from_date='01/01/2015', to_date='01/01/2019', as_json=False, order='ascending')
#
#
#stocks = investpy.get_stocks_list()
#
#funds = investpy.get_funds_list()
#
#countries = investpy.get_fund_countries()
##df = investpy.get_stock_historical_data(stock='bbva', country='spain', from_date='01/01/2015', to_date='01/01/2019')
#
##W1DOW
#df = investpy.get_stock_historical_data(stock='TS', country= 'spain', from_date='01/01/2015', to_date='01/01/2019')
#



country = 'sweden'

start_date = datetime(2019, 12, 20,)
end_date = datetime.now()



funds_df = investpy.get_funds(country=country)
countries = investpy.get_fund_countries()
funds_list = investpy.get_funds_list(country=country)
# Retrieve a dictionary with all the funds and all of their information fields
funds_dict = investpy.get_funds_dict(country=country)

fund = funds_list[10]


class Stock:
    def __init__(self, name, start_date , end_date):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.df = []
        self.dates = []
        self.closingValues = []
        self.daysSinceToday = []
        
    def parseDF(self):
        
        dates = []
        datetimes = []
        daysSinceToday = []
        today = datetime.now()
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
            
        self.dates = dates
        self.closingValues = closingValues
        self.daysSinceToday = daysSinceToday    
    
        return dates, closingValues, daysSinceToday
    def loadData(self):
        from_date = str(self.start_date.day) + '/' + str(self.start_date.month) + '/' + str(self.start_date.year)
        to_date = str(self.end_date.day) + '/' + str(self.end_date.month) + '/' + str(self.end_date.year)
        self.df = investpy.get_fund_historical_data(fund=fund, country=country, from_date= from_date, to_date= to_date)

        self.parseDF()

#dates, values , daysSinceToday = parseDF(df)


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


fund1 = Stock(fund, start_date , end_date)
fund1.loadData()
fund1.plotMe()











