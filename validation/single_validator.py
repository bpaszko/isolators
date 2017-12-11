import pandas as pd

from tools.utils import split_by_filename, open_images
from validation.common import find_in_labels
from basic import Frame
from detection.detector import Detector


class SingleValidator:
    def __init__(self, path_to_model, threshold=0.9):
        self.detector = Detector(path_to_model)
        self.score = {
            'correct': 0,
            'incorrect': 0,
            'not_found': 0,
        }
        self.threshold = threshold

    def evaluate(self, labels_path):
        labels = pd.read_csv(labels_path)
        labels = split_by_filename(labels, 'path')
        images = open_images([image_labels.path for image_labels in labels])
        unfiltered_predictions = self.detector.detect(images)
        predictions = [[p for p in p_img if p.score >= self.threshold and p.name == 1]
                       for p_img in unfiltered_predictions]

        for image_labels, image_predictions in zip(labels, predictions):
            frames = [Frame(label['xmin'] / label['width'], label['ymin'] / label['height'],
                            label['xmax'] / label['width'], label['ymax'] / label['height'])
                      for i, label in image_labels.object.iterrows()]
            self.evaluate_single_image(image_predictions, frames)

    def evaluate_single_image(self, predictions, labels):
        for prediction in predictions:
            label = find_in_labels(labels, prediction)
            if not label:
                self.score['incorrect'] += 1
            else:
                self.score['correct'] += 1
                labels.remove(label)

                self.score['not_found'] += len(labels)

    def __repr__(self):
        return '#### RESULTS ####\n' \
               'Found correct: %d\n' \
               'Not found: %d\n' \
               'Found incorrect: %d' % \
               (self.score['correct'], self.score['not_found'], self.score['incorrect'])