import pandas as pd

from validation.common import find_in_labels
from tools.utils import split_by_filename, open_images
from basic import Prediction


class MainValidator:
    def __init__(self, detector):
        self.detector = detector
        self.score = {
            'isolators': {
                'correct': 0,
                'incorrect': 0,
                'not_found': 0,
            },
            'gaps': {
                'correct': 0,
                'incorrect': 0,
                'not_found': 0,
            }
        }

    def evaluate(self, labels_path):
        labels = pd.read_csv(labels_path)
        labels = split_by_filename(labels, 'path')
        images = open_images([image_labels.path for image_labels in labels])
        predictions = self.detector.run_detection(images)

        for image_labels, isolators, faults in zip(labels, predictions[0], predictions[1]):
            frames = [Prediction(label['xmin'] / label['width'], label['ymin'] / label['height'],
                                 label['xmax'] / label['width'], label['ymax'] / label['height'],
                                 score=1, name=label['class'])
                      for i, label in image_labels.object.iterrows()]
            self.evaluate_single_image((isolators, faults), frames)

    def evaluate_single_image(self, predictions, labels):
        isolators, faults = predictions
        isolators_labels = [label for label in labels if label.name == 'isolator']
        faults_labels = [label for label in labels if label.name == 'gap']
        for prediction in isolators:
            label = find_in_labels(isolators_labels, prediction)
            if not label:
                self.score['isolators']['incorrect'] += 1
            else:
                self.score['isolators']['correct'] += 1
                isolators_labels.remove(label)
        self.score['isolators']['not_found'] += len(isolators_labels)

        for prediction in faults:
            label = find_in_labels(faults_labels, prediction)
            if not label:
                self.score['gaps']['incorrect'] += 1
            else:
                self.score['gaps']['correct'] += 1
                faults_labels.remove(label)
        self.score['gaps']['not_found'] += len(faults_labels)

    def __repr__(self):
        return '#### Isolators ####\n' \
               'Found correct: %d\n' \
               'Not found: %d\n' \
               'Found incorrect: %d\n' \
               '\n' \
               '#### Faults ####\n' \
               'Found correct: %d\n' \
               'Not found: %d\n' \
               'Found incorrect: %d\n' % \
               (self.score['isolators']['correct'], self.score['isolators']['not_found'],
                self.score['isolators']['incorrect'], self.score['gaps']['correct'],
                self.score['gaps']['not_found'], self.score['gaps']['incorrect'])
