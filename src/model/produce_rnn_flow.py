import pandas as pd
import numpy as np

def aggregate_time(df):
    for h in range(24):
        df["h%s"%(h)]=np.nan
        df.loc[df.hour==h,"h%s"%(h)] = df.loc[df.hour==h,"ClientMacAddr"]

    df = df.groupby(["Level","latBlock","lngBlock","month","day"])\
           .agg({"h%s"%(h):"max" for h in range(24)})\
           .reset_index().fillna(0).astype("int")
    return df
