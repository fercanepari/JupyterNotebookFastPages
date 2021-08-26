# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 12:31:56 2021

@author: CanepariF
"""

import pandas as pd 
import matplotlib.pyplot as plt
import yfinance as yf 
import datetime
import streamlit as st
import plotly.graph_objects as go

pd.options.mode.chained_assignment = None

tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
tickers = tickers.Symbol.to_list()

tickers = [i.replace('.','-') for i in tickers]
#The following one has no enough data
tickers.remove('OGN')

#For quick test
#tickers = [
# 'VTR',
# 'EXPE'
#]


def RSIcalc(asset):
    df = yf.download(asset, start='2011-01-01')
    
    df['MA200'] = df['Adj Close'].rolling(window=200).mean()
    df['price change'] = df['Adj Close'].pct_change()
    df['Upmove'] = df['price change'].apply(lambda x: x if x > 0 else 0)
    df['Downmove'] = df['price change'].apply(lambda x: abs(x) if x < 0 else 0)
    df['avg Up'] = df['Upmove'].ewm(span=19).mean()
    df['avg Down'] = df['Downmove'].ewm(span=19).mean()

    df = df.dropna()
    df['RS'] = df['avg Up']/df['avg Down']
    df['RSI'] = df['RS'].apply(lambda x: 100-(100/(x+1)))
    df.loc[(df['Adj Close'] > df['MA200']) & (df['RSI'] < 30), 'Buy'] = 'Yes'
    df.loc[(df['Adj Close'] < df['MA200']) | (df['RSI'] > 30), 'Buy'] = 'No'

    return df   


def getSignals(df):
    Buying_dates = []
    Selling_dates = []
    
    if not df.empty and len(df) > 11:
        for i in range(len(df) - 11):
            if "Yes" in df['Buy'].iloc[i]:
                Buying_dates.append(df.iloc[i+1].name)
                for j in range(1, 11):
                    if df['RSI'].iloc[i + j] > 40:
                        Selling_dates.append(df.iloc[i+j+1].name)
                        break
                    elif j == 10:
                        Selling_dates.append(df.iloc[i+j+1].name)
    
    return Buying_dates, Selling_dates



matrixsignals = []
matrixprofits = []
counter = 1

totalfields = len(tickers)

st.title("Find stock oportunities to buy, among S&P 500 companies")

st.text("Using Relative Strength Index - RSI We can find signals to buy an asset across time")
st.text("The following algorithm fetches all the tickers and if there is a signal to buy")
st.text("in the recent days, it is displayed. ")
st.text("For the found signal, we plot a chart with the asset close values across time, and all  ")
st.text("the buy signals obtained with RSI strategy.")

st.text("The list of all tickers is obtained from wikipedia (https://en.wikipedia.org/wiki/List_of_S%26P_500_companies)")

st.text("To start the process press the button...")

result = st.button("Start Process")

if result:
       
    print("Processing assets to find buy signals")
    st.text("Processing assets to find buy signals")
    
    progress_bar = st.progress(0)
    
    status_text = st.empty()
    
    for i in range(totalfields):  
        # Update progress bar.
        progess = (i * 100 / totalfields) / 100
        print(progess)
        progress_bar.progress(progess)
        
        
        
        frame = RSIcalc(tickers[i])
        buy, sell = getSignals(frame)
        Profits = (frame.loc[sell].Open.values - frame.loc[buy].Open.values)/frame.loc[buy].Open.values
        matrixsignals.append(buy)
        matrixprofits.append(Profits)
        
        #Date range to check if there is a signal to buy the asset
        dateTo = datetime.datetime.today()
        dateFrom = dateTo + datetime.timedelta(days=-60)
        
        dfBuy = frame.loc[dateFrom:dateTo, ['Buy']]
        toBuy = dfBuy[dfBuy['Buy']=='Yes']
        toBuy['Ticker'] = tickers[i]
        
        print('Processed: ' + str(counter) + ' of ' + str(totalfields))
        
        # Update status text.
        status_text.text(
            'Processed: ' + str(counter) + ' of ' + str(totalfields))
        
        counter = counter + 1
        
        #In case we have a signal to buy in the specified period, let's plot it
        if not toBuy.empty:
            print('Asset to buy: ')
            
            plt.figure(figsize=(12,5))
            plt.scatter(frame.loc[buy].index, frame.loc[buy]['Adj Close'], marker='^', c='g')
            plt.plot(frame['Adj Close'], alpha=0.7)
            plt.title(label=tickers[i])
            
            st.pyplot(plt)
            
            st.write(toBuy)
            #st.line_chart(frame['Adj Close'])
    
            #st.plotly_chart(plt)
            
            print(toBuy)
            
#matrixsignalsbyAsset = dict(zip(tickers, matrixsignals))  





