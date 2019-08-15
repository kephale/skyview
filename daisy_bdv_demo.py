import dask.array
import daisy
import numpy as np
import random
import scyview as sv
import os


import jnius_config
jnius_config.add_options('-Xmx60g')

import numpy as np

import time

import imglyb
import imglyb.accesses
import imglyb.cell
import imglyb.util

from jnius import cast, JavaException, autoclass, PythonJavaClass, java_method

PythonHelpers               = autoclass('net.imglib2.python.Helpers')

for dtype in (np.uint8, np.int8, np.uint16, np.int16, np.uint32, np.int32, np.uint64, np.int64, np.float32, np.float64):
    arr = np.arange(10, dtype=dtype)
    acc = imglyb.accesses.as_array_access(arr, volatile=True)
    print(arr)
    print(np.array(acc.getCurrentStorageArray()))

print()

for dtype in (np.uint8, np.int8, np.uint16, np.int16, np.uint32, np.int32, np.uint64, np.int64, np.float32, np.float64):
    arr = np.arange(10, dtype=dtype)
    acc = imglyb.accesses.as_array_access(arr, volatile=False)
    print(arr)
    print(np.array(acc.getCurrentStorageArray()))


if os.path.isdir('test_array.zarr'):
    ds = daisy.open_ds(
        'test_array.zarr',
        'test')
else:
    ds = daisy.prepare_ds(
        'test_array.zarr',
        'test',
        total_roi=daisy.Roi((0, 0, 0), (100, 100, 100)),
        voxel_size=(1, 1, 1),
        write_size=(8, 8, 8),
        dtype=np.float32)
    d = np.arange(100**3, dtype=np.float32)/(100**3)
    ds.data[:] = d.reshape(ds.data.shape)

print(ds.shape)
    
import dask.array
# shape  = (100, 200, 300)
# chunks = (64, 64, 64)

shape  = (64, 64, 64)
#chunks = (64, 64, 64)
chunks = (8, 8, 8)

numel  = shape[0]*shape[1]*shape[2]
# to see that it irregular chunks fail, uncomment next line:
# chunks = (64, 64, (64,36,100,100))
#data   = dask.array.from_array(np.random.randint(255, size=shape, dtype=np.uint8), chunks=chunks).rechunk(chunks)

from imglyb.cell import *

import itertools

def get_rois(total_roi, block_size):
    # This truncates the edge if the block_roi is not evenly divisible into total_roi
    rois = []
    dim_offsets = []
    for d in range(len(total_roi)):
        start = []
        for x in range(0, total_roi[d]-block_size[d], block_size[d]):
            start.append(x)
        dim_offsets.append(start)
    rois = [daisy.Roi(tuple(start), block_size) for start in itertools.product(*dim_offsets)]
    return rois

def daisy_array_as_cached_cell_img(
        ds,
        roi_size=None,
        cache_generator=SoftRefLoaderCache,
        volatile_access=False):
    rois       = get_rois(ds.shape, roi_size)
    dims       = ds.data.shape
    block_size = roi_size# if roi_size else tuple(c[0] for c in ds.data)
    return as_cached_cell_img(
        func            = lambda index : ds[rois[index]].to_ndarray(),
        cell_grid       = PythonHelpers.makeGrid(dims, block_size),
        dtype           = ds.dtype,
        cache_generator = cache_generator,
        volatile_access  = volatile_access
    )

img    = daisy_array_as_cached_cell_img(ds, volatile_access=True, roi_size=chunks)
rois   = get_rois(ds.shape, chunks)
#slices = dask.array.core.slices_from_chunks(data.chunks)
#slices = [ roi.to_slices() for roi in rois ]

# alternative way generate cell img:
# def make_access(index):
#     try:
#         chunk    = data[slices[index]].compute()
#         refGuard = imglyb.util.ReferenceGuard(chunk)
#         address  = chunk.ctypes.data
#         target   = imglyb.accesses.as_array_access(chunk, volatile=True)
#         return target
#     except JavaException as e:
#         print('exception    ', e)
#         print('cause        ', e.__cause__ )
#         print('inner message', e.innermessage)
#         if e.stacktrace:
#             for line in e.stacktrace:
#                 print(line)

#         raise e
# access_generator = imglyb.cell.MakeAccess(make_access)
# img              = PythonHelpers.imgFromFunc(
#     shape,
#     chunks,
#     access_generator,
#     imglyb.types.UnsignedByteType(),
#     imglyb.accesses.as_array_access(data[slices[0]].compute(), volatile=True))

class MakeAccessBiFunction(PythonJavaClass):
    __javainterfaces__ = ['java/util/function/BiFunction']

    def __init__(self, func):
        super(MakeAccessBiFunction, self).__init__()
        self.func = func

    @java_method('(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;')
    def apply(self, t, u):
        return self.func(t, u)

def make_access(index, size):
    try:
        chunk    = ds[rois[index]].to_ndarray()
        refGuard = imglyb.util.ReferenceGuard(chunk)
        address  = chunk.ctypes.data
        target   = imglyb.accesses.as_array_access(chunk, volatile=True)
        #print('make_access ' + str(chunk))
        return target
    except JavaException as e:
        print('exception    ', e)
        print('cause        ', e.__cause__ )
        print('inner message', e.innermessage)
        if e.stacktrace:
            for line in e.stacktrace:
                print(line)
        raise e

access_generator = MakeAccessBiFunction(make_access)
img              = PythonHelpers.imgWithCellLoaderFromFunc(
    shape,
    chunks,
    access_generator,
    imglyb.types.FloatType(),    
#    imglyb.types.UnsignedByteType(),
    imglyb.accesses.as_array_access(ds[rois[0]].to_ndarray(), volatile=True))




try:
    # pass
    imglyb.util.BdvFunctions.show(img, 'WAS DA LOS?')
except JavaException as e:
    print('exception    ', e)
    print('cause        ', e.__cause__ )
    print('inner message', e.innermessage)
    if e.stacktrace:
        for line in e.stacktrace:
            print(line)


while True:
    time.sleep(0.5)
