# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os,sys
import glob
import tensorflow.python.platform
from six.moves import xrange  # pylint: disable=redefined-builtin
import tensorflow as tf
import numpy as np
from tensorflow.python.platform import gfile
import utils

reload(sys) 
sys.setdefaultencoding("utf8")

# The Input image is resize to the same height, and padding to the same width
IMAGE_HEIGHT = 28
IMAGE_WIDTH = 28
NUM_FEATURES = 28
MAX_IMAGE_HEIGHT = 800
MAX_LABEL_LENTH = 60

num_examples = utils.FLAGS.num_examples
num_preprocess_threads = utils.FLAGS.num_preprocess_threads
num_examples_eval = 600

def read_labeled_image_list(data_dir):
    """Trace teh data_dir, record the image_file_path and lables
    Args:
       data_dir: a folder keeps the train/test images and lables
    Returns:
       List with all filenames and lables
    """
    filenames = []
    labels = []
    lengths = []
    in_path = data_dir +  "train*"
    print(in_path)
    for img_file in glob.glob(in_path):
        label_file = img_file[:-3] + "txt"
        if os.path.exists(label_file):
            # read labels
            with open(label_file) as file:
              label = file.read().decode("utf-8").strip()
              code = utils.encode(label)
              length = len(code)
              if length <= MAX_LABEL_LENTH:
                code = np.lib.pad(code, (0, MAX_LABEL_LENTH - length), 'constant')
                labels.append(code)
                lengths.append(MAX_LABEL_LENTH)
                filenames.append(img_file)
              else:
                print(label)
          
    return filenames, labels, lengths

def read_images_from_disk(input_queue):
    """Consumes a single filename and label as a ' '-delimited string.
    Args:
      filename_and_label_tensor: A scalar string tensor.
    Returns:
      Two tensors: the decoded image, and the string label.
    """
    label = input_queue[1]
    # label = tf.read_file(input_queue[1])
    # print(label)

    file_contents = tf.read_file(input_queue[0])
    example = tf.image.decode_jpeg(file_contents, channels=3)
    example = tf.image.transpose_image(example)
    return example, label, input_queue[1]
                                          
def read_ocr_data(filename_queue):
    """Reads and parses examples from OCR data files.

    Recommendation: if you want N-way read parallelism, call this function
    N times.  This will give you N independent Readers reading different
    files & positions within those files, which will give better mixing of
    examples.

    Args:
    filename_queue: A queue of strings with the filenames to read from.

    Returns:
    An object representing a single example, with the following fields:
        height: number of rows in the result (32)
        width: number of columns in the result (32)
        depth: number of color channels in the result (3)
        key: a scalar string Tensor describing the filename & record number
        for this example.
        label: an int32 Tensor with the label in the range 0..9.
        uint8image: a [height, width, depth] uint8 Tensor with the image data
    """

    class OCRRecord(object):
      pass
    result = OCRRecord()
    
    reader  = tf.WholeFileReader()
    result.key, value = reader.read(filename_queue)

    # Convert from a string to a vector of uint8 that is record_bytes long.
    image = tf.image.decode_jpeg(value)

    # swap x, y;  each row as feature sequence which inputs in bi-lstm
    result.image = tf.transpose(image, (1, 0, 2))

    tokens = tf.string_split(result.key, '/')

    file_name = tokens[1][-1][:-4]
    result.label = g_labels[file_name]
    return result


def _generate_image_and_label_batch(image, label, label_length, min_queue_examples,
                                    batch_size):
  """Construct a queued batch of images and labels.

  Args:
    image: 3-D Tensor of [height, width, 3] of type.float32.
    label: 1-D Tensor of type.int32
    min_queue_examples: int32, minimum number of samples to retain
      in the queue that provides of batches of examples.
    batch_size: Number of images per batch.

  Returns:
    images: Images. 4D tensor of [batch_size, height, width, 3] size.
    labels: Labels. 1D tensor of [batch_size] size.
  """
  # Create a queue that shuffles the examples, and then
  # read 'batch_size' images + labels from the example queue.

  image, height = pad_image(image)
  zero_pads = tf.zeros([MAX_LABEL_LENTH - tf.shape(label)[0]], dtype=label.dtype)
  label = tf.concat([label, zero_pads], 0)
  label = tf.reshape(label, [MAX_LABEL_LENTH])
  # image = tf.reshape(image, [MAX_IMAGE_HEIGHT, IMAGE_WIDTH, 3])
  
  # label = pad_zeros(label, label_length)
  # label = tf.reshape(label, [MAX_LABEL_LENTH])
  # label = tf.zeros([MAX_LABEL_LENTH], tf.int32)

  images, image_heights, labels, label_lengths = tf.train.shuffle_batch(
      [image, height, label, MAX_LABEL_LENTH],
      batch_size=batch_size,
      num_threads=num_preprocess_threads,
      capacity=min_queue_examples + 3 * batch_size,
      min_after_dequeue=min_queue_examples)

  # labels = trim_zeros(labels)
  # flat_labels = tf.concat(0, labels)
  flat_labels = tf.reshape(labels, [-1])
  # images, image_heights = pad_images(images)

  # labels = tf.reshape(labels, [batch_size])
  
  # images, labels, seq_lens = tf.train.batch([image, label, height], batch_size=batch_size)
  # encode_labels = utils.encode_label(labels)
  # batch_labels, batch_labels_len = utils.get_label_and_lens(labels)
  
  # batch_inputs, batch_seq_len = utils.pad_input_sequences(images)
  
  # Display the training images in the visualizer.
  # tf.image_summary('images', images)

  return images, tf.cast(image_heights/4, tf.int32), flat_labels, label_lengths


