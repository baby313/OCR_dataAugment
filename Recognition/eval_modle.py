from ctypes import *
import sys
import os.path
import numpy as np
import cv2,time,os
import tensorflow as tf
import utils as utils
import train_cnn_lstm_ctc as model

FLAGS = utils.FLAGS
image_height = 28
batch_size = 128
def eval(data_path):
    # val_feeder=utils.DataIterator(data_dirs=["/data/linkface/OcrData/OcrFakeTestData/"])
    val_feeder=utils.DataIterator(data_dirs=[data_path])
    print('get image: ',val_feeder.size)

    num_eval_samples = val_feeder.size 
    num_batches_per_epoch = int(num_eval_samples/batch_size)

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

        print('=============================begin evaluation=============================')

        start = time.time()
        batch_time = time.time()
        total_lines = 0
        total_hit_lines = 0
        total_chars = 0
        total_hit_chars = 0

        #the tracing part
        for cur_batch in range(num_batches_per_epoch):
            batch_time = time.time()
            indexs = range(cur_batch*batch_size, (cur_batch+1)*batch_size)
            batch_inputs, batch_seq_len, batch_labels, batch_lab_len, labels = val_feeder.input_index_generate_batch_warp(indexs)
            val_feed={g.inputs: batch_inputs,
                    g.seq_len: batch_seq_len,
                    g.output_keep_prob: 1.0,
                    g.input_keep_prob: 1.0}
            # print(batch_labels)
            d = sess.run(g.decoded[0], val_feed)
            dense_decoded = tf.sparse_tensor_to_dense(d, default_value=0).eval(session=sess)
            reco_time = time.time()

            hit_lines, lines, hit_chars, chars = utils.accuracy_calculation2(labels, dense_decoded,ignore_value=0,isPrint=False)
            
            total_lines += lines
            total_hit_lines += hit_lines
            total_chars += chars
            total_hit_chars += hit_chars
            log = "Batch {}, Lines {}, Chars {},  line accuracy = {:.5f}, char accuracy = {:.5f}, recognize time = {:.3f}, total time={:3f}"
            print(log.format(cur_batch + 1, lines, chars, hit_lines * 1.0 / lines, hit_chars * 1.0 / chars,  reco_time - batch_time, time.time()-batch_time))

        print('=============================Total Result=============================')
        print(data_path)
        log = "time = {:.3f}, line accuracy = {:.5f}, char accuracy = {:.5f}"
        print(log.format(time.time()-start, total_hit_lines * 1.0 / total_lines, total_hit_chars * 1.0 / total_chars))
        print("Lines {}, Chars {}".format(total_lines, total_chars))

path = "/home/linkface/tf-faster-rcnn/data/VechileLicense2017/Vechile2017/DetectedTestRegions/"
for i in range(10):
    eval(path + str(i) + '/')