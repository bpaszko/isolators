from basic.datahandlers import DirectoryHandler, ImageHandler, VideoHandler

import os


def get_data_handler(source_path, save_path=None, max_images=200):
    if os.path.isdir(source_path):
        return DirectoryHandler(source_path, save_path=save_path, max_images=max_images)
    elif source_path.endswith('.mp4'):
        return VideoHandler(source_path, save_path=save_path, max_frames=max_images)
    else:
        return ImageHandler(source_path, save_path=save_path)