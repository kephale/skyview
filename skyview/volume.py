class Volume:

    def __init__(self, data, chunk_shape, voxel_size, offset):

        self.data = data
        self.chunk_shape = chunk_shape
        self.voxel_size = voxel_size
        self.offset = offset
