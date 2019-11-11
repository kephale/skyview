# XInitThreads must be the first X11 call made on linux systems
#   under some cases Python seems to make X11 calls before we get into SciView
#   therefore we make this call as early as possible
import os, ctypes, sys
if os.name == 'posix' and sys.platform != 'darwin':
    try:
        x11 = ctypes.cdll.LoadLibrary('libX11.so')
        x11.XInitThreads()
    except:
        print('Warning: failed to run XInitThreads()')

from .daisy import daisy_array_to_img
from .events import Events
from .img_wrapper import arraylike_to_img
from .viewer import Viewer

__all__ = ['Viewer', 'Events', 'daisy_array_to_img']
