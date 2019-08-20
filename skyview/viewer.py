from .annotation_layer import AnnotationLayer
from .volume import Volume
from .img_wrapper import ij

class Viewer:

    def __init__(self):

        self.volumes = {}
        self.annotation_layers = {}
        self.sciview = self._setup_()        

    def _setup_(self):
        # Launch SciView inside ImageJ
        cmd = 'sc.iview.commands.LaunchViewer'
        result = ij.command().run(cmd, True).get()
        sciview = result.getOutput('sciView')
        sciview.getFloor().setVisible(False)
        return sciview
        
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
        self.sciview.moveCamera(position)

    def show(self):
        input('Press enter to terminate')
