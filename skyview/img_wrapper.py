from . import configure_jnius  # noqa
import imglyb.accesses
import imglyb.types
from jnius import JavaException, autoclass, PythonJavaClass, java_method

import math
import numpy as np

PythonHelpers = autoclass('net.imglib2.python.Helpers')


class MakeAccessBiFunction(PythonJavaClass):
    __javainterfaces__ = ['java/util/function/BiFunction']

    def __init__(self, func):
        super(MakeAccessBiFunction, self).__init__()
        self.func = func

    @java_method('(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;')
    def apply(self, t, u):
        return self.func(t, u)


def chunk_index_to_slices(shape, chunk_shape, cell_index):

    chunks_xyz = tuple(
        int(math.ceil(s/sh))
        for s, sh in zip(shape, chunk_shape))[::-1]

    cell_coordinates_xyz = []
    dims = len(chunks_xyz)

    i = cell_index
    for d in range(dims):
        c = i % chunks_xyz[d]
        cell_coordinates_xyz.append(c)
        i = (i - c)//chunks_xyz[d]

    cell_coordinates = cell_coordinates_xyz[::-1]

    slices = tuple(
        slice(c*cs, (c + 1)*cs)
        for c, cs in zip(cell_coordinates, chunk_shape))

    return slices


def get_chunk(array, chunk_shape, chunk_index):

    slices = chunk_index_to_slices(array.shape, chunk_shape, chunk_index)
    return np.ascontiguousarray(array[slices])


def get_chunk_access(array, chunk_shape, index, size):

    try:

        chunk = get_chunk(array, chunk_shape, index)
        target = imglyb.accesses.as_array_access(chunk, volatile=True)
        return target

    except JavaException as e:

        print("exception    ", e)
        print("cause        ", e.__cause__)
        print("inner message", e.innermessage)
        if e.stacktrace:
            for line in e.stacktrace:
                print(line)
        raise e


def arraylike_to_img(array, chunk_shape):

    access_generator = MakeAccessBiFunction(
        lambda i, s: get_chunk_access(array, chunk_shape, i, s))

    shape_xyz = array.shape[::-1]
    chunk_shape_xyz = chunk_shape[::-1]

    img = PythonHelpers.imgWithCellLoaderFromFunc(
        shape_xyz,
        chunk_shape_xyz,
        access_generator,
        imglyb.types.for_np_dtype(array.dtype, volatile=True),
        imglyb.accesses.as_array_access(
            get_chunk(array, chunk_shape, 0),
            volatile=True))  # TODO: is array access really needed here?

    return img
