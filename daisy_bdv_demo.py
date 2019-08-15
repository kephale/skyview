import jnius_config
jnius_config.add_options('-Xmx60g')

import imglyb.accesses
import imglyb.cell
import imglyb.util

from jnius import JavaException, autoclass, PythonJavaClass, java_method
import daisy
import itertools
import numpy as np
import os
import scyview as sv

PythonHelpers = autoclass('net.imglib2.python.Helpers')

def create_test_array():

    ds = daisy.prepare_ds(
        'test_array.zarr',
        'test',
        total_roi=daisy.Roi((0, 0, 0), (20, 40, 80)),
        voxel_size=(1, 1, 1),
        write_size=(2, 4, 4),
        dtype=np.float32)
    ds.data[:,:,0:40] = 0.5
    ds.data[:,:,40:60] = 0.75
    ds.data[:,:,60:80] = 1.0
    ds.data[:,0:20,:] *= 0.5

    return ds

def cell_index_to_roi(total_roi, voxel_size, chunk_shape, cell_index):

    chunk_size = chunk_shape*voxel_size
    chunks_xyz = (total_roi/chunk_size).get_shape()[::-1]
    cell_coordinates_xyz = []
    dims = len(chunks_xyz)

    i = cell_index
    for d in range(dims):
        c = i % chunks_xyz[d]
        cell_coordinates_xyz.append(c)
        i = (i - c)//chunks_xyz[d]

    cell_coordinates = cell_coordinates_xyz[::-1]

    roi = daisy.Roi(
        total_roi.get_begin() + daisy.Coordinate(cell_coordinates)*chunk_size,
        chunk_size)

    return roi

def cell_index_to_ndarray(array, cell_index):

    print("requesting ndarray for index %d" % cell_index)

    roi = cell_index_to_roi(
        array.roi,
        array.voxel_size,
        array.chunk_shape,
        cell_index)

    print("ROI for index %d: %s" % (cell_index, roi))

    return np.ascontiguousarray(array.to_ndarray(roi))

class MakeAccessBiFunction(PythonJavaClass):
    __javainterfaces__ = ['java/util/function/BiFunction']

    def __init__(self, func):
        super(MakeAccessBiFunction, self).__init__()
        self.func = func

    @java_method('(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;')
    def apply(self, t, u):
        return self.func(t, u)

def make_access(array, index, size):
    try:
        chunk    = cell_index_to_ndarray(array, index)
        # TODO: what does refGuard do?
        # refGuard = imglyb.util.ReferenceGuard(chunk)
        # address  = chunk.ctypes.data
        target   = imglyb.accesses.as_array_access(chunk, volatile=True)
        return target
    except JavaException as e:
        print('exception    ', e)
        print('cause        ', e.__cause__ )
        print('inner message', e.innermessage)
        if e.stacktrace:
            for line in e.stacktrace:
                print(line)
        raise e

def daisy_array_to_img(array):

    access_generator = MakeAccessBiFunction(lambda i, s: make_access(array, i, s))

    shape_xyz = array.shape[::-1]
    if array.chunk_shape is not None:
        chunk_shape_xyz = array.chunk_shape[::-1]
    else:
        chunk_shape_xyz = (128,)*len(shape_xyz)

    img = PythonHelpers.imgWithCellLoaderFromFunc(
        shape_xyz,
        chunk_shape_xyz,
        access_generator,
        imglyb.types.FloatType(), # TODO: use array.dtype
        imglyb.accesses.as_array_access(
            cell_index_to_ndarray(array, 0),
            volatile=True)) # TODO: is array access really needed here?

    return img

try:
    array = create_test_array()
    img = daisy_array_to_img(array)
    src = imglyb.util.BdvFunctions.show(img, 'test out-of-core array')
    src.setDisplayRange(0, 1)
except JavaException as e:
    print('exception    ', e)
    print('cause        ', e.__cause__ )
    print('inner message', e.innermessage)
    if e.stacktrace:
        for line in e.stacktrace:
            print(line)

del array

input("Press ENTER to quit")
