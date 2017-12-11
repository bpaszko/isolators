from basic import App, Painter
from detection.main_detector import MainDetector

import os
import time
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--save_path', default=None, help='path to directory where detections will be saved')
    parser.add_argument('--show', action='store_true', help='show all detections with matplotlib')
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


def main():
    args = parse_args()
    config_path, source_path = args['config_path'], args['image_path']
    save_path, show = args['save_path'], args['show']
    detector = MainDetector(config_path)
    painter = Painter(show)
    app = App(detector, painter)
    app.load_data(source_path, save_path)
    t1 = time.time()
    app.run()
    print("Time taken: %f" % (time.time()-t1))


if __name__ == '__main__':
    main()