import cv2,time,os
import tensorflow as tf
import numpy as np
import utils as utils
import train_cnn_lstm_ctc as model

FLAGS = utils.FLAGS
image_height = 28

def predict(images, seq_lens):
    g = model.Graph()
    with tf.Session(graph = g.graph) as sess:
        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver(tf.global_variables(),max_to_keep=100)
        ckpt = tf.train.latest_checkpoint(FLAGS.checkpoint_dir)
        if ckpt:
            saver.restore(sess,ckpt)
            print('restore from ckpt{}'.format(ckpt))
        else:
            print('cannot restore')

        start = time.time()
        feed={ g.inputs: images,
             g.seq_len: seq_lens}
        d = sess.run(g.decoded[0], feed)
        dense_decoded = tf.sparse_tensor_to_dense(d,default_value=-1).eval(session=sess)

        result = []
        for d in dense_decoded:
            res = '' 
            for i in d:
                if i == -1:
                    res+=' '
                else:
                    res+=utils.decode_maps[i]
            result.append(res)
        
        return result, time.time() - start

