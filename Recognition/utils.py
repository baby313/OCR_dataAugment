# coding=utf-8
import os,sys
import glob
import numpy as np
import tensorflow as tf
import random
import cv2,time
from tensorflow.python.client import device_lib
import editdistance

reload(sys) 
sys.setdefaultencoding("utf8")
print sys.getdefaultencoding()
#num_train_samples = 128000

num_features=28
image_height=28
max_width = 360
SPACE_INDEX=0
SPACE_TOKEN=''

maxPrintLen = 10
tf.app.flags.DEFINE_boolean('restore', True, 'whether to restore from the latest checkpoint')
tf.app.flags.DEFINE_string('checkpoint_dir', './checkpoint_read_one_time/', 'the checkpoint dir')
tf.app.flags.DEFINE_float('initial_learning_rate', 1e-3, 'inital lr')

tf.app.flags.DEFINE_integer('num_layers', 2, 'number of layer')
tf.app.flags.DEFINE_integer('num_hidden', 400, 'number of hidden')
tf.app.flags.DEFINE_integer('num_epochs', 10000, 'maximum epochs')
tf.app.flags.DEFINE_integer('batch_size', 64, 'the batch_size')
tf.app.flags.DEFINE_integer('num_preprocess_threads', 4, 'number of preprocess threads')
tf.app.flags.DEFINE_integer('save_steps', 1000, 'the step to save checkpoint')
tf.app.flags.DEFINE_integer('validation_steps', 10000, 'the step to validation')


tf.app.flags.DEFINE_float('decay_rate', 0.8, 'the lr decay rate')
tf.app.flags.DEFINE_float('beta1', 0.9, 'parameter of adam optimizer beta1')
tf.app.flags.DEFINE_float('beta2', 0.999, 'adam parameter beta2')

tf.app.flags.DEFINE_integer('decay_steps', 3000, 'the lr decay_step for momentum optimizer')
tf.app.flags.DEFINE_float('momentum', 0.9, 'the momentum')

tf.app.flags.DEFINE_string('log_dir', './log', 'the logging dir')
tf.app.flags.DEFINE_integer('num_examples', 250000, 'number of train examples')
tf.app.flags.DEFINE_string('train_dir', '/data/linkface/OcrData/tfrecords/train_real*', """Path to the ocr data directory.""")
tf.app.flags.DEFINE_string('test_dir', '/data/linkface/OcrData/tfrecords/test_s*', """Path to the ocr data directory.""")

tf.app.flags.DEFINE_integer('max_steps', 1000000, """Number of batches to run.""")
tf.app.flags.DEFINE_integer('num_gpus', 4, """How many GPUs to use.""")
tf.app.flags.DEFINE_boolean('log_device_placement', False, """Whether to log device placement.""")
                        
FLAGS=tf.app.flags.FLAGS

#num_batches_per_epoch = int(num_train_samples/FLAGS.batch_size)

encode_maps={}
decode_maps={}
def loadDict(dictPath):
    pos = len(encode_maps)
    with open(dictPath) as file:
        for line in file:
            char = line.decode("utf-8").strip()
            if char not in encode_maps:
                encode_maps[char]=pos
                decode_maps[pos]=char
                pos += 1

encode_maps[SPACE_TOKEN]=SPACE_INDEX
decode_maps[SPACE_INDEX]=SPACE_TOKEN
loadDict("../Dicts/Chars.txt")
loadDict("../Dicts/GB2312.txt")
NUM_CLASSES = len(encode_maps)
NUM_CLASSES += 1
print("Char set: ", NUM_CLASSES)

def encode(label):
    code = []
    if label == SPACE_TOKEN:
        code = [SPACE_INDEX]
    else:
        for i in range(len(label)):
            if label[i] in encode_maps:
                code.append(encode_maps[label[i]])
            else:
                code.append(SPACE_INDEX)
                print(label[i])
    return code

def encode_labels(labels):
    codes = [encode(label) for label in labels]
    return codes

def decode(code):
    res = ''
    for i in encode_label:
        if i < 0:
            res += ' '
        else:
            res += decode_maps[i]
    return res

def decode_lables(codes):
    labels = [decode(code) for code in codes]
    return labels

