from .annotation import Annotation

class Line(Annotation):

    def __init__(self, start, end, width, color):

        super(Line, self).__init__()

        self.start = start
        self.end = end
        self.width = width
        self.color = color
