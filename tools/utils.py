from collections import namedtuple
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import cv2
import skvideo.io


def split_by_filename(df, group):
    data = namedtuple('data', [group, 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def extract_predictions_from_image(image, frames):
    all_extracted = []
    height, width = image.shape[:2]
    for frame in frames:
        ymin, ymax = int(frame.ymin * height), int(frame.ymax * height)
        xmin, xmax = int(frame.xmin * width), int(frame.xmax * width)
        extracted = image[ymin:ymax, xmin:xmax, :]
        all_extracted.append(extracted)
    return all_extracted


def open_images(paths):
    images = []
    if isinstance(paths, str):
        paths = [paths]

    for path in paths:
        if not path.endswith('jpg'):
            continue
        try:
            image = Image.open(path)
        except Exception:  # Change for special exception
            continue
        images.append(np.array(image))
    return images


def read_avi(path):
    cap = skvideo.io.vreader(path)

    frames = []
    for frame in cap:
        frames.append(frame)
    return frames


def show_prediction(image, prediction, color):
    height, width, _ = image.shape
    x1, y1 = prediction.xmin * width, prediction.ymin * height
    x2, y2 = prediction.xmax * width, prediction.ymax * height
    plt.plot([x1, x2, x2, x1, x1], [y1, y1, y2, y2, y1], color=color)


def draw_prediction(image, prediction, color):
    colors = {'red': (255, 0, 0),
              'green': (0, 255, 0)
              }
    height, width, _ = image.shape
    x1, y1 = int(prediction.xmin * width), int(prediction.ymin * height)
    x2, y2 = int(prediction.xmax * width), int(prediction.ymax * height)
    cv2.rectangle(image, (x1, y1), (x2, y2), colors[color], 5)
    return image


def visualise(image, best):
    height, width, _ = image.shape
    borders = []
    for i in best:
        x1, y1 = i.xmin * width, i.ymin * height
        x2, y2 = i.xmax * width, i.ymax * height
        borders.append(([x1,x2,x2,x1,x1],[y1,y1,y2,y2,y1]))
    plt.imshow(image)
    for xs, ys in borders:
        plt.plot(xs, ys)
    plt.show()