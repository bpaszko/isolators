def check_overlap(frame1, frame2, threshold=0.6):
    overlap = frame1.count_overlap(frame2)
    return overlap / frame1.area >= threshold and overlap / frame2.area >= threshold


def find_in_labels(labels, prediction):
    for label in labels:
        if check_overlap(prediction, label):
            return label
