from .sphere import Sphere
from .line import Line
from .text import Text
from jnius import autoclass

__scMaterial__ = autoclass('graphics.scenery.Material')
__scSphere__ = autoclass('graphics.scenery.Sphere')
__glVector__ = autoclass('cleargl.GLVector')

class AnnotationLayer:

    def __init__(self, sciview):

        self.sciview = sciview
        self.annotations = {}

    def add_sphere(self, position, color, radius):

        sphere = Sphere(position, color, radius)
        self.annotations[sphere.id] = sphere

        color = self.sciview.getGLVector(float(1), float(1), float(1))
        sc_material = __scMaterial__()
        sc_material.setAmbient(color)
        sc_material.setDiffuse(color)
        sc_material.setSpecular(color)
        sc_sphere = __scSphere__(radius, 20)
        sc_sphere.setMaterial(sc_material)
        sc_sphere.setPosition(self.sciview.getGLVector(position[0], position[1], position[2]))
        
        self.sciview.addNode(sc_sphere, False)

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
