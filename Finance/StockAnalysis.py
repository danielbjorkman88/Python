# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 11:56:35 2020

@author: malyr
"""

#InvestPy installation:
#import sys
#!{sys.executable} -m pip install investpy -U

import investpy
from datetime import datetime
from StockClass import *
from MarketClass import *


country = 'United States'
#country = 'sweden'
funds_list = investpy.get_funds_list(country=country)
fundName = funds_list[10]
sampling_from = datetime(2014, 1, 1,)
compare_start = datetime(2015, 1, 20,) 
compare_end = datetime(2020, 2, 18,)


country = 'United States'

name = "Uniusdt"
name = 'Bitcoin'


crypt = Crypto(name, country, sampling_from , compare_start , compare_end)
#crypt.plotMe()

name = 'Tether'
sampling_from = datetime(2017, 3, 23,)
compare_start = sampling_from
crypt = Crypto(name, country, sampling_from , compare_start , compare_end)
crypt.plotMe()



cryptos = investpy.get_cryptos_list()

names = []
names.append('Bitcoin')
names.append('Obsidian')
names.append("Ethereum")
names.append("Litecoin")


#Market
marketName = 'Crypto Market'
country = 'United States'
market1 = CryptoMarket(marketName, names, country, sampling_from , compare_start , compare_end)
market1.plotMe( )


#name = "BAND, Band Protocol"

#
##Stocks
#fund1 = Stock(fundName, country, sampling_from , compare_start , compare_end)
##fund1.plotMe()
#
#
#names = []
#for i in range(len(funds_list)):
#    names.append(funds_list[i])
#
#    
#    
##Market
#marketName = 'Marknad1'
#market1 = Market(marketName, names, country, sampling_from , compare_start , compare_end)
#market1.plotMe( )
##market1.compareDates(datetime(2019, 1, 15,) , datetime(2020, 1, 20,))
##market1.plotMe( )
#
#

