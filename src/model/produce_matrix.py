import numpy as np
import pandas as pd
from copy import deepcopy

# This script contains function tranforming dataset presenting in blocks to matrix
# to features and labels for CNN training.

def matrixTrans(df, level, between=7):
    cols = [c for c in df.columns if c not in ["Level","latBlock","lngBlock","month","day","hour","ClientMacAddr"]]
    tf = deepcopy(df.loc[df['Level'] == level])
    latMax = tf.latBlock.max()+1
    lngMax = tf.lngBlock.max()+1
    tf["order"] = tf.month * 10**2+ tf.day
    orders = sorted(tf["order"].unique())

    def generator():
        for hour in tf.hour.unique():
            yield hour

    g = generator()
    num = 0
    for h in g:
        num+= len(orders)-between
    features = np.zeros((num,lngMax,latMax,between))
    features_add = np.zeros((num,len(cols)))
    labels = np.zeros((num,lngMax,latMax))

    g = generator()
    index = 0
    for hour in g:
        temp = tf.loc[(tf.hour==hour)]
        for i in range(between, len(orders)):
            next_ = temp.loc[tf.order==orders[i]]
            if len(next_)==0:
                continue
            features_add[index,:] = next_.iloc[0][cols]
            for _,row in next_.iterrows():
                labels[index, row['lngBlock'],row['latBlock']] = row['ClientMacAddr']
            for b in range(between):
                prev = temp.loc[tf.order==orders[i-1-b]]
                for _, row in prev.iterrows():
                    features[index, row['lngBlock'],row['latBlock'],b] = row['ClientMacAddr']
            index += 1
            if index==num:
                return features,features_add, labels

    del tf
    features = features[:index,:,:,:]
    features_add = features_add[:index,:]
    labels = labels[:index,:,:]
    return features, features_add, labels
