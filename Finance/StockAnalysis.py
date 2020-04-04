# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 11:56:35 2020

@author: malyr
"""



import investpy
import numpy as np
import matplotlib.pyplot as plt
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
fund = funds_list[10]
start_date = datetime(2019, 12, 20,)

## Stocks
#fund1 = Stock(fund, country, start_date )
#fund1.loadData()
#fund1.compareDates(datetime(2020, 1, 20,) , datetime(2020, 2, 20,))
#fund1.plotMe()

names = []
names.append( funds_list[10])
names.append( funds_list[11])

market1 = Market(names, country, start_date )
market1.loadData()
market1.plotMe()





