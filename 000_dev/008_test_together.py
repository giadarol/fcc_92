import xtrack as xt
import numpy as np

env = xt.Environment()
env.call('fccee_z_parameters.py')
env.call('fccee_z_elements.py')
env.call('fccee_z_lattice.py')
# env.call('fccee_z_strengths.py')

line = env['fccee_p_ring']

env.vars.load_json('strengths_quads_00_arc_cell.json')
env.vars.load_json('strengths_quads_01_ffccsyl.json')
env.vars.load_json('strengths_quads_02_ffccsxl.json')
env.vars.load_json('strengths_quads_03_ffccsyr.json')
env.vars.load_json('strengths_quads_04_ffccsxr.json')
env.vars.load_json('strengths_quads_05_ffds_lr.json')
env.vars.load_json('strengths_quads_06_straight.json')
env.vars.load_json('strengths_sext_00_arc_cell.json')
env.vars.load_json('strengths_sext_01_straight.json')
env.vars.load_json('strengths_sext_02_final_focus.json')

tt = line.get_table(attr=True)

tw4d = line.twiss4d()

# Remove lag (radiatio is off)
env['rf_lag'] = 0.5

tw6d = line.twiss()

import matplotlib.pyplot as plt
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

act.mom_acceptance(plot=True, with_progress=1)
plt.show()