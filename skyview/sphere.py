from .annotation import Annotation

class Sphere(Annotation):

    def __init__(self, position, color, radius):

        super(Sphere, self).__init__()

        self.position = position
        self.color = color
        self.radius = radius
