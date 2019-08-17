from .annotation_layer import AnnotationLayer
from .volume import Volume

class Viewer:

    def __init__(self):

        self.volumes = {}
        self.annotation_layers = {}
        self.sciview = None  # TODO: create actual scivew instance

    def add_volume(
            self,
            name,
            data,
            chunk_shape=None,
            voxel_size=None,
            offset=None):

        volume = Volume(data, chunk_shape, voxel_size, offset)
        self.volumes[name] = volume

        # TODO: add to sciview

        return volume

    def add_annotation_layer(self, name):

        layer = AnnotationLayer(self.sciview)
        self.annotation_layers[name] = layer

        # TODO: add to sciview

        return layer

    def set_position(self, position):
        # TODO
        pass

    def show(self):
        # TODO
        pass
