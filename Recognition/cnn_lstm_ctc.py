"""Builds the OCR network.

Summary of available functions:

 # Compute input images and labels for training. If you would like to run
 # evaluations, use input() instead.
 inputs, labels = distorted_inputs()

 # Compute inference on the model inputs to make a prediction.
 predictions = inference(inputs)

 # Compute the total loss of the prediction with respect to the labels.
 loss = loss(predictions, labels)

 # Create a graph to run one step of training with respect to the loss.
 train_op = train(loss, global_step)
"""
# pylint: disable=missing-docstring
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import gzip
import os
import re
import sys

import tensorflow.python.platform
from six.moves import urllib
import tensorflow as tf
import warpctc_tensorflow
import utils
import ocr_input

FLAGS=utils.FLAGS

# Global constants describing the CIFAR-10 data set.
IMAGE_HEIGHT = ocr_input.IMAGE_HEIGHT
NUM_FEATURES = ocr_input.NUM_FEATURES
NUM_CLASSES = utils.NUM_CLASSES
# num_examples = ocr_input.num_examples
# num_examples_eval = ocr_input.num_examples_eval


# Constants describing the training process.
MOVING_AVERAGE_DECAY = 0.9999     # The decay to use for the moving average.
NUM_EPOCHS_PER_DECAY = 350.0      # Epochs after which learning rate decays.
LEARNING_RATE_DECAY_FACTOR = 0.1  # Learning rate decay factor.
INITIAL_LEARNING_RATE = 0.1       # Initial learning rate.

# If a model is trained with multiple GPU's prefix all Op names with tower_name
# to differentiate the operations. Note that this prefix is removed from the
# names of the summaries when visualizing a model.
TOWER_NAME = 'tower'

def _activation_summary(x):
  """Helper to create summaries for activations.

  Creates a summary that provides a histogram of activations.
  Creates a summary that measure the sparsity of activations.

  Args:
    x: Tensor
  Returns:
    nothing
  """
  # Remove 'tower_[0-9]/' from the name in case this is a multi-GPU training
  # session. This helps the clarity of presentation on tensorboard.
  tensor_name = re.sub('%s_[0-9]*/' % TOWER_NAME, '', x.op.name)
  tf.summary.histogram(tensor_name + '/activations', x)
  tf.summary.scalar(tensor_name + '/sparsity', tf.nn.zero_fraction(x))


def _variable_on_cpu(name, shape, initializer):
  """Helper to create a Variable stored on CPU memory.

  Args:
    name: name of the variable
    shape: list of ints
    initializer: initializer for Variable

  Returns:
    Variable Tensor
  """
  with tf.device('/cpu:0'):
    var = tf.get_variable(name, shape, initializer=initializer, dtype=tf.float32)
  return var


def _variable_with_weight_decay(name, shape, stddev, wd):
  """Helper to create an initialized Variable with weight decay.

  Note that the Variable is initialized with a truncated normal distribution.
  A weight decay is added only if one is specified.

  Args:
    name: name of the variable
    shape: list of ints
    stddev: standard deviation of a truncated Gaussian
    wd: add L2Loss weight decay multiplied by this float. If None, weight
        decay is not added for this Variable.

  Returns:
    Variable Tensor
  """
  var = _variable_on_cpu(name, shape,
                         tf.truncated_normal_initializer(stddev=stddev))
  if wd:
    weight_decay = tf.multiply(tf.nn.l2_loss(var), wd, name='weight_loss')
    tf.add_to_collection('losses', weight_decay)
  return var


def distorted_inputs():
  """Construct distorted input for OCR training using the Reader ops.

  Returns:
    images: Images. 4D tensor of [batch_size, IMAGE_SIZE, IMAGE_SIZE, 3] size.
    labels: Labels. 1D tensor of [batch_size] size.

  Raises:
    ValueError: If no train_dir
  """
  if not FLAGS.train_dir:
    raise ValueError('Please supply a train_dir')
  return ocr_input.distorted_inputs(data_dir=FLAGS.train_dir,
                                        batch_size=FLAGS.batch_size)


