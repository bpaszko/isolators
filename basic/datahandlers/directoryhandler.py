import os

from basic.datahandlers import DataHandler
from tools.utils import open_images


class DirectoryHandler(DataHandler):
    """ Loads images from directory. Assumes that all images have the same size """

    def __init__(self, directory_path, max_images=1000):
        self.directory_path = directory_path
        self._images_paths = self._get_paths()
        self._current_image = 0
        self.max_images = max_images

    def __iter__(self):
        return self

    def __next__(self):
        if self._current_image >= len(self._images_paths):
            raise StopIteration

        paths = self._images_paths[self._current_image: self._current_image + self.max_images]
        images = open_images(paths)
        self._current_image += self.max_images
        return images

    def save(self):
        pass

    def _get_paths(self):
        if not os.path.isdir(self.directory_path):
            raise Exception

        all_paths = os.listdir(self.directory_path)
        return [os.path.join(self.directory_path, path) for path in all_paths if path.endswith('.jpg')]
