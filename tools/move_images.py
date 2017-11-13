import argparse
import os

import numpy as np
from PIL import Image


def check_for_duplicates(image, destination_dir):
    image_array = np.array(image)
    for image_name_2 in os.listdir(destination_dir):
        destination_path = os.path.join(destination_dir, image_name_2)
        image_2 = Image.open(destination_path)
        if np.array_equal(image_array, np.array(image_2)):
            return True
    return False


def find_next_file_number(dir):
    jpgs = [name[:-4] for name in os.listdir(dir) if name.endswith('.jpg')]
    max_num = max([int(name) for name in jpgs if name.isdigit()])
    return max_num + 1


def move_images(source_dir, destination_dir, check_duplicates=True):
    img_num = find_next_file_number(destination_dir)
    for image_name in os.listdir(source_dir):
        source_path = os.path.join(source_dir, image_name)
        image = Image.open(source_path)
        if check_duplicates and check_for_duplicates(image, destination_dir):
            continue

        destination_path = os.path.join(destination_dir, str(img_num) + '.jpg')
        image.save(destination_path)
        os.remove(source_path)
        img_num += 1


def parse_args():
    parser = argparse.ArgumentParser(description='Move all images from source directory to destination.\
                                                  Omit duplicates')
    required_named = parser.add_argument_group('Required keyword arguments')
    required_named.add_argument('--source_path', required=True, help='Path to source directory with images')
    required_named.add_argument('--destination_path', required=True, help='Path to destination directory')
    args = vars(parser.parse_args())
    source_dir = args['source_path']
    destination_dir = args['destination_path']

    if not os.path.isdir(source_dir):
        print('%s is not a valid path to directory!' % source_dir)
        exit(1)

    if not os.path.isdir(destination_dir):
        print('%s is not a valid path to directory!' % destination_dir)
        exit(1)

    return args


if __name__ == '__main__':
    args = parse_args()
    source_dir, destination_dir = args['source_path'], args['destination_path']
    move_images(source_dir, destination_dir)

