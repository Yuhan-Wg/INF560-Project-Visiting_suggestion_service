import pandas as pd
import numpy as np
import os

cols=['Daily Rainfall Total (mm)', 'Highest 30 Min Rainfall (mm)',
       'Highest 60 Min Rainfall (mm)', 'Highest 120 Min Rainfall (mm)',
       'Mean Temperature (∞C)', 'Maximum Temperature (∞C)',
       'Minimum Temperature (∞C)', 'Mean Wind Speed (km/h)',
       'Max Wind Speed (km/h)','Year', 'Month', 'Day']

def timedate_process(df):
    # Find the input dir
    weatherData = pd.DataFrame()
    for p in ["./","../","../../","../../../"]:
        if "input" in os.listdir(p):
            weatherFilePath = p+ "input/weather/"
            break
    # Load weather data
    for file in os.listdir(weatherFilePath):
        temp = pd.read_csv(weatherFilePath+file,encoding ='mac_roman',usecols=cols)
        weatherData = pd.concat([temp, weatherData], axis=0).replace("ó",np.nan).astype(float)
    del temp
    weatherData.fillna(weatherData.mean(),inplace=True)

    # Format datetime in df and weatherData into same format
    weatherData['localtime'] = pd.to_datetime(weatherData[['Year', 'Month', 'Day']])
    df['year'] = 2018
    df['localtime'] = pd.to_datetime(df[['year', 'month', 'day']])
    #df['minute'] = df['quarter'] * 15
    #del df['quarter']
    weatherData.drop(['Year', 'Month', 'Day'], axis=1, inplace=True)


    # Holiday feature
    df["dayofweek"] = df['localtime'].dt.weekday
    df["holiday"] = False
    for holiday in [89, 121, 149, 166, 221, 234, 310, 359]:
        df["holiday"] |= (df["localtime"].dt.dayofyear == holiday)
    df = df.merge(weatherData, on="localtime", how="left")


    # Events in gallery
    #1-> CHILDREN'S FESTIVAL: SMALL BIG DREAMERS 2018
    #2-> (RE)COLLECT: THE MAKING OF OUR ART COLLECTION
    df['eventFest'] = (df['localtime'].dt.dayofyear> 160) & (df['localtime'].dt.dayofyear< 252)
    df['eventArt'] = (df['localtime'].dt.dayofyear> 131) & (df['localtime'].dt.dayofyear< 231)

    # Event in Asian Civilisations Museum
    df["eventinACM"] = False
    for i in [104, 107, 110, 117, 118, 122, 128, 131, 145, 146, 159, 166, 173, 181, 182, 186, 187, 209, 226, 237]:
        df["eventinACM"] |= (df['localtime'].dt.dayofyear ==i)

    # Event in Peninsula Shopping Centre Singapore
    df["eventinPSCS"] = False
    for i in [129, 176, 206, 220]:
         df["eventinPSCS"] |= (df['localtime'].dt.dayofyear ==i)

    del df['localtime'],df["year"]
    #df["localtime"] = pd.to_datetime(df[['year', 'month', 'day','hour','minute']])
    #df.drop(['year', 'month', 'day','hour','quarter'], inplace= True,axis=1)
    return df
