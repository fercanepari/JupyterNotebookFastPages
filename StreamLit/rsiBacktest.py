# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 23:09:26 2021

@author: Fernando
"""

import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import yfinance as yf 
import datetime

def RSIcalc(asset, start, end):
    df = yf.download(asset, start, end)
    
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
st.text("A continuación, se usa esta estrategia, y se grafican todas las señales de")
st.text("compra sugeridas para el período de tiempo seleccionado.")

st.text("La lista de activos (SP500) la obtenemos de Wikipedia (https://en.wikipedia.org/wiki/List_of_S%26P_500_companies)")

start = st.date_input('Start', value=pd.to_datetime('2011-01-01'))
end = st.date_input('End', value=pd.to_datetime('today'))

diffDays = end - start
print(diffDays.days)

ticker = st.selectbox('Seleccione el activo a procesar: ', tickers)
print(ticker)

if len(ticker) > 0 and diffDays.days > 300:
    
    frame = RSIcalc(ticker, start, end)
    buy, sell = getSignals(frame)

    dfBuy = frame.loc[:, ['Buy']]
    toBuy = dfBuy[dfBuy['Buy']=='Yes']

       
    if not toBuy.empty:
        print('Asset to buy: ')
          
        
        plt.figure(figsize=(12,8))
        #plt.set_facecolor('black')
        ax1 = plt.subplot(211)
        ax1.plot(frame.index, frame['Adj Close'], color='lightgray', alpha=0.5)
        ax1.set_title("Adjusted Close Price", color='white')
        
        ax1.grid(True, color='#555555')
        ax1.set_axisbelow(True)
        ax1.set_facecolor('black')
        ax1.figure.set_facecolor('#121212')
        ax1.tick_params(axis='x', colors='white')
        ax1.tick_params(axis='y', colors='white')
        ax1.scatter(frame.loc[buy].index, frame.loc[buy]['Adj Close'], marker='^', c='yellow')
        #ax1.scatter(frame.loc[sell].index, frame.loc[sell]['Adj Close'], marker='v', c='red')
        
        
        ax2 = plt.subplot(212, sharex=ax1)
        ax2.plot(frame.index, frame['RSI'], color='lightgray')
        ax2.axhline(0, linestyle='--', alpha = 0.5, color='#ff0000')
        ax2.axhline(10, linestyle='--', alpha = 0.5, color='#ffaa00')
        ax2.axhline(20, linestyle='--', alpha = 0.5, color='#00ff00')
        ax2.axhline(30, linestyle='--', alpha = 0.5, color='#cccccc')
        ax2.axhline(70, linestyle='--', alpha = 0.5, color='#cccccc')
        ax2.axhline(80, linestyle='--', alpha = 0.5, color='#00ff00')
        ax2.axhline(90, linestyle='--', alpha = 0.5, color='#ffaa00')
        ax2.axhline(100, linestyle='--', alpha = 0.5, color='#ff0000')
        
        
        ax2.set_title("RSI Value", color='white')
        ax2.grid(False)
        ax2.set_axisbelow(True)
        ax2.set_facecolor('black')
        ax2.figure.set_facecolor('black')
        ax2.tick_params(axis='x', colors='white')
        ax2.tick_params(axis='y', colors='white')
        
        plt.show()
        
        st.pyplot(plt)
        plt.close()

        st.text("Señales de compra obtenidas: ")
        toBuy
    else:
        st.text("No se encontraron señales de compra en el período.")
else:
    st.text("El rango de fechas debe ser superior a 300 dias.")