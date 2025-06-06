import xtrack as xt
import numpy as np
import matplotlib.pyplot as plt

plt.close('all')

env = xt.Environment()
env.call('../fccee_z_lattice.py')
env.call('../fccee_z_strengths.py')

line = env['fccee_p_ring']
# Remove lag (radiation is off)
env['rf_lag'] = 0.5
line.twiss()

import sys
sys.path.append('../dev')
from momentum_acceptance import ActionMomentumAcceptance
nemitt_x = 6.33e-5
nemitt_y = 1.69e-7
energy_spread=3.9e-4
nn_y_r=15
max_y_r=15
global_xy_limit = 10e-2
num_turns = 100
act = ActionMomentumAcceptance(line,
            nemitt_x, nemitt_y, nn_y_r, max_y_r, energy_spread,
            global_xy_limit=global_xy_limit, num_turns=num_turns)

plt.figure()
act.mom_acceptance(plot=True, with_progress=1)
plt.show()