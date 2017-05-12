import os,sys
#import config
import numpy as np
import tensorflow as tf
import random
import cv2,time
import logging,datetime
from tensorflow.python.client import device_lib
from tensorflow.python.client import timeline
import warpctc_tensorflow
import utils

os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID" 

FLAGS=utils.FLAGS
#26*2 + 10 digit + blank + space
num_classes=utils.NUM_CLASSES
num_features=utils.num_features

logger = logging.getLogger('Traing for ocr using CNN+LSTM+CTC')
logger.setLevel(logging.INFO)

def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

def conv2d(x, W):
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

def max_pool_3x3(x):
  return tf.nn.max_pool(x, ksize=[1, 3, 3, 1], strides=[1, 3, 3, 1], padding='SAME')

#with tf.get_default_graph()._kernel_label_map({'CTCLoss':'WarpCTC'}):
#with tf.device('/gpu:1'):
class Graph(object):
    def __init__(self):
        self.graph = tf.Graph()
        with self.graph.as_default():
            # e.g: log filter bank or MFCC features
            # Has size [batch_size, max_stepsize, num_features], but the
            # batch_size and max_stepsize can vary along each step
            self.inputs = tf.placeholder(tf.float32, [None, None, num_features, 3])
            
            # Here we use sparse_placeholder that will generate a
            # SparseTensor required by ctc_loss op.
            # self.labels = tf.sparse_placeholder(tf.int32)
            self.labels = tf.placeholder(tf.int32,[None])
            
            # 1d array of size [batch_size]
            self.seq_len = tf.placeholder(tf.int32, [None])
            self.label_len= tf.placeholder(tf.int32, [None])

            self.output_keep_prob = tf.placeholder("float")
            self.input_keep_prob = tf.placeholder("float")

            # CNN model
            W_conv1 = weight_variable([5, 5, 3, 64])
            b_conv1 = bias_variable([64])
            h_conv1 = tf.nn.relu(conv2d(self.inputs, W_conv1) + b_conv1)

            W_conv2 = weight_variable([3, 3, 64, 64])
            b_conv2 = bias_variable([64])
            h_conv2 = tf.nn.relu(conv2d(h_conv1, W_conv2) + b_conv2)

            h_pool1 = max_pool_2x2(h_conv2)
            # out [batch_size, max_stepsize/4, num_features/4, 64]

            W_conv3 = weight_variable([3, 3, 64, 128])
            b_conv3 = bias_variable([128])
            h_conv3 = tf.nn.relu(conv2d(h_conv2, W_conv3) + b_conv3)

            h_pool2 = max_pool_2x2(h_conv3)

            shape = tf.shape(self.inputs)
            batch_s, max_timesteps, features_num = shape[0], shape[1], shape[2]
            # 16 = 64 / 4
            conv_out = tf.reshape(h_pool2, [batch_s, -1, num_features * 32])

            # print(conv_out.shape)
            # Defining the cell
            # Can be:
            #   tf.nn.rnn_cell.RNNCell
            #   tf.nn.rnn_cell.GRUCell
            cell1 = tf.contrib.rnn.LSTMCell(FLAGS.num_hidden, state_is_tuple=True)
            cell1 = tf.contrib.rnn.DropoutWrapper(cell = cell1,input_keep_prob=self.input_keep_prob, output_keep_prob=self.output_keep_prob)
            
            cell2 = tf.contrib.rnn.LSTMCell(FLAGS.num_hidden, state_is_tuple=True)
            cell2 = tf.contrib.rnn.DropoutWrapper(cell = cell2,input_keep_prob=self.input_keep_prob, output_keep_prob=self.output_keep_prob)
            # The second output is the last state and we will no use that
            outputs, _ = tf.nn.bidirectional_dynamic_rnn(cell1, cell2, conv_out, self.seq_len, dtype=tf.float32)
            
            #Stacking rnn cells
            # stack = tf.contrib.rnn.MultiRNNCell([tf.contrib.rnn.LSTMCell(FLAGS.num_hidden,state_is_tuple=True) for _ in range(FLAGS.num_layers)] , state_is_tuple=True)
            # outputs, _ = tf.nn.dynamic_rnn(stack, conv_out, self.seq_len, dtype=tf.float32)
            
            # Reshaping to apply the same weights over the timesteps
            outputs = tf.reshape(outputs, [-1, FLAGS.num_hidden])
            
            # Truncated normal with mean 0 and stdev=0.1
            # Tip: Try another initialization
            # see https://www.tensorflow.org/versions/r0.9/api_docs/python/contrib.layers.html#initializers
            W = tf.Variable(tf.truncated_normal([FLAGS.num_hidden,
                                                num_classes],
                                                stddev=0.1,dtype=tf.float32),name='W')
            # Zero initialization
            # Tip: Is tf.zeros_initializer the same?
            b = tf.Variable(tf.constant(0., dtype = tf.float32,shape=[num_classes],name='b'))
        
            # Doing the affine projection
            logits = tf.matmul(outputs, W) + b
        
            # Reshaping back to the original shape
            logits = tf.reshape(logits, [batch_s, -1, num_classes])
        
            # Time major
            logits = tf.transpose(logits, (1, 0, 2))
        
            self.global_step = tf.Variable(0,trainable=False)
        
            # self.loss = tf.nn.ctc_loss(labels=self.labels,inputs=logits, sequence_length=self.seq_len)
            self.loss = warpctc_tensorflow.ctc(activations=logits,flat_labels=self.labels,label_lengths=self.label_len,input_lengths=self.seq_len)

            self.cost = tf.reduce_mean(self.loss)
        
            #learning_rate=tf.train.exponential_decay(FLAGS.initial_learning_rate,
            #        global_step, 
            #        FLAGS.decay_steps,
            #        FLAGS.decay_rate,staircase=True)
        
            #optimizer = tf.train.MomentumOptimizer(learning_rate=learning_rate,
            #        momentum=FLAGS.momentum,use_nesterov=True).minimize(cost,global_step=global_step)
            self.optimizer = tf.train.AdamOptimizer(learning_rate=FLAGS.initial_learning_rate,
                    beta1=FLAGS.beta1,beta2=FLAGS.beta2).minimize(self.loss,global_step=self.global_step)
        
            # Option 2: tf.contrib.ctc.ctc_beam_search_decoder
            # (it's slower but you'll get better results)
            #decoded, log_prob = tf.nn.ctc_greedy_decoder(logits, seq_len,merge_repeated=False)
            self.decoded, self.log_prob = tf.nn.ctc_beam_search_decoder(logits, self.seq_len,merge_repeated=False)
        
            # Inaccuracy: label error rate
            #self.lerr = tf.reduce_mean(tf.edit_distance(tf.cast(self.decoded[0], tf.int32), self.labels))

            tf.summary.scalar('cost',self.cost)
            # tf.summary.scalar('lerr',self.lerr)
            self.merged_summay = tf.summary.merge_all()