class DataIterator:
    def __init__(self, data_dirs):
        self.image_names = []
        self.images = []
        self.labels= []
        self.lens = []

        for data_dir in data_dirs:
            in_path = data_dir +  "*.jpg"
            #print(in_path)
            for img_file in glob.glob(in_path):
                label_file = img_file[:-3] + "txt"
                # print(label_file)
                if os.path.exists(label_file):
                    self.image_names.append(img_file)
                    im = cv2.imread(img_file).astype(np.float32)/255.
                    
                    # resize to same height(image_height=28), different width will consume time on padding
                    image_width = im.shape[0] * im.shape[1] / image_height
                    im = cv2.resize(im,(image_width, image_height))

                    # tensorflow must fix size image in batch
                    # shape =  im.shape
                    # height, width = shape[0], shape[1]
                    # if width >= max_width:
                    #     im = cv2.resize(im,(max_width, image_height))
                    # else:
                    #     w = max_width - width
                    #     h = height - image_height
                    #     im = cv2.copyMakeBorder(im, 0, h, 0, w, cv2.BORDER_CONSTANT, (0,0,0))

                    # swap x, y;  each row as feature sequence which inputs in bi-lstm
                    im = im.swapaxes(0,1)
                    self.images.append(im)

                    # after pooling, the feature length or the height of the image is resize to height/4
                    # self.lens.append(width/4)

                    # read labels
                    with open(label_file) as file:
                        code = file.read().decode("utf-8").strip()
                        # print(code)
                        # print(len(code))
                        # label = [SPACE_INDEX if code == SPACE_TOKEN else encode_maps[c] for c in list(code)]
                        label = []
                        if code == SPACE_TOKEN:
                            label = [SPACE_INDEX]
                        else:
                            for i in range(len(code)):
                                if code[i] in encode_maps:
                                    label.append(encode_maps[code[i]])
                                else:
                                    label.append(SPACE_INDEX)
                                    print(code[i])

                        # print(label)
                        self.labels.append(label)
                        #print(label_file,' ',code)
            #random.shuffle(self.image_names)

    @property
    def size(self):
        return len(self.labels)

    def the_label(self,indexs):
        labels=[]
        for i in indexs:
            labels.append(self.labels[i])
        return labels

    #@staticmethod
    #def data_augmentation(images):
    #    if FLAGS.random_flip_up_down:
    #        images = tf.image.random_flip_up_down(images)
    #    if FLAGS.random_brightness:
    #        images = tf.image.random_brightness(images, max_delta=0.3)
    #    if FLAGS.random_contrast:
    #        images = tf.image.random_contrast(images, 0.8, 1.2)
    #    return images

    def get_input_lens(self,sequences):
        lengths = np.asarray([len(s) for s in sequences], dtype=np.int64)
        return sequences,lengths

    
    def input_index_generate_batch(self,index=None):
        if index:
            image_batch=[self.images[i] for i in index]
            label_batch=[self.labels[i] for i in index]
        else:
            # get the whole data as input
            image_batch=self.images
            label_batch=self.labels

        # def get_input_lens(sequences):
        #     lengths = np.asarray([len(s) for s in sequences], dtype=np.int64)
        #     return sequences,lengths
        # batch_inputs,batch_seq_len = get_input_lens(np.array(image_batch))
        #batch_inputs,batch_seq_len = pad_input_sequences(np.array(image_batch))
        # batch_labels = sparse_tuple_from_label(label_batch)
        batch_inputs, batch_seq_len = pad_input_sequences(image_batch)

        return batch_inputs, batch_seq_len/4, label_batch

    def input_index_generate_batch_warp(self,index=None):
        if index:
            image_batch=[self.images[i] for i in index]
            label_batch=[self.labels[i] for i in index]
        else:
            # get the whole data as input
            image_batch=self.images
            label_batch=self.labels
        image_batch=np.array(image_batch)
        #print(image_batch.shape)
        batch_inputs, batch_seq_len = pad_input_sequences(image_batch)
        # batch_inputs,batch_seq_len = self.get_input_lens(image_batch)
        batch_labels,batch_labels_len = get_label_and_lens(label_batch)
        #sparse_labels = sparse_tuple_from_label(label_batch)
        return batch_inputs,batch_seq_len/4, batch_labels,batch_labels_len

def get_label_and_lens(sequences,dtype=np.int32):
    '''
    Args:
        sequences:a list of lists of dtype where each element is a sequence
    Returns:
        A tuple with(flat_labels,per_lebel_len_list)
    '''
    flat_labels = []
    labels_len=[]

    for n, seq in enumerate(sequences):
        flat_labels.extend(seq)
        labels_len.append(len(seq))

    flat_labels = np.asarray(flat_labels, dtype=dtype)
    labels_len = np.asarray(labels_len, dtype=dtype)
    return flat_labels,labels_len

    def input_index_generate_batch_warp(self,index=None):
        if index:
            image_batch=[self.images[i] for i in index]
            label_batch=[self.labels[i] for i in index]
        else:
            # get the whole data as input
            image_batch=self.images
            label_batch=self.labels
        image_batch=np.array(image_batch)
        #print(image_batch.shape)
        batch_inputs, batch_seq_len = pad_input_sequences(image_batch)
        # batch_inputs,batch_seq_len = self.get_input_lens(image_batch)
        batch_labels,batch_labels_len = get_label_and_lens(label_batch)
        #sparse_labels = sparse_tuple_from_label(label_batch)
        return batch_inputs,batch_seq_len/4, batch_labels,batch_labels_len

