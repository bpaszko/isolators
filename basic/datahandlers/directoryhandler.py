import os

from basic.datahandlers import DataHandler
from tools.utils import open_images
from PIL import Image


class DirectoryHandler(DataHandler):
    """ Loads images from directory. Assumes that all images have the same size """

    def __init__(self, directory_path, save_path=None, max_images=200):
        self.directory_path = directory_path
        self._save_path = save_path
        self.max_images = max_images

        self._images_paths = self._get_paths()
        self._current_image = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._current_image >= len(self._images_paths):
            raise StopIteration

        paths = self._images_paths[self._current_image: self._current_image + self.max_images]
        images = open_images(paths)
        self._current_image += self.max_images
        return images

    def save(self, images):
        if not self._save_path:
            return

        for image, src_path in zip(images, self._images_paths[self._current_image - self.max_images:self._current_image]):
            name = src_path.split('/')[-1]
            dst_path = os.path.join(self._save_path, name)
            pil_image = Image.fromarray(image)
            pil_image.save(dst_path)

    def _get_paths(self):
        if not os.path.isdir(self.directory_path):
            raise Exception

        all_paths = os.listdir(self.directory_path)
        return [os.path.join(self.directory_path, path) for path in all_paths if path.endswith('.jpg')]
