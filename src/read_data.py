import pandas as pd

"""
Test Enviroment:
OS: Windows 10
Executer: jupyter notebook
CPU freq: 4.3GHZ
RAM: 32 GB
###
Cost:
Wall time: 4min 46s
Memory usage: 5.1 GB
(In Bytes:
    Index                    80
    ClientMacAddr    2080550000
    Level             260068750
    lat               520137500
    lng               520137500
    localtime        2080550000
)
###
Details:
>df.info(memory_usage='deep')
    RangeIndex: 260068750 entries, 0 to 260068749
    Data columns (total 5 columns):
    ClientMacAddr    int64
    Level            int8
    lat              float16
    lng              float16
    localtime        datetime64[ns]
    dtypes: datetime64[ns](1), float16(2), int64(1), int8(1)
    memory usage: 5.1 GB
"""

def read_csv(file_path):
    col_dtypes = {
    "Level":'int8',
    "ClientMacAddr":'int64',
    "lat":'float16',
    "lng":'float16'
    }
    df = pd.read_csv(file_path,dtype=col_dtypes,
                     parse_dates=['localtime'],infer_datetime_format=True)
    return df
