import pandas as pd

"""
Test Enviroment:
OS: Windows 10
Executer: jupyter notebook
CPU freq: 4.3GHZ
RAM: 32 GB
### ### ###
Cost:(Origin_input.csv)
Read into memory:
Wall time: 7min 1s
Memory usage: 8.0 GB
Details:
(In Bytes:
    Index                    80
    ClientMacAddr    2080550000 int64
    Level             260068750 int8
    lat              2080550000 float64
    lng              2080550000 float64
    localtime        2080550000 datetime64[ns]
)
"""

def read_csv(file_path,mode='block'):
    switchCase={
        'block':readCSVBlock,
        'divided':readCSVDivided,
        'reduced':readCSVReduced
    }
    try:
        return switchCase[mode](file_path)
    except:
        print("Wrong Mode.")
        return "WRONG"


def readCSVBlock(file_path):
    col_dtypes = {
    "Level":'int8',
    "latBlock":'int8',
    "lngBlock":'int8',
    'month':'int8',
    'day':'int8',
    'hour':'int8',
    'quarter':'int8'
    }
    df = pd.read_csv(file_path,dtype=col_dtypes)
    return df

def readCSVDivided(file_path):
    col_dtypes = {
    "Level":'int8',
    "ClientMacAddr":'int64',
    "latBlock":'int8',
    "lngBlock":'int8',
    'month':'int8',
    'day':'int8',
    'hour':'int8',
    'minute':'int8'
    }
    df = pd.read_csv(file_path,dtype=col_dtypes)
    return df

def readCSVReduced(file_path):
    col_dtypes = {
    "Level":'int8',
    "ClientMacAddr":'int64',
    "lat":'float64',
    "lng":'float64'
    }
    df = pd.read_csv(file_path,dtype=col_dtypes,
                     parse_dates=['localtime'],infer_datetime_format=True)
    return df
