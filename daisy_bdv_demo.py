import daisy
import numpy as np
import scyview as sv
import imglyb

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

array = create_test_array()
img = sv.daisy_array_to_img(array)
src = imglyb.util.BdvFunctions.show(img, 'test out-of-core array')
src.setDisplayRange(0, 1)

del array

input("Press ENTER to quit")