def inputs():
  """Construct input for OCR evaluation using the Reader ops.

  Args:
    eval_data: bool, indicating if one should use the train or eval data set.

  Returns:
    images: Images. 4D tensor of [batch_size, IMAGE_SIZE, IMAGE_SIZE, 3] size.
    labels: Labels. 1D tensor of [batch_size] size.

  Raises:
    ValueError: If no test_dir
  """
  if not FLAGS.test_dir:
    raise ValueError('Please supply a test_dir')
  return ocr_input.inputs(data_dir=FLAGS.test_dir,
                              batch_size=FLAGS.batch_size)

def inference(images, seq_lens):
    # CNN model
    with tf.variable_scope('conv1') as scope:
      kernel = _variable_with_weight_decay('weights', shape=[3, 3, 3, 64],
                                          stddev=1e-4, wd=0.1)
      conv = tf.nn.conv2d(images, kernel, [1, 1, 1, 1], padding='SAME')
      biases = _variable_on_cpu('biases', [64], tf.constant_initializer(0.0))
      bias = tf.nn.bias_add(conv, biases)
      conv1 = tf.nn.relu(bias, name=scope.name)
      _activation_summary(conv1)

    # pool1
    pool1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1],
                          padding='SAME', name='pool1')
    # norm1
    # norm1 = tf.nn.lrn(pool1, 4, bias=1.0, alpha=0.001 / 9.0, beta=0.75,
    #                 name='norm1')

    # conv2
    with tf.variable_scope('conv2') as scope:
      kernel = _variable_with_weight_decay('weights', shape=[3, 3, 64, 128],
                                          stddev=1e-4, wd=0.1)
      conv = tf.nn.conv2d(pool1, kernel, [1, 1, 1, 1], padding='SAME')
      biases = _variable_on_cpu('biases', [128], tf.constant_initializer(0.1))
      bias = tf.nn.bias_add(conv, biases)
      conv2 = tf.nn.relu(bias, name=scope.name)
      _activation_summary(conv2)

    # norm2
    # norm2 = tf.nn.lrn(conv2, 4, bias=1.0, alpha=0.001 / 9.0, beta=0.75,
    #                   name='norm2')
    # pool2
    pool2 = tf.nn.max_pool(conv2, ksize=[1, 2, 2, 1],
                         strides=[1, 2, 2, 1], padding='SAME', name='pool2')

    shape = tf.shape(pool2)
    batch_s, max_timesteps, features_num = shape[0], shape[1], shape[2]

    # 32 = 128 / 4
    conv_out = tf.reshape(pool2, [batch_s, -1, NUM_FEATURES * 32])

    # bi-lstm
    with tf.variable_scope('forward'):
      lstm_fw_cell = tf.contrib.rnn.BasicLSTMCell(FLAGS.num_hidden, reuse=tf.get_variable_scope().reuse)
    with tf.variable_scope('backward'):
      lstm_bw_cell = tf.contrib.rnn.BasicLSTMCell(FLAGS.num_hidden, reuse=tf.get_variable_scope().reuse)  

    stack = tf.contrib.rnn.MultiRNNCell([lstm_fw_cell, lstm_bw_cell], state_is_tuple=True)
      
    # with tf.variable_scope('cell2') as scope:
    #   cell2 = tf.contrib.rnn.LSTMCell(FLAGS.num_hidden,state_is_tuple=True, reuse=True)

    
    # # The second output is the last state and we will no use that
    outputs, _ = tf.nn.dynamic_rnn(stack, conv_out, seq_lens, dtype=tf.float32)
    # Reshaping to apply the same weights over the timesteps
    outputs = tf.reshape(outputs, [-1, FLAGS.num_hidden])
    
    with tf.variable_scope('fc') as scope:
      W = _variable_with_weight_decay('weights', shape=[FLAGS.num_hidden, NUM_CLASSES],stddev=1e-4, wd=0.1)
      b = _variable_on_cpu('biases', [NUM_CLASSES], tf.constant_initializer(0.1))
      logits = tf.matmul(outputs, W) + b
      logits = tf.reshape(logits, [batch_s, -1, NUM_CLASSES])
      # Time major
      logits = tf.transpose(logits, (1, 0, 2))
      # _activation_summary(logits)

    return logits

