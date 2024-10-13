# -*- coding: utf-8 -*-
"""algoritme_(2).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mlTnojv5Rxlis_lx1MVijICXpCFnUEsV
"""

from urllib.request import urlretrieve
from datetime import datetime
import pandas as pd

def get_historical_data_url(ticker):
    unix_oldest_date = 0
    unix_newest_date = int(datetime.now().timestamp())
    return f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={unix_oldest_date}&period2={unix_newest_date}&interval=1d&events=history&includeAdjustedClose=true"

get_historical_data_url("AAPL")

def download_data(ticker):
    url = get_historical_data_url(ticker)
    df = pd.read_csv(url)
    # filename = f"{ticker}.csv"
    # df.to_csv(filename)
    return df

"""RSI CALCULATOR

"""

def get_gain_los(data):
    loss = []
    gain = []
    for i in range(len(data)):
        difference = data[i]-data[i-1]
        if(i != 0):
            if(difference <= 0):
                loss.append(-1 * difference)
            elif(difference > 0):
                gain.append(difference)
    return loss, gain

loss, gain = get_gain_los([20,19,50,45,68,46,65,65,84,52,57,65,98,12,34])
sum(gain)/len(gain), sum(loss)/len(loss)

def get_average_gain_loss(data):
  loss, gain = get_gain_los(data)
  avg_loss = 0
  avg_gain = 0
  if(len(loss) != 0):
    avg_loss = sum(loss)/len(loss)

  if(len(gain) != 0):
    avg_gain = sum(gain)/len(gain)

  return avg_loss, avg_gain

def get_rsi(data):
    loss, gain = get_average_gain_loss(data)
    if loss != 0:
      rs = gain / loss
      rsi = 100 - (100 / (1 + rs))
      return rsi
    else:
      return 0

def get_rsi_column(data, count, onlyLast = False):
  rsi_row = []
  for i in range(len(data)):
    i += 1
    start = i - count
    if start < 0:
      start = 0
    rsi_value = (get_rsi(data[start:i]))
    if rsi_value != 0:
      rsi_row.append(rsi_value)
    else:
      rsi_row.append(0)
  return rsi_row


get_rsi_column([20,19,50,45,68,46,65,65,84,52,57,65,98,32,39], 14)

"""Berekenen van Bollinger bands"""

def calculate_boba_row(df,count, onlyLastOne=False):
  # df = data.copy()
  if not onlyLastOne:
    df['SMA'] = df['Open'].rolling(window=count).mean()
    df['SD'] = df['Open'].rolling(window=count).std()
  elif onlyLastOne:

    df['SMA'] = df['Open'][-count:].mean()
    df['SD'] = df['Open'][-count:].std()

  # Bereken Upper en Lower Bollinger Bands
  upper_band_row = df['SMA'] + (2 * df['SD'])
  lower_band_row = df['SMA'] - (2 * df['SD'])

  return upper_band_row, lower_band_row

"""Dataframe klaarmaken en ophalen

average volumes berekenen
"""

def calculate_avg_volumes(df, count,onlyLastOne=False):
  # Bereken het gemiddelde volume van de voorgaande
  if not onlyLastOne:
    df['avg_volume'] = df['Volume'].rolling(window=count).mean()
    df['avg_open'] = df['Open'].rolling(window=count).mean()
  elif onlyLastOne:

    df['avg_volume'] = df['Volume'][-count:].mean()
    df['avg_open'] = df['Open'][-count:].mean()
  return df

"""rsi berekenen"""

def calculate_rsi_df(df, count, onlyLastOne=False):
    # Bereken de RSI-waarde
    df[f"Rsi{count}"] = get_rsi_column(df["Open"].array,count,onlyLastOne)
    return df

def calculate_boba_df(df, count, onlyLastOne=False):
  #Bereken bollinger bands
    df[f"lower_band_{count}"], df[f"upper_band_{count}"] = calculate_boba_row(df,count, onlyLastOne)
    return df

"""datum naar unix time"""

from datetime import datetime
def convert_dates_to_int(df):
     #Datum vervangen door int
  return int(datetime.strptime(df, "%Y-%m-%d").timestamp())

def convert_int_to_dates(df):
  return datetime.fromtimestamp(df).strftime("%Y-%m-%d")

def get_df_ready(df, count):
  print(df.info())
  #close mag niet weggesmeten worden anders is het onmogelijk om model te trainen
  #df = df.drop("Close", axis=1)
  df = df.drop("Adj Close", axis=1)
  df = df.drop("High", axis=1)
  df = df.drop("Low", axis=1)
  df = df.dropna()
  df = calculate_avg_volumes(df, count)
  df = calculate_rsi_df(df, count)
  df = calculate_boba_df(df, count)
  df['Date'] = df['Date'].apply(convert_dates_to_int)
  return df

def calculate_axis(df, target):
  X = df.drop(columns=[target])
  y = df[target]
  return X, y

"""Uitvoeren close predict algoritme"""

import pandas as pd
import xgboost as xgb
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def get_xgboost_model(X_train,y_train):
  gbm = xgb.XGBRegressor(max_depth=4, n_estimators=500, learning_rate=0.03)
  gbm.fit(X_train, y_train)
  return gbm

def test_xgboost(gbm, X_test, y_test):
  predictions = gbm.predict(X_test)
  solutions = pd.DataFrame({'Actual': y_test, 'Predicted': predictions})
  solutions_sorted = solutions.sort_index(ascending=True)
  print(solutions_sorted.iloc[-10:])
  mse = mean_squared_error(y_test, predictions)
  print("Mean Squared Error:", mse)

  return predictions

# df = download_data("AAPL")
# df = get_df_ready(df);
# X,y = calculate_axis(df, "Close")
# X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)
# model = get_xgboost_model(X_train,y_train)
# test_xgboost(model,X_test,y_test)

