from tools.utils import open_images
from detection.main_detector import MainDetector

import os
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--save_path', default=None, help='path to directory where detections will be saved')
    parser.add_argument('--show', action='store_true', help='path to image or directory with images')
    required_named = parser.add_argument_group('required keyword arguments')
    required_named.add_argument('--config_path', required=True, help='path to config file')
    required_named.add_argument('--image_path', required=True, help='path to image or directory with images')
    args = vars(parser.parse_args())

    if not os.path.exists(args['image_path']):
        print('Image_path is not a valid path to image or directory!')
        exit(1)

    if not args['save_path'] and not args['show']:
        print('WARNING! Images won\'t be saved or shown! Stop execution if not intended!')

    return args


def get_images(source_path):
    if os.path.isdir(source_path):
        images_paths = [os.path.join(source_path, img) for img in os.listdir(source_path)]
        return open_images(images_paths)
    else:
        return open_images(source_path)


def main():
    args = parse_args()
    config_path, source_path = args['config_path'], args['image_path']
    save_path, visualise = args['save_path'], args['show']
    app = MainDetector(config_path)
    images = get_images(source_path)
    app.run_detection(images, save_path, show=visualise)


if __name__ == '__main__':
    main()