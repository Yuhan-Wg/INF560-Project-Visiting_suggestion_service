import numpy as np
import pandas as pd
from copy import deepcopy

# This script contains function tranforming dataset presenting in blocks to matrix
# to features and labels for CNN training.

def matrixTrans(df, level, between=7):
    """
    Useful columns:
    Level	latBlock	lngBlock	count
    month	day	hour	count	minute
    """
    tf = deepcopy(df.loc[df['Level'] == level])
    latMax = tf.latBlock.max()+1
    lngMax = tf.lngBlock.max()+1
    tf["order"] = tf.month * 10**2+ tf.day
    orders = sorted(tf["order"].unique())

    def generator():
        for hour in tf.hour.unique():
            for minute in tf.minute.unique():
                yield hour,minute

    g = generator()
    num = 0
    for h,m in g:
        num+= len(orders)-between
    features = np.zeros((num,lngMax,latMax,between))
    labels = np.zeros((num,lngMax,latMax))

    g = generator()
    index = 0
    for hour,minute in g:
        temp = tf.loc[(tf.hour==hour)&(tf.minute==minute)]
        for i in range(between, len(orders)):    
            next = temp.loc[tf.order==orders[i]]
            for _,row in next.iterrows():
                labels[index, row['lngBlock'],row['latBlock']] = row['count']
            for b in range(between):
                prev = temp.loc[tf.order==orders[i-1-b]]
                for _, row in prev.iterrows():
                    features[index, row['lngBlock'],row['latBlock'],b] = row['count']
            index += 1
            if index==num:
                return features, labels

    del tf
    features = features[:index,:,:,:]
    labels = labels[:index,:,:]
    return features, labels
