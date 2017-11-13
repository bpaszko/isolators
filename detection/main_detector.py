import matplotlib.pyplot as plt

from detection.detector import Detector
from tools.utils import extract_predictions_from_image, show_prediction
from basic.prediction import Prediction


class MainDetector:
    def __init__(self, config_path):
        isolators_model_path, faulty_model_path = MainDetector._parse_config(config_path)
        self._initialize_models(isolators_model_path, faulty_model_path)

    def run_detection(self, images, save_path, show=False):
        isolators = self._get_isolators(images)
        faults = self._get_faults(images, isolators)
        MainDetector.visualise(images, isolators, faults, save_path, show)

    @staticmethod
    def visualise(all_images, all_isolators, all_faults, save_dir, show):
        for image, isolators, faults in zip(all_images, all_isolators, all_faults):
            plt.imshow(image)
            for isolator in isolators:
                show_prediction(image, isolator, color='green')

            for frame in faults:
                show_prediction(image, frame, color='red')

            if save_dir:  # TODO
                #plt.savefig()
                pass

            if show:
                plt.show()

    def _get_faults(self, images, isolators):
        all_faults = []
        for image, isolators_per_image in zip(images, isolators):
            extracted_isolators = extract_predictions_from_image(image, isolators_per_image)
            faults = self.faults_detector.detect(extracted_isolators)
            faults = [Prediction.filter(f, thresholds=[0.9], names=[1]) for f in faults]
            mapped_faults = MainDetector._map_to_image(faults, isolators_per_image)
            all_faults.append(mapped_faults)
        return all_faults

    @staticmethod
    def _map_to_image(faults, isolators):
        def map_coord(a, b):
            # b is inside a
            a_width, a_height = a.xmax - a.xmin, a.ymax - a.ymin
            new_b_xmin, new_b_xmax = a.xmin + a_width * b.xmin, a.xmin + a_width * b.xmax
            new_b_ymin, new_b_ymax = a.ymin + a_height * b.ymin, a.ymin + a_height * b.ymax
            return Prediction(new_b_xmin, new_b_ymin, new_b_xmax, new_b_ymax, b.score, b.name)

        mapped_faults = []
        for faults_per_isolator, isolator in zip(faults, isolators):
            for fault in faults_per_isolator:
                mapped_faults.append(map_coord(isolator, fault))
        return mapped_faults

    def _get_isolators(self, images):
        isolators = self.isolators_detector.detect(images)
        return [Prediction.filter(i, thresholds=[0.9], names=[1]) for i in isolators]

    @staticmethod
    def _parse_config(config_path):
        with open(config_path, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip() and not line.strip().startswith('#')]

        isolators_model_path = lines[0]
        faulty_model_path = lines[1]
        return isolators_model_path, faulty_model_path

    def _initialize_models(self, isolators_model_path, faulty_model_path):
        self.isolators_detector = Detector(isolators_model_path)
        self.faults_detector = Detector(faulty_model_path)
