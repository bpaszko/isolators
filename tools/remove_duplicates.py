import argparse
import os

from PIL import Image
import numpy as np


def get_duplicates(dir_path):
    to_delete = []
    all_images = os.listdir(dir_path)

    for i, img_name_1 in enumerate(all_images):
        full_path_1 = os.path.join(dir_path, img_name_1)
        image_1 = Image.open(full_path_1)

        for img_name_2 in all_images[i+1:]:
            full_path_2 = os.path.join(dir_path, img_name_2)
            if full_path_1 == full_path_2:
                continue

            image_2 = Image.open(full_path_2)

            if image_1.size != image_2.size:
                continue

            if np.array_equal(np.array(image_1), np.array(image_2)):
                to_delete.append(full_path_2)
    return set(to_delete)


def delete_duplicates(duplicates):
    for path in duplicates:
        os.remove(path)


def remove_duplicates(dir_path):
    duplicates = get_duplicates(dir_path)
    delete_duplicates(duplicates)


def parse_args():
    parser = argparse.ArgumentParser(description='Remove duplicate images from directory.')
    required_named = parser.add_argument_group('Required keyword arguments')
    required_named.add_argument('--directory_path', required=True, help='Path to directory with images')
    args = vars(parser.parse_args())
    directory_dir = args['directory_path']

    if not os.path.isdir(directory_dir):
        print('%s is not a valid path to directory!' % directory_dir)
        exit(1)

    return args


if __name__ == '__main__':
    args = parse_args()
    dir_path = args['directory_path']
    remove_duplicates(dir_path)