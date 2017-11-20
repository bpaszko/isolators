from basic.datahandlers import DataHandler
from tools.utils import open_images


class ImageHandler(DataHandler):
    """ Loads images from given paths or directory one by one. Assumes they have different shapes and cannot be
        batched together.
        """

    def __init__(self, images_paths):
        self.images_paths = images_paths
        self._current_image = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._current_image >= len(self.images_paths):
            raise StopIteration

        image = open_images([self._current_image])
        self._current_image += 1
        return image

    def save(self):
        pass
