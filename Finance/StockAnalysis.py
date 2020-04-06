# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 11:56:35 2020

@author: malyr
"""



import investpy
#import numpy as np
#import matplotlib.pyplot as plt
from datetime import datetime
from StockClass import Stock 
from MarketClass import Market 
#
#country = 'sweden'
#fund = funds_list[10]
#start_date = datetime(2019, 12, 20,)
#end_date = datetime.now()
#


#funds_df = investpy.get_funds(country=country)
#countries = investpy.get_fund_countries()
# Retrieve a dictionary with all the funds and all of their information fields
#funds_dict = investpy.get_funds_dict(country=country)




country = 'sweden'
funds_list = investpy.get_funds_list(country=country)
fundName = funds_list[10]
fundName = funds_list[11]
sampling_from = datetime(2019, 1, 1,)

compare_start = datetime(2020, 1, 20,) 
compare_end = datetime(2020, 3, 17,)

#Stocks
#fund1 = Stock(fundName, country, sampling_from , compare_start , compare_end)
#fund1.plotMe()
#fund1.compareDates(datetime(2015, 1, 20,) , datetime(2020, 2, 20,))
#fund1.plotMe()

#fund2 = Stock(fund2, country, sampling_from )
#fund2.loadData()
#fund2.compareDates(datetime(2018, 1, 20,) , datetime(2020, 2, 20,))
#fund2.plotMe()

names = []
for i in range(10,30):
    names.append(funds_list[i])
#names.append( funds_list[10])
#names.append( funds_list[11])
#names.append( funds_list[12])
#names.append( funds_list[13])

marketName = 'Marknad1'



market1 = Market(marketName, names, country, sampling_from , compare_start , compare_end)
market1.plotMe( )
market1.compareDates(datetime(2019, 12, 20,) , datetime(2020, 4, 1,))
market1.plotMe( )





