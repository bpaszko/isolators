from PIL import Image
import argparse
import numpy as np

from detector import Detector
from tools.utils import visualise


def parse_args():
    parser = argparse.ArgumentParser(description='Run detection on single image. Uses only one model.')
    required_named = parser.add_argument_group('Required keyword arguments')
    required_named.add_argument('--model_path', required=True, help='Path to model')
    required_named.add_argument('--image_path', required=True, help='Path to image')
    args = vars(parser.parse_args())
    return args


def main():
    args = parse_args()
    path_to_model, path_to_image = args['model_path'], args['image_path']
    image = Image.open(path_to_image)
    image_np = np.array(image)

    detector = Detector(path_to_model)
    predictions = detector.detect([image_np])
    best = []
    for i in predictions[0]:
        if i.score >= 0.7:
            print(i.score)
            best.append(i)
    visualise(image_np, best)


if __name__ == '__main__':
    main()