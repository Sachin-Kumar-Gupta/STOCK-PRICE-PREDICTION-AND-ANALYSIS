# -*- coding: utf-8 -*-
"""Capital Asset Pricing Model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OPRqMSSqzl-Lo_7BipgfZ4oZoaPhuXk8

# Capital Asset Pricing Model(CAMP)
It is relation between expected return and risk of securities.

It indicate expected return on a security is equall to the risk free return plus risk premium.

# BETA 
Represent slope of the regression line(market return vs stock return).
It is used in CAPM which describe relation between systematic return and expected return fr assets.

# CAPM Formula
Expected return of security = risk free rate of return + BETA between stock and market*(Risk Premium)
"""

# Importing Libraries 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff

stocks = pd.read_csv('stock.csv')
stocks.head(4)

stocks = stocks.sort_values(by = 'Date')
stocks

def normalize(df):
  x = df.copy()
  for i in x.columns[1:]:
    x[i] = x[i]/ x[i][0]
  return x

def interactive_plot(df,title):
  fig = px.line(title = title)
  for i in df.columns[1:]:
    fig.add_scatter(x = df['Date'], y = df[i], name = i)
  fig.show()

interactive_plot(stocks,'Prices')

interactive_plot(normalize(stocks), 'Prices')

"""# Calculate Daily Return"""

def daily_return(df):
  df_daily_return = df.copy()
  for i in df.columns[1:]:
    for j in range(1, len(df)):
      df_daily_return[i][j] = ((df[i][j] - df[i][j-1] )/ df[i][j]) *100

    df_daily_return[i][0] = 0

  return df_daily_return

stock_daily_return = daily_return(stocks)
stock_daily_return

stock_daily_return.mean()

"""# Calculating BETA for single Stock"""

stock_daily_return['AAPL']

#Market Stock
stock_daily_return['sp500']

"""# Plotting graph between selected stock and market stock"""

stock_daily_return.plot(kind = 'scatter', x = 'sp500', y = 'AAPL')

beta, alpha = np.polyfit(stock_daily_return['sp500'], stock_daily_return['AAPL'],1)
print('Beta for {} stock is {} and alpha is {} '.format('AAPL',beta, alpha))

stock_daily_return.plot(kind = 'scatter', x = 'sp500', y = 'AAPL')
plt.plot(stock_daily_return['sp500'], beta*stock_daily_return['sp500'] + alpha, color = 'r')

beta

#Average daily rate of return of sp500
stock_daily_return['sp500'].mean()

#Annual rate of return of sp500
rm = stock_daily_return['sp500'].mean()*252
rm

#Assume risk free rate be zero
rf = 0

#Calculate return for any stock using CAPM
er_APPL = rf +beta*(rm-rf)
er_APPL

"""# Calculate BETA for All Stocks"""

#creating Placeholder for all beta and alpha values
beta = {}
alpha = {}
for i in stock_daily_return.columns:
  if i != 'Date' and i != 'sp500':
    stock_daily_return.plot(kind = 'scatter', x = 'sp500', y = i)
    b,a = np.polyfit(stock_daily_return['sp500'],stock_daily_return[i], 1)
    plt.plot(stock_daily_return['sp500'], b*stock_daily_return['sp500'] + a , '-', color= 'r')

    beta[i] = b
    alpha[i] = a

    plt.show()

beta

# Alpha describe strategy ability to beat market and also indicate excess return or abnormal rate of return
alpha

for i in stock_daily_return.columns:
  if i != 'Date' and i != 'sp500':
    fig = px.scatter(stock_daily_return, x = 'sp500', y = i , title = i)
    b, a = np.polyfit(stock_daily_return['sp500'],stock_daily_return[i], 1 )
    fig.add_scatter(x = stock_daily_return['sp500'],y = b*stock_daily_return['sp500'] + a)
    fig.show()

"""# Calculate Return For Portfolio Using CAPM"""

# Obtining all stocks name
keys = list(beta.keys())
keys

# Expected Return Dictionary
ER = {}
rf = 0
rm = stock_daily_return['sp500'].mean()*252

for i in keys:
  ER[i] = rf + (beta[i]*(rm-rf))

for i in keys:
  print('Expected return based on CAPM for {} is {} '.format(i, ER[i]))

portfolio_weight = 1/8 *np.ones(8)
portfolio_weight

# Assuming equal weights in portfolio
ER_portfolio = sum(list(ER.values())* portfolio_weight)
ER_portfolio

print("Expected Return Based on CAPM is {}% ".format(ER_portfolio))

"""# Calculating Expected Return if only to invest in AAPL and AMZN at 50%"""

ER_portfolio = (0.5*ER['AAPL']) + (0.5*ER['AMZN'])
ER_portfolio

