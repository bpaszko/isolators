import pandas as pd
from PIL import Image
import argparse
import os

from tools.utils import split_by_filename


def parse_args():
    parser = argparse.ArgumentParser(description='Extract parts of given image and save them as new images.')
    required_named = parser.add_argument_group('Required keyword arguments')
    required_named.add_argument('--labels_path', required=True, help='Path to csv file with labels.')
    required_named.add_argument('--output_path', required=True, help='Path to directory where extracted images\
                                                                      should be saved.')
    args = vars(parser.parse_args())
    output_dir = args['output_path']

    if not os.path.isdir(output_dir):
        print('%s is not a valid path to directory!' % output_dir)
        exit(1)

    return args


def main():
    args = parse_args()
    labels_csv, output_dir = args['labels_path'], args['output_path']
    df = pd.read_csv(labels_csv)
    labels = split_by_filename(df, 'path')
    for image_labels in labels:
        img_path = image_labels.path
        try:
            image = Image.open(img_path)
        except Exception:
            continue

        for i, label in image_labels.object.iterrows():
            xmin, xmax = label['xmin'], label['xmax']
            ymin, ymax = label['ymin'], label['ymax']
            img_name = label['filename']
            cropped = image.crop((xmin, ymin, xmax, ymax))

            save_path = os.path.join(output_dir, str(i) + '_' + img_name)
            try:
                cropped.save(save_path)
            except Exception:
                continue


if __name__ == '__main__':
    main()
