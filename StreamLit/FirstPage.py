# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 01:27:23 2021

@author: CanepariF
"""

import yfinance as yf
import pandas as pd
import datetime

tickers = ('XCH')
#tickers = ('BTC')

dateTo = datetime.datetime.today()
dateFrom = dateTo + datetime.timedelta(days=-10)

df = yf.download(tickers, dateFrom, dateTo)

print(df)
         
         