from basic.frame import Frame


class Prediction(Frame):
    def __init__(self, xmin, ymin, xmax, ymax, score, name):
        super().__init__(xmin, ymin, xmax, ymax)
        self.name = name
        self.score = score

    @staticmethod
    def filter(predicitons, *, thresholds, names):
        return [p for p in predicitons if p.name in names and p.score >= thresholds[names.index(p.name)]]

    def __repr__(self):
        return super().__repr__() + '\nClass: %d\nScore: %f' % (self.name, self.score)