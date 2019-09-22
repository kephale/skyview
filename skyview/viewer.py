from .annotation_layer import AnnotationLayer
from .img_wrapper import ij
from .volume import Volume
import daisy

class Viewer:

    def __init__(self):

        self.volumes = {}
        self.annotation_layers = {}
        self.sciview = self.__create_sciview()

    def add_volume(
            self,
            name,
            array,
            chunk_shape=None,
            voxel_size=None,
            offset=None):

        if isinstance(array, daisy.Array):

            if chunk_shape is None:
                chunk_shape = data.chunk_shape
            if voxel_size is None:
                voxel_size = data.voxel_size
            if offset is None:
                offset = data.roi.get_begin()

            array = array.data

        volume = Volume(array, chunk_shape, voxel_size, offset)
        self.volumes[name] = volume

        self.sciview.addVolume(volume.to_img())

        return volume

    def add_annotation_layer(self, name):

        layer = AnnotationLayer(self.sciview)
        self.annotation_layers[name] = layer

        # TODO: add to sciview

        return layer

    def set_position(self, position):
        self.sciview.moveCamera(position)

    def show(self):
        input("Press ENTER to quit...")
        self.close()

    def close(self):
        self.sciview.close()

    def __create_sciview(self):
        # Launch SciView inside ImageJ
        cmd = 'sc.iview.commands.LaunchViewer'
        result = ij.command().run(cmd, True).get()
        sciview = result.getOutput('sciView')
        sciview.getFloor().setVisible(False)
        return sciview
