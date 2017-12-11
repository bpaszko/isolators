import os

from tools.utils import open_images
from detection.detector import Detector


class DirectoryValidator:
    def __init__(self, path_to_model, threshold=0.9):
        self.detector = Detector(path_to_model)
        self.found_incorrect = 0
        self.threshold = threshold

    def evaluate(self, dir_path):
        paths = os.listdir(dir_path)
        images = open_images(paths)
        unfiltered_predictions = self.detector.detect(images)
        predictions = [[p for p in p_img if p.score >= self.threshold and p.name == 1]
                       for p_img in unfiltered_predictions]

        for image_predictions in predictions:
            if image_predictions:
                self.found_incorrect += len(image_predictions)

    def __repr__(self):
        return 'Found incorrect: %d' % self.found_incorrect
