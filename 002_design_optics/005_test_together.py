import xtrack as xt
import numpy as np
import matplotlib.pyplot as plt

plt.close('all')

env = xt.Environment()
env.call('../fccee_z_lattice.py')

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
# tw4d.plot()
# tw4d.plot('wx_chrom wy_chrom')
# tw4d.plot('ddx')

env['rfc'].frequency = 121200*3306.828357898286
# Remove lag (radiatio is off)
env['rf_lag'] = 0.5

tw6d = line.twiss()
tw6d.plot()
tw6d.plot('wx_chrom wy_chrom')
tw6d.plot('ddx')

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