def loss(logits, seq_lens, labels, label_lens):
    loss = warpctc_tensorflow.ctc(activations=logits,flat_labels=labels,label_lengths=label_lens,input_lengths=seq_lens)
    cost = tf.reduce_mean(loss)
    tf.add_to_collection('losses', cost)
    return tf.add_n(tf.get_collection('losses'), name='total_loss')

def _add_loss_summaries(total_loss):
  """Add summaries for losses in CIFAR-10 model.

  Generates moving average for all losses and associated summaries for
  visualizing the performance of the network.

  Args:
    total_loss: Total loss from loss().
  Returns:
    loss_averages_op: op for generating moving averages of losses.
  """
  # Compute the moving average of all individual losses and the total loss.
  loss_averages = tf.train.ExponentialMovingAverage(0.9, name='avg')
  losses = tf.get_collection('losses')
  loss_averages_op = loss_averages.apply(losses + [total_loss])

  # Attach a scalar summary to all individual losses and the total loss; do the
  # same for the averaged version of the losses.
  for l in losses + [total_loss]:
    # Name each loss as '(raw)' and name the moving average version of the loss
    # as the original loss name.
    tf.summary.scalar(l.op.name +' (raw)', l)
    tf.summary.scalar(l.op.name, loss_averages.average(l))

  return loss_averages_op


def train(total_loss, global_step):
  """Train OCR model.

  Create an optimizer and apply to all trainable variables. Add moving
  average for all trainable variables.

  Args:
    total_loss: Total loss from loss().
    global_step: Integer Variable counting the number of training steps
      processed.
  Returns:
    train_op: op for training.
  """
  # Variables that affect learning rate.
  num_batches_per_epoch = ocr_input.num_examples / FLAGS.batch_size
  decay_steps = int(num_batches_per_epoch * NUM_EPOCHS_PER_DECAY)

  # Decay the learning rate exponentially based on the number of steps.
  lr = tf.train.exponential_decay(FLAGS.initial_learning_rate,
                                  global_step,
                                  decay_steps,
                                  LEARNING_RATE_DECAY_FACTOR,
                                  staircase=True)
  tf.summary.scalar('learning_rate', lr)

  # Generate moving averages of all losses and associated summaries.
  loss_averages_op = _add_loss_summaries(total_loss)

  # Compute gradients.
  with tf.control_dependencies([loss_averages_op]):
    opt = tf.train.tf.train.AdamOptimizer(learning_rate=lr,
                    beta1=FLAGS.beta1,beta2=FLAGS.beta2)
    grads = opt.compute_gradients(total_loss)

  # Apply gradients.
  apply_gradient_op = opt.apply_gradients(grads, global_step=global_step)

  # Add histograms for trainable variables.
  for var in tf.trainable_variables():
    tf.summary.histogram(var.op.name, var)

  # Add histograms for gradients.
  for grad, var in grads:
    if grad:
      tf.summary.histogram(var.op.name + '/gradients', grad)

  # Track the moving averages of all trainable variables.
  variable_averages = tf.train.ExponentialMovingAverage(
      MOVING_AVERAGE_DECAY, global_step)
  variables_averages_op = variable_averages.apply(tf.trainable_variables())

  with tf.control_dependencies([apply_gradient_op, variables_averages_op]):
    train_op = tf.no_op(name='train')

  return train_op