def train():
    g = Graph()
    with g.graph.as_default():
        print('loading train data, please wait---------------------')
        train_feeder=utils.DataIterator(data_dirs=["/data/linkface/OcrData/OcrTrainData/", "/data/linkface/OcrData/OcrTrainDataElse/"])
        # train_feeder=utils.DataIterator(data_dirs=["/data/linkface/OcrData/OcrTestData_s/"])
        print('get image: ',train_feeder.size)

        print('loading validation data, please wait---------------------')
        val_feeder=utils.DataIterator(data_dirs=["/data/linkface/OcrData/OcrTestData_s/"])
        print('get image: ',val_feeder.size)

    num_train_samples = train_feeder.size # 12800
    num_batches_per_epoch = int(num_train_samples/FLAGS.batch_size) # example: 12800/64

    config=tf.ConfigProto(log_device_placement=False,allow_soft_placement=True)
    with tf.Session(graph=g.graph,config=config) as sess:
        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver(tf.global_variables(),max_to_keep=100)
        train_writer=tf.summary.FileWriter(FLAGS.log_dir+'/train',sess.graph)
        if FLAGS.restore:
            ckpt = tf.train.latest_checkpoint(FLAGS.checkpoint_dir)
            if ckpt:
                # the global_step will restore sa well
                saver.restore(sess,ckpt)
                print('restore from the checkpoint{0}'.format(ckpt))

        print('=============================begin training=============================')
        # the cuda trace
        #run_metadata = tf.RunMetadata()
        #trace_file = open('timeline.ctf.json','w')
        val_inputs,val_seq_len,val_labels,val_lab_len=val_feeder.input_index_generate_batch_warp()
        val_feed = {
            g.inputs: val_inputs,
            g.labels: val_labels,
            g.seq_len: val_seq_len,
            g.label_len: val_lab_len,
            g.output_keep_prob: 1.0,
            g.input_keep_prob: 1.0
        }

        for cur_epoch in range(FLAGS.num_epochs):
            shuffle_idx=np.random.permutation(num_train_samples)
            train_cost = train_err=0
            start = time.time()
            batch_time = time.time()
            #the tracing part
            for cur_batch in range(num_batches_per_epoch):
                batch_time = time.time()
                indexs = [shuffle_idx[i%num_train_samples] for i in range(cur_batch*FLAGS.batch_size,(cur_batch+1)*FLAGS.batch_size)]
                batch_inputs, batch_seq_len, batch_labels, batch_lab_len = train_feeder.input_index_generate_batch_warp(indexs)
                feed = {
                    g.inputs: batch_inputs,
                    g.labels: batch_labels,
                    g.seq_len: batch_seq_len,
                    g.label_len: batch_lab_len,
                    g.output_keep_prob: 1.0,
                    g.input_keep_prob: 0.8
                }
                
                batch_cost, step, _ = sess.run([g.cost, g.global_step, g.optimizer], feed)
                train_cost+=batch_cost*FLAGS.batch_size
                
                if (cur_batch+1)%100==0:
                    print("Batch {}, Cost {}, Time {}".format(cur_batch, batch_cost, time.time()-batch_time))
                    # dense_decoded = tf.sparse_tensor_to_dense(decoded, default_value=0).eval(session=sess)
                    # hit_lines, lines, hit_chars, chars = utils.accuracy_calculation2(batch_labels, dense_decoded,ignore_value=0,isPrint=True)
                    # log = "Batch {}, Cost: {}, Lines {}, Chars {},  line accuracy = {:.3f}, char accuracy = {:.3f}, time = {:.3f}"
                    # print(log.format(cur_batch, batch_cost, lines, chars, hit_lines * 1.0 / lines, hit_chars * 1.0 / chars,time.time()-batch_time))

                # save the checkpoint
                if step%FLAGS.save_steps == 0:
                    if not os.path.isdir(FLAGS.checkpoint_dir):
                        os.mkdir(FLAGS.checkpoint_dir)
                    logger.info('save the checkpoint of{0}',format(step))
                    saver.save(sess,os.path.join(FLAGS.checkpoint_dir,'ocr-model'),global_step=step)

            #validation
            avg_train_cost=train_cost/(num_batches_per_epoch*FLAGS.batch_size)
            d = sess.run(g.decoded[0], val_feed)
            dense_decoded = tf.sparse_tensor_to_dense(d, default_value=0).eval(session=sess)
            hit_lines, lines, hit_chars, chars = utils.accuracy_calculation2(val_feeder.labels, dense_decoded,ignore_value=0,isPrint=True)
        
            now = datetime.datetime.now()
            log = "{}-{} {}:{}:{} Epoch {}/{}, Lines {}, Chars {},  line accuracy = {:.3f}, char accuracy = {:.3f},train_cost = {:.3f}, time = {:.3f}"
            print(log.format(now.month,now.day,now.hour,now.minute,now.second,
                cur_epoch+1, FLAGS.num_epochs, lines, chars, hit_lines * 1.0 / lines, hit_chars * 1.0 / chars, avg_train_cost, time.time()-start))
        

if __name__ == '__main__':
    train()

