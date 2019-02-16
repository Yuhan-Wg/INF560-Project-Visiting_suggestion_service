import pandas as pd
import sys

"""
This file is used to reduce memory cost of dataset.
Prepare at least 18.0GB free disk space.

Input Format (In CLI):
python reduce_cost.py <free memory (GB)> <input file path> <output file path>

Run the command above and have a Cappuccino.
Total process costs 20mins on my PC.

!! If crashed, please reduce input of free memory size.
"""

def mapper(x):
    return int(x.replace(':',''),16)

def reduceCost(chunk):
    #Level
    chunk['Level']=chunk['Level'].map({'Level 1':1,'Level B1':0,'Level5':5}).astype('int8')

    #ClientMacAddr
    chunk['ClientMacAddr'] = chunk['ClientMacAddr'].apply(mapper)

    #localtime
    chunk['localtime'] =pd.to_datetime(chunk['localtime'].apply(lambda x:x[:19]),format='%Y-%m-%d %H:%M:%S')
    return chunk

def main(argv):
    memory_size = int(argv[1]) #in GB
    chunk_size = int(memory_size * 1024**3 / 2 / 300)
    chunk_num = 260*10**6//chunk_size+1
    columns = ['Level', 'ClientMacAddr', 'lat', 'lng', 'localtime']
    pd.DataFrame(columns=columns).to_csv(argv[3],index=False)
    print("Initialization ---- total %s chunks"%(chunk_num))
    print("Finish:"+chunk_num*'-'+' %02d'%(0),end='\r')

    for i,chunk in enumerate(pd.read_csv(argv[2],usecols=columns, chunksize=chunk_size)):
        chunk=reduceCost(chunk)
        chunk.to_csv(argv[3], mode='a',header=False, index=False)
        print("Finish:"+(i+1)*'>'+(chunk_num-i)*'-'+' %02d'%(100*(i+1)/chunk_num),end='\r')
    print("-----------Complete---------------")


if __name__ == '__main__':
    main(sys.argv)
