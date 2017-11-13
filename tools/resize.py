from PIL import Image
import os
import argparse

MAX_WIDTH = 800
MAX_HEIGHT = 600


def resize(image, path):
    old_w, old_h = image.size
    if old_w <= MAX_WIDTH and old_h <= MAX_HEIGHT:
        return

    new_h, new_w = old_h, old_w
    if new_w > MAX_WIDTH:
        new_w = MAX_WIDTH
        new_h = int(old_h / old_w * new_w)
        image = image.resize((new_w, new_h), Image.ANTIALIAS)

    old_h, old_w = new_h, new_w
    if new_h > MAX_HEIGHT:
        new_h = MAX_HEIGHT
        new_w = int(old_w / old_h * new_h)
        image = image.resize((new_w, new_h), Image.ANTIALIAS)

    image.save(path)


def iter_dir(dir_path):
    for img_name in os.listdir(dir_path):
        full_path = os.path.join(dir_path, img_name)
        img = Image.open(full_path)
        resize(img, full_path)


def parse_args():
    parser = argparse.ArgumentParser(description='Resize all images in directory to be at most 800x600.')
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
    iter_dir(dir_path)