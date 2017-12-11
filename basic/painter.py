from tools.utils import draw_prediction

import matplotlib.pyplot as plt


class Painter:
    def __init__(self, show):
        self.show = show

    def draw_predictions(self, images, predictions):
        isolators, faults = predictions
        for image, isolators, faults in zip(images, isolators, faults):
            for isolator in isolators:
                draw_prediction(image, isolator, color='green')

            for fault in faults:
                draw_prediction(image, fault, color='red')

            if self.show:
                plt.imshow(image)
                plt.show()
