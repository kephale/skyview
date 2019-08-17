from .sphere import Sphere
from .line import Line
from .text import Text

class AnnotationLayer:

    def __init__(self, sciview):

        self.sciview = sciview
        self.annotations = {}

    def add_sphere(self, position, color, radius):

        sphere = Sphere(position, color, radius)
        self.annotations[sphere.id] = sphere

        # TODO: update sciview

        return sphere

    def add_line(self, start, end, width, color):

        line = Line(start, end, width, color)
        self.annotations[line.id] = line

        # TODO: update sciview

        return line

    def add_text(self, msg, position):

        text = Text(msg, position)
        self.annotations[text.id] = text

        # TODO: update sciview

        return text

    def remove(self, annotation_id):

        if annotation_id not in self.annotations:
            return

        annotation = self.annotations[annotation_id]
        del self.annotations[annotation_id]

        # TODO: update sciview

    def register_callback(self, event, callback):
        # TODO
        pass
