import daisy
import numpy as np
import random
import skyview as sv
import os

# create a SciView viewer

viewer = sv.create_viewer()

# add 10 spheres at random locations

num_spheres = 10
for k in range(num_spheres):
    sphere = viewer.add_sphere()
    x = float(random.uniform(-10, 10))
    y = float(random.uniform(-10, 10))
    z = float(random.uniform(-10, 10))

    # all of that should also be keyword arguments to add_sphere
    sphere.set_position(z, y, x)
    sphere.set_radius(2.0)
    sphere.set_color(128, 0, 44)

# create an array-like

if os.path.isdir('test_array.zarr'):
    ds = daisy.open_ds(
        'test_array.zarr',
        'test')
else:
    ds = daisy.prepare_ds(
        'test_array.zarr',
        'test',
        total_roi=daisy.Roi((0, 0, 0), (10, 100, 100)),
        voxel_size=(10, 1, 1),
        read_size=(10, 10, 10),
        dtype=np.float32)
    d = np.arange(10*100*100, dtype=np.float32)/(10*100*100)
    ds.data[:] = d.reshape(ds.data.shape)

viewer.add_volume(
    ds.data,
    voxel_size=ds.voxel_size,
    offset=ds.roi.get_offset())

input("Press ENTER to quit")
