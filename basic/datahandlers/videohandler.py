import skvideo.io
import numpy as np
import os

from basic.datahandlers import DataHandler


class VideoHandler(DataHandler):
    def __init__(self, video_path, save_path=None, max_frames=1000):
        self.video_path = video_path
        self.reader = skvideo.io.vreader(self.video_path)
        self.max_frames = max_frames
        self.save_path = self._create_save_path(save_path)
        self.writer = None
        if self.save_path:
            self.writer = skvideo.io.FFmpegWriter(self.save_path)

    def __iter__(self):
        return self

    def __next__(self):
        frames = []
        try:
            for i, frame in zip(range(self.max_frames), self.reader):
                frames.append(frame)
            if not frames:
                raise StopIteration
            return np.array(frames)

        except StopIteration:
            if not frames:
                raise StopIteration

            return np.array(frames)
        except:
            return np.array(frames)

    def save(self, images):
        if not self.writer:
            return

        images = np.array(images)
        for image in images:
            self.writer.writeFrame(image)

    def close(self):
        if self.writer:
            self.writer.close()

    def _create_save_path(self, path):
        save_path = path
        if not path:
            return None

        elif os.path.isdir(path):
            parts = self.video_path.split('/')
            name = 'processed_' + parts[-1]
            save_path = os.path.join(path, name)

        return save_path
