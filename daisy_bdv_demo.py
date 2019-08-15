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

def cell_index_to_roi(total_roi, voxel_size, chunk_shape, cell_index):

    chunk_size = chunk_shape*voxel_size
    chunks = (total_roi/chunk_size).get_shape()[::-1]
    cell_coordinates = []
    dims = len(chunks)

    i = cell_index
    for d in range(dims):
        c = i % chunks[d]
        cell_coordinates.append(c)
        i = (i - c)//chunks[d]

    cell_coordinates = cell_coordinates[::-1]

    roi = daisy.Roi(
        total_roi.get_begin() + daisy.Coordinate(cell_coordinates)*chunk_size,
        chunk_size)

    return roi

def cell_index_to_ndarray(ds, cell_index):

    print("requesting ndarray for index %d" % cell_index)

    roi = cell_index_to_roi(
        ds.roi,
        ds.voxel_size,
        ds.chunk_shape,
        cell_index)

    print("ROI for index %d: %s" % (cell_index, roi))

    return np.ascontiguousarray(ds.to_ndarray(roi))

class MakeAccessBiFunction(PythonJavaClass):
    __javainterfaces__ = ['java/util/function/BiFunction']

    def __init__(self, func):
        super(MakeAccessBiFunction, self).__init__()
        self.func = func

    @java_method('(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;')
    def apply(self, t, u):
        return self.func(t, u)

def make_access(ds, index, size):
    try:
        chunk    = cell_index_to_ndarray(ds, index)
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

access_generator = MakeAccessBiFunction(lambda i, s: make_access(ds, i, s))
img = PythonHelpers.imgWithCellLoaderFromFunc(
    ds.shape[::-1],
    ds.chunk_shape[::-1],
    access_generator,
    imglyb.types.FloatType(), # TODO: use ds.dtype
    imglyb.accesses.as_array_access(
        cell_index_to_ndarray(ds, 0),
        volatile=True)) # TODO: is array access really needed here?

try:
    src = imglyb.util.BdvFunctions.show(img, 'test out-of-core array')
    src.setDisplayRange(0, 1)
except JavaException as e:
    print('exception    ', e)
    print('cause        ', e.__cause__ )
    print('inner message', e.innermessage)
    if e.stacktrace:
        for line in e.stacktrace:
            print(line)

input("Press ENTER to quit")
