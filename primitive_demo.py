import pysciview.core as pysv
import random
import numpy as np

# Configure pysciview
psv = pysv.PySciView()
psv.config()

# Make a SciView instance, this launches ImageJ and SciView
sv = psv.create()

# Make 10 spheres
num_spheres = 10
for k in range(num_spheres):
    sphere = sv.addSphere()
    x = float(random.uniform(-10,10))
    y = float(random.uniform(-10,10))
    z = float(random.uniform(-10,10))
    a = np.array([x,y,z],dtype='float32')
    #sphere.setPosition(pysv.GLVector(a))
