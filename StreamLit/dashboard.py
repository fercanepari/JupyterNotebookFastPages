# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 09:48:21 2021

@author: CanepariF
"""

import streamlit as st
import yfinance as yf
import pandas as pd
#import datetime
import matplotlib.pyplot as plt

st.title("Finance dashboard")

tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
tickers = tickers.Symbol.to_list()

tickers = [i.replace('.','-') for i in tickers]
#tickers = ('TSLA','AAPL','MSFT','BTC-USD','ETH-USD')

#dropdown = tickers 
dropdown = st.multiselect('Pick your assets', tickers)


start = st.date_input('Start', value=pd.to_datetime('2021-01-01'))
end = st.date_input('End', value=pd.to_datetime('today'))
#start = datetime.date(2021, 1, 1)
#end = datetime.date.today()

def relativeRet(df):
    rel = df.pct_change()
    cumret = (1+rel).cumprod()-1
    cumret = cumret.fillna(0)
    return cumret
    
def get_data(symbols, start, end):
    """Read stock data (adjusted close) for given symbols from yahoo finance."""

    df_temp = yf.download(symbols, start, end)['Adj Close']
    df_temp = df_temp.fillna(method='bfill')        
    return df_temp


def get_rolling_mean(values, window):
    """Return rolling mean of given values, using specified window size."""
    return values.rolling(window=window).mean()

def get_rolling_std(values, window):
    """Return rolling standard deviation of given values, using specified window size."""
    # TODO: Compute and return rolling standard deviation
    return values.rolling(window=window).std()

def get_bollinger_bands(rm, rstd):
    """Return upper and lower Bollinger Bands."""
    # TODO: Compute upper_band and lower_band
    upper_band = rm + (rstd * 2)
    lower_band = rm - (rstd * 2)
    return upper_band, lower_band

if len(dropdown) > 0:
    df = relativeRet(yf.download(dropdown, start, end)['Adj Close'])
    st.header('Returns of {}'.format(dropdown))
    st.line_chart(df)
    
    #df
    
    dfAll = get_data(dropdown, start, end)   
    #dfAll
    st.header('Bollinger bands')
    
    for ticker in dropdown:

        if len(dropdown) == 1:
            # Compute Bollinger Bands
            # 1. Compute rolling mean
            rm_Ticker = get_rolling_mean(dfAll, window=20)
            
            # 2. Compute rolling standard deviation
            rstd_Ticker = get_rolling_std(dfAll, window=20)
        
            # 3. Compute upper and lower bands
            upper_band, lower_band = get_bollinger_bands(rm_Ticker, rstd_Ticker)
            
            # Plot raw ticker values, rolling mean and Bollinger Bands
            ax = dfAll.plot(title="Bollinger Bands", label=ticker)
            rm_Ticker.plot(label='Rolling mean', ax=ax)
            upper_band.plot(label='upper band', ax=ax)
            lower_band.plot(label='lower band', ax=ax)
            
            # Add axis labels and legend
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")
            ax.legend(loc='upper left')
            
    
            plt.plot(dfAll)
            plt.title(label=ticker)
            
        else:
            # Compute Bollinger Bands
            # 1. Compute rolling mean
            rm_Ticker = get_rolling_mean(dfAll[ticker], window=20)
        
            # 2. Compute rolling standard deviation
            rstd_Ticker = get_rolling_std(dfAll[ticker], window=20)
        
            # 3. Compute upper and lower bands
            upper_band, lower_band = get_bollinger_bands(rm_Ticker, rstd_Ticker)
    
            # Plot raw ticker values, rolling mean and Bollinger Bands
            ax = dfAll[ticker].plot(title="Bollinger Bands", label=ticker)
            rm_Ticker.plot(label='Rolling mean', ax=ax)
            upper_band.plot(label='upper band', ax=ax)
            lower_band.plot(label='lower band', ax=ax)
        
            # Add axis labels and legend
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")
            ax.legend(loc='upper left')
            #plt.show()
    
            print(dfAll[ticker])
    
            plt.plot(dfAll[ticker])
            plt.title(label=ticker)
        
            
        st.pyplot(plt)
        plt.close()


    