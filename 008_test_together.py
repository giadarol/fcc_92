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

twr = line.twiss(
    start='ip_mid::1',
    end='mid_cell_edge_r::2',
    betx=env['bxip'],
    bety=env['byip'],
)

twl = line.twiss(
    start='mid_cell_edge_l::1',
    end='ip_mid::1',
    init_at='ip_mid::1',
    betx=env['bxip'],
    bety=env['byip'],
)

tw = line.twiss(
    start='mid_cell_edge_l::0',
    end='mid_cell_edge_r::2',
    init_at='ip_mid::1',
    betx=env['bxip'],
    bety=env['byip'],
)

tw_on_mom = line.twiss4d(compute_chromatic_properties=False)

import matplotlib.pyplot as plt
plt.close('all')
twl.plot()
twr.plot()
tw.plot()
tw_on_mom.plot()
plt.show()
