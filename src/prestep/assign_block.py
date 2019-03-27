import pandas as pd
import numpy as np
import sys

"""
This file is used to calculate block size.
Prepare at least 200MB free disk space.

Input Format (In CLI):
python assign_block.py <input file path> <output file path>

Run the command above and have a Cappuccino.
Total process costs 5mins on my PC.

"""

def assignBlock(df,timeBlockSize=15):
    df['quarter'] = (df.minute//timeBlockSize).astype("int8")
    group = df.groupby(by=['Level','latBlock','lngBlock','month','day','hour','quarter']).agg({"ClientMacAddr":"nunique"}).reset_index(name='count')
    return group

def main(argv):
    col_dtypes = {
        "Level":'int8',
        "latBlock":'int8',
        "lngBlock":'int8',
        'month':'int8',
        'day':'int8',
        'hour':'int8',
        'minute':'int8'
    }
    columns = ['Level', 'latBlock', 'lngBlock','month','day','hour','minute']
    df=pd.read_csv(argv[1],usecols=col_dtypes.keys(),dtype=col_dtypes)
    print("Read into Memory")
    group=assignBlock(df)
    group.to_csv(argv[2],index=False)

if __name__=="__main__":
    main(sys.argv)
