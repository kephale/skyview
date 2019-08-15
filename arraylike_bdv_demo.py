import numpy as np
import scyview as sv
import imglyb

def create_test_array():

    array = np.zeros((20, 40, 80), dtype=np.float32)
    array[:,:,0:40] = 0.5
    array[:,:,40:60] = 0.75
    array[:,:,60:80] = 1.0
    array[:,0:20,:] *= 0.5

    return array

array = create_test_array()
img = sv.arraylike_to_img(array, (10, 20, 60))
src = imglyb.util.BdvFunctions.show(img, 'test array-like')
src.setDisplayRange(0, 1)

del array

input("Press ENTER to quit")

