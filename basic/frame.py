class Frame:
    def __init__(self, xmin, ymin, xmax, ymax):
        assert(ymax >= ymin and xmax >= xmin)
        self.ymax = ymax
        self.ymin = ymin
        self.xmax = xmax
        self.xmin = xmin
        self.area = (xmax-xmin)*(ymax-ymin)

    def count_overlap(self, frame2):
        dx = min(self.xmax, frame2.xmax) - max(self.xmin, frame2.xmin)
        dy = min(self.ymax, frame2.ymax) - max(self.ymin, frame2.ymin)
        if (dx >= 0) and (dy >= 0):
            return dx * dy
        return 0

    def __repr__(self):
        return 'Top-left: (%f, %f)\nRight-bottom: (%f, %f)' % (self.xmin, self.ymin, self.xmax, self.ymax)