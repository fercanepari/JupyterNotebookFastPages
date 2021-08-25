# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 09:48:21 2021

@author: CanepariF
"""

import streamlit as st
import yfinance as yf
import pandas as pd

st.title("Finance dashboard")

tickers = ('TSLA','AAPL','MSFT','BTC-USD','ETH-USD')

dropdown = st.multiselect('Pick your assets', tickers)


start = st.date_input('Start', value=pd.to_datetime('2021-01-01'))
end = st.date_input('End', value=pd.to_datetime('today'))

def relativeRet(df):
    rel = df.pct_change()
    cumret = (1+rel).cumprod()-1
    cumret = cumret.fillna(0)
    return cumret
    


if len(dropdown) > 0:
    df = relativeRet(yf.download(dropdown, start, end)['Adj Close'])
    st.header('Returns of {}'.format(dropdown))
    st.line_chart(df)
    
    