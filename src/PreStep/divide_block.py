import pandas as pd
import numpy as np
import sys

"""
This file is used to divide records into blocks.
Prepare at least 9.3GB free disk space.

Input Format (In CLI):
python divide_block.py <free memory (GB)> <input file path> <output file path>

Run the command above and have a Cappuccino.
Total process costs 20mins on my PC.

!! If crashed, please reduce input of free memory size.
"""


def mapFloor5(df,blockNum={'lng':50,'lat':50}):
    mask=(df.Level==5)
    #df.loc[mask,'lngBlock']=np.round(df.loc[mask].lng,6).map(MAPPER).astype('int8')
    MinMaxMapper={
    'lat':[1.29027486,1.29086614],
    'lng':[103.85146999999999,103.85173],
    }

    for f in ['lng','lat']:
        #fMin and fMax
        fMin=MinMaxMapper[f][0] #df.loc[mask,['lat']].min()
        fMax=MinMaxMapper[f][1] #df.loc[mask,['lat']].max()
        edge=np.round((fMax-fMin)*1/blockNum[f]/2,7)
        fMin-=edge
        fMax+=edge
        df.loc[mask,f+'Block'] = ((df.loc[mask,f]-fMin)/(fMax-fMin) * blockNum[f]).astype('int8')
    return df

def mapFloor1(df,blockNum={'transformedLng':50,'transformedLat':50}):
    mask=(df.Level==1)
    lngMax = 0.0013678100000049653 #df.loc[mask].lng.max()-df.loc[mask].lng.min()
    latMax = 0.0015226099999998688 #df.loc[mask].lat.max()-df.loc[mask].lat.min()
    lngMin = 103.850815 #df.loc[mask].lng.min()
    latMin = 1.28961633 #df.loc[mask].lat.min()
    df.loc[mask,'transformedLng'] = df.loc[mask,'lng']-lngMin
    df.loc[mask,'transformedLat'] = df.loc[mask,'lat'] - latMin -latMax/lngMax * df.loc[mask,'transformedLng']

    transformedMinMaxMapper={
    'transformedLng':[0.0,0.0013678100000049653],
    'transformedLat':[-0.0004549742729702752,0.0003869574631660687]
    }

    for f in ['transformedLng','transformedLat']:
        fMin=transformedMinMaxMapper[f][0] #df.loc[mask,f].min()
        fMax=transformedMinMaxMapper[f][1] #df.loc[mask,f].max()
        edge=np.round((fMax-fMin)*1/blockNum[f]/2,7)
        fMin-=edge
        fMax+=edge
        df.loc[mask,f[-3:].lower()+'Block'] = ((df.loc[mask,f]-fMin)/(fMax-fMin) * blockNum[f]).astype('int8')
        del df[f]
    return df

def mapFloorB1(df,blockNum={'transformedLng':50,'transformedLat':50}):
    mask=(df.Level==0)
    lngMax = 0.0007586800000041194 #df.loc[mask].lng.max()-df.loc[mask].lng.min()
    latMax = 0.001228809999999969 #df.loc[mask].lat.max()-df.loc[mask].lat.min()
    lngMin = 103.85125389 # df.loc[mask].lng.min()
    latMin = 1.28970571 #df.loc[mask].lat.min()
    df.loc[mask,'transformedLng'] = df.loc[mask,'lng']- lngMin
    df.loc[mask,'transformedLat'] = df.loc[mask,'lat']-latMin-latMax/lngMax * df.loc[mask,'transformedLng']

    transformedMinMaxMapper={
    'transformedLng':[0.0,0.0007586800000041194],
    'transformedLat':[-0.0004127313021250311,0.0004330021423923565]
    }

    for f in ['transformedLng','transformedLat']:
        fMin=transformedMinMaxMapper[f][0] #df.loc[mask,f].min()
        fMax=transformedMinMaxMapper[f][1] #df.loc[mask,f].max()
        edge=np.round((fMax-fMin)*1/blockNum[f]/2,7)
        fMin-=edge
        fMax+=edge
        df.loc[mask,f[-3:].lower()+'Block'] = ((df.loc[mask,f]-fMin)/(fMax-fMin) * blockNum[f]).astype('int8')
        del df[f]
    return df

def mapFloorAll(df,blockNum={'lng':50,'lat':50}):
    MinMaxMapper={
    'lat':[1.28961633,1.29113894],
    'lng':[103.850815,103.85218281],
    }
    for f in ['lng','lat']:
        #fMin and fMax
        fMin=MinMaxMapper[f][0] #df.loc[mask,['lat']].min()
        fMax=MinMaxMapper[f][1] #df.loc[mask,['lat']].max()
        edge=np.round((fMax-fMin)*1/blockNum[f]/2,7)
        fMin-=edge
        fMax+=edge

        df[f+'Block'] = ((df[f]-fMin)/(fMax-fMin) * blockNum[f]).astype('int8')
    return df

def divideBlock(chunk):
    chunk['lngBlock']=pd.Series(127, dtype='int8',index=chunk.index)
    chunk['latBlock']=pd.Series(127, dtype='int8',index=chunk.index)
    chunk=mapFloor5(chunk)
    chunk=mapFloor1(chunk)
    chunk=mapFloorB1(chunk)

    chunk['month'] = chunk.localtime.dt.month.astype("int8")
    chunk['day'] = chunk.localtime.dt.day.astype("int8")
    chunk['hour'] = chunk.localtime.dt.hour.astype("int8")
    chunk['minute'] = chunk.localtime.dt.minute.astype("int8")
    return chunk

def main(argv):
    memory_size = int(argv[1]) #in GB
    chunk_size = int(memory_size * 1024**3 / 2 / 100)
    chunk_num = 260*10**6//chunk_size+1
    col_dtypes = {
    "Level":'int8',
    "ClientMacAddr":'int64',
    "lat":'float64',
    "lng":'float64'
    }

    columns = ['Level', 'ClientMacAddr', 'latBlock', 'lngBlock','month','day','hour','minute']
    pd.DataFrame(columns=columns).to_csv(argv[3],index=False)

    print("Initialization ---- total %s chunks"%(chunk_num))
    print("Finish:"+chunk_num*'-'+' %02d'%(0),end='\r')

    for i,chunk in enumerate(pd.read_csv(argv[2],dtype=col_dtypes,
                     parse_dates=['localtime'],infer_datetime_format=True,chunksize=chunk_size)):
        chunk = divideBlock(chunk)
        chunk.to_csv(argv[3], mode='a',header=False, index=False,columns=columns)
        print("Finish:"+(i+1)*'>'+(chunk_num-i)*'-'+' %02d'%(100*(i+1)/chunk_num),end='\r')
    print("-----------Complete---------------")


if __name__=='__main__':
    main(sys.argv)