def read_and_decode(filename_queue):
    
    reader = tf.TFRecordReader()

    _, serialized_example = reader.read(filename_queue)

    features = tf.parse_single_example(
      serialized_example,
      # Defaults are not specified since both keys are required.
      features={
        'image/height': tf.FixedLenFeature([], tf.int64),
        'image/width': tf.FixedLenFeature([], tf.int64),
        'image/shape': tf.FixedLenFeature([], tf.string),
        'image/colorspace': tf.FixedLenFeature([], tf.string),
        'image/channels': tf.FixedLenFeature([], tf.int64),
        'image/class/label': tf.FixedLenFeature([], tf.string),
        'image/class/text': tf.FixedLenFeature([], tf.string),
        'image/format': tf.FixedLenFeature([], tf.string),
        'image/filename': tf.FixedLenFeature([], tf.string),
        'image/encoded': tf.FixedLenFeature([], tf.string)
        })

    image = tf.image.decode_jpeg(features['image/encoded'],  channels=3)
    shape = tf.decode_raw(features['image/shape'], tf.int32)
    image = tf.reshape(image, shape)

    # swap x, y;  each row as feature sequence which inputs in bi-lstm
    image = tf.transpose(image, (1, 0, 2))

    label = tf.decode_raw(features['image/class/label'], tf.int32)
    label_length = tf.shape(label)[0]
    text =  features['image/class/text']
    
    return image, text, label, label_length

def distorted_inputs(data_dir, batch_size): 
  files = [ file for file in glob.glob(data_dir)]
  filename_queue = tf.train.string_input_producer(files, shuffle=True)
  image, text, label, label_length = read_and_decode(filename_queue)
  
  # height = reshaped_image.shape[0]
  # width = reshaped_image.shape[1]

  # Image processing for training the network. Note the many random
  # distortions applied to the image.

  # Because these operations are not commutative, consider randomizing
  # randomize the order their operation.
  # distorted_image = tf.image.random_crop(reshaped_image, [height, width])
  distorted_image = tf.image.random_brightness(image, max_delta=63)
  distorted_image = tf.image.random_contrast(distorted_image,lower=0.2, upper=1.8)
  distorted_image = tf.image.random_saturation(distorted_image,lower=0.2, upper=1.8)

  # Subtract off the mean and divide by the variance of the pixels.
  float_image = tf.image.per_image_standardization(distorted_image)

  # Ensure that the random shuffling has good mixing properties.
  # min_fraction_of_examples_in_queue = 0.4
  # min_queue_examples = int(num_examples *
  #                          min_fraction_of_examples_in_queue)
  min_queue_examples = 1000
  print ('Filling queue with %d OCR images before starting to train. '
         'This will take a few minutes.' % min_queue_examples)

  # Generate a batch of images and labels by building up a queue of examples.
  return _generate_image_and_label_batch(float_image, label, label_length,
                                         min_queue_examples, batch_size)


def inputs(data_dir, batch_size):
  """Construct input for OCR evaluation using the Reader ops.

  Args:
    eval_data: bool, indicating if one should use the train or eval data set.
    data_dir: Path to the OCR data directory.
    batch_size: Number of images per batch.

  Returns:
    images: Images. 4D tensor of [batch_size, IMAGE_SIZE, IMAGE_SIZE, 3] size.
    labels: Labels. 1D tensor of [batch_size] size.
  """
  
  files = [ file for file in glob.glob(data_dir)]
  filename_queue = tf.train.string_input_producer(files, shuffle=True)
  image, text, label, label_length = read_and_decode(filename_queue)

  # Subtract off the mean and divide by the variance of the pixels.
  float_image = tf.image.per_image_standardization(image)

  # Ensure that the random shuffling has good mixing properties.
  # min_fraction_of_examples_in_queue = 0.4
  # min_queue_examples = int(num_examples_eval *
  #                          min_fraction_of_examples_in_queue)
  min_queue_examples = 300
  # Generate a batch of images and labels by building up a queue of examples.
  return _generate_image_and_label_batch(float_image, labels, label_length,
                                         min_queue_examples, batch_size)

def pad_zeros(sequence, len):
  sequence = np.lib.pad(sequence, (0, MAX_LABEL_LENTH), 'constant')

  return sequence

def trim_zeros(sequences):
  for i in range(len(sequences)):
    sequences[i] = np.trim_zeros(sequences[i], 'b')
  return sequences

# add bottom or right paddings to make sure all images are in same size
def pad_images(images):
  image_heights = []
  for image in images:
    image_heights.append(tf.shape(image)[0])

  max_height = max(image_heights)
  padding_images = []
  for image in images:
    image = tf.image.pad_to_bounding_box(image, 0, 0, max_height, IMAGE_WIDTH)
    padding_images.append(image)

  return padding_images, image_heights

def pad_image(image):
  pimage = tf.image.pad_to_bounding_box(image, 0, 0, MAX_IMAGE_HEIGHT, IMAGE_WIDTH)
  return pimage, tf.shape(image)[0]
