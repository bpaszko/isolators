
import os
import argparse
import pandas as pd
import xml.etree.ElementTree as ET


def parse_args():
    parser = argparse.ArgumentParser(description='Create csv file with images\' labels based on xml files.')
    required_named = parser.add_argument_group('Required keyword arguments')
    required_named.add_argument('--labels_path', required=True, help='Path to directory with xml labels')
    args = vars(parser.parse_args())
    labels_dir = args['labels_path']

    if not os.path.isdir(labels_dir):
        print('%s is not a valid path to directory!' % labels_dir)
        exit(1)

    return args


def get_labels_from_xml(label_file):
    all_labels = []

    tree = ET.parse(label_file)
    root = tree.getroot()
    img_file = root.find('filename').text
    img_path = root.find('path').text
    size = root.find('size')
    height = int(size.find('height').text)
    width = int(size.find('width').text)

    for obj in root.findall('object'):
        label_name = obj.find('name').text
        bndbox = obj.find('bndbox')
        xmin = int(bndbox.find('xmin').text)
        xmax = int(bndbox.find('xmax').text)
        ymin = int(bndbox.find('ymin').text)
        ymax = int(bndbox.find('ymax').text)

        all_labels.append((img_file, img_path, width, height, label_name,
                           xmin, ymin, xmax, ymax))

    return all_labels


def get_labels_from_dir(labels_dir):
    all_labels = []
    for label_file in os.listdir(labels_dir):
        if not label_file.endswith('.xml'):
            continue

        all_labels += get_labels_from_xml(os.path.join(labels_dir, label_file))
    return all_labels


def convert_to_csv(labels):
    columns = ['filename', 'path', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    df = pd.DataFrame(labels, columns=columns)
    return df


def main():
    args = parse_args()
    labels_dir = args['labels_path']
    labels = get_labels_from_dir(labels_dir)
    labels = convert_to_csv(labels)
    labels.to_csv(os.path.join(labels_dir, 'labels.csv'))
    print('Successfully converted!')

if __name__ == '__main__':
    main()

