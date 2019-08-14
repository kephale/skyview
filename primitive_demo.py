import scyview.core as syvw
import random
import numpy as np

# Configure pysciview
syvw_gen = syvw.ScyView()
syvw_gen.config()

# Make a SciView instance, this launches ImageJ and SciView
syv = syvw_gen.create()

# Make 10 spheres
num_spheres = 10
for k in range(num_spheres):
    sphere = syv.addSphere()
    x = float(random.uniform(-10,10))
    y = float(random.uniform(-10,10))
    z = float(random.uniform(-10,10))
    syv.setPosition(sphere,x,y,z)
    #sphere.setPosition(psv.glvector(x,y,z))

import time

time.sleep(5000)
