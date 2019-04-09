import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf



>>>>>>> 8c26027616b4deae15db3cd053ee1ef7bef901c3
def rnn_perpare(data):
    #normalized data
    normalized_data = (data - np.mean(data)) / np.std(data)
    ##### train_len define the length of train dataset
    ##### brench size is the size of one brench
    train_x,train_y=[],[]
    for i in range(train_len-brech_len-1):
        train_x.append(np.expand_dims(data[i : i + brench_len], axis=1).tolist())
        train_y.append(data[i+1:i+brench_len+1].tolist())

    #### test_len define the length of test set
    test_x,test_y=[],[]
    for i in range(test_len-brech_len-1):
        train_x.append(np.expand_dims(data[i : i + brench_len], axis=1).tolist())
        train_y.append(data[i+1:i+brench_len+1].tolist())

    input_dim = 1
    X = tf.placeholder(tf.float32, [None, seq_size, input_dim])
    Y = tf.placeholder(tf.float32, [None, seq_size])

# regression
def visit_rnn(hidden_layer_size=15):
    W = tf.Variable(tf.random_normal([hidden_layer_size, 1]), name='W')
    b = tf.Variable(tf.random_normal([1]), name='b')
    cell = tf.nn.rnn_cell.BasicLSTMCell(hidden_layer_size)
    outputs, states = tf.nn.dynamic_rnn(cell, X, dtype=tf.float32)
    W_repeated = tf.tile(tf.expand_dims(W, 0), [tf.shape(X)[0], 1, 1])
    out = tf.matmul(outputs, W_repeated) + b
    out = tf.squeeze(out)
    return out

# Train the RNN
def train_rnn():
    out = ass_rnn()

    loss = tf.reduce_mean(tf.square(out - Y))
    train_op = tf.train.AdamOptimizer(learning_rate=0.003).minimize(loss)

    saver = tf.train.Saver(tf.global_variables())
    with tf.Session() as sess:
        #tf.get_variable_scope().reuse_variables()
        sess.run(tf.global_variables_initializer())

        for step in range(10000):
            _, loss_ = sess.run([train_op, loss], feed_dict={X: train_x, Y: train_y})
            if step % 10 == 0:
                #test loss
                print(step, loss_)
    print("save: ", saver.save(sess, 'visit.model'))

    #train_rnn()
     return True

# Make prediction
def prediction():
    out = ass_rnn()

    saver = tf.train.Saver(tf.global_variables())
    with tf.Session() as sess:
        #tf.get_variable_scope().reuse_variables()
        saver.restore(sess, './visit.model')

        prev_seq = train_x[-1]
        predict = []
        for i in range(12):
            next_seq = sess.run(out, feed_dict={X: [prev_seq]})
            predict.append(next_seq[-1])
            prev_seq = np.vstack((prev_seq[1:], next_seq[-1]))

    plt.figure()
    plt.plot(list(range(len(normalized_data))), normalized_data, color='b')
    plt.plot(list(range(len(normalized_data), len(normalized_data) + len(predict))), predict, color='r')
    plt.show()
    return True
