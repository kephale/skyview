from .img_wrapper import arraylike_to_img

def daisy_array_to_img(array):

    if array.chunk_shape is not None:
        chunk_shape = array.chunk_shape
    else:
        chunk_shape = (128,)*len(array.shape)

    return arraylike_to_img(
        array.data,
        chunk_shape)
