import argparse
import os

from PIL import Image
import numpy as np


def get_duplicates(dir_path1, dir_path2):
    duplicates = []
    images_1 = os.listdir(dir_path1)
    images_2 = os.listdir(dir_path2)

    for i, img_name_1 in enumerate(images_1):
        full_path_1 = os.path.join(dir_path1, img_name_1)
        image_1 = Image.open(full_path_1)

        for img_name_2 in images_2:
            full_path_2 = os.path.join(dir_path2, img_name_2)
            if full_path_1 == full_path_2:
                continue

            image_2 = Image.open(full_path_2)

            if image_1.size != image_2.size:
                continue

            if np.array_equal(np.array(image_1), np.array(image_2)):
                duplicates.append((full_path_1, full_path_2))

    return set(duplicates)


def print_duplicates(duplicates):
    if not duplicates:
        print('No duplicates detected!')
        exit(0)

    for im1, im2 in duplicates:
        print('%s --> %s' % (im1, im2))


def list_duplicates(dir_path1, dir_path2):
    duplicates = get_duplicates(dir_path1, dir_path2)
    print_duplicates(duplicates)


def parse_args():
    parser = argparse.ArgumentParser(description='List all images from first directory which are present in second one.')
    required_named = parser.add_argument_group('Required keyword arguments')
    required_named.add_argument('--first_path', required=True, help='Path to first directory with images')
    required_named.add_argument('--second_path', required=True, help='Path to second directory with images')
    args = vars(parser.parse_args())
    first_dir = args['first_path']
    second_dir = args['second_path']

    if not os.path.isdir(first_dir):
        print('%s is not a valid path to directory!' % first_dir)
        exit(1)

    if not os.path.isdir(second_dir):
        print('%s is not a valid path to directory!' % second_dir)
        exit(1)

    return args


if __name__ == '__main__':
    args = parse_args()
    dir_path1, dir_path2 = args['first_path'], args['second_path']
    list_duplicates(dir_path1, dir_path2)