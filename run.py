from detection.main_detector import MainDetector
from basic.datahandlers import *

import os
import time
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


def get_data_handler(source_path, save_path):
    if os.path.isdir(source_path):
        return DirectoryHandler(source_path)
    elif source_path.endswith('.mp4'):
        return VideoHandler(source_path, save_path=save_path, max_frames=5)
    else:
        return ImageHandler(source_path)


def main():
    args = parse_args()
    config_path, source_path = args['config_path'], args['image_path']
    save_path, visualise = args['save_path'], args['show']
    data_handler = get_data_handler(source_path, save_path)
    app = MainDetector(config_path, data_handler)
    t1 = time.time()
    app.run_detection()
    print(time.time()-t1)

if __name__ == '__main__':
    main()