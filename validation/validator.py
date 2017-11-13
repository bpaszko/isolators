import pandas as pd
import numpy as np

from tools.utils import split_by_filename
from basic import Frame
from PIL import Image
import os

from detection.detector import Detector


class Validator:
    def __init__(self, path_to_model):
        self.detector = Detector(path_to_model)
        self.true_positives = 0
        self.false_positives = 0
        self.true_negatives = 0
        self.false_negatives = 0
        self.total = 0

    def evaluate(self, labels_paths):
        for path in labels_paths:
            labels = pd.read_csv(path)
            labels = split_by_filename(labels, 'path')
            images = []
            for image_labels in labels:
                img_path = image_labels.path
                try:
                    image = Image.open(img_path)
                except Exception:
                    continue

                images.append(np.array(image))
            predictions = [[p for p in p_img if p.score >= 0.9 and p.name == 1] for p_img in self.detector.detect(images)]

            for image_labels, image_predictions in zip(labels, predictions):
                frames = [Frame(label['xmin'] / label['width'], label['ymin'] / label['height'],
                                label['xmax'] / label['width'], label['ymax'] / label['height'])
                          for i, label in image_labels.object.iterrows()]
                self.evaluate_single_image(image_predictions, frames)

    def evaluate_directory(self, dir_path):
        images = []
        for img_name in os.listdir(dir_path):
            if not img_name.endswith('jpg'):
                continue
            img_path = os.path.join(dir_path, img_name)
            try:
                image = Image.open(img_path)
            except Exception:
                continue
            images.append(np.array(image))
        predictions = [[p for p in p_img if p.score >= 0.9 and p.name == 1] for p_img in self.detector.detect(images)]
        for i, p in enumerate(predictions):
            if p:
                self.false_positives += len(p)

    def evaluate_single_image(self, predictions, labels):
        for prediction in predictions:
            label = Validator.find_in_labels(labels, prediction)
            if not label:
                self.false_positives += 1
            else:
                self.true_positives += 1
                labels.remove(label)

        self.false_negatives += len(labels)

    def __repr__(self):
        return 'Found correct: %d\nNot found: %d\nFound incorrect: %d' % \
               (self.true_positives, self.false_negatives, self.false_positives)

    @staticmethod
    def find_in_labels(labels, prediction):
        for label in labels:
            if Validator.check_overlap(prediction, label):
                return label

    @staticmethod
    def check_overlap(frame1, frame2, threshold=0.6):
        overlap = frame1.count_overlap(frame2)
        return overlap / frame1.area >= threshold and overlap / frame2.area >= threshold
