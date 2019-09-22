from .img_wrapper import arraylike_to_img


class Volume:

    def __init__(self, data, chunk_shape, voxel_size, offset):

        self.data = data
        self.chunk_shape = chunk_shape
        self.voxel_size = voxel_size
        self.offset = offset

    def to_img(self):

        return arraylike_to_img(
            self.data,
            self.chunk_shape)
