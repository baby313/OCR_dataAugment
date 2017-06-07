# coding=utf-8

import os,sys
import cv2,time
import tensorflow as tf
import numpy as np
import utils as utils
import train_cnn_lstm_ctc as network

FLAGS = utils.FLAGS
image_height = 28

reload(sys) 
sys.setdefaultencoding("utf8")

class Predictor:
    def __init__(self, sess, model_path):
        # self.sess = sess
        self.model_path = model_path
        self.network = network.Graph()

        config=tf.ConfigProto(log_device_placement=False,allow_soft_placement=True)
        self.sess = tf.Session(graph=self.network.graph, config=config)

        with self.sess.as_default():
            with self.network.graph.as_default(), tf.device('/cpu:0'):
                self.sess.run(tf.global_variables_initializer())

                ckpt = tf.train.latest_checkpoint(model_path)
                saver = tf.train.Saver(tf.global_variables(),max_to_keep=100)
                if ckpt:
                    saver.restore(self.sess, ckpt)
                    print('restore from ckpt{}'.format(ckpt))
                else:
                    print('cannot restore')
                

    def predict(self, images, seq_lens):
        with tf.device('/cpu:0'):
            feed={ self.network.inputs: images,
                self.network.seq_len: seq_lens,
                self.network.output_keep_prob: 1.0,
                self.network.input_keep_prob: 1.0}
            code = self.sess.run(self.network.dense_decoded, feed)
            # dense_decoded = tf.sparse_tensor_to_dense(code, default_value=-1).eval(session=self.sess)

        result = []
        for d in code:
            res = '' 
            for i in d:
                if i == -1:
                    res+=''
                else:
                    res+=utils.decode_maps[i]
            result.append(res)
        
        return result

def predict(images, seq_lens):
    net = network.Graph()
    config=tf.ConfigProto(log_device_placement=False,allow_soft_placement=True)
    with tf.Session(graph = net.graph, config=config) as sess:
        with net.graph.as_default(), tf.device('/cpu:0'):
            sess.run(tf.global_variables_initializer())
            saver = tf.train.Saver(tf.global_variables(),max_to_keep=100)
            ckpt = tf.train.latest_checkpoint('/home/linkface/OCR/Recognition/checkpoint_bilstm_dropout_0.5/')
            if ckpt:
                saver.restore(sess,ckpt)
                print('restore from ckpt{}'.format(ckpt))
            else:
                print('cannot restore')

            feed={ net.inputs: images,
                    net.seq_len: seq_lens,
                    net.output_keep_prob: 1.0,
                    net.input_keep_prob: 1.0}
            start = time.time()
            d = sess.run(net.decoded[0], feed)
            # print('decode take time: {0}'.format(time.time() - start))
            dense_decoded = tf.sparse_tensor_to_dense(d,default_value=-1).eval(session=sess)
            # print('dense decode take time: {0}'.format(time.time() - start))
            result = []
            for d in dense_decoded:
                res = '' 
                for i in d:
                    if i == -1:
                        res+=''
                    else:
                        res+=utils.decode_maps[i]
                result.append(res)
            # print('totally take time: {0}'.format(time.time() - start))

            return result, time.time() - start

