import pandas as pd
import os

def timedate_process(weatherFilePath = "../../input/weather/", df):
    # Load weather data
    weatherData = pd.DataFrame()
    for file in os.listdir(weatherFilePath):
        temp = pd.read_csv(weatherFilePath+file)
        weatherData = pd.concat([temp, weatherData], axis=0)
    del temp

    weatherData['localtime'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
    df['year'] = 2018
    df['localtime'] = pd.to_datetime(df[['year', 'month', 'day']])
    weatherData.drop(['Year', 'Month', 'Day'], axis=1, inplace=True)

    df["weekofday"] = df['localtime'].dt.weekday
    df["holiday"] = False
    for holiday in [89, 121, 149, 166, 221, 234, 310, 359]:
        df["holiday"] |= (df["localtime"].dt.dayofyear == holiday)
    df = df.merge(weatherData, on="localtime", how="left")


    #topic
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


    df['quarter'] *= 15
    df["localtime"] = pd.to_datetime(df[['year', 'month', 'day','hour','quarter']])
    df.drop(['year', 'month', 'day','hour','quarter'], inplace= True, axis=1)

    for i in data_timelist:
        temp_topic=[]
        if int(holiday_test) > 160 and int(holiday_test)<252:
            temp_topic.append(1)
        if int(holiday_test) > 131 and int(holiday_test)<231:
            temp_topic.append(2)
        #print(temp_topic)
        topic_list.append(temp_topic)

    return df
