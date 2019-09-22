import daisy
import numpy as np
import time
start = time.time()
import skyview as sv
print("Imported skyview in %.3fs" % (time.time() - start))
start = time.time()
import imglyb
print("Imported imglyb in %.3fs" % (time.time() - start))

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

start = time.time()
array = create_test_array()
print("Created test array in %.3fs" % (time.time() - start))

img = sv.daisy_array_to_img(array)
src = imglyb.util.BdvFunctions.show(img, 'test out-of-core array')
src.setDisplayRange(0, 1)

del array

input("Press ENTER to quit")