def get_label_and_lens(sequences,dtype=np.int32):
    '''
    Args:
        sequences:a list of lists of dtype where each element is a sequence
    Returns:
        A tuple with(flat_labels,per_lebel_len_list)
    '''
    flat_labels = []
    labels_len=[]

    for n, seq in enumerate(sequences):
        flat_labels.extend(seq)
        labels_len.append(len(seq))

    flat_labels = np.asarray(flat_labels, dtype=dtype)
    labels_len = np.asarray(labels_len, dtype=dtype)
    return flat_labels,labels_len

def accuracy_calculation(original_seq,decoded_seq,ignore_value=-1,isPrint = True):
    if  len(original_seq)!=len(decoded_seq):
        print('original lengths is different from the decoded_seq,please check again')
        return 0
    count = 0
    for i,origin_label in enumerate(original_seq):
        decoded_label  = [j for j in decoded_seq[i] if j!=ignore_value]
        if isPrint and i<maxPrintLen:
            print('seq{0:4d}: origin: {1}'.format(i, origin_label))
            print('seq{0:4d}: decoded:{1}'.format(i, decoded_label))
        if origin_label == decoded_label: count+=1
    return count*1.0/len(original_seq)

def accuracy_calculation2(original_seq,decoded_seq,ignore_value=-1,isPrint = True):
    if  len(original_seq)!=len(decoded_seq):
        print('original lengths is different from the decoded_seq,please check again')
        return 0
    
    line_hit_count = 0
    char_hit_count = 0
    total_chars = 0
    total_lines = 0

    for i,origin_label in enumerate(original_seq):
        decoded_label  = [j for j in decoded_seq[i] if j!=ignore_value]
        distance = editdistance.eval(origin_label, decoded_label)
        total_chars += len(origin_label)
        char_hit_count += max(len(origin_label) - distance, 0)
        total_lines += 1
        if distance == 0: line_hit_count += 1

    return line_hit_count, total_lines, char_hit_count, total_chars

def sparse_tuple_from_label(sequences, dtype=np.int32):
    """Create a sparse representention of x.
    Args:
        sequences: a list of lists of type dtype where each element is a sequence
    Returns:
        A tuple with (indices, values, shape)
    """
    indices = []
    values = []
    # print(sequences)
    for n, seq in enumerate(sequences):
        indices.extend(zip([n]*len(seq), range(len(seq))))
        values.extend(seq)

    indices = np.asarray(indices, dtype=np.int64)
    values = np.asarray(values, dtype=dtype)
    shape = np.asarray([len(sequences), np.asarray(indices).max(0)[1]+1], dtype=np.int64)

    return indices, values, shape

def pad_input_sequences(sequences, maxlen=None, dtype=np.float32,
                  padding='post', truncating='post', value=0.):
    '''Pads each sequence to the same length: the length of the longest
    sequence.
        If maxlen is provided, any sequence longer than maxlen is truncated to
        maxlen. Truncation happens off either the beginning or the end
        (default) of the sequence. Supports post-padding (default) and
        pre-padding.
        Args:
            sequences: list of lists where each element is a sequence
            maxlen: int, maximum length
            dtype: type to cast the resulting sequence.
            padding: 'pre' or 'post', pad either before or after each sequence.
            truncating: 'pre' or 'post', remove values from sequences larger
            than maxlen either in the beginning or in the end of the sequence
            value: float, value to pad the sequences to the desired value.
        Returns
            x: numpy array with dimensions (number_of_sequences, maxlen)
            lengths: numpy array with the original sequence lengths
    '''
    lengths = np.asarray([len(s) for s in sequences], dtype=np.int64)

    nb_samples = len(sequences)
    if maxlen is None:
        maxlen = np.max(lengths)

    # take the sample shape from the first non empty sequence
    # checking for consistency in the main loop below.
    sample_shape = tuple()
    for s in sequences:
        if len(s) > 0:
            sample_shape = np.asarray(s).shape[1:]
            break

    x = (np.ones((nb_samples, maxlen) + sample_shape) * value).astype(dtype)
    for idx, s in enumerate(sequences):
        if len(s) == 0:
            continue  # empty list was found
        if truncating == 'pre':
            trunc = s[-maxlen:]
        elif truncating == 'post':
            trunc = s[:maxlen]
        else:
            raise ValueError('Truncating type "%s" not understood' % truncating)

        # check `trunc` has expected shape
        trunc = np.asarray(trunc, dtype=dtype)
        if trunc.shape[1:] != sample_shape:
            raise ValueError('Shape of sample %s of sequence at position %s is different from expected shape %s' %
                             (trunc.shape[1:], idx, sample_shape))

        if padding == 'post':
            x[idx, :len(trunc)] = trunc
        elif padding == 'pre':
            x[idx, -len(trunc):] = trunc
        else:
            raise ValueError('Padding type "%s" not understood' % padding)
    return x, lengths

