import pysciview.core as pysv
from jnius import autoclass
import random

#GLVector = autoclass('cleargl.GLVector')

psv = pysv.PySciView()
psv.config()
sv = psv.create()

num_spheres = 10

for k in range(num_spheres):
    sphere = sv.addSphere()
    x = random.uniform(-10,10)
    y = random.uniform(-10,10)
    z = random.uniform(-10,10)
    #sphere.setPosition(GLVector(x,y,z))
