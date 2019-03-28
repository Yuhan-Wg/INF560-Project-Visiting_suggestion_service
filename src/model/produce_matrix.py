import numpy as np
import pandas as pd
from copy import deepcopy

# This script contains function tranforming dataset presenting in blocks to matrix
# to features and labels for CNN training.

def matrixTrans(df, level, between=1):
    """
    Useful columns:
    Level	latBlock	lngBlock	count
    month	day	hour	count	minute
    """
    tf = deepcopy(df.loc[df['Level'] == level])
    latMax = tf.latBlock.max()+1
    lngMax = tf.lngBlock.max()+1
    tf["order"] = tf.month * 10**6+ tf.day *10**4 + tf.hour*10**2+tf.minute
    orders = sorted(tf["order"].unique())
    features = np.zeros((len(orders),lngMax,latMax))
    labels = np.zeros((len(orders),lngMax,latMax))
    index = 0
    for i in range(len(orders)-between):
        prev = tf.loc[tf.order==orders[i]]
        next = tf.loc[tf.order==orders[i+between]]
        if prev.day.max() != next.day.max():
            continue
        # If in the same day
        for _, row in prev.iterrows():
            features[index, row['lngBlock'],row['latBlock']] = row['count']
        for _,row in next.iterrows():
            labels[index, row['lngBlock'],row['latBlock']] = row['count']
        index += 1

    del tf["order"]
    features = features[:index,:,:]
    labels = labels[:index,:,:]
    return features, labels
