from tools.utils import get_data_handler


class App:
    def __init__(self, detector, painter, data_handler=None):
        self.detector = detector
        self.data_handler = data_handler
        self.painter = painter

    def run(self):
        if not self.data_handler:
            raise Exception

        detections = []
        for images_batch in self.data_handler:
            detections_batch = self.detector.run_detection(images_batch)
            processed_images = self.painter.draw_predictions(images_batch, detections_batch)
            self.data_handler.save(processed_images)
            detections.append(detections_batch)
        self.data_handler.close()
        return detections

    def load_data(self, source_path, save_path=None, max_images=200):
        self.data_handler = get_data_handler(source_path, save_path, max_images)
