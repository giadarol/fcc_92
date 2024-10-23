import xtrack as xt
import numpy as np

env = xt.Environment()
env.call('fccee_z_parameters.py')
env.call('fccee_z_elements.py')
env.call('fccee_z_lattice.py')
env.call('fccee_z_strengths.py')