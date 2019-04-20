import pandas as pd
import numpy as np
from copy import deepcopy

def aggregate_time(df):
    for h in range(24):
        df["h%s"%(h)]=np.nan
        df.loc[df.hour==h,"h%s"%(h)] = df.loc[df.hour==h,"ClientMacAddr"]

    df = df.groupby(["Level","latBlock","lngBlock","month","day"])\
           .agg({"h%s"%(h):"max" for h in range(24)})\
           .reset_index().fillna(0).astype("int")

    df1 = deepcopy(df)
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            if i==0 and j==0:
                continue
            df_temp = deepcopy(df1)
            df_temp.loc[:,"lngBlock"]+=i
            df_temp.loc[:,"latBlock"]+=j
            df_temp.rename(columns={"h%s"%(h):"h%s_%s_%s"%(h,i,j) for h in range(24)}, inplace=True)
            df = df.merge(df_temp,how="left",on=["Level","latBlock","lngBlock","month","day"])

    for h in range(24):
        df["h%s_neighbor1"%(h)] = df[["h%s_%s_%s"%(h,i,j) for i,j in [(0,1),(0,-1),(-1,0),(1,0)]]].mean(axis=1)

    for h in range(24):
        df["h%s_neighbor2"%(h)] = df[["h%s_%s_%s"%(h,i,j) for i in [-1,1] for j in [-1,1]]].mean(axis=1)

    df.drop(["h%s_%s_%s"%(h,i,j) for h in range(24) for i in [-1,0,1] for j in [-1,0,1] if i!=0 or j!=0], axis=1, inplace=True)

    df['year'] = 2018
    df["days"] = pd.to_datetime(df[['year', 'month', 'day']]).dt.dayofyear-91
    del df['year']
    return df
