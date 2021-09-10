# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 23:09:26 2021

@author: Fernando
"""

import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import yfinance as yf 
#import datetime


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


tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
tickers = tickers.Symbol.to_list()
tickers = [i.replace('.','-') for i in tickers]

st.title("Estrategia RSI - Backtest de ordenes de compra.")

st.text("Usando el Indice de fuerza relativo (RSI en inglés)  podemos buscar señales de ") 
st.text("compra cuando el activo está sobrevendido")
st.text("En el siguiente programa, se grafican todas las señales de compra que de ")
st.text("hubiesen generado en los últimos 10 años.")

st.text("La lista de activos (SP500) la obtenemos de Wikipedia (https://en.wikipedia.org/wiki/List_of_S%26P_500_companies)")


ticker = st.selectbox('Seleccione el activo a procesar: ', tickers)
print(ticker)
if len(ticker) > 0:
    
    frame = RSIcalc(ticker)
    buy, sell = getSignals(frame)

    dfBuy = frame.loc['2011-01-01':'2021-08-24', ['Buy']]
    toBuy = dfBuy[dfBuy['Buy']=='Yes']

    if not toBuy.empty:
        print('Asset to buy: ')
        
        plt.figure(figsize=(12,5))
        plt.scatter(frame.loc[buy].index, frame.loc[buy]['Adj Close'], marker='^', c='g')
        plt.plot(frame['Adj Close'], alpha=0.7)
        plt.title(label=ticker)    
        
        st.pyplot(plt)
        plt.close()

