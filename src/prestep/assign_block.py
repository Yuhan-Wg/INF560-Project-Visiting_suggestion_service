import pandas as pd
import numpy as np
import sys
import os


"""
This file is used to calculate block size.
Prepare at least 200MB free disk space.

Input Format (In CLI):
python assign_block.py <input file path> <output file path1> <output file path2>

Run the command above and have a Cappuccino.
Total process costs 5mins on my PC.

"""
def mkdir(path):
	folder = os.path.exists(path)
	if not folder:
		os.makedirs(path)

def assignBlock(df,timeBlockSize=15):
    #df['quarter'] = (df.minute//timeBlockSize).astype("int8")
    group = df.groupby(by=['Level','latBlock','lngBlock','month','day','hour']).agg({"ClientMacAddr":"nunique"}).reset_index()
    return group

def main(argv):
    col_dtypes = {
        "Level":'int8',
        "latBlock":'int8',
        "lngBlock":'int8',
        'month':'int8',
        'day':'int8',
        'hour':'int8',
        'minute':'int8',
        "ClientMacAddr":'int64'
    }
    columns = ['Level', 'latBlock', 'lngBlock','month','day','hour','minute']
    df=pd.read_csv(argv[1],usecols=col_dtypes.keys(),dtype=col_dtypes)
    print("Read into Memory")
    group=assignBlock(df)
    for month in group["month"].unique():
        tempm = group.loc[group.month==month]
        for day in tempm.day.unique():
            tempd=tempm.loc[tempm.day==day]
            mkdir(argv[2]+"/%d/%d"%(month,day))
            for level in tempd.Level.unique():
                tempd[tempd.Level==level].to_csv(argv[2]+"/%d/%d/level%d.csv"%(month,day,level),index=False)
    group.to_csv(argv[3],index=False)

if __name__=="__main__":
    main(sys.argv)
