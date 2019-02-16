import pandas as pd
import numpy as np
import sys
from reduce_cost import *
from divide_block import *

"""
For now, this file conclude steps in reduce_cost.py and divide_block.py.
Prepare at least 8.8GB free disk space.

Input Format (In CLI):
python one_step.py <free memory (GB)> <input file path> <output file path>

Run the command above and have a Cappuccino.
Total process costs 40mins on my PC.

!! If crashed, please decrease input of free memory size.
"""

def oneStep(argv):
    memory_size = int(argv[1]) #in GB
    chunk_size = int(memory_size * 1024**3 / 2 / 300)
    chunk_num = 260*10**6//chunk_size+1
    columns = ['Level', 'ClientMacAddr', 'lat', 'lng', 'localtime']
    columns_block = ['Level', 'ClientMacAddr', 'latBlock', 'lngBlock','month','day','hour','minute']
    pd.DataFrame(columns=columns_block).to_csv(argv[3],index=False)
    print("Initialization ---- total %s chunks"%(chunk_num))
    print("Finish:"+chunk_num*'-'+' %02d'%(0),end='\r')

    col_dtypes = {
    "lat":'float64',
    "lng":'float64'
    }

    for i,chunk in enumerate(pd.read_csv(argv[2],dtype=col_dtypes,usecols=columns, chunksize=chunk_size)):
        # Reduce cost
        chunk = reduceCost(chunk)
        chunk = divideBlock(chunk)
        chunk.to_csv(argv[3], mode='a',header=False, index=False,columns=columns_block)
        print("Finish:"+(i+1)*'>'+(chunk_num-i)*'-'+' %02d'%(100*(i+1)/chunk_num),end='\r')
    print("-----------Complete---------------")


if __name__=="__main__":
    oneStep(sys.argv)
