import tensorflow as tf
import pandas as pd

import io
from PIL import Image

from utils import split_by_filename
from object_detection.utils import dataset_util
# From tensorflow/models/research/
# export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim

flags = tf.app.flags
flags.DEFINE_string('csv_input', '', 'Path to the CSV input')
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
FLAGS = flags.FLAGS


def class_to_id(class_text):
    if class_text == 'isolator':
        return 1
    if class_text == 'gap':
        return 1
    return None


def create_tf_example(group):
    with tf.gfile.GFile(group.path, 'rb') as fid:
        encoded_jpg = fid.read()

    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size
    filename = group.path.split('/')[-1].encode('utf8')

    image_format = b'jpeg'
    xmins, xmaxs, ymins, ymaxs = [], [], [], []
    classes_text, classes = [], []

    for i, data in group.object.iterrows():
        xmins.append(data['xmin'] / width)
        xmaxs.append(data['xmax'] / width)

        ymins.append(data['ymin'] / height)
        ymaxs.append(data['ymax'] / height)

        class_text = data['class']
        classes_text.append(class_text.encode('utf8'))
        classes.append(class_to_id(class_text))

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example


def main(_):
    writer = tf.python_io.TFRecordWriter(FLAGS.output_path)
    examples = pd.read_csv(FLAGS.csv_input)
    grouped = split_by_filename(examples, 'path')

    for group in grouped:
        tf_example = create_tf_example(group)
        writer.write(tf_example.SerializeToString())

    writer.close()


if __name__ == '__main__':
    tf.app.run()