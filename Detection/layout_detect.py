# coding=utf-8
import os,sys
import glob
import json
import numpy as np
import fileinput
import tensorflow as tf

reload(sys) 
sys.setdefaultencoding("utf8")


NUM_LABELS = 10

# train_data_dir = '/Users/lairf/Documents/LinkfaceTrainingData/VechileLicense2017/JPEGImages/labelAll/'
# test_data_dir = '/Users/lairf/Documents/LinkfaceTrainingData/VechileLicense2017/JPEGImages/labelTest/'
# checkpoint_dir = '/Users/lairf/Documents/LinkfaceTrainingData/VechileLicense2017/JPEGImages/layout/'

train_data_dir = '/home/linkface/tf-faster-rcnn/data/VechileLicense2017/label/'
test_data_dir = '/home/linkface/tf-faster-rcnn/data/VechileLicense2017/labelTest/'
checkpoint_dir = '/home/linkface/tf-faster-rcnn/data/VechileLicense2017/layout/'

def dense_to_one_hot(labels_dense, num_classes=10):
  """Convert class labels from scalars to one-hot vectors."""
  num_labels = labels_dense.shape[0]
  index_offset = np.arange(num_labels) * num_classes
  labels_one_hot = np.zeros((num_labels, num_classes))
  labels_one_hot.flat[index_offset + labels_dense.ravel()] = 1
  return labels_one_hot

def loadData(path):
    in_path = path +  "*.json"
    boxdata = []
    labels = []
    for json_file in glob.glob(in_path):
        with open(json_file) as file:
            text = file.read().decode("utf-8").strip()
            data = json.loads(text)
            lines = data['objects']['ocr']
            outboxes = []
            outlabels = []
            label = 0
            if lines and len(lines) == 10:
                for line in lines:
                    left = (int(line['position']['left']) - 310)/620.0
                    top = (int(line['position']['top']) - 210)/420.0
                    right = (int(line['position']['right']) - 310)/620.0
                    bottom = (int(line['position']['bottom']) - 210)/420.0
                    outboxes.append([left, top, right - left, bottom - top])
                    boxdata.append([left, top, right - left, bottom - top])
                    outlabels.append(label)
                    label += 1
                
                # check card version
                if outboxes[4][2] > outboxes[5][2]: # old version
                    outlabels[4] = 5
                    outlabels[5] = 4
                    outlabels[6] = 7
                    outlabels[7]= 6
            
                labels.extend(outlabels)

    return boxdata, dense_to_one_hot(np.asarray(labels))

train_data, train_label = loadData(train_data_dir)
test_data, test_label = loadData(test_data_dir)

num_train_samples = len(train_label)
print("train:", num_train_samples)
print("test:", len(test_label))

# Linear Regression Modle
x = tf.placeholder("float", [None, 4])
W1 = tf.Variable(tf.zeros([4, 10]))
b1 = tf.Variable(tf.zeros([10]))

# o1 = tf.nn.relu(tf.matmul(x, W1) + b1)

# W2 = tf.Variable(tf.zeros([10, 10]))
# b2 = tf.Variable(tf.zeros([10]))

y = tf.nn.softmax(tf.matmul(x, W1) + b1)
y_ = tf.placeholder("float", [None,10])

cross_entropy = -tf.reduce_sum(y_*tf.log(tf.clip_by_value(y,1e-10,1.0)))
train_step = tf.train.AdamOptimizer(0.001).minimize(cross_entropy)

correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    saver = tf.train.Saver(tf.global_variables(),max_to_keep=100)
    ckpt = tf.train.latest_checkpoint(checkpoint_dir)
    if ckpt:
        # the global_step will restore sa well
        saver.restore(sess,ckpt)
        print('restore from the checkpoint{0}'.format(ckpt))

    print('=============================begin training=============================')

    batch_size = 64
    num_batches_per_epoch = num_train_samples / batch_size
    for epoch in range(100000):
        #the tracing part
        shuffle_idx=np.random.permutation(num_train_samples)
        train_cost = 0
        for cur_batch in range(num_batches_per_epoch):
            indexs = [shuffle_idx[i%num_train_samples] for i in range(cur_batch*batch_size,(cur_batch+1)*batch_size)]
            data_batch=[train_data[i] for i in indexs]
            label_batch=[train_label[i] for i in indexs]

            loss, _ = sess.run([cross_entropy, train_step], feed_dict={x: data_batch, y_: label_batch})
            train_cost += loss

        print("Step: {},  loss: {}".format(epoch+1, train_cost))
        if epoch % 20 == 0:
            print 'Accuracy: ', sess.run(accuracy, feed_dict={x: test_data, y_: test_label})
            # save the checkpoint
            if not os.path.isdir(checkpoint_dir):
                os.mkdir(checkpoint_dir)
            print('save the checkpoint')
            saver.save(sess, os.path.join(checkpoint_dir,'layout-model'),global_step=i)


   # print 'Accuracy: ', sess.run(accuracy, feed_dict={x: test_data, y_: test_labels})
    print 'Accuracy: ', sess.run(accuracy, feed_dict={x: test_data, y_: test_label})
    