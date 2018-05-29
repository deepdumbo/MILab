# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Routine for decoding the CIFAR-10 binary file format."""
 
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import re
import sys
import numpy as np
import orldb_input
import pandas as pd
import imageio
from sklearn.model_selection import train_test_split

from six.moves import xrange  # pylint: disable=redefined-builtin
import tensorflow as tf

# Process images of this size. Note that this differs from the original CIFAR
# image size of 32 x 32. If one alters this number, then the entire model
# architecture will change and any model would need to be retrained.
IMAGE_SIZE = 56*46

# Global constants describing the CIFAR-10 data set.
NUM_CLASSES = 40
NUM_EXAMPLES_PER_EPOCH_FOR_TRAIN = 320
NUM_EXAMPLES_PER_EPOCH_FOR_EVAL = 80

def _generate_image_and_label_batch(image, label, min_queue_examples,
                                    batch_size,shuffle):
  """Construct a queued batch of images and labels.

  Args:
    image: 3-D Tensor of [height, width, 3] of type.float32.
    label: 1-D Tensor of type.int32
    min_queue_examples: int32, minimum number of samples to retain
      in the queue that provides of batches of examples.
    batch_size: Number of images per batch.
    shuffle: boolean indicating whether to use a shuffling queue.

  Returns:
    images: Images. 4D tensor of [batch_size, height, width, 3] size.
    labels: Labels. 1D tensor of [batch_size] size.
  """
  '''
  # Create a queue that shuffles the examples, and then
  # read 'batch_size' images + labels from the example queue.
  num_preprocess_threads = 16
  if shuffle:
    images, label_batch = tf.train.shuffle_batch(
        [image, label],
    #    batch_size=batch_size,
        num_threads=num_preprocess_threads,
        capacity=min_queue_examples + 3 * batch_size,
        min_after_dequeue=min_queue_examples)
  else:
  '''
  num_preprocess_threads = 16
  images, label_batch = tf.train.batch(
        [image, label],
        batch_size=batch_size,
        num_threads=num_preprocess_threads,
        capacity=min_queue_examples + 3 * batch_size)
  
  # Display the training images in the visualizer.
  #tf.summary.image('images', images)

  return images, tf.reshape(label_batch, [batch_size])
def read_my_file_format(filename_queue,label_queue):
    reader_image = tf.WholeFileReader()
    
    #df_data = pd.DataFrame()
#    filename_list = list(filename_queue)
#    for file in filename_list:
    fname,image = reader_image.read(filename_queue)
    image_decode = tf.image.decode_bmp(image)
    
    image.set_shape([1,56*46])
    
    label = label_queue.dequeue()
    #imageio.imread(filename_queue,flatten=True)
    #[person,person_num] = re.findall('\d\d',filename_queue)
    #data_read = {'image':image_read,'person':person,'person_num':person_num}
    #df_data = df_data.append(data_read,ignore_index=True)

    # Train-Test Split

#    image_train = pd.DataFrame()
#    image_test = pd.DataFrame()

#    for person in image_raw.person.unique():
#        data_train, data_test = train_test_split(image_raw[image_raw.person == person],test_size = 0.2)
#        image_train = image_train.append(data_train)
#        image_test = image_test.append(data_test)

#    image_train = image_train.sample(frac=1)
#    image_test = image_test.sample(frac=1)
    #mat_data = [np.array(img.reshape(1,56*46)) for img in df_data['image']]
    #mat_data = np.vstack(mat_data)
    #labels_person = map(int,df_data['person'].values)

    return image,label

def inputs(eval_data,batch_size):
    """Construct input for CIFAR evaluation using the Reader ops.

    Args:
        eval_data: bool, indicating if one should use the train or eval data set.
        data_dir: Path to the CIFAR-10 data directory.
        batch_size: Number of images per batch.

    Returns:
        images: Images. 4D tensor of [batch_size, IMAGE_SIZE, IMAGE_SIZE, 3] size.
        labels: Labels. 1D tensor of [batch_size] size.
    """
    try:
    #For Windows
        file_path = 'D:\\Matlab_Drive\\Data\\ORLDB'
    except:
    # For Linux
        file_path = '/home/herokwon/data/ORLDB'

    file_list = os.listdir(file_path)
    file_list = [os.path.join(file_path,s) for s in file_list if ".bmp" in s]

    file_train, file_test = train_test_split(file_list,test_size = 0.2)
    
    if not eval_data:
        num_examples_per_epoch = NUM_EXAMPLES_PER_EPOCH_FOR_TRAIN
        filenames = file_train
    else:
        num_examples_per_epoch = NUM_EXAMPLES_PER_EPOCH_FOR_EVAL
        filenames = file_test

    with tf.name_scope('input'):
        
        labels = [int(re.findall('\d\d',f)[0]) for f in filenames]

        # Create a queue that produces the filenames to read.
        label_queue = tf.FIFOQueue(len(filenames),tf.int32,shapes=[[]])
        label_enqueue = label_queue.enqueue_many([tf.constant(labels)])
        filename_queue = tf.train.string_input_producer(filenames,shuffle=False)

        # Read examples from files in the filename queue.
        #read_input,label = read_my_file_format(filename_queue,label_queue)
        reader_image = tf.WholeFileReader()
        fname,image = reader_image.read(filename_queue)
        image_decode = tf.image.decode_bmp(image)
        reshaped_image = tf.cast(image_decode, tf.float32)
    
        resized_image = tf.image.resize_image_with_crop_or_pad(image_decode,
                                                           56, 46)
        #image_decode.set_shape([1,56*46])
    
        label = label_queue.dequeue()
    #    images, labels = data_mat , data_df['person'].values
    #    labels = np.array(list(map(int,labels)))
        
        #label.set_shape([1])
        
        # Ensure that the random shuffling has good mixing properties.
        min_fraction_of_examples_in_queue = 0.4
        min_queue_examples = int(num_examples_per_epoch *
                                min_fraction_of_examples_in_queue)

    # Generate a batch of images and labels by building up a queue of examples.
    return _generate_image_and_label_batch(resized_image, label,
                                            min_queue_examples,batch_size,
                                            shuffle=True)