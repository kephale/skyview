
import h5py
import os
import PIL
import wget

def load_or_download(name):
    # https://cremi.org
    
    target = os.path.join(os.path.expanduser('~'), 'Downloads', f'{name}.hdf')
    
    if not os.path.exists(target):
        source = f'https://cremi.org/static/data/{name}.hdf'.replace('+', '%2B')
        print(f'Sample {name} not found at {target}. Will download from {source} (this might take a few minutes)')
        wget.download(source, target)
        
    return h5py.File(target, 'r')['volumes/raw'][()]


import imglyb
import imglyb.util as util

name = 'sample_A_20160501'
data = load_or_download(name)
img  = imglyb.to_imglib(data)
#data.shape

bdv = imglyb.util.BdvFunctions.show(img, name)
