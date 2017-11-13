import tensorflow as tf
import numpy as np

from object_detection.utils import label_map_util
from basic.prediction import Prediction


class Detector:
    """ This class detects objects from given images.
        Requires a saved model.
        """

    def __init__(self, path_to_graph):
        self._set_up_graph(path_to_graph)

    def detect(self, images):
        """ Method which handles detection of objects - main API of class

            Args:
                images (list of numpy 3d-arrays) - images on which detection should be made

            Returns:
                List of Predictions which describe detected objects
        """
        predictions = []
        with self.detection_graph.as_default():
            with tf.Session(graph=self.detection_graph) as sess:
                # Definite input and output Tensors for detection_graph
                image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
                # Each box represents a part of the image where a particular object was detected.
                detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
                # Each score represent how level of confidence for each of the objects.
                # Score is shown on the result image, together with the class label.
                detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
                detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
                num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')
                for image in images:
                    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                    image_np_expanded = np.expand_dims(image, axis=0)
                    # Actual detection.
                    (boxes, scores, classes, num) = sess.run(
                        [detection_boxes, detection_scores, detection_classes, num_detections],
                        feed_dict={image_tensor: image_np_expanded})
                    image_predictions = []
                    for box, score, class_ in zip(np.squeeze(boxes), np.squeeze(scores), np.squeeze(classes)):
                        adjusted_box = box[1], box[0], box[3], box[2]
                        prediction = Prediction(*adjusted_box, score, class_)
                        image_predictions.append(prediction)
                    predictions.append(image_predictions)
        return predictions

    def _set_up_graph(self, path_to_graph):
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(path_to_graph, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

