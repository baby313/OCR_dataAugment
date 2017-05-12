import tensorflow as tf
import matplotlib.pyplot as plt

tfrecords_filenames = [
    '/Users/lairf/AI-projects/OCR/Data/address_train_tfrecord/validation-00000-of-00001'
]

filename_queue = tf.train.string_input_producer(tfrecords_filenames, num_epochs=10)


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

    # Convert from a scalar string tensor (whose single string has
    # length mnist.IMAGE_PIXELS) to a uint8 tensor with shape
    # [mnist.IMAGE_PIXELS].
    image = tf.image.decode_jpeg(features['image/encoded'],  channels=3)
    shape = tf.decode_raw(features['image/shape'], tf.int32)
    image = tf.reshape(image, shape)

    label = tf.decode_raw(features['image/class/label'], tf.int32)
    text =  features['image/class/text']
    
    return image, text, label

# Even when reading in multiple threads, share the filename
# queue.
image, text, label = read_and_decode(filename_queue)

images,texts, labels = tf.train.shuffle_batch(
      [image,text, label],
      batch_size=2,
      num_threads=1,
      capacity=2,
      min_after_dequeue=2)


# The op for initializing the variables.
init_op = tf.group(tf.global_variables_initializer(),
                   tf.local_variables_initializer())

with tf.Session()  as sess:
    
    sess.run(init_op)
    
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)
    
    # Let's read off 3 batches just for example
    for i in xrange(1):
        print (label)
        img, text, label = sess.run([image, text, label])
        print(img.shape)
        
        print('current batch')
        
        # We selected the batch size of two
        # So we should get two image pairs in each batch
        # Let's make sure it is random

        print(text)
        print(label)
        plt.imshow(img)
        plt.show()
        
    
    coord.request_stop()
    coord.join(threads)