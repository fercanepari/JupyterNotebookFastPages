# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 01:04:24 2021

@author: CanepariF
"""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import yfinance as yf
import datetime as dt

#%matplotlib notebook

asset = 'TSLA'

#frame = yf.download(asset, start='2021-09-15', end='2021-09-20',interval='1m',)
#print(frame)

def getminutedata(symbol, dateTo):
    frame = yf.download(asset, start=dateTo, interval='1m')
    frame = frame.iloc[:,:6]
    frame.columns = ['Time','Open','High','Low','Close','Volume']
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)
    return frame    

def animate(i):
    start = dt.datetime.now() + dt.timedelta(days=-5)
    data = getminutedata(asset, start)
    plt.cla()
    plt.plot(data.index, data.Close)
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title(asset)
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    print(data)

ani = FuncAnimation(plt.gcf(), animate, 1000)

plt.tight_layout()
plt.show()

    



