import xtrack as xt
import numpy as np

env = xt.Environment()

env.call('../fccee_z_lattice.py')
env.call('../fccee_z_strengths.py')

line_thick = env.fccee_p_ring
tw_thick = line_thick.twiss4d(strengths=True)

# Sort quads by beta function
tw_quads = tw_thick.rows[tw_thick.element_type == 'Quadrupole']
bet_max_xy = [(max([tw_quads.betx[ii], tw_quads.bety[ii]]))
              for ii in range(len(tw_quads))]
tw_quads['bet_max_xy'] = np.array(bet_max_xy)
i_sorted = np.argsort(bet_max_xy)
tw_quads_sorted = tw_quads.rows[i_sorted[::-1]]

line = line_thick.copy(shallow=True)

Strategy = xt.slicing.Strategy
Teapot = xt.slicing.Teapot

slicing_strategies = [
    Strategy(slicing=None),  # Default catch-all as in MAD-X
    Strategy(slicing=Teapot(2), element_type=xt.Bend),
    # Strategy(slicing=Teapot(5), element_type=xt.Quadrupole),
    # Quad with betas above 5000 m
    Strategy(slicing=Teapot(200), name=r'qd0al.*'),
    Strategy(slicing=Teapot(200), name=r'qd0br.*'),
    Strategy(slicing=Teapot(200), name=r'qd6l.*'),
    Strategy(slicing=Teapot(200), name=r'qy1l.*'),
    Strategy(slicing=Teapot(200), name=r'qd7r.*'),
    Strategy(slicing=Teapot(200), name=r'qy1r.*'),
    Strategy(slicing=Teapot(200), name=r'qd7l.*'),
    Strategy(slicing=Teapot(200), name=r'qd6r.*'),
    Strategy(slicing=Teapot(200), name=r'qd0ar.*'),
    # Quads with betas above 2000 m
    Strategy(slicing=Teapot(100), name=r'qd0bl.*'),
    Strategy(slicing=Teapot(100), name=r'qy3l.*'),
    Strategy(slicing=Teapot(100), name=r'qf1ar.*'),
    Strategy(slicing=Teapot(100), name=r'qf1al.*'),
    Strategy(slicing=Teapot(100), name=r'qf1bl.*'),
    Strategy(slicing=Teapot(100), name=r'qd1l.*'),
    Strategy(slicing=Teapot(100), name=r'qf1br.*'),
    Strategy(slicing=Teapot(100), name=r'qy2l.*'),
    Strategy(slicing=Teapot(100), name=r'qf2l.*'),
    Strategy(slicing=Teapot(100), name=r'qd1r.*'),
    # Arc cell quads
    Strategy(slicing=Teapot(5), name=r'qd1a.*'),
    Strategy(slicing=Teapot(5), name=r'qf2a.*'),
    Strategy(slicing=Teapot(5), name=r'qd3a.*'),
    Strategy(slicing=Teapot(5), name=r'qf4a.*'),
    Strategy(slicing=Teapot(5), name=r'qd5a.*'),
    Strategy(slicing=Teapot(5), name=r'qf6a.*'),
]

line.slice_thick_elements(slicing_strategies=slicing_strategies)

tw = line.twiss4d(strengths=True)

print(f'Qx thick: {tw_thick.qx}')
print(f'Qx thin:  {tw.qx}, error: {tw.qx - tw_thick.qx:.2e}')
print(f'Qy thick: {tw_thick.qy}')
print(f'Qy thin:  {tw.qy}, error: {tw.qy - tw_thick.qy:.2e}')

line.to_json('fccee_p_ring_thin.json.gz')


line['rf_lag'] = 0.5
line.twiss()

import sys
sys.path.append('../dev')
from momentum_acceptance import ActionMomentumAcceptance
import matplotlib.pyplot as plt
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