"""Het voorspellen van de y-waardes (retourneert enkel y-waardes)"""

def predict_xgboost_close(gbm, X_test):

    # Make predictions
    predictions = gbm.predict(X_test)

    return predictions

"""Plotten van voorspelde tov reele waarde (OUD)

"""

import matplotlib.pyplot as plt


# Plot werkelijke vs voorspelde waarden
def plot_prediction(X_test,y_test,y_pred):
  resultaten = pd.DataFrame({"Date": X_test.index, "Werkelijke": y_test, "Voorspeld": y_pred})
  resultaten = resultaten.sort_values(by="Date")  # Sorteer op tijdstempel als dat nog niet is gebeurd

  # Maak de lijngrafiek
  plt.figure(figsize=(10, 6))
  plt.plot(resultaten["Date"], resultaten["Werkelijke"], label="Werkelijke waarden", marker='o')
  plt.plot(resultaten["Date"], resultaten["Voorspeld"], label="Voorspelde waarden", marker='x')
  plt.xlabel("Datum")
  plt.ylabel("Waarde")
  plt.title("Werkelijke vs Voorspelde waarden")
  plt.xticks(rotation=45)  # Draai de datums voor leesbaarheid
  plt.legend()
  plt.grid(True)

  # Inzoomen op de laatste honderd waarden
  laatste_honderd = resultaten.iloc[-30:]  # Krijg de laatste honderd rijen
  plt.xlim(laatste_honderd["Date"].iloc[0], laatste_honderd["Date"].iloc[-1])  # Stel het bereik van de x-as in
  plt.ylim(150, 200)  # Beperk y-as van 150 tot 200

  plt.tight_layout()
  plt.show()

"""Retourneert de laatste rij van een gegeven dataframe (als een dataframe)"""

def get_last_row(X_values):
  row = X_values.iloc[-1:]
  return row

def get_before_last_row(X_values):
  row = X_values.iloc[-2]


  return row

"""Voorspellen van de standaard features ("Open","Volume","Date")"""

def add_new_row(df, count, volume_model):
  new_row = get_last_row(df)
  last_row = get_last_row(df)
  #open_prediction = open_model.predict(last_row)

  #Open vandaag = close van gisteren
  new_row["Open"] = last_row["Close"]

  #volume voorspellen maar eerst oude volume verwijderen voor acurate voorspelling
  last_row = last_row.drop("Volume",axis=1)
  print("pred volume")
  print(last_row)
  volume_prediction = volume_model.predict(last_row)
  print(volume_prediction)
  print("succes volume pred")

  #Volume vervangen
  new_row["Volume"] = volume_prediction;

  #De dag 1 dag opschuiven
  #!WAT ALS DE BEURS DE DAG EROP NIET OPEN IS
  new_row["Date"] = last_row["Date"] + 24*3600;

  count = count*2
  # rij toevoegen aan dataframe en dataframe nieuwe features berekenen
  df = pd.concat([df, new_row], ignore_index=True)
  df = calculate_avg_volumes(df, count, onlyLastOne=True)
  df = calculate_boba_df(df, count, onlyLastOne=True)
  df = calculate_rsi_df(df, count)
  return df

def predict_last_row_open(df,open_model):
  last_row = get_last_row(df)
  last_row = last_row.drop("Close",axis=1)

  open_prediction = open_model.predict(last_row)

  df.loc[df.index[-1], "Open"] = open_prediction[0]
  return df

# df = get_df_ready(download_data("AAPL"))
# print(df.tail())
# X, y = calculate_axis(df, "Open")
# open_model = get_xgboost_model(X, y)
# X, y = calculate_axis(df, "Volume")
# volume_model = get_xgboost_model(X, y)
# df = predict_new_row(df, open_model, volume_model)
# print(df.tail())

"""Voorspellen van de standaard features van een aantal nieuwe rijen (retourneert alleen de nieuwe rijen als dataframe)

Ik heb dit zo gedaan zodat je kan zien op de grafiek wat de reele waarden zijn en wat de voorspelde waarden zijn

"""

def predict_new_rows(count, df):
   #Het dataframe omzetten naar X & y waardes
  #Model maken adhv X & y
  X, y = calculate_axis(df, "Close")
  open_model = get_xgboost_model(X, y)



  X, y = calculate_axis(df, "Volume")
  print(X)
  volume_model = get_xgboost_model(X, y)

  #Het dataframe omzetten naar X & y waardes
  #Model maken adhv X & y
  #MOdel wordt hier gemaakt omdat je anders altijd een nieuwe rij maakt
  for i in range(count):
    df = add_new_row(df, count, volume_model)
    df = predict_last_row_open(df,open_model)
  return df

def split_train_test(X,y):
  total_size = len(X)

  # Bepaal het indexpunt waar de 80% grens ligt
  split_index = int(0.8 * total_size)

  # Splits de gegevens op basis van de index
  X_train, X_test = X[:split_index], X[split_index:]
  y_train, y_test = y[:split_index], y[split_index:]
  return X_train, X_test, y_train, y_test

"""Het printen van de nieuwe voorspelde waardes in een grafiek"""

download_data("AAPL").drop("Close", axis=1)

def print_new_predictions(count,name):
  df = download_data(name)
  df = get_df_ready(df, count*2);
  prediction = predict_new_rows(count, df)
  print(prediction.tail(15))
  plt.plot(prediction['Date'].iloc[-(count+1):] ,prediction["Open"].iloc[-(count+1):] , color='r')
  plt.plot(df["Date"].iloc[-10:], df["Open"].iloc[-10:], label="Werkelijke waarden", color='b')
  plt.grid()
  plt.show()

print_new_predictions(10,"AAPL")

