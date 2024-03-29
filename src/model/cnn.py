from __future__ import absolute_import, division, print_function

import tensorflow as tf
import numpy as np
import pandas as pd


def cnn_model(input, labels, **parameters):
    # Input Layer
    size = parameters.get("size", (50,50))
    kernel_size = parameters.get("kernel_size", [(3,3),(3,3),(3,3)])
    #pool_size = parameters.get("pool_size", [(2,2),(3,3),(2,2)])
    strides = parameters.get("strides", [2,2,2])
    filters = parameters.get("filter", [32, 64, 16])

    input_layer = tf.reshape(input, [-1, size[0], size[1], 1])
    label_layer = tf.reshape(labels, [-1, size[0]*size[1]])

    # We only add conv layers with 'same' padding in our model
    # since It's a n*n -> n*n prediction (previous distribution -> future prediction)
    # dimensions should be kept same

    # Convolutional Layer and Pooling Layer#1
    conv1 = tf.layers.conv2d(
      inputs=input_layer,
      filters=filters[0],
      kernel_size=kernel_size[0],
      padding="same",
      activation=tf.nn.relu)

    # Convolutional Layer #2 and Pooling Layer #2
    conv2 = tf.layers.conv2d(
      inputs=conv1,
      filters=filters[1],
      kernel_size=kernel_size[1],
      padding="same",
      activation=tf.nn.relu)
    ]
    # Convolutional Layer #2 and Pooling Layer #2
    conv3 = tf.layers.conv2d(
      inputs=conv2,
      filters=filters[2],
      kernel_size=kernel_size[2],
      padding="same",
      activation=tf.nn.relu)

    # Dense Layer
    conv3_flat = tf.reshape(conv3, [-1, size[0]*size[1]*filters[2]])
    dense = tf.layers.dense(inputs=conv3_flat, units=1024, activation=tf.nn.relu)
    dropout = tf.layers.dropout(inputs=dense, rate=0.4, training= True)

    # Logits Layer
    logits = tf.layers.dense(inputs=dropout, units= size[0]*size[1])

    # Loss
    loss = tf.losses.mean_squared_error(labels=label_layer, logits=logits)

    # Train
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
    train_op = optimizer.minimize(loss=loss,global_step=tf.train.get_global_step())
    return tf.estimator.EstimatorSpec(mode =  tf.estimator.ModeKeys.TRAIN, loss=loss, train_op=train_op